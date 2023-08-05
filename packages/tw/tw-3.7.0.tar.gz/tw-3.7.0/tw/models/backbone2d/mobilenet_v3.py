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
"""
  Creates a MobileNetV3 Model as defined in:
  Andrew Howard, Mark Sandler, Grace Chu, Liang-Chieh Chen, Bo Chen, Mingxing Tan, 
  Weijun Wang, Yukun Zhu, Ruoming Pang, Vijay Vasudevan, Quoc V. Le, Hartwig Adam. (2019).
  
  Searching for MobileNetV3
  
  arXiv preprint arXiv:1905.02244.
"""
import functools
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

import tw

from .efficientnet import EfficientNetBuilder
from .efficientnet import efficientnet_init_weights
from .efficientnet import resolve_bn_args
from .efficientnet import build_model_with_cfg
from .efficientnet import decode_arch_def
from .efficientnet import decode_arch_def

IMAGENET_INCEPTION_MEAN = (0.5, 0.5, 0.5)
IMAGENET_INCEPTION_STD = (0.5, 0.5, 0.5)
IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)
BN_EPS_TF_DEFAULT = 1e-3


def _cfg(url='', **kwargs):
  return {
      'url': url, 'num_classes': 1000, 'input_size': (3, 224, 224), 'pool_size': (1, 1),
      'crop_pct': 0.875, 'interpolation': 'bilinear',
      'mean': IMAGENET_DEFAULT_MEAN, 'std': IMAGENET_DEFAULT_STD,
      'first_conv': 'conv_stem', 'classifier': 'classifier',
      **kwargs
  }


default_cfgs = {
    'mobilenetv3_large_075': _cfg(url=''),
    'mobilenetv3_large_100': _cfg(
        interpolation='bicubic',
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/mobilenetv3_large_100_ra-f55367f5.pth'),
    'mobilenetv3_large_100_miil': _cfg(
        interpolation='bilinear', mean=(0, 0, 0), std=(1, 1, 1),
        url='https://miil-public-eu.oss-eu-central-1.aliyuncs.com/model-zoo/ImageNet_21K_P/models/timm/mobilenetv3_large_100_1k_miil_78_0.pth'),
    'mobilenetv3_large_100_miil_in21k': _cfg(
        interpolation='bilinear', mean=(0, 0, 0), std=(1, 1, 1),
        url='https://miil-public-eu.oss-eu-central-1.aliyuncs.com/model-zoo/ImageNet_21K_P/models/timm/mobilenetv3_large_100_in21k_miil.pth', num_classes=11221),
    'mobilenetv3_small_075': _cfg(url=''),
    'mobilenetv3_small_100': _cfg(url=''),

    'mobilenetv3_rw': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/mobilenetv3_100-35495452.pth',
        interpolation='bicubic'),

    'tf_mobilenetv3_large_075': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_large_075-150ee8b0.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
    'tf_mobilenetv3_large_100': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_large_100-427764d5.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
    'tf_mobilenetv3_large_minimal_100': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_large_minimal_100-8596ae28.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
    'tf_mobilenetv3_small_075': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_small_075-da427f52.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
    'tf_mobilenetv3_small_100': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_small_100-37f49e2b.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),
    'tf_mobilenetv3_small_minimal_100': _cfg(
        url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/tf_mobilenetv3_small_minimal_100-922a7843.pth',
        mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD),

    'fbnetv3_b': _cfg(),
    'fbnetv3_d': _cfg(),
    'fbnetv3_g': _cfg(),
}


