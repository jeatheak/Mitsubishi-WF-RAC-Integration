"""Aircon Base"""

from aenum import StrEnum


class AirconCommands(StrEnum):
    """Enum of all the supported airco commands"""

    Operation = "Operation"
    OperationMode = "OperationMode"
    AirFlow = "AirFlow"
    WindDirectionUD = "WindDirectionUD"
    WindDirectionLR = "WindDirectionLR"
    PresetTemp = "PresetTemp"
    Entrust = "Entrust"
    # CoolHotJudge = ''

    # Vacant = ''
    # ModelNr = ''
    # IsSelfCleanOperation = ''
    # IsSelfCleanReset = ''


class AirconBase:
    """Base class of the aircon class"""

    Operation: bool
    OperationMode: int
    AirFlow: int
    WindDirectionUD: int
    WindDirectionLR: int
    PresetTemp: float
    Entrust: bool
    ModelNr: int
    Vacant: bool
    CoolHotJudge: bool


class Aircon(AirconBase):
    """Aircon (recieve) class extends AirconBase class"""

    IndoorTemp: float
    OutdoorTemp: float
    Electric: float | None
    ErrorCode: str


class AirconStat(AirconBase):
    """Aircon (command) class extends AirconBase class"""

    def __init__(self, aircon: Aircon) -> None:
        self.Operation = aircon.Operation
        self.OperationMode = aircon.OperationMode
        self.AirFlow = aircon.AirFlow
        self.WindDirectionUD = aircon.WindDirectionUD
        self.WindDirectionLR = aircon.WindDirectionLR
        self.PresetTemp = aircon.PresetTemp
        self.Entrust = aircon.Entrust
        self.ModelNr = aircon.ModelNr
        self.Vacant = aircon.Vacant
        self.CoolHotJudge = aircon.CoolHotJudge
        self.IsSelfCleanOperation = False
        self.IsSelfCleanReset = False

    IsSelfCleanOperation: bool
    IsSelfCleanReset: bool
