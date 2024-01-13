import datetime
import time
import csv
from typing import List

import pygame
import cv2
import random

def ideal_type_task(
    screen_width: int,
    screen_height: int,
    isi: int,
    background_path: str,
    image_folder: str,
    num_trials: int,
    num_images: int,
    event_save_path: str,
    sex: str,
):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    flag = True # 이벤트 정보를 한 번만 저장하기 위한 플래그
    
    ## 시행 횟수에 대한 외부 루프
    for _ in range(num_trials):
        # 각 시행에서 이미지 수에 대한 내부 루프
        random_order = random.sample(range(num_images), num_images)
        for num_image in random_order:
            running = True # 내부 루프 제어를 위한 플래그
            current_screen = "background" # 초기 화면 상태
            response = "CR" # 기본 응답

            start_time_rt = 0
            end_time_rt = 0
            start_time_st = pygame.time.get_ticks() # 자극 제시 시작 시간 기록

            while running:
                # 이벤트 처리 루프
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            response = "HIT"
                            end_time_rt = pygame.time.get_ticks() # 응답 시간 기록
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                # "background" 화면에 대한 코드
                if current_screen == "background":
                    back_image = pygame.image.load(background_path)
                    screen.blit(
                        back_image,
                        (
                            screen_width // 2 - back_image.get_width() // 2,
                            screen_height // 2 - back_image.get_height() // 2,
                        ),
                    )
                    pygame.display.flip()
                    clock.tick(60)

                    # 이벤트 정보를 한 번만 CSV 파일에 저장
                    if flag:
                        current_time = datetime.datetime.now()
                        hour = str(current_time).split(" ")[1].split(":")[0]
                        min = str(current_time).split(" ")[1].split(":")[1]
                        sec = str(current_time).split(" ")[1].split(":")[2]

                        filename = f"{event_save_path}/ideal_type_event_{hour}.{min}.{sec}.csv"
                        with open(filename, mode="w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(["ISI", "RT", "Response", "Stimulus"])
                        flag = False # 이벤트 정보를 다시 저장하지 않도록 플래그 설정

                    # 일정 시간(1000 밀리초)이 경과하면 "stimulus" 화면으로 전환
                    elapsed_time = pygame.time.get_ticks() - start_time_st
                    if(elapsed_time >= 1000):
                        current_screen = "stimulus"
                        start_time_st = pygame.time.get_ticks()
                        
                # "stimulus" 화면에 대한 코드
                elif current_screen == "stimulus":
                    start_time_rt = start_time_st

                    if sex == "males":
                        task_image = pygame.image.load(f"{image_folder}/M{num_image+1}.jpg")
                    elif sex == "females":
                        task_image = pygame.image.load(f"{image_folder}/F{num_image+1}.jpg")
                    else:
                        raise ValueError("Invalid sex type")
                    
                    # 자극 이미지를 표시
                    screen.blit(
                        task_image,
                        (
                            screen_width // 2 - task_image.get_width() // 2,
                            screen_height // 2 - task_image.get_height() // 2,
                        ),
                    )
                    pygame.display.flip()
                    clock.tick(60)
                    
                    # 일정 시간(1000 밀리초)이 경과하면 "background" 화면으로 전환
                    elapsed_time = pygame.time.get_ticks() - start_time_st
                    if(elapsed_time >= 1000):
                        if response == "HIT":
                            #rt = end_time_rt - start_time_rt
                            rt = 1000
                        else:
                            rt = 1000

                        # CSV 파일에 결과 기록
                        with open(filename, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(
                                [
                                    isi,
                                    rt,
                                    response,
                                    num_image + 1,
                                ]
                            )
                        
                        running = False # 내부 루프 종료
                        current_screen = "background" # "background" 화면으로 전환
                        start_time_st = pygame.time.get_ticks() # 자극 제시 시간 초기화

    time.sleep(10) # 종료하기 전 10초 대기
    pygame.quit()















