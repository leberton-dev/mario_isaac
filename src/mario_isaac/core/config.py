import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScreenConfig:
    width: int
    height: int
    title: str

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

class Config:
    def __init__(self) -> None:
        self._parser: configparser.ConfigParser = configparser.ConfigParser()
        config_path = Path(__file__).resolve().parent.parent / "config.ini"
        _ = self._parser.read(config_path)
        self.screen: ScreenConfig
        self.virtual_screen: ScreenConfig

    def load(self) -> None:
        self.screen = ScreenConfig(int(self._parser["screen"]["width"]),
                                   int(self._parser["screen"]["height"]),
                                   self._parser["screen"]["title"])
        self.virtual_screen = ScreenConfig(int(self._parser["virtual_screen"]["width"]),
                                           int(self._parser["virtual_screen"]["height"]),
                                           "")
    
