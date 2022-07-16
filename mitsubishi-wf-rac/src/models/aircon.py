from .airconBase import AirconBase

class Aircon(AirconBase):
    IndoorTemp: float
    OutdoorTemp: float
    Electric: float
    ErrorCode: str