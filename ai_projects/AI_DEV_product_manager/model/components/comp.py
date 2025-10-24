import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
import numpy as np
import sys

class PositionalEncoding:
    def __init__(self):
        pass
    def forward(self, linear: torch.Tensor) -> np.ndarray:
        positions = np.arange(0, linear.shape[-2])
        index_vals = np.arange(0, linear.shape[-1])
        index_vals = 1 / np.power(10000, (np.float32(index_vals // 2) / linear.shape[-1]))
        
        grad = np.zeros((linear.shape[-2], linear.shape[-1]), dtype=np.float32)
        # print(grad.shape)
        grad[:, 0::2] = np.sin(positions[:, None] * index_vals[0::2])
        grad[:, 1::2] = np.cos(positions[:, None] * index_vals[1::2])
        
        grad = torch.tensor(grad, dtype=torch.float32)
        return linear + grad

class Attention(nn.Module):
    def __init__(self, d_model, heads, drop_out=0.2):
        super().__init__()
        self.small_d_model = d_model // heads
        self.heads = heads
        self.qw = nn.Linear(d_model, d_model)
        self.kw = nn.Linear(d_model, d_model)
        self.vw = nn.Linear(d_model, d_model)
        self.o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(drop_out)
    
    def forward(self, linear: torch.Tensor, masked: bool):
        batch_size, seq, d_model = linear.shape
        q: torch.Tensor = self.qw(linear)
        k: torch.Tensor = self.kw(linear)
        v: torch.Tensor = self.vw(linear)
        
        q.view(batch_size, seq, self.heads, self.small_d_model)
        k.view(batch_size, seq, self.heads, self.small_d_model)
        v.view(batch_size, seq, self.heads, self.small_d_model)
        
        q.transpose(1, 2)
        k.transpose(1, 2)
        v.transpose(1, 2)
        
            
        k_t = k.transpose(-2, -1)
        qk = torch.matmul(q, k_t)
        
        qk /= torch.sqrt(torch.tensor(q.shape[-1], dtype=torch.float32))
        
        qk = f.softmax(qk, dim=-1)
        if masked:
            zeros = torch.ones(qk.shape, dtype=torch.float32)
            mask = torch.tril(zeros)
            mask = mask.to(torch.float32)
            # print(mask.shape, qkv.shape)
            qk = torch.mul(qk, mask)
        qkv = torch.matmul(qk, v)
        
        qkv = qkv.transpose(1, 2).contiguous().view(batch_size, seq, d_model)
        out = self.o(qkv)
        out = self.dropout(out)
        
        return out

class FeedForward(nn.Module):
    def __init__(self, d_model, d_hidden, dropout):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_hidden)
        self.linear2 = nn.Linear(d_hidden, d_model)
        self.gelu = nn.GELU()
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, linear: torch.Tensor):
        return self.dropout(self.linear2(self.gelu(self.linear1(linear))))        

class ScalarDmode(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.net =nn.Sequential(
            nn.Linear(1, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model),
        )
    
    def forward(self, linear: torch.Tensor):
        return self.net(linear.unsqueeze(-1))

class Transformerblock(nn.Module):
    def __init__(self, d_model, d_hidden, heads, dropout):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attention = Attention(d_model, heads, dropout)
        
        self.norm2 = nn.LayerNorm(d_model)
        self.ff_block = FeedForward(d_model, d_hidden , dropout)
        
    
    def forward(self, linear: torch.Tensor, masked = False):
        linear = linear + self.attention(self.norm1(linear), masked)
        linear = linear + self.ff_block(self.norm2(linear))
        
        return linear