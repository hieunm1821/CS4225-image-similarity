from pyspark.sql import Row
import torch
import torch.nn as nn
import torchvision.models as models
from torch.autograd import Variable

pretrained_model = torch.load('resnet50-0676ba61.pth')
resnet50 = models.resnet50(pretrained=False)
resnet50.load_state_dict(pretrained_model, strict=False)

modules=list(resnet50.children())[:-1]
resnet50=nn.Sequential(*modules)
for p in resnet50.parameters():
    p.requires_grad = False
    
import PIL
import numpy as np
from torchvision.transforms import transforms
test_transforms = transforms.Compose([transforms.Resize(224),
                                      transforms.ToTensor(),
                                     ])

def encode_row(row):
    row_dict = row.asDict()
    img = PIL.Image.open(row_dict["path"])
    image_tensor = test_transforms(img).float()
    image_tensor = image_tensor.unsqueeze_(0)
    img_var = Variable(image_tensor) # assign it to a variable
    features_var = resnet50(img_var) # get the output from the last hidden layer of the pretrained resnet
    features = features_var.data # get the tensor out of the variable
    features_list = features.flatten().tolist()
    features_string = ','.join([str(elem) for elem in features_list])
    row_dict["vector"] = features_string
    newrow = Row(**row_dict)
    return newrow

def encode(img_path):
    img = PIL.Image.open(img_path)
    image_tensor = test_transforms(img).float()
    image_tensor = image_tensor.unsqueeze_(0)
    img_var = Variable(image_tensor) # assign it to a variable
    features_var = resnet50(img_var) # get the output from the last hidden layer of the pretrained resnet
    features = features_var.data # get the tensor out of the variable
    return features.flatten().tolist()