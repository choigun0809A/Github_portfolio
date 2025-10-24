import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as f
import numpy as np
from model.components import comp as cp
import sys

## generative model this was
class ModelV1(nn.Module):
    def __init__(self, heads, transformers, dmodel, d_hidden, input_size, output_size, drop_out=0.2):
        super().__init__()
        self.embedding = cp.ScalarDmode(dmodel)
        self.pe = cp.PositionalEncoding()
        
        self.transformers = nn.ModuleList(
            [cp.Transformerblock(dmodel,d_hidden, heads, drop_out) for _ in range(transformers)]      
        )
        
        self.out = nn.Linear(dmodel, output_size)
        
        self.optimizer = optim.Adam(self.parameters(), lr=0.0001)
        self.cross_entr= nn.CrossEntropyLoss()
        self.smoothl1loss = nn.SmoothL1Loss()
        self.mse = nn.MSELoss()
        
    
    def forward(self, x: torch.Tensor, masked: bool):
        x = self.embedding(x)
        x = self.pe.forward(x)
        
        for transformer in self.transformers:
            x = transformer.forward(x, masked)
        
        x = self.out(x)
        x_sum = torch.sum(x, dim=1)
        return x_sum
    
## layered model this is
class ModelV2(nn.Module):
    def __init__(self, input_size = 4, output_size = 4):
        super().__init__()
        
        self.l1 = nn.Linear(input_size, 64)
        self.gelu1 = nn.GELU()
        self.l2 = nn.Linear(64, 256)
        self.gelu2 = nn.GELU()
        self.l3 = nn.Linear(256, 256)
        self.gelu3 = nn.GELU()
        self.l4 = nn.Linear(256, 64)
        self.gelu4 = nn.GELU()
        
        self.out = nn.Linear(64, output_size)
        
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.cross_entr= nn.CrossEntropyLoss()
        self.smoothl1loss = nn.SmoothL1Loss()
        self.mse = nn.MSELoss()
    
    def forward(self, x: torch.Tensor, masked: bool = False):
        x = self.l1(x)
        x = self.gelu1(x)
        x = self.l2(x)
        x = self.gelu2(x)
        x = self.l3(x)
        x = self.gelu3(x)
        x = self.l4(x)
        x = self.gelu4(x)
        
        x = self.out(x)
        # print(x)
        return x
    

class ModelV3(nn.Module):
    def __init__(self, input_size = 4, output_size = 4):
        super().__init__()
        
        self.l1 = nn.Linear(input_size, 256)
        self.gelu1 = nn.GELU()
        self.l2 = nn.Linear(256, 512)
        self.gelu2 = nn.GELU()
        self.l3 = nn.Linear(512, 512)
        self.gelu3 = nn.GELU()
        self.l4 = nn.Linear(512, 512)
        self.gelu4 = nn.GELU()
        self.l5 = nn.Linear(512, 256)
        
        self.out = nn.Linear(256, output_size)
        
        self.optimizer = optim.Adam(self.parameters(), lr=0.0001)
        self.cross_entr= nn.CrossEntropyLoss()
        self.smoothl1loss = nn.SmoothL1Loss()
        self.mse = nn.MSELoss()
    
    def forward(self, x: torch.Tensor, masked: bool = False):
        x = self.l1(x)
        x = self.gelu1(x)
        x = self.l2(x)
        x = self.gelu2(x)
        x = self.l3(x)
        x = self.gelu3(x)
        x = self.l4(x)
        x = self.gelu4(x)
        x = self.l5(x)
        
        x = self.out(x)
        # print(x)
        return x
    
class ModelV4(nn.Module):
    def __init__(self, output_size=4):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 2, padding='same'),
            nn.BatchNorm2d(16),
            nn.GELU(),

            nn.Conv2d(16, 32, 2, padding='same'),
            nn.BatchNorm2d(32),
            nn.GELU(),

            nn.Conv2d(32, 64, 2, padding='same'),
            nn.BatchNorm2d(64),
            nn.GELU(),

            nn.Conv2d(64, 128, 2, padding='same'),
            nn.BatchNorm2d(128),
            nn.GELU(),

            nn.MaxPool2d(2, 2)
        )

        self.classifier = nn.Sequential(
            nn.Linear(128*5*5, 512),
            nn.GELU(),
            nn.Linear(512, 512),
            nn.GELU(),
            nn.Linear(512, 256),
            nn.GELU(),
            nn.Linear(256, output_size)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=1e-4)
        self.cross_entr = nn.CrossEntropyLoss()
        self.smoothl1loss = nn.SmoothL1Loss()
        self.mse = nn.MSELoss()

    def forward(self, x):
        x = self.features(x)
        x = x.view(-1, 128*5*5)
        x = self.classifier(x)
        return x