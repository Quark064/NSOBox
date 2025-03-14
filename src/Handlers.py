from json import loads
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from ADB import ADBCommand
from Hijacker import Hijacker
from DataPacks import FTask
from ADB import ADBCommand, ADBUtil
from Strings import SharedPreferences, TokenData, NSOApp

class HandlerCommon:
    def SendResponse(self, statusCode: int, headers: dict[str, str] | None = None, body: str | None = None) -> None:
        self.send_response(statusCode)

        contentType = "application/json"
        try:
            loads(body)
        except Exception:
            contentType = "application/text"
        
        if body != None:
            self.send_header("Content-Type", contentType)
        
        if headers != None:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()

        try:
            if body != None:
                self.wfile.write(body.encode())
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            print("[!] Client disconnected before response was sent.")
        except Exception as e:
            print(f"[!] Unexpected error in SendResponse: {e}")


class FRequestHandler(BaseHTTPRequestHandler, HandlerCommon):
    def __init__(self, *args, hijacker: Hijacker, **kwargs):
        self.GENERATION_TIMEOUT_SECS = 20

        self.hijacker = hijacker

        self.prepareEnvCmd = ADBCommand()
        self.prepareEnvCmd.AddCommand("setenforce 0")
        self.prepareEnvCmd.AddCommand("am force-stop com.nintendo.znca")
        self.prepareEnvCmd.UseSU()
        
        self.startActivityCmd = ADBCommand()
        self.startActivityCmd.AddCommand(f"am start -n com.nintendo.znca/{NSOApp.MainActivity()}")

        self.startWebViewActivity = ADBCommand()
        self.startWebViewActivity.AddCommand(f'am start -a android.intent.action.VIEW -d "{NSOApp.AppletLaunchURL()}"')

        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        path = self.path.split('?')[0]
        match(path.lower()):
            case "/f1":
                self.GenF(FTask.HashMethod.F1)
            case "/f2":
                self.GenF(FTask.HashMethod.F2)
            case _:
                self.SendResponse(
                    statusCode = 404,
                    body = "Not a valid endpoint."
                )

    def GenF(self, method: FTask.HashMethod):
        tokenName = "id_token" if method == FTask.HashMethod.F1 else "web_api_token"

        # Get the Token from the URL parameters
        try:
            parsedURL = urlparse(self.path)
            token = str(parse_qs(parsedURL.query)[tokenName][0])
        except Exception:
            self.SendResponse(
                statusCode = 400,
                body = f"No '{tokenName}' URL parameter was given."
            )
            return

        # Get the Current ID from the Token
        try:
            tokenTask = FTask(token, method)
        except Exception:
            self.SendResponse(
                statusCode = 400,
                body = f"Failed to decode the given '{tokenName}'."
            )
            return

        # Generate the F Token using the Android Device
        try:
            # Attempt to set as the current MITM Task
            res = self.hijacker.AttemptSet(tokenTask)
            while not res.Successful:
                res.CurrTask.Completed.wait()
                res = self.hijacker.AttemptSet(tokenTask)

            # Prepare the environment for modification
            self.prepareEnvCmd.Run()
            
            # Groom NSO's application storage
            if method == FTask.HashMethod.F1:
                ADBUtil.OverwriteFile(SharedPreferences.Path(), SharedPreferences.V1Layout(), useSU=True)
                ADBUtil.OverwriteFile(TokenData.Path(), TokenData.V1Layout(), useSU=True)
                self.startActivityCmd.Run()
            else:
                ADBUtil.OverwriteFile(SharedPreferences.Path(), SharedPreferences.V2Layout(tokenTask.Token, tokenTask.ID), useSU=True)
                ADBUtil.OverwriteFile(TokenData.Path(), TokenData.V1Layout(), useSU=True)
                self.startWebViewActivity.Run()
            
            tokenTask.Completed.wait(self.GENERATION_TIMEOUT_SECS)

            # Check if the Task completed or if it failed to get a response in time
            if tokenTask.Completed.isSet():
                self.SendResponse(
                    statusCode = 200,
                    headers = {
                        f"User-V{str(method.value)}-ID": tokenTask.ID
                    },
                    body = tokenTask.F.ToJSON()
                )
            else:
                self.SendResponse(
                    statusCode = 500,
                    body = f"The generation request timed out: did not receive token from device within the time limit ({int(self.GENERATION_TIMEOUT_SECS)} seconds)."
                )
                self.hijacker.ClearTask()

        except Exception as ex:
            self.SendResponse(
                statusCode = 500,
                body = f"An internal server exception occurred generating F{str(method.value)} Token.\n\n{str(ex)}"
            )
