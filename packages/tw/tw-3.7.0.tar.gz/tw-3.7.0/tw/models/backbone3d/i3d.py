# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
"""I3D"""

import tw
import torch.nn


def get_padding_shape(filter_shape, stride):
  def _pad_top_bottom(filter_dim, stride_val):
    pad_along = max(filter_dim - stride_val, 0)
    pad_top = pad_along // 2
    pad_bottom = pad_along - pad_top
    return pad_top, pad_bottom

  padding_shape = []
  for filter_dim, stride_val in zip(filter_shape, stride):
    pad_top, pad_bottom = _pad_top_bottom(filter_dim, stride_val)
    padding_shape.append(pad_top)
    padding_shape.append(pad_bottom)
  depth_top = padding_shape.pop(0)
  depth_bottom = padding_shape.pop(0)
  padding_shape.append(depth_top)
  padding_shape.append(depth_bottom)

  return tuple(padding_shape)


def simplify_padding(padding_shapes):
  all_same = True
  padding_init = padding_shapes[0]
  for pad in padding_shapes[1:]:
    if pad != padding_init:
      all_same = False
  return all_same, padding_init


class Unit3Dpy(torch.nn.Module):
  def __init__(self,
               in_channels,
               out_channels,
               kernel_size=(1, 1, 1),
               stride=(1, 1, 1),
               activation='relu',
               padding='SAME',
               use_bias=False,
               use_bn=True):
    super(Unit3Dpy, self).__init__()

    self.padding = padding
    self.activation = activation
    self.use_bn = use_bn
    if padding == 'SAME':
      padding_shape = get_padding_shape(kernel_size, stride)
      simplify_pad, pad_size = simplify_padding(padding_shape)
      self.simplify_pad = simplify_pad
    elif padding == 'VALID':
      padding_shape = 0
    else:
      raise ValueError(
          'padding should be in [VALID|SAME] but got {}'.format(padding))

    if padding == 'SAME':
      if not simplify_pad:
        self.pad = torch.nn.ConstantPad3d(padding_shape, 0)
        self.conv3d = torch.nn.Conv3d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            bias=use_bias)
      else:
        self.conv3d = torch.nn.Conv3d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            padding=pad_size,
            bias=use_bias)
    elif padding == 'VALID':
      self.conv3d = torch.nn.Conv3d(
          in_channels,
          out_channels,
          kernel_size,
          padding=padding_shape,
          stride=stride,
          bias=use_bias)
    else:
      raise ValueError(
          'padding should be in [VALID|SAME] but got {}'.format(padding))

    if self.use_bn:
      self.batch3d = torch.nn.BatchNorm3d(out_channels)

    if activation == 'relu':
      self.activation = torch.nn.functional.relu

  def forward(self, inp):
    if self.padding == 'SAME' and self.simplify_pad is False:
      inp = self.pad(inp)
    out = self.conv3d(inp)
    if self.use_bn:
      out = self.batch3d(out)
    if self.activation is not None:
      out = torch.nn.functional.relu(out)
    return out


class MaxPool3dTFPadding(torch.nn.Module):
  def __init__(self, kernel_size, stride=None, padding='SAME'):
    super(MaxPool3dTFPadding, self).__init__()
    if padding == 'SAME':
      padding_shape = get_padding_shape(kernel_size, stride)
      self.padding_shape = padding_shape
      self.pad = torch.nn.ConstantPad3d(padding_shape, 0)
    self.pool = torch.nn.MaxPool3d(kernel_size, stride)

  def forward(self, inp):
    inp = self.pad(inp)
    out = self.pool(inp)
    return out


class Mixed(torch.nn.Module):
  def __init__(self, in_channels, out_channels):
    super(Mixed, self).__init__()
    # Branch 0
    self.branch_0 = Unit3Dpy(
        in_channels, out_channels[0], kernel_size=(1, 1, 1))

    # Branch 1
    branch_1_conv1 = Unit3Dpy(
        in_channels, out_channels[1], kernel_size=(1, 1, 1))
    branch_1_conv2 = Unit3Dpy(
        out_channels[1], out_channels[2], kernel_size=(3, 3, 3))
    self.branch_1 = torch.nn.Sequential(branch_1_conv1, branch_1_conv2)

    # Branch 2
    branch_2_conv1 = Unit3Dpy(
        in_channels, out_channels[3], kernel_size=(1, 1, 1))
    branch_2_conv2 = Unit3Dpy(
        out_channels[3], out_channels[4], kernel_size=(3, 3, 3))
    self.branch_2 = torch.nn.Sequential(branch_2_conv1, branch_2_conv2)

    # Branch3
    branch_3_pool = MaxPool3dTFPadding(
        kernel_size=(3, 3, 3), stride=(1, 1, 1), padding='SAME')
    branch_3_conv2 = Unit3Dpy(
        in_channels, out_channels[5], kernel_size=(1, 1, 1))
    self.branch_3 = torch.nn.Sequential(branch_3_pool, branch_3_conv2)

  def forward(self, inp):
    out_0 = self.branch_0(inp)
    out_1 = self.branch_1(inp)
    out_2 = self.branch_2(inp)
    out_3 = self.branch_3(inp)
    out = torch.cat((out_0, out_1, out_2, out_3), 1)
    return out


