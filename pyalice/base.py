from dataclasses import field, dataclass
from pathlib import Path
from typing import Union, Dict, List, Optional, Iterable, Text

import numpy as np
from pyannote.audio.core.io import AudioFile
from pyannote.core import Segment, Annotation
from pyannote.database import Protocol, get_protocol
from sklearn.linear_model import LinearRegression
from typing_extensions import Literal
from pyannote.audio.pipelines import MultilabelDetectionPipeline

Features = np.ndarray
PyannoteProtocol = Union[str, Protocol]


class BaseDataset:

    def iter_train(self):
        pass

    def iter_val(self):
        pass

    def __iter__(self) -> Iterable[Path]:
        pass


class AudioFilesDataset(BaseDataset):
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
    label: str
    features: Dict[str, np.ndarray] = field(default_factory=dict)

    def audio_segment(self, sampling_rate: float = 1600):
        pass


class VTCModel:

    def __init__(self, model: Union[Text, Path], hparams_file: Union[Text, Path] = None):
        self.mlt_pilepine = MultilabelDetectionPipeline.from_pretrained(model, hparams_file=hparams_file)

    def predict(self, audio_file: AudioFile) -> Annotation:
        return self.mlt_pilepine.apply(audio_file)

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
    pass


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
        for feat_name, feature_proc in self.feature_extractors.items():
            feat = feature_proc.feature(audio_segment)
            audio_segment.features[feat_name] = feat

    def retrain_features(self, dataset: BaseDataset,
                         only_features: Optional[List[Literal["syllables", "phones"]]]):
        pass
