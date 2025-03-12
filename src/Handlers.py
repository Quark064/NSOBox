import subprocess
import json

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from ADB import ADBCommand
from Hijacker import Hijacker
from DataPacks import FTask
from ADB import ADBCommand
from Strings import Utils, SharedPreferences, NSOApp

class FRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, hijacker: Hijacker, **kwargs):
        self.hijacker = hijacker

        startCmd = ADBCommand()
        startCmd.AddCommand("setenforce 0")
        startCmd.AddCommand("am force-stop com.nintendo.znca")
        startCmd.AddCommand(f'echo "{Utils.ToHexString(SharedPreferences.V1Layout())}" > {SharedPreferences.Path()}')
        startCmd.AddCommand(f"am start -n com.nintendo.znca/{NSOApp.MainActivity()}")
        startCmd.UseSU()
        
        self.startCmd = startCmd.Build()

        endCmd = ADBCommand()
        endCmd.AddCommand("am force-stop com.nintendo.znca")
        
        self.endCmd = endCmd.Build()

        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        # Get the ID Token from the URL parameters
        try:
            parsedURL = urlparse(self.path)
            idToken = str(parse_qs(parsedURL.query)['id_token'][0])
        except Exception:
            self.SendResponse(
                statusCode = 400,
                body = "No 'id_token' URL parameter was given."
            )
            return

        # Get the User ID from the ID Token
        try:
            tokenTask = FTask(idToken)
        except Exception:
            self.SendResponse(
                statusCode = 400,
                body = "Failed to decode the given 'id_token'."
            )
            return

        # Generate the F Token using the Android Device
        try:
            # Attempt to set as the current MITM Task
            res = self.hijacker.AttemptSet(tokenTask)
            while not res.Successful:
                res.CurrTask.Completed.wait()
                res = self.hijacker.AttemptSet(tokenTask)

            # Process the Task
            subprocess.call(self.endCmd, shell=True)
            subprocess.call(self.startCmd, shell=True)
            tokenTask.Completed.wait()

            self.SendResponse(
                statusCode = 200,
                headers = {
                    "User-ID": tokenTask.ID
                },
                body = tokenTask.F.ToJSON()
            )

        except Exception as ex:
            self.SendResponse(
                statusCode = 500,
                body = f"An internal server exception occurred generating F Token.\n\n{str(ex)}"
            )
    
    def SendResponse(self, statusCode: int, headers: dict[str, str] | None = None, body: str | None = None) -> None:
        self.send_response(statusCode)

        contentType = "application/json"
        try:
            json.loads(body)
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
