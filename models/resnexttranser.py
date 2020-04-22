import os
import torchvision
from PIL import Image
from torchvision import datasets, models, transforms
import torch
import torch.nn as nn
import torch.nn.functional as F

classes=133
input_size=224

# instantiate the CNN
#model_transfer = models.resnext101_32x8d(pretrained=True, progress=True)