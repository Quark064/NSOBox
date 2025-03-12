from mitmproxy import http
from json import loads
from threading import Lock

from DataPacks import FTask, FPack, FTaskSetResult
from Strings import ServerResponse

class Hijacker:
    def __init__(self) -> None:
        self.currentTask: None | FTask = None
        self.__lock = Lock()

    def SetTask(self, task: FTask | None) -> None:
        with self.__lock:
            self.currentTask = task

    def GetTask(self) -> None | FTask:
        with self.__lock:
            return self.currentTask
    
    def AttemptSet(self, task: FTask) -> FTaskSetResult:
        with self.__lock:
            if self.currentTask == None:
                self.currentTask = task
                return FTaskSetResult(True, None)
            
            return FTaskSetResult(False, self.currentTask)


    def request(self, flow: http.HTTPFlow) -> None:
        if self.GetTask() == None:
            flow.response = None
            flow.kill()
            return
        
        elif "accounts.nintendo.com/connect/1.0.0/api/token" in flow.request.pretty_url:
            res = ServerResponse.Body.APIToken(self.GetTask().IDToken)

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.APIToken(len(res))
            )
            return
        
        elif "api.accounts.nintendo.com/2.0.0/users/me" in flow.request.pretty_url:
            res = ServerResponse.Body.GetUser(self.GetTask().ID)

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.GetUser()
            )
            return
        
        elif "api-lp1.znc.srv.nintendo.net/v3/Account/Login" in flow.request.pretty_url:
            req = flow.request.data.content.decode("utf-8")
            req = loads(req)

            pack = FPack(
                req["parameter"]["timestamp"],
                req["parameter"]["requestId"],
                req["parameter"]["f"]
            )

            task = self.GetTask()
            self.SetTask(None)
            task.Complete(pack)

        flow.response = None
        flow.kill()
