import pdb
import torch
import numpy as np
import torch.nn as nn

from torch import Tensor
from torch.nn import functional as F
from torch.nn.utils.rnn import pad_packed_sequence
from torch.nn.utils.rnn import pack_padded_sequence

# typing import
from typing import Dict, Iterable, Optional

class ImageTextClassifier(nn.Module):
    def __init__(
        self, 
        num_classes: int,       # Number of classes 
        img_input_dim: int,     # Image data input dim
        text_input_dim: int,    # Text data input dim
        d_hid: int=64,          # Hidden Layer size
        en_att: bool=False,     # Enable self attention or not
        att_name: str='',       # Attention Name
        d_head: int=6           # Head dim
    ):
        super(ImageTextClassifier, self).__init__()
        self.dropout_p = 0.1
        self.en_att = en_att
        self.att_name = att_name
        
        # Projection head
        self.img_proj = nn.Sequential(
            nn.Linear(img_input_dim, d_hid),
            nn.ReLU(),
            nn.Dropout(self.dropout_p),
            nn.Linear(d_hid, d_hid)
        )
            
        # RNN module
        self.text_rnn = nn.GRU(
            input_size=text_input_dim, 
            hidden_size=d_hid, 
            num_layers=1, 
            batch_first=True, 
            dropout=self.dropout_p, 
            bidirectional=False
        )

        # Self attention module
        if self.att_name == "fuse_base":
            self.fuse_att = FuseBaseSelfAttention(
                d_hid=d_hid,
                d_head=d_head
            )
        
        # classifier head
        if self.en_att and self.att_name == "fuse_base":
            self.classifier = nn.Sequential(
                nn.Linear(d_hid*d_head, 64),
                nn.ReLU(),
                nn.Dropout(self.dropout_p),
                nn.Linear(64, num_classes)
            )
        else:
            # classifier head
            self.classifier = nn.Sequential(
                nn.Linear(d_hid*2, 64),
                nn.ReLU(),
                nn.Dropout(self.dropout_p),
                nn.Linear(64, num_classes)
            )
            
        self.init_weight()
        
    def init_weight(self):
        for m in self._modules:
            if type(m) == nn.Linear:
                torch.nn.init.xavier_uniform(m.weight)
                m.bias.data.fill_(0.01)
            if type(m) == nn.Conv1d:
                torch.nn.init.xavier_uniform(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x_img, x_text, len_i, len_t):
        # 1. img proj
        x_img = self.img_proj(x_img[:, 0, :])
        
        # 2. Rnn forward
        if len_t[0] != 0:
            x_text = pack_padded_sequence(
                x_text, 
                len_t.cpu().numpy(), 
                batch_first=True, 
                enforce_sorted=False
            )
        x_text, _ = self.text_rnn(x_text)
        if len_t[0] != 0:
            x_text, _ = pad_packed_sequence(x_text, batch_first=True)
        
        # 3. Attention
        if self.en_att:
            if self.att_name == "fuse_base":
                # get attention output
                x_mm = torch.cat((x_img.unsqueeze(dim=1), x_text), dim=1)
                x_mm = self.fuse_att(x_mm, len_i, len_t, 1)
        else:
            # 4. Average pooling
            x_text = torch.mean(x_text, axis=1)
            x_mm = torch.cat((x_img, x_text), dim=1)
            
        # 4. MM embedding and predict
        preds = self.classifier(x_mm)
        return preds, x_mm

