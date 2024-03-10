from __future__ import annotations

import abc
import pathlib

import pandas as pd


class Geocoder(abc.ABC):

    def __init__(self, samples: int | None = None):
        self.__df = pd.read_csv(pathlib.Path().parent / "data" / "sample_data.csv")
        self._samples = samples

    @abc.abstractmethod
    def _apply_geocoding(self, area_id: str) -> str:
        pass

    def geocode(self) -> pd.DataFrame:
        df_to_geocode = self.__df.copy()
        if self._samples is not None:
            df_to_geocode = df_to_geocode.sample(self._samples)
        df_to_geocode["paths"] = df_to_geocode["area_id"].apply(self._apply_geocoding)

        return df_to_geocode
