import os
import copy
from typing import List

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from .preprocess import PreprocessEEG


class AnalyzeEEG:
    def __init__(self, channels: List, fs: int):
        self.preprocess_eeg = PreprocessEEG(channels, fs)

    def analyze_erp(
        self,
        eeg_filename: str,
        event_filename: str,
        result_dir: str,
        num_types: int,
        lowcut: float = 1.0,
        highcut: float = 30.0,
        tmin: float = -0.2,
        tmax: float = 1.0,
    ):
        # Check result directory
        if not os.path.isdir(result_dir):
            os.makedirs(result_dir)

        # Read eeg and events
        eeg, eeg_times = self.preprocess_eeg.read_eeg(eeg_filename)
        eeg = self.preprocess_eeg.normalize(eeg)  # Normalize
        events = self.preprocess_eeg.read_events(event_filename)

        # Synchronize time interval
        eeg_start_tm = eeg_filename.split("_")[-1].replace(".csv", "")
        event_start_tm = event_filename.split("_")[-1].replace(".csv", "")
        events = self.preprocess_eeg.synchronize_time_interval(
            events, eeg_start_tm, event_start_tm
        )

        # Apply filter (1-30 Hz)
        self.preprocess_eeg.filter(eeg, lowcut=lowcut, highcut=highcut)

        avg_evoked_list = []
        times_list = []
        for i in range(1, num_types + 1):
            avg_evoked, times = self.preprocess_eeg.epochs(
                eeg, events=events, event_id=i, tmin=tmin, tmax=tmax
            )
            avg_evoked_list.append(avg_evoked)
            times_list.append(times)
        return eeg, eeg_times, avg_evoked_list, times_list

    def analyze_erp_range(
        self,
        eeg_filename: str,
        event_filename: str,
        result_dir: str,
        num_types: int,
        cut: float = 13.0,
        freq_range: float = 2.0,
        tmin: float = 0.0,
        tmax: float = 1.0,
    ):
        # Check result directory
        if not os.path.isdir(result_dir):
            os.makedirs(result_dir)

        # Read eeg and events
        eeg, eeg_times = self.preprocess_eeg.read_eeg(eeg_filename)
        eeg = self.preprocess_eeg.normalize(eeg)  # Normalize
        events = self.preprocess_eeg.read_events(event_filename)

        # Synchronize time interval
        eeg_start_tm = eeg_filename.split("_")[-1].replace(".csv", "")
        event_start_tm = event_filename.split("_")[-1].replace(".csv", "")
        events = self.preprocess_eeg.synchronize_time_interval(
            events, eeg_start_tm, event_start_tm
        )

        self.preprocess_eeg.filter(eeg, lowcut=cut-freq_range, highcut=cut+freq_range)

        avg_evoked_list = []
        times_list = []
        for i in range(1, num_types + 1):
            avg_evoked, times = self.preprocess_eeg.epochs(
                eeg, events=events, event_id=i, tmin=tmin, tmax=tmax
            )
            avg_evoked_list.append(avg_evoked)
            times_list.append(times)
        return eeg, eeg_times, avg_evoked_list, times_list

    