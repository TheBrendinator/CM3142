from typing import TypedDict


class ClimateData(TypedDict):
    time_recorded: str
    humidity: float
    temperature: float
