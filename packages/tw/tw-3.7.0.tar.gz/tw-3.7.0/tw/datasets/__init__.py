# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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

from .base import SampleCollator
from .base import BatchMultiSampler

from .mnist import Mnist
from .cifar import Cifar10
from .imagenet import ImageNet
from .widerface import WiderFace, WiderFaceTest
from .coco import CocoDetection

from .avec2014 import Avec2014
from .avec2014 import Avec2014Video

from .general import ImageLabel
from .general import ImageSalientDet
from .general import ImagesDataset
from .general import ImageEnhance
from .general import ImageFolderEnhance
from .general import VideoFolderEnhance

from .quality_assess import PIPAL
from .quality_assess import TID2013
from .quality_assess import KonIQ10k
from .quality_assess import SPAQ
from .quality_assess import LIVEC
from .quality_assess import LIVE2005
from .quality_assess import LIVEMD
from .quality_assess import CSIQ
from .quality_assess import FLIVE
from .quality_assess import VQA_III

from .point_cloud import SensatUrban

from . import pil

from torch.utils.data import *
