from dataclasses import field, dataclass
from pathlib import Path
from typing import Union, Dict

import numpy as np
from pyannote.core import Segment, Annotation
from pyannote.database import Protocol, get_protocol
from sklearn.linear_model import LinearRegression

AudioFile = Union[Path, np.ndarray]
Features = np.ndarray
PyannoteProtocol = Union[str, Protocol]


class BaseDataset:
    pass


class AclewDataset(BaseDataset):
    pass


class PyannoteDataset(BaseDataset):

    def __init__(self, protocol: PyannoteProtocol):
        if isinstance(protocol, str):
            protocol = get_protocol(protocol)
        self.protocol = protocol


@dataclass
class AudioSegment:
    audio: np.ndarray
    sampling_rate: float


@dataclass
class AudioFileSegment:
    audio_file: Path
    segment: Segment
    features: Dict[str, np.ndarray] = field(default_factory=dict)

    def audio_segment(self, sampling_rate: float = 1600):
        pass


class VTCModel:

    def predict(self, audio_file: AudioFile, sampling_rate: int = 16000) -> Annotation:
        pass

    def finetune(self, dataset: BaseDataset):
        pass

    def retrain(self, dataset: BaseDataset):
        pass


class BaseFeatureExtractor:

    def feature(self, audio_segment: AudioFileSegment) -> Features:
        pass

    @property
    def size(self) -> int:
        raise NotImplementedError()


class PhoneRecognition(BaseFeatureExtractor):

    def retrain(self, dataset: BaseDataset):
        raise NotImplementedError()


class SyllableCounter(BaseFeatureExtractor):

    def retrain(self, dataset: BaseDataset):
        raise NotImplementedError()


class SignalFeatures(BaseFeatureExtractor):
    pass


class LinguisticEstimatorPipeline:
    def __init__(self):
        self.feature_extractors: Dict[str, BaseFeatureExtractor] = {
            "syllables": SyllableCounter(),
            "phones": PhoneRecognition(),
            "signal": SignalFeatures()
        }
        self.linear_estimator = LinearRegression()

    def estimate(self, audio_segment: AudioFileSegment):
        pass

    def retrain_features(self, dataset: BaseDataset, only_features : ):
        pass
