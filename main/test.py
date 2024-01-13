from typing import List

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from StyleGAN.generate_ideal_type import generate_ideal_type


# def make_result_images(
#     image_nums: List, image_folder: str, result_dir: str, 
# ):
#     image_nums = [x + 1 for x in image_nums]
#     images = [Image.open(f"{image_folder}/F{i}.jpg") for i in image_nums]
#     print(images[0].size)
#     # Calculate the width and height of the combined image
#     combined_width = 512*(len(image_nums)//2 +1)
#     combined_height = 512*2  # Choose the maximum height

#     # Create a new blank image with the calculated dimensions
#     combined_image = Image.new("RGB", (combined_width, combined_height), color="white")

#     # Paste the three images onto the new image
#     for i in range(len(image_nums)):
#         if i < len(image_nums)//2 +1:
#             combined_image.paste(images[i], (512*i, 0))
#         else:        
#             combined_image.paste(images[i], (512*(i-len(image_nums)//2 -1), 512))

#     draw = ImageDraw.Draw(combined_image)
#     text = f'당신의 선택은 {image_nums} 입니다.'
#     font_size = 50
#     font = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", font_size)
#     # 텍스트 너비와 높이를 구하고 이미지 중앙 상단에 위치시키기
#     text_width, text_height = draw.textsize(text, font=font)
#     text_x = (combined_image.width - text_width) // 2
#     text_y = 10  # 상단과 적당한 간격 두기
    
#     # 텍스트 그리기 (하얀색)
#     draw.text((text_x, text_y), text, font=font, fill="white")
            
#     # 변경된 이미지 저장
#     combined_image.save(f"{result_dir}/answer.png")
#     combined_image.show(f"{result_dir}/answer.png")
    
    
# make_result_images(image_nums = [3,1,2, 5,4, 6, 7], image_folder = "images/females/", result_dir= 'plot/females')


generate_ideal_type(recommendation_list = [1,2, 5,6, 8, 10, 13, 14], sex='female', pkl_path = './StyleGAN/metrics', latent_path = './StyleGAN/latent', result_dir='.', active_or_passive = 'passive')


##기준 latent1.png

## 각각이 의미하는 바 확인
# weight_sum_each => 16x512중 하나의 열에 5, 나머지 열에 1의 가중치로 각각의 열의 의미 확인
# weight_dict = {
#     1: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],
#     }


# for j in range(16):
#     latents[0][:,j] = latents[0][:,j] * weight_dict[1][j]


# syn_img = g_synthesis(latents[0])
# syn_img = (syn_img+1.0)/2.0
# save_image(syn_img.clamp(0,1),f"weight_sum_each_15.png")

## 묶음이 의미하는 바 확인
# weight_sum => 0:3, 3:6, 6:9, 9:12, 12: 각각 가중치 2,1,1,1,1로 번갈아가면서 실험


# weight_dict = {
#     1: [0.5, 0.4, 0.4, 0.4, 0.4],
#     2: [0.2, 0.2, 0.2, 0.2, 0.2],
#     3: [0.15, 0.15, 0.15, 0.15, 0.15],
#     4: [0.1, 0.12, 0.1, 0.1, 0.1],
#     5: [0.05, 0.08, 0.08, 0.05, 0.05],
#     6: [0.04, 0.06, 0.06, 0.04, 0.04],
#     7: [0.03, 0.05, 0.05, 0.03, 0.03],
#     8: [0.02, 0.04, 0.04, 0.02, 0.02],
#     }


# for i in range(len(recommendation_list)):
#     for j in range(5):
#         if j == 0:
#             latents[i][:, 0:3] = latents[i][:, 0:3] * weight_dict[i+1][j]
#         elif j == 1:
#             latents[i][:, 3:6] = latents[i][:, 3:6] * weight_dict[i+1][j]
#         elif j == 2:
#             latents[i][:, 6:9] = latents[i][:, 6:9] * weight_dict[i+1][j]
#         elif j == 3:
#             latents[i][:, 9:12] = latents[i][:, 9:12] * weight_dict[i+1][j]
#         elif j == 4:
#             latents[i][:, 12:] = latents[i][:, 12:] * weight_dict[i+1][j]

# # 리스트에 있는 텐서들을 더하기
# sum_tensor = torch.sum(torch.stack(latents), dim=0)
# print(sum_tensor.shape)

# syn_img = g_synthesis(sum_tensor)
# syn_img = (syn_img+1.0)/2.0
# save_image(syn_img.clamp(0,1),f"weight_sum_0.png")



