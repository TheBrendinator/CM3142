from typing import TypedDict


class ClimateData(TypedDict):
    time_recorded: str
    humidity: float
    temperature: float


class LightingData(TypedDict):
    time_recorded: str


class ServiceData(TypedDict):
    time_recorded: str


class SleepData(TypedDict):
    time_recorded: str


class DisplayData(TypedDict):
    climate: ClimateData
    lighting: LightingData
    service: ServiceData
    sleep: SleepData