class MobileNetV3(nn.Module):
  """ MobiletNet-V3

  Based on my EfficientNet implementation and building blocks, this model utilizes the MobileNet-v3 specific
  'efficient head', where global pooling is done before the head convolution without a final batch-norm
  layer before the classifier.

  Paper: https://arxiv.org/abs/1905.02244
  """

  MEAN = [0.485, 0.456, 0.406]
  STD = [0.229, 0.224, 0.225]
  SIZE = [224, 224]
  SCALE = 255
  CROP = 0.875

  def __init__(self, block_args, num_classes=1000, in_chans=3, stem_size=16, num_features=1280, head_bias=True,
               pad_type='', act_layer=None, norm_layer=None, se_layer=None, se_from_exp=True,
               round_chs_fn=tw.nn.conv._round_channels, drop_rate=0., drop_path_rate=0., global_pool='avg',
               output_backbone=False):
    super(MobileNetV3, self).__init__()
    act_layer = act_layer or nn.ReLU
    norm_layer = norm_layer or nn.BatchNorm2d
    se_layer = se_layer or tw.nn.SqueezeExciteModule
    self.num_classes = num_classes
    self.num_features = num_features
    self.drop_rate = drop_rate
    self.output_backbone = output_backbone

    # Stem
    stem_size = round_chs_fn(stem_size)
    self.conv_stem = tw.nn.conv._create_conv2d(in_chans, stem_size, 3, stride=2, padding=pad_type)
    self.bn1 = norm_layer(stem_size)
    self.act1 = act_layer()

    # Middle stages (IR/ER/DS Blocks)
    builder = EfficientNetBuilder(
        output_stride=32, pad_type=pad_type, round_chs_fn=round_chs_fn, se_from_exp=se_from_exp,
        act_layer=act_layer, norm_layer=norm_layer, se_layer=se_layer, drop_path_rate=drop_path_rate)
    self.blocks = nn.Sequential(*builder(stem_size, block_args))
    self.feature_info = builder.features
    head_chs = builder.in_chs

    # Head + Pooling
    coeff = 1
    if global_pool == 'avg':
      self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
    elif global_pool == 'max':
      self.global_pool = nn.AdaptiveMaxPool2d((1, 1))
    elif global_pool == 'avgmax':
      self.global_pool = tw.nn.AdaptiveAvgMaxPool2d(1)
    elif global_pool == 'catavgam':
      self.global_pool = tw.nn.AdaptiveCatAvgMaxPool2d(1)
      coeff = 2
    else:
      raise NotImplementedError(global_pool)

    num_pooled_chs = head_chs * coeff
    self.conv_head = tw.nn.conv._create_conv2d(num_pooled_chs, self.num_features, 1, padding=pad_type, bias=head_bias)
    self.act2 = act_layer()
    self.flatten = nn.Flatten(1) if global_pool else nn.Identity()  # don't flatten if pooling disabled

    # build fc
    if num_classes <= 0:
      self.classifier = nn.Identity()
    else:
      self.classifier = nn.Linear(self.num_features, num_classes)

    efficientnet_init_weights(self)

  # def as_sequential(self):
  #   layers = [self.conv_stem, self.bn1, self.act1]
  #   layers.extend(self.blocks)
  #   layers.extend([self.global_pool, self.conv_head, self.act2])
  #   layers.extend([nn.Flatten(), nn.Dropout(self.drop_rate), self.classifier])
  #   return nn.Sequential(*layers)

  # def get_classifier(self):
  #   return self.classifier

  # def reset_classifier(self, num_classes, global_pool='avg'):
  #   self.num_classes = num_classes
  #   # cannot meaningfully change pooling of efficient head after creation
  #   self.global_pool = SelectAdaptivePool2d(pool_type=global_pool)
  #   self.flatten = nn.Flatten(1) if global_pool else nn.Identity()  # don't flatten if pooling disabled
  #   self.classifier = Linear(self.num_features, num_classes) if num_classes > 0 else nn.Identity()

  def forward(self, x):
    x = self.conv_stem(x)
    x = self.bn1(x)
    x = self.act1(x)
    x = self.blocks(x)
    x = self.global_pool(x)
    x = self.conv_head(x)
    if self.output_backbone:
      return x, x, x, x
    x = self.act2(x)
    x = self.flatten(x)
    if self.drop_rate > 0.:
      x = F.dropout(x, p=self.drop_rate, training=self.training)
    return self.classifier(x)


def _create_mnv3(variant, pretrained=False, **kwargs):
  features_only = False
  model_cls = MobileNetV3
  kwargs_filter = None
  model = build_model_with_cfg(
      model_cls, variant, pretrained,
      default_cfg=default_cfgs[variant],
      pretrained_strict=not features_only,
      kwargs_filter=kwargs_filter,
      **kwargs)
  return model


def _gen_mobilenet_v3_rw(variant, channel_multiplier=1.0, pretrained=False, **kwargs):
  """Creates a MobileNet-V3 model.

  Ref impl: ?
  Paper: https://arxiv.org/abs/1905.02244

  Args:
    channel_multiplier: multiplier to number of channels per layer.
  """
  arch_def = [
      # stage 0, 112x112 in
      ['ds_r1_k3_s1_e1_c16_nre_noskip'],  # relu
      # stage 1, 112x112 in
      ['ir_r1_k3_s2_e4_c24_nre', 'ir_r1_k3_s1_e3_c24_nre'],  # relu
      # stage 2, 56x56 in
      ['ir_r3_k5_s2_e3_c40_se0.25_nre'],  # relu
      # stage 3, 28x28 in
      ['ir_r1_k3_s2_e6_c80', 'ir_r1_k3_s1_e2.5_c80', 'ir_r2_k3_s1_e2.3_c80'],  # hard-swish
      # stage 4, 14x14in
      ['ir_r2_k3_s1_e6_c112_se0.25'],  # hard-swish
      # stage 5, 14x14in
      ['ir_r3_k5_s2_e6_c160_se0.25'],  # hard-swish
      # stage 6, 7x7 in
      ['cn_r1_k1_s1_c960'],  # hard-swish
  ]
  model_kwargs = dict(
      block_args=decode_arch_def(arch_def),
      head_bias=False,
      round_chs_fn=functools.partial(tw.nn.conv._round_channels, multiplier=channel_multiplier),
      norm_layer=functools.partial(nn.BatchNorm2d, **resolve_bn_args(kwargs)),
      act_layer=nn.Hardswish,
      se_layer=functools.partial(tw.nn.SqueezeExciteModule, gate_layer=nn.Hardsigmoid),
      **kwargs,
  )
  model = _create_mnv3(variant, pretrained, **model_kwargs)
  return model


def _gen_mobilenet_v3(variant, channel_multiplier=1.0, pretrained=False, **kwargs):
  """Creates a MobileNet-V3 model.

  Ref impl: ?
  Paper: https://arxiv.org/abs/1905.02244

  Args:
    channel_multiplier: multiplier to number of channels per layer.
  """
  if 'small' in variant:
    num_features = 1024
    if 'minimal' in variant:
      act_layer = nn.ReLU
      arch_def = [
          # stage 0, 112x112 in
          ['ds_r1_k3_s2_e1_c16'],
          # stage 1, 56x56 in
          ['ir_r1_k3_s2_e4.5_c24', 'ir_r1_k3_s1_e3.67_c24'],
          # stage 2, 28x28 in
          ['ir_r1_k3_s2_e4_c40', 'ir_r2_k3_s1_e6_c40'],
          # stage 3, 14x14 in
          ['ir_r2_k3_s1_e3_c48'],
          # stage 4, 14x14in
          ['ir_r3_k3_s2_e6_c96'],
          # stage 6, 7x7 in
          ['cn_r1_k1_s1_c576'],
      ]
    else:
      act_layer = nn.Hardswish
      arch_def = [
          # stage 0, 112x112 in
          ['ds_r1_k3_s2_e1_c16_se0.25_nre'],  # relu
          # stage 1, 56x56 in
          ['ir_r1_k3_s2_e4.5_c24_nre', 'ir_r1_k3_s1_e3.67_c24_nre'],  # relu
          # stage 2, 28x28 in
          ['ir_r1_k5_s2_e4_c40_se0.25', 'ir_r2_k5_s1_e6_c40_se0.25'],  # hard-swish
          # stage 3, 14x14 in
          ['ir_r2_k5_s1_e3_c48_se0.25'],  # hard-swish
          # stage 4, 14x14in
          ['ir_r3_k5_s2_e6_c96_se0.25'],  # hard-swish
          # stage 6, 7x7 in
          ['cn_r1_k1_s1_c576'],  # hard-swish
      ]
  else:
    num_features = 1280
    if 'minimal' in variant:
      act_layer = nn.ReLU
      arch_def = [
          # stage 0, 112x112 in
          ['ds_r1_k3_s1_e1_c16'],
          # stage 1, 112x112 in
          ['ir_r1_k3_s2_e4_c24', 'ir_r1_k3_s1_e3_c24'],
          # stage 2, 56x56 in
          ['ir_r3_k3_s2_e3_c40'],
          # stage 3, 28x28 in
          ['ir_r1_k3_s2_e6_c80', 'ir_r1_k3_s1_e2.5_c80', 'ir_r2_k3_s1_e2.3_c80'],
          # stage 4, 14x14in
          ['ir_r2_k3_s1_e6_c112'],
          # stage 5, 14x14in
          ['ir_r3_k3_s2_e6_c160'],
          # stage 6, 7x7 in
          ['cn_r1_k1_s1_c960'],
      ]
    else:
      act_layer = nn.Hardswish
      arch_def = [
          # stage 0, 112x112 in
          ['ds_r1_k3_s1_e1_c16_nre'],  # relu
          # stage 1, 112x112 in
          ['ir_r1_k3_s2_e4_c24_nre', 'ir_r1_k3_s1_e3_c24_nre'],  # relu
          # stage 2, 56x56 in
          ['ir_r3_k5_s2_e3_c40_se0.25_nre'],  # relu
          # stage 3, 28x28 in
          ['ir_r1_k3_s2_e6_c80', 'ir_r1_k3_s1_e2.5_c80', 'ir_r2_k3_s1_e2.3_c80'],  # hard-swish
          # stage 4, 14x14in
          ['ir_r2_k3_s1_e6_c112_se0.25'],  # hard-swish
          # stage 5, 14x14in
          ['ir_r3_k5_s2_e6_c160_se0.25'],  # hard-swish
          # stage 6, 7x7 in
          ['cn_r1_k1_s1_c960'],  # hard-swish
      ]
  se_layer = functools.partial(tw.nn.SqueezeExciteModule, gate_layer=nn.Hardsigmoid,
                               force_act_layer=nn.ReLU, rd_round_fn=tw.nn.conv._round_channels)
  model_kwargs = dict(
      block_args=decode_arch_def(arch_def),
      num_features=num_features,
      stem_size=16,
      round_chs_fn=functools.partial(tw.nn.conv._round_channels, multiplier=channel_multiplier),
      norm_layer=functools.partial(nn.BatchNorm2d, **resolve_bn_args(kwargs)),
      act_layer=act_layer,
      se_layer=se_layer,
      **kwargs,
  )
  model = _create_mnv3(variant, pretrained, **model_kwargs)
  return model


