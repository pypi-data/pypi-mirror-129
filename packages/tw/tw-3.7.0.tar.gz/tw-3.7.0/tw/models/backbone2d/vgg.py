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
"""VGG form torchvision.model """
import torch
import torch.nn as nn
from tw.utils.checkpoint import load_state_dict_from_url

model_urls = {
    'vgg11': 'https://download.pytorch.org/models/vgg11-bbd30ac9.pth',
    'vgg13': 'https://download.pytorch.org/models/vgg13-c768596a.pth',
    'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
    'vgg19': 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth',
    'vgg11_bn': 'https://download.pytorch.org/models/vgg11_bn-6002323d.pth',
    'vgg13_bn': 'https://download.pytorch.org/models/vgg13_bn-abd245e5.pth',
    'vgg16_bn': 'https://download.pytorch.org/models/vgg16_bn-6c64b313.pth',
    'vgg19_bn': 'https://download.pytorch.org/models/vgg19_bn-c79401a0.pth',
}


class VGG(nn.Module):

  MEAN = [0.485, 0.456, 0.406]
  STD = [0.229, 0.224, 0.225]
  SIZE = [224, 224]
  SCALE = 255
  CROP = 0.875

  def __init__(self, features, num_classes=1000, init_weights=True):
    super(VGG, self).__init__()
    self.features = features
    self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
    self.classifier = nn.Sequential(
        nn.Linear(512 * 7 * 7, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, num_classes),
    )
    if init_weights:
      self._initialize_weights()

  def forward(self, x):
    x = self.features(x)
    x = self.avgpool(x)
    x = torch.flatten(x, 1)
    x = self.classifier(x)
    return x

  def _initialize_weights(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
          nn.init.constant_(m.bias, 0)
      elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias, 0)
      elif isinstance(m, nn.Linear):
        nn.init.normal_(m.weight, 0, 0.01)
        nn.init.constant_(m.bias, 0)


def make_layers(cfg, batch_norm=False):
  layers = []
  in_channels = 3
  for v in cfg:
    if v == 'M':
      layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
    else:
      conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
      if batch_norm:
        layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
      else:
        layers += [conv2d, nn.ReLU(inplace=True)]
      in_channels = v
  return nn.Sequential(*layers)


cfgs = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}


def _vgg(arch, cfg, batch_norm, pretrained, **kwargs):
  if pretrained:
    kwargs['init_weights'] = False
  model = VGG(make_layers(cfgs[cfg], batch_norm=batch_norm), **kwargs)
  if pretrained:
    load_state_dict_from_url(model, model_urls[arch])
  return model


def vgg11(pretrained=False, **kwargs):
  """VGG 11-layer model (configuration "A") from
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg11', 'A', False, pretrained, **kwargs)


def vgg11_bn(pretrained=False, **kwargs):
  """VGG 11-layer model (configuration "A") with batch normalization
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg11_bn', 'A', True, pretrained, **kwargs)


def vgg13(pretrained=False, **kwargs):
  """VGG 13-layer model (configuration "B")
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg13', 'B', False, pretrained, **kwargs)


def vgg13_bn(pretrained=False, **kwargs):
  """VGG 13-layer model (configuration "B") with batch normalization
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg13_bn', 'B', True, pretrained, **kwargs)


def vgg16(pretrained=False, **kwargs):
  """VGG 16-layer model (configuration "D")
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg16', 'D', False, pretrained, **kwargs)


def vgg16_bn(pretrained=False, **kwargs):
  """VGG 16-layer model (configuration "D") with batch normalization
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg16_bn', 'D', True, pretrained, **kwargs)


def vgg19(pretrained=False, **kwargs):
  """VGG 19-layer model (configuration "E")
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg19', 'E', False, pretrained, **kwargs)


def vgg19_bn(pretrained=False, **kwargs):
  """VGG 19-layer model (configuration 'E') with batch normalization
  `"Very Deep Convolutional Networks For Large-Scale Image Recognition" <https://arxiv.org/pdf/1409.1556.pdf>`_

  Args:
      pretrained (bool): If True, returns a model pre-trained on ImageNet
      progress (bool): If True, displays a progress bar of the download to stderr
  """
  return _vgg('vgg19_bn', 'E', True, pretrained, **kwargs)
