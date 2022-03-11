import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("pyalice")
logger.setLevel(logging.INFO)

@dataclass
class WorkSpace:
    root_path: Path

    def initialize(self):
        pass

    @property
    def model_parameters(self):
        return self.root_path / "parameters/"


