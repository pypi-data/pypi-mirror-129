"""
Module to handle pipeline for timeseries
"""
import json
from abc import ABC
from datetime import datetime
from io import BytesIO
from typing import List, Tuple

import pandas as pd
import apache_beam.transforms.core as beam_core
from azure.core.exceptions import ResourceNotFoundError

from ..core.enums import TimeResolution
from .azure_data_storage import Dataset
from ..core.io import get_file_path_with_respect_to_time_resolution


class ConvertEventToTuple(beam_core.DoFn, ABC):
    """
    Takes a list of events and converts them to a list of tuples (datetime, event)
    """
    def __init__(self, date_key_name: str, date_format: str, time_resolution: TimeResolution):
        super().__init__()

        self.date_key_name = date_key_name
        self.date_format = date_format
        self.time_resolution = time_resolution

    def process(self, element, *args, **kwargs) -> List:
        """
        Overwrites beam.DoFn process.
        """
        res = []
        for event in element:
            datetime_obj = pd.to_datetime(event[self.date_key_name], format=self.date_format)
            res.append((self.__convert_datetime_to_time_resolution(datetime_obj), event))

        return res

    def __convert_datetime_to_time_resolution(self, datetime_obj: datetime):
        if self.time_resolution == TimeResolution.NONE:
            return '1970-01-01T00:00:00'
        if self.time_resolution == TimeResolution.YEAR:
            return f'{datetime_obj.year}-01-01T00:00:00'
        if self.time_resolution == TimeResolution.MONTH:
            return f'{datetime_obj.year}-{datetime_obj.month:02d}-01T00:00:00'
        if self.time_resolution == TimeResolution.DAY:
            return f'{datetime_obj.year}-{datetime_obj.month:02d}-{datetime_obj.day:02d}T00:00:00'
        if self.time_resolution == TimeResolution.HOUR:
            return f'{datetime_obj.year}-{datetime_obj.month:02d}-{datetime_obj.day:02d}T{datetime_obj.hour:02d}:00:00'
        if self.time_resolution == TimeResolution.MINUTE:
            return f'{datetime_obj.year}-{datetime_obj.month:02d}-{datetime_obj.day:02d}T{datetime_obj.hour:02d}:' + \
                   f'{datetime_obj.minute:02d}:00'
        message = 'Unknown enum type'
        raise ValueError(message)


class JoinUniqueEventData(beam_core.DoFn, ABC):
    """"
    Takes a list of events and join it with processed events, if such exists, for the particular event time.
    It will only keep unique pairs.
    """
    def __init__(self, datasets: Dataset, time_resolution: TimeResolution, index_columns: list = None):
        super().__init__()

        self.datasets = datasets
        self.time_resolution = time_resolution
        self.index_columns = index_columns

    def process(self, element, *args, **kwargs) -> List[Tuple]:
        """
        Overwrites beam.DoFn process.
        """
        date = pd.to_datetime(element[0])
        events_df = pd.DataFrame.from_dict(element[1])

        try:
            file_path = get_file_path_with_respect_to_time_resolution(date, self.time_resolution, 'data.parquet')
            file_content = self.datasets.read_file(file_path)
            processed_events_df = pd.read_parquet(BytesIO(file_content), engine='pyarrow')

            processed_events = pd.concat([events_df, processed_events_df], axis=0)
            processed_events.drop_duplicates(inplace=True, ignore_index=True, subset=self.index_columns, keep='first')

            processed_events = processed_events.to_dict(orient='records')

            return [(date, processed_events)]
        except ResourceNotFoundError:
            events_df.drop_duplicates(inplace=True, ignore_index=True)
            events = json.loads(events_df.to_json(orient='records'))

            return [(date, events)]


class UploadEventsToDestination(beam_core.DoFn, ABC):
    """
    Uploads events to destination
    """

    def __init__(self, dataset: Dataset, time_resolution: TimeResolution):
        super().__init__()
        self.dataset = dataset
        self.time_resolution = time_resolution

    def process(self, element, *args, **kwargs):
        """
        Overwrites beam.DoFn process.
        """
        date = element[0]
        events = element[1]

        data = pd.DataFrame(events).to_parquet(engine='pyarrow', compression='snappy')
        sub_file_path = get_file_path_with_respect_to_time_resolution(date, self.time_resolution, 'data.parquet')
        file_path = f'{sub_file_path}'
        self.dataset.upload_file(file_path, BytesIO(data))


class ConvertToDict(beam_core.DoFn, ABC):
    """
    Takes a list of events and converts them to a list of tuples (datetime, event)
    """

    def process(self, element, *args, **kwargs) -> List:
        """
        Overwrites beam.DoFn process.
        """
        dataframe = pd.read_parquet(BytesIO(element), engine='pyarrow')
        # It would be better to use records.to_dict, but pandas uses narray type which JSONResponse can't handle.
        return [json.loads(dataframe.to_json(orient='records'))]
