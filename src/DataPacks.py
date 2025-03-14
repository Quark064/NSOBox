from dataclasses import dataclass
from json import loads, dumps
from threading import Event
from enum import Enum

from Strings import Utils

@dataclass
class FPack:
    Timestamp: int
    RequestID: str
    F: str

    def ToJSON(self) -> str:
        res = {
            "timestamp": self.Timestamp,
            "requestId": self.RequestID,
            "f": self.F
        }

        return dumps(res)

class FTask:
    class HashMethod(Enum):
        F1 = 1
        F2 = 2

    def __init__(self, token: str, method: HashMethod) -> None:
        self.Completed: Event = Event()
        self.Token: str     = token
        self.Method           = method
        self.F: None | FPack  = None

        payload = self.Token.split('.')[1]
        self.ID: str = loads(Utils.DecodeB64String(payload))["sub"]

    
    def Complete(self, data: FPack) -> None:
        self.F = data
        self.Completed.set()

@dataclass
class FTaskSetResult:
    Successful: bool
    CurrTask: FTask | None