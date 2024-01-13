import os
import sys
sys.path.append('C:/Users/yebin/바탕 화면/신경공학 기말/FINAL/main/StyleGAN')

import torch
import torch.optim as optim
import torch.nn as nn
from torchvision import models
from torchvision.utils import save_image
from torchvision import transforms
from collections import OrderedDict
import numpy as np
import pickle
import torch_utils
from PIL import Image
from lpips import LPIPS
from math import log10
from tqdm import tqdm
import re
from PIL import Image, ImageDraw, ImageFont


def generate_ideal_type(recommendation_list, sex, pkl_path, latent_path, result_dir, active_or_passive):
    ## 디바이스 설정
    #device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'

    ## StyleGAN 로드
    with open(f'{pkl_path}/stylegan3-r-ffhqu-1024x1024.pkl', 'rb') as f:
        G = pickle.load(f)['G_ema'].to(device)

    g_all = nn.Sequential(OrderedDict([('g_mapping', G.mapping),
            ('g_synthesis', G.synthesis)
        ]))

    g_all.eval()
    g_all.to(device)
    g_mapping, g_synthesis = g_all[0],g_all[1]
    print(device)

    ## latent vector 로드
    latents  = []
    for i in recommendation_list:
        latent = np.load(f'{latent_path}/latent{i}.npy')
        latent = torch.tensor(latent, dtype=torch.float32, device=device)
        latents.append(latent)


    ## latent vector 가중합
    weight = [0.5, 0.3, 0.1, 0.05, 0.02, 0.01, 0.01, 0.01][:len(recommendation_list)] # latent vector 합칠 전체 가중치
    for idx, latent in enumerate(latents):
        if idx == 0:
            latents[0] = latent * weight[idx]
        else:
            latents[0] += latent * weight[idx]

    ## 합성 이미지 생성 및 저장
    syn_img = g_synthesis(latents[0])
    syn_img = (syn_img+1.0)/2.0
    save_image(syn_img.clamp(0,1),f"{result_dir}/{active_or_passive}_{sex}_ideal_type.png")
    
    ## 이미지 보여주기
    syntesis_image = Image.open(f"{result_dir}/{active_or_passive}_{sex}_ideal_type.png")

    # 글씨 쓰기
    draw = ImageDraw.Draw(syntesis_image)
    text = f'[{active_or_passive}]'
    font_size = 70 
    font = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", font_size)
    
    # 텍스트 너비와 높이를 구하고 이미지 중앙 하단에 위치시키기
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (syntesis_image.width - text_width) // 2
    bottom_margin = 10  # 하단 여백 크기
    text_y = syntesis_image.height - text_height - bottom_margin
    
    # 텍스트 그리기 (검은색)
    draw.text((text_x, text_y), text, font=font, fill="black")   
    
    syntesis_image.show() 