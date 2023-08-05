# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import math
import torch
from torch import nn
import torch.nn.functional as F


def default_conv(in_channels, out_channels, kernel_size, bias=True):
  return nn.Conv2d(in_channels, out_channels, kernel_size, padding=(kernel_size//2), bias=bias)


class MeanShift(nn.Conv2d):
  def __init__(self, rgb_range, rgb_mean, rgb_std, sign=-1):
    super(MeanShift, self).__init__(3, 3, kernel_size=1)
    std = torch.Tensor(rgb_std)
    self.weight.data = torch.eye(3).view(3, 3, 1, 1)
    self.weight.data.div_(std.view(3, 1, 1, 1))
    self.bias.data = sign * rgb_range * torch.Tensor(rgb_mean)
    self.bias.data.div_(std)
    self.weight.requires_grad = False
    self.bias.requires_grad = False


class Upsampler(nn.Sequential):
  def __init__(self, conv, scale, n_feat, act=False, bias=True):
    m = []
    if (scale & (scale - 1)) == 0:    # Is scale = 2^n?
      for _ in range(int(math.log(scale, 2))):
        m.append(conv(n_feat, 4 * n_feat, 3, bias))
        m.append(nn.PixelShuffle(2))
        if act:
          m.append(act())
    elif scale == 3:
      m.append(conv(n_feat, 9 * n_feat, 3, bias))
      m.append(nn.PixelShuffle(3))
      if act:
        m.append(act())
    else:
      raise NotImplementedError

    super(Upsampler, self).__init__(*m)


class DA_conv(nn.Module):
  def __init__(self, channels_in, channels_out, kernel_size, reduction):
    super(DA_conv, self).__init__()
    self.channels_out = channels_out
    self.channels_in = channels_in
    self.kernel_size = kernel_size

    self.kernel = nn.Sequential(
        nn.Linear(16, 16, bias=False),
        nn.LeakyReLU(0.1, True),
        nn.Linear(16, 16 * self.kernel_size * self.kernel_size, bias=False)
    )
    self.conv = default_conv(channels_in, channels_out, 1)
    self.ca = CA_layer(channels_in, channels_out, reduction)

    self.relu = nn.LeakyReLU(0.1, True)

  def forward(self, x):
    '''
    :param x[0]: feature map: B * C * H * W
    :param x[1]: degradation representation: B * C
    '''
    b, c, h, w = x[0].size()

    # branch 1
    kernel = self.kernel(x[1]).view(-1, 1, self.kernel_size, self.kernel_size)
    out = self.relu(F.conv2d(x[0].view(1, -1, h, w), kernel, groups=b*c, padding=(self.kernel_size-1)//2))
    out = self.conv(out.view(b, -1, h, w))

    # branch 2
    out = out + self.ca(x)

    return out


class CA_layer(nn.Module):
  def __init__(self, channels_in, channels_out, reduction):
    super(CA_layer, self).__init__()
    self.conv_du = nn.Sequential(
        nn.Conv2d(channels_in, channels_in//reduction, 1, 1, 0, bias=False),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(channels_in // reduction, channels_out, 1, 1, 0, bias=False),
        nn.Sigmoid()
    )

  def forward(self, x):
    '''
    :param x[0]: feature map: B * C * H * W
    :param x[1]: degradation representation: B * C
    '''
    att = self.conv_du(x[1][:, :, None, None])

    return x[0] * att


class DAB(nn.Module):
  def __init__(self, conv, n_feat, kernel_size, reduction):
    super(DAB, self).__init__()

    self.da_conv1 = DA_conv(n_feat, n_feat, kernel_size, reduction)
    self.da_conv2 = DA_conv(n_feat, n_feat, kernel_size, reduction)
    self.conv1 = conv(n_feat, n_feat, kernel_size)
    self.conv2 = conv(n_feat, n_feat, kernel_size)

    self.relu = nn.LeakyReLU(0.1, True)

  def forward(self, x):
    '''
    :param x[0]: feature map: B * C * H * W
    :param x[1]: degradation representation: B * C
    '''

    out = self.relu(self.da_conv1(x))
    out = self.relu(self.conv1(out))
    out = self.relu(self.da_conv2([out, x[1]]))
    out = self.conv2(out) + x[0]

    return out


class DAG(nn.Module):
  def __init__(self, conv, n_feat, kernel_size, reduction, n_blocks):
    super(DAG, self).__init__()
    self.n_blocks = n_blocks
    modules_body = [
        DAB(conv, n_feat, kernel_size, reduction)
        for _ in range(n_blocks)
    ]
    modules_body.append(conv(n_feat, n_feat, kernel_size))

    self.body = nn.Sequential(*modules_body)

  def forward(self, x):
    '''
    :param x[0]: feature map: B * C * H * W
    :param x[1]: degradation representation: B * C
    '''
    res = x[0]
    for i in range(self.n_blocks):
      res = self.body[i]([res, x[1]])
    res = self.body[-1](res)
    res = res + x[0]

    return res


class DASR(nn.Module):
  def __init__(self, in_channels=1, out_channels=1):
    super(DASR, self).__init__()

    self.n_groups = 5
    n_blocks = 5
    n_feats = 16
    kernel_size = 3
    reduction = 8
    scale = 2

    conv = default_conv

    # RGB mean for DIV2K
    rgb_mean = (0.4488, 0.4371, 0.4040)
    rgb_std = (1.0, 1.0, 1.0)
    # self.sub_mean = MeanShift(255.0, rgb_mean, rgb_std)
    # self.add_mean = MeanShift(255.0, rgb_mean, rgb_std, 1)

    # head module
    modules_head = [conv(in_channels, n_feats, kernel_size)]
    self.head = nn.Sequential(*modules_head)

    # compress
    self.compress = nn.Sequential(
        nn.Linear(32, 16, bias=False),
        nn.LeakyReLU(0.1, True)
    )

    # body
    modules_body = [
        DAG(default_conv, n_feats, kernel_size, reduction, n_blocks)
        for _ in range(self.n_groups)
    ]
    modules_body.append(conv(n_feats, n_feats, kernel_size))
    self.body = nn.Sequential(*modules_body)

    # tail
    modules_tail = [Upsampler(conv, scale, n_feats, act=False),
                    conv(n_feats, out_channels, kernel_size)]
    self.tail = nn.Sequential(*modules_tail)

  def forward(self, x, k_v):

    k_v = self.compress(k_v)

    # head
    x = self.head(x)

    # body
    res = x
    for i in range(self.n_groups):
      res = self.body[i]([res, k_v])
    res = self.body[-1](res)
    res = res + x

    # tail
    x = self.tail(res)

    return x


if __name__ == "__main__":

  import tw

  model = DASR()
  tw.flops.register(model)

  with torch.no_grad():
    model(torch.randn(1, 1, 360, 640), torch.randn(1, 32))

  print(tw.flops.accumulate(model))
