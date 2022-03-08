from pathlib import Path
from typing import Union
import numpy as np

AudioFile = Union[Path, np.ndarray]

class Dataset:
    pass


class VTCModel:

    def predict(self, audio_file: AudioFile, sampling_rate: int = 16000):
        pass

    def finetune(self):
        pass

    def retrain(self):
        pass


class BaseFeatureExtractor:
    pass


class PhoneRecognition(BaseFeatureExtractor):
    pass


class SyllableCounter(BaseFeatureExtractor):
    pass


class SignalFeatures(BaseFeatureExtractor):
    pass


class LinearModel:
    pass