def mobilenetv3_large_075(pretrained=False, **kwargs):
  """ MobileNet V3 """
  model = _gen_mobilenet_v3('mobilenetv3_large_075', 0.75, pretrained=pretrained, **kwargs)
  return model


def mobilenetv3_large_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  model = _gen_mobilenet_v3('mobilenetv3_large_100', 1.0, pretrained=pretrained, **kwargs)
  return model


def mobilenetv3_large_100_miil(pretrained=False, **kwargs):
  """ MobileNet V3
  Weights taken from: https://github.com/Alibaba-MIIL/ImageNet21K
  """
  model = _gen_mobilenet_v3('mobilenetv3_large_100_miil', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0, 0, 0]
  model.STD = [1, 1, 1]
  return model


def mobilenetv3_large_100_miil_in21k(pretrained=False, **kwargs):
  """ MobileNet V3, 21k pretraining
  Weights taken from: https://github.com/Alibaba-MIIL/ImageNet21K
  """
  model = _gen_mobilenet_v3('mobilenetv3_large_100_miil_in21k', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0, 0, 0]
  model.STD = [1, 1, 1]
  return model


def mobilenetv3_small_075(pretrained=False, **kwargs):
  """ MobileNet V3 """
  model = _gen_mobilenet_v3('mobilenetv3_small_075', 0.75, pretrained=pretrained, **kwargs)
  return model


def mobilenetv3_small_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  model = _gen_mobilenet_v3('mobilenetv3_small_100', 1.0, pretrained=pretrained, **kwargs)
  return model


def mobilenetv3_rw(pretrained=False, **kwargs):
  """ MobileNet V3 """
  if pretrained:
    # pretrained model trained with non-default BN epsilon
    kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  model = _gen_mobilenet_v3_rw('mobilenetv3_rw', 1.0, pretrained=pretrained, **kwargs)
  return model


def tf_mobilenetv3_large_075(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_large_075', 0.75, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model


def tf_mobilenetv3_large_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_large_100', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model


def tf_mobilenetv3_large_minimal_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_large_minimal_100', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model


def tf_mobilenetv3_small_075(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_small_075', 0.75, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model


def tf_mobilenetv3_small_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_small_100', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model


def tf_mobilenetv3_small_minimal_100(pretrained=False, **kwargs):
  """ MobileNet V3 """
  kwargs['bn_eps'] = BN_EPS_TF_DEFAULT
  kwargs['pad_type'] = 'same'
  model = _gen_mobilenet_v3('tf_mobilenetv3_small_minimal_100', 1.0, pretrained=pretrained, **kwargs)
  model.MEAN = [0.5, 0.5, 0.5]
  model.STD = [0.5, 0.5, 0.5]
  return model
