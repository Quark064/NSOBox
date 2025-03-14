from mitmproxy import http
from json import loads
from threading import Lock

from DataPacks import FTask, FPack, FTaskSetResult
from Strings import ServerResponse, TokenData

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
    
    def ClearTask(self) -> None:
        self.SetTask(None)

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
        
        if self.GetTask().Method == FTask.HashMethod.F1:
            self.GenF1(flow)
        else:
            self.GenF2(flow)
        

    def GenF1(self, flow: http.HTTPFlow) -> None:
        if "accounts.nintendo.com/connect/1.0.0/api/token" in flow.request.pretty_url:
            res = ServerResponse.Body.APITokens(self.GetTask().Token, TokenData.DummyAccess())

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.APITokens(len(res))
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
            self.ClearTask()
            task.Complete(pack)

        flow.response = None
        flow.kill()
    

    def GenF2(self, flow: http.HTTPFlow) -> None:
        if "accounts.nintendo.com/connect/1.0.0/api/token" in flow.request.pretty_url:
            res = ServerResponse.Body.APITokens(TokenData.DummyID(), TokenData.DummyAccess())

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.APITokens(len(res))
            )
            return
        
        elif "api.accounts.nintendo.com/2.0.0/users/me" in flow.request.pretty_url:
            res = ServerResponse.Body.GetUser(TokenData.DummyV1ID())

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.GetUser()
            )
            return
        
        elif "api-lp1.znc.srv.nintendo.net/v1/Game/ListWebServices" in flow.request.pretty_url:
            res = ServerResponse.Body.ListWebServices()

            flow.response = http.Response.make(
                200,
                res.encode("utf-8"),
                ServerResponse.Header.ListWebServices()
            )
            return
        
        elif "api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken" in flow.request.pretty_url:
            req = flow.request.data.content.decode("utf-8")
            req = loads(req)

            pack = FPack(
                req["parameter"]["timestamp"],
                req["parameter"]["requestId"],
                req["parameter"]["f"]
            )

            task = self.GetTask()
            self.ClearTask()
            task.Complete(pack)

        flow.response = None
        flow.kill()