class I3D(torch.nn.Module):
  def __init__(self,
               num_classes,
               modality='rgb',
               dropout_keep_prob=0.5,
               name='inception'):
    super(I3D, self).__init__()

    self.name = name
    self.num_classes = num_classes
    if modality == 'rgb':
      in_channels = 3
    elif modality == 'flow':
      in_channels = 2
    else:
      raise ValueError(
          '{} not among known modalities [rgb|flow]'.format(modality))
    self.modality = modality

    conv3d_1a_7x7 = Unit3Dpy(
        out_channels=64,
        in_channels=in_channels,
        kernel_size=(7, 7, 7),
        stride=(2, 2, 2),
        padding='SAME')
    # 1st conv-pool
    self.conv3d_1a_7x7 = conv3d_1a_7x7
    self.maxPool3d_2a_3x3 = MaxPool3dTFPadding(
        kernel_size=(1, 3, 3), stride=(1, 2, 2), padding='SAME')
    # conv conv
    conv3d_2b_1x1 = Unit3Dpy(
        out_channels=64,
        in_channels=64,
        kernel_size=(1, 1, 1),
        padding='SAME')
    self.conv3d_2b_1x1 = conv3d_2b_1x1
    conv3d_2c_3x3 = Unit3Dpy(
        out_channels=192,
        in_channels=64,
        kernel_size=(3, 3, 3),
        padding='SAME')
    self.conv3d_2c_3x3 = conv3d_2c_3x3
    self.maxPool3d_3a_3x3 = MaxPool3dTFPadding(
        kernel_size=(1, 3, 3), stride=(1, 2, 2), padding='SAME')

    # Mixed_3b
    self.mixed_3b = Mixed(192, [64, 96, 128, 16, 32, 32])
    self.mixed_3c = Mixed(256, [128, 128, 192, 32, 96, 64])

    self.maxPool3d_4a_3x3 = MaxPool3dTFPadding(
        kernel_size=(3, 3, 3), stride=(2, 2, 2), padding='SAME')

    # Mixed 4
    self.mixed_4b = Mixed(480, [192, 96, 208, 16, 48, 64])
    self.mixed_4c = Mixed(512, [160, 112, 224, 24, 64, 64])
    self.mixed_4d = Mixed(512, [128, 128, 256, 24, 64, 64])
    self.mixed_4e = Mixed(512, [112, 144, 288, 32, 64, 64])
    self.mixed_4f = Mixed(528, [256, 160, 320, 32, 128, 128])

    # Ugly hack because I didn't use tensorflow's exact padding function
    self.pad_5a = torch.nn.ConstantPad3d((0, 0, 0, 0, 0, 1), 0)
    self.maxPool3d_5a_2x2 = MaxPool3dTFPadding(
        kernel_size=(2, 2, 2), stride=(2, 2, 2), padding='SAME')

    # Mixed 5
    self.mixed_5b = Mixed(832, [256, 160, 320, 32, 128, 128])
    self.mixed_5c = Mixed(832, [384, 192, 384, 48, 128, 128])

    # self.avg_pool = torch.nn.AvgPool3d((2, 7, 7), (1, 1, 1))
    self.avg_pool = torch.nn.AdaptiveAvgPool3d((2, 1, 1))
    self.dropout = torch.nn.Dropout(dropout_keep_prob)
    self.conv3d_0c_1x1 = Unit3Dpy(
        in_channels=1024,
        out_channels=self.num_classes,
        kernel_size=(1, 1, 1),
        activation=None,
        use_bias=True,
        use_bn=False)
    self.endpoints = {}

    # [NOTE] remove out softmax layer
    # self.softmax = torch.nn.Softmax(1)

  def forward(self, inp):
    # Preprocessing
    out = self.conv3d_1a_7x7(inp)
    out = self.maxPool3d_2a_3x3(out)
    out = self.conv3d_2b_1x1(out)
    out = self.conv3d_2c_3x3(out)
    self.endpoints['2c'] = out
    out = self.maxPool3d_3a_3x3(out)
    out = self.mixed_3b(out)
    out = self.mixed_3c(out)
    self.endpoints['3c'] = out
    out = self.maxPool3d_4a_3x3(out)
    out = self.mixed_4b(out)
    out = self.mixed_4c(out)
    out = self.mixed_4d(out)
    out = self.mixed_4e(out)
    out = self.mixed_4f(out)
    self.endpoints['4f'] = out
    out = self.pad_5a(out)
    out = self.maxPool3d_5a_2x2(out)
    out = self.mixed_5b(out)
    out = self.mixed_5c(out)
    self.endpoints['5c'] = out
    out = self.avg_pool(out)
    self.endpoints['gap'] = out
    out = self.dropout(out)
    out = self.conv3d_0c_1x1(out)
    out = out.squeeze(3)
    out = out.squeeze(3)
    out = out.mean(2)
    # [NOTE] where we remove out softmax layer
    # out_logits = out
    # out = self.softmax(out_logits)
    return out  # , out_logits


if __name__ == '__main__':
  model = I3D(num_classes=400, modality='rgb')
  # if modality=='Flow', please change the 2nd dimension 3==>2
  data = torch.autograd.Variable(torch.rand(10, 3, 16, 224, 224))
  out = model(data)
  # print(model)
  # print(out[0].size())
