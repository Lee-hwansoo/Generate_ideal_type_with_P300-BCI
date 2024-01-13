import os
from typing import List
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from sklearn.metrics import accuracy_score

def recommend_ideal_type_both(
    event_filename: str, avg_evoked_list: List, times_list: List, channels: List, sex: str, recommendation_num: int, num_trials: int,
):

    max_values_per_channels = []
    for channel_idx in range(len(channels)):
        max_values = []
        for time in range(len(times_list)):
            selected_indices = [
                index
                for index, value in enumerate(times_list[time])
                if 0.1 <= value <= 0.45 #0.1~0.45사이에서 p300 검출
            ]
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            max_value = max(avg_evoked_list[time][channel_idx][start_index : end_index + 1])
            max_values.append(max_value)
        max_values_per_channels.append(max_values)

    indices_of_largest_values_per_channels = []
        
    for channel in range(len(max_values_per_channels)):
        indices_of_largest_values = sorted(
            range(len(max_values_per_channels[channel])),
            key=lambda i: max_values_per_channels[channel][i],
            reverse=True,
        )

        largest_values = [max_values_per_channels[channel][i] for i in indices_of_largest_values]
        top_values_and_indices = [
            (value, index)
            for value, index in zip(largest_values, indices_of_largest_values)
        ]
        indices_of_largest_values_per_channels.append(top_values_and_indices)

    top_values_and_indices = sum(indices_of_largest_values_per_channels, [])
    sorted_top_values_and_indices = sorted(
        top_values_and_indices, key=lambda i: i[0], reverse=True
    )

    ## 추천 리스트 생성을 위한 데이터프레임 생성
    recommend_df = pd.read_csv(event_filename)
    recommend_df['Response'] = recommend_df['Response'].apply(lambda x: 1 if x == 'HIT' else 0) #hit를 1로 변환    
    
    ## result에 max컬럼 추가(erp max값)
    result = recommend_df.groupby('Stimulus')['Response'].sum().reset_index() #stimulus로 그룹핑
    result['max'] = [0 for _ in range(len(result))] #0으로 초기화
    # max값 넣기
    for i in sorted_top_values_and_indices:
        mask = result.loc[result['Stimulus'] == (i[1]+1)].index #해당 자극의 인덱스 찾기(+1 해줘야됨)
        max_value = result.loc[mask, 'max'].values[0] #해당 자극의 max값 가져오기
        
        if max_value < i[0]: #현재 max값이 들어있는거보다 크면 max값 업데이트
            result.loc[mask, 'max'] = i[0] 

    ## Active
    #정렬
    sorted_result_a = result.sort_values(by=['Response', 'max'], ascending=False) #Hit 기준 정렬 후 max 값으로 추가 정렬
    active_list = sorted_result_a.iloc[:recommendation_num]['Stimulus'].to_list() #상위 몇개 뽑기
    
    ## Passive
    #정렬
    sorted_result_p = result.sort_values(by='max', ascending=False) #max 값으로 정렬
    passive_list = sorted_result_p.iloc[:recommendation_num]['Stimulus'].to_list() #상위 몇개 뽑기

    print(f'[액티브] 당신이 끌리는 연예인은 순서대로 {active_list} 입니다.')
    print(f'[패시브] 당신이 끌리는 연예인은 순서대로 {passive_list} 입니다.')
    
    ## 정확도 구하기
    # 순서를 고려하지 않은 정확도(passive, active에 존재유무)
    accuracy = 0
    for i in active_list:
        for j in passive_list:
            if i == j:
                accuracy +=1
    accuracy = accuracy/len(active_list)
    # 순서를 고려한 정확도    
    include_order_accuracy = accuracy_score(active_list, passive_list)
    
    print("Active와 Passive의 정확도:", accuracy)
    print("순서 포함 정확도: ", include_order_accuracy)
    
    return active_list, passive_list



def make_result_images(
    recommendation_list: List, sex: str, image_folder: str, result_dir: str, passive_or_active: str,
):
    ## 결과 보여줄 이미지들 로드
    images = [Image.open(f"{image_folder}/F{i}.jpg").resize((512,512)) for i in recommendation_list]

    ## combine 이미지를 위한 width, height 계산
    combined_width = 512*((len(recommendation_list)+1)//2)
    combined_height = 512*2 +100 

    ## 새로운 이미지 생성
    combined_image = Image.new("RGB", (combined_width, combined_height), color="white")

    ## 이미지 붙여넣기
    for i in range(len(recommendation_list)):
        if i < (len(recommendation_list)+1)//2:
            combined_image.paste(images[i], (512*i, 0))
        else:        
            combined_image.paste(images[i], (512*(i-(len(recommendation_list)+1)//2), 512))

    ## 글씨 쓰기
    draw = ImageDraw.Draw(combined_image)
    text = f'[{passive_or_active}] 당신의 선택은 {recommendation_list} 입니다.'
    font_size = 70 
    font = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", font_size)
    # 텍스트 너비와 높이를 구하고 이미지 중앙 하단에 위치시키기
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (combined_image.width - text_width) // 2
    bottom_margin = 10  # 하단 여백 크기
    text_y = combined_image.height - text_height - bottom_margin
    
    # 텍스트 그리기 (검은색)
    draw.text((text_x, text_y), text, font=font, fill="black")
            
    ## 변경된 이미지 저장 및 보여주기
    if not os.path.exists(result_dir):#디렉토리 없으면 생성
        os.makedirs(result_dir)
    
    combined_image.save(f"{result_dir}/selected_{passive_or_active}.png")
    combined_image.show(f"{result_dir}/selected_{passive_or_active}.png")