import os
from typing import List
from datetime import datetime

import pandas as pd

from src.task import ideal_type_task
from src.analysis import AnalyzeEEG
from src.plot import PlotEEG
from src.recommendation import recommend_ideal_type_both, make_result_images
from StyleGAN.generate_ideal_type import generate_ideal_type

def erp_ideal_type(
    screen_width: int,
    screen_height: int,
    fs: int,
    channels: List,
    isi: int,
    background_path: str,
    sex: str,
    image_folder: str,
    num_trials: int,
    num_images: int,
    event_save_path: str,
    result_dir: str,
    result_dir2: str,
    recommendation_num: int,
    lowcut: float = 1.0,
    highcut: float = 30.0,
    tmin: float = -0.2,
    tmax: float = 1.0,
):
    today = str(datetime.now().date())
    #today = '2023-12-18'
    if not os.path.exists(f"./data/{today}"):
        os.makedirs(f"./data/{today}")
    if not os.path.exists(f"./event/{today}"):
        os.makedirs(f"./event/{today}")

    
    ## task 수행
    ideal_type_task(
        screen_width=screen_width,
        screen_height=screen_height,
        isi=isi,
        background_path=background_path,
        image_folder=image_folder,
        num_trials=num_trials,
        num_images=num_images,
        event_save_path=f"{event_save_path}/{today}",
        sex=sex
    )

    ## 데이터 가져오기
    rawdata_folders = os.listdir("C:/MAVE_RawData")

    text_file_name = f"C:/MAVE_RawData/{rawdata_folders[-1]}/Rawdata.txt"
    data_df = pd.read_csv(text_file_name, delimiter="\t")

    record_start_time = data_df.iloc[0, 0]
    hour = str(record_start_time).split(":")[0]
    min = str(record_start_time).split(":")[1]
    sec = str(record_start_time).split(":")[2].split(".")[0]

    data_df = data_df[channels]
    data_file_path = f"./data/{today}/Rawdata_{hour}.{min}.{sec}.csv"
    data_df.to_csv(data_file_path, index=False)

    event_paths = os.listdir(f"./event/{today}")
    event_file = f"./event/{today}/{event_paths[-1]}"

    ## EEG 분석
    analyze_eeg = AnalyzeEEG(channels=channels, fs=fs)
    eeg, eeg_times, avg_evoked_list, times_list = analyze_eeg.analyze_erp(
        eeg_filename=data_file_path,
        event_filename=event_file,
        result_dir=result_dir,
        num_types=num_images,
        lowcut=lowcut,
        highcut=highcut,
        tmin=tmin,
        tmax=tmax,
    )

    ## EEG 그래프 그리기
    plot_eeg = PlotEEG(
        channels=channels,
        result_dir=result_dir,
        is_show=False,
        is_save=True,
        eeg=eeg,
        eeg_times=eeg_times,
        eeg_filename="eeg_raw",
    )
    plot_eeg.plot_eeg()
    if sex == "males":
        for i in range(num_images):
            plot_eeg.plot_electrode(
                avg_evoked_list[i],
                times_list[i],
                filename=f"males_{i+1}_electrode",
            )
    elif sex == "females":
        for i in range(num_images):
            plot_eeg.plot_electrode(
                avg_evoked_list[i],
                times_list[i],
                filename=f"females_{i+1}_electrode",
            )
    else:
        raise ValueError("Invalid clothes type")

    ## 이상형 리스트 추천
    active_list, passive_list = recommend_ideal_type_both(
        avg_evoked_list=avg_evoked_list,
        times_list=times_list,
        channels=channels,
        sex=sex,
        recommendation_num = recommendation_num,
        num_trials=num_trials,
        event_filename = event_file,
    )
    
    ## 이상형 결과 보여주기
    make_result_images(recommendation_list = active_list, sex=sex, image_folder = image_folder, result_dir=result_dir2, passive_or_active='active')
    make_result_images(recommendation_list = passive_list, sex=sex, image_folder = image_folder, result_dir=result_dir2, passive_or_active='passive')
    
    ## 이상형 생성 결과 보여주기
    generate_ideal_type(recommendation_list = active_list, sex=sex, pkl_path = './StyleGAN/metrics', latent_path = './StyleGAN/latent', result_dir=result_dir2, active_or_passive = 'active')
    generate_ideal_type(recommendation_list = passive_list, sex=sex, pkl_path = './StyleGAN/metrics', latent_path = './StyleGAN/latent', result_dir=result_dir2, active_or_passive = 'passive')


if __name__ == "__main__":
    import argparse
    import ast

    def parse_list(string: str):
        try:
            parsed_list = ast.literal_eval(string)
            if isinstance(parsed_list, list):
                return parsed_list
            else:
                raise argparse.ArgumentTypeError("Invalid list format")
        except (ValueError, SyntaxError):
            raise argparse.ArgumentTypeError("Invalid list format")

    parser = argparse.ArgumentParser(
        description="Insert arguments for function of erp combination"
    )
    parser.add_argument(
        "--screen_width",
        type=int,
        default=1920,
        help="Set screen width of combination task",
    )
    parser.add_argument(
        "--screen_height",
        type=int,
        default=1080,
        help="Set screen height of combination task",
    )
    parser.add_argument(
        "--fs", type=int, default=256, help="Get resolution of EEG device"
    )
    parser.add_argument(
        "--channels",
        type=parse_list,
        default="['EEG_Fp1', 'EEG_Fp2']",
        help="Get channels of EEG device",
    )
    parser.add_argument(
        "--isi",
        type=int,
        default=1000,
        help="Set inter-stimulus interval of combination task",
    )
    parser.add_argument(
        "--image_path",
        type=str,
        default="./images",
        help="Get image data path to use in the task",
    )
    parser.add_argument(
        "--sex",
        type=str,
        default="females",
        help="Set type of clothes to use in the task",
    )
    parser.add_argument(
        "--num_trials",
        type=int,
        default=10,
        help="Set number of trials to use in the task",
    )
    parser.add_argument(
        "--num_images",
        type=int,
        default=30,
        help="Set number of clothes to use in the task",
    )
    parser.add_argument(
        "--event_save_path",
        type=str,
        default="./event",
        help="Set a record of events file saving path",
    )
    parser.add_argument(
        "--result_dir",
        type=str,
        default="./plot",
        help="Set a EEG, ERP plots saving path",
    )
    parser.add_argument(
        "--result_dir2",
        type=str,
        default="./result",
        help="Set a EEG, ERP plots saving path",
    )
    parser.add_argument(
        "--result_dir_num",
        type=int,
        default=0,
        help="Set a EEG, ERP plots detailed saving path",
    )
    parser.add_argument(
        "--lowcut",
        type=float,
        default=1.0,
        help="Set butter filter lowcut to get ERP",
    )
    parser.add_argument(
        "--highcut",
        type=float,
        default=30.0,
        help="Set butter filter highcut to get ERP",
    )
    parser.add_argument(
        "--tmin",
        type=float,
        default=-0.2,
        help="Set epoch tmin to get ERP",
    )
    parser.add_argument(
        "--tmax",
        type=float,
        default=1.0,
        help="Set epoch tmax to get ERP",
    )
    parser.add_argument(
        "--recommendation_num",
        type=int,
        default=3,
        help="Set recommendation numbers",
    )
    args = parser.parse_args()

    erp_ideal_type(
        screen_width=args.screen_width,
        screen_height=args.screen_height,
        fs=args.fs,
        channels=args.channels,
        isi=args.isi,
        background_path=f"{args.image_path}/backgrounds/B0.jpg",
        image_folder=f"{args.image_path}/{args.sex}",
        sex=f"{args.sex}",
        num_trials=args.num_trials,
        num_images=args.num_images,
        event_save_path=f"{args.event_save_path}",
        result_dir=f"{args.result_dir}/{args.sex}/{args.result_dir_num}",
        result_dir2=f"{args.result_dir2}/{args.sex}/{args.result_dir_num}",
        lowcut=args.lowcut,
        highcut=args.highcut,
        tmin=args.tmin,
        tmax=args.tmax,
        recommendation_num = args.recommendation_num,
    )
