import json
import time

from datetime import datetime, timezone
from base64 import b64decode

class Utils:
    def ToHexString(string: str) -> str:
        return ''.join(f'\\x{ord(char):02x}' for char in string)
    
    def DecodeB64String(b64: str) -> str:
        padCheck = len(b64) % 4
        if padCheck:
            b64 += '=' * (4 - padCheck)

        enBytes = b64.encode("ascii")
        deBytes = b64decode(enBytes)

        return deBytes.decode("ascii")

class SharedPreferences:
    def V1Layout() -> str:
        lines = [
            '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
            '<map>',
            '<string name="LastDeviceLanguageKey">USen</string>',
            '<string name="CoralNAUserKey"></string>',
            '<boolean name="GameWebServiceNotificationUnreadFlagById-4834290508791808" value="false"/>',
            '<string name="FirebaseRegistrationToken"></string>',
            '<boolean name="HasRequestBluetoothConnectPermission" value="false"/>',
            '<boolean name="HasShownFavoriteBalloon" value="true"/>',
            '<string name="GameWebServiceNotificationList"></string>',
            '<string name="AnnouncementListAPICacheKey">[]</string>',
            '<boolean name="HasShownNotificationDialog" value="false"/>',
            '<int name="Version" value="1"/>',
            '<string name="CoralUserKeyV2"></string>',
            '<long name="CoralAccessTokenExpiredAtKeyV2" value="0"/>',
            '<int name="LastDisplayModeCategory" value="0"/>',
            '<string name="GameWebServiceOrder"></string>',
            '<string name="AnalyticsCollectionStatus">reject</string>',
            '<boolean name="HasShownDataUsage" value="true"/>',
            '</map>'
        ]

        return "".join(lines)
    
    def Path() -> str:
        return "/data/data/com.nintendo.znca/shared_prefs/com.nintendo.znca_preferences.xml"

class NSOApp:
    def MainActivity() -> str:
        return "com.nintendo.coral.ui.boot.BootActivity"


class ServerResponse:
    class Header:
        def APIToken(contentLength: int) -> dict:
            return {
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": str(contentLength),
                    "Server": "nginx",
                    "X-Content-Type-Options": "nosniff",
                    "Strict-Transport-Security": "max-age=2592000; includeSubDomains",
                    "Pragma": "no-cache",
                    "Connection": "keep-alive",
                    "Cache-Control": "private, no-cache, must-revalidate, no-store",
                }
        
        def GetUser() -> dict:
            return {
                    "Date": datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                    "Content-Type": "application/json; charset=UTF-8",
                    "Transfer-Encoding": "chunked",
                    "Connection": "keep-alive",
                    "Server": "nginx",
                    "X-Content-Type-Options": "nosniff",
                    "Strict-Transport-Security": "max-age=2592000; includeSubDomains"
                }

    class Body:
        def APIToken(idToken: str) -> str:
            res =   {
                      "token_type": "Bearer",
                      "id_token": idToken,
                      "scope": [
                          "openid",
                          "user",
                          "user.birthday",
                          "user.mii",
                          "user.screenName"
                      ],
                      "access_token": "eyJqa3UiOiJodHRwczovL2FjY291bnRzLm5pbnRlbmRvLmNvbS8xLjAuMC9jZXJ0aWZpY2F0ZXMiLCJraWQiOiI1ZDc3MDc0NC0yZjVjLTQ4YzQtYjZiNC1mODRiZTU0MGExYTkiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI0YzgzYWVmMC04M2IzLTQ3NGMtODY0ZS1jNzkxNTQ3MTkwOTYiLCJhdWQiOiI3MWI5NjNjMWI3YjZkMTE5IiwiYWM6c2NwIjpbMCw4LDksMTcsMjNdLCJ0eXAiOiJ0b2tlbiIsImFjOmdydCI6NjQsInN1YiI6IjU5NjUyMDE3ZmQ0YjgzYzYiLCJleHAiOjE3NDEzNzUyNjMsImlhdCI6MTc0MTM3NDM2MywiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5uaW50ZW5kby5jb20ifQ.iUinEO62v0MvtLZ1CY4bPvaqpCYsax7aNR7HiA8ZWL7ERXeWG11Y2PmjOfETAuC45gwzdeMTadYOxa-4f_J1YorXp-TMpvb-RMqn-a3JN-GKxZLL0Fov_Mck43bVvj4X_e6ZZn0Kk8CUS8rC5it9XPbced24PfRNPTaGEmo1UpRk-rgexB6N8_jWaT5Dcx2ycG7u94UoSVnQAz5DbnIDopWTaHllZngaxNutePtapwYj43HGOeBCjAEJZEyC5GII7iLexaBRwqt5nt2ubrE-PhGCvSJouzDvYpYmaV4Zz8YXLRh33RsNSX2EreTC2sP1NU4KnJs3DeCV0A9eBEY1OA",
                      "expires_in": 900
                    }

            return json.dumps(res)

        def GetUser(id: str) -> str:
            res = {
                "eachEmailOptedIn": {
                    "deals": {
                        "optedIn": False,
                        "updatedAt": 1600000000
                    },
                    "survey": {
                        "optedIn": False,
                        "updatedAt": 1600000000
                    }
                },
                "candidateMiis": [],
                "createdAt": 1600000000,
                "iconUri": "https://cdn.accounts.nintendo.com/icons/v1/62414737-3ba3-4aa4-9f02-13a843594e72.png",
                "emailOptedInUpdatedAt": 1600000000,
                "region": None,
                "language": "US-en",
                "phoneNumberEnabled": None,
                "analyticsOptedInUpdatedAt": 1600000000,
                "timezone": { 
                    "name": "UTC",
                    "utcOffsetSeconds": 0,
                    "id": "UTC",
                    "utcOffset": "+00:00"
                },
                "mii": None,
                "clientFriendsOptedIn": True,
                "emailVerified": True,
                "birthday": "2000-10-10",
                "id": id,
                "updatedAt": int(time.time() - 60),
                "nickname": "Client",
                "gender": "male",
                "isChild": False,
                "emailOptedIn": False,
                "screenName": "•••••@•••••",
                "analyticsOptedIn": False,
                "country": "US",
                "analyticsPermissions": {
                    "targetMarketing": {
                        "updatedAt": 1600000000,
                        "permitted": False
                    },
                    "internalAnalysis": {
                        "permitted": False,
                        "updatedAt": 1600000000
                    }
                },
                "clientFriendsOptedInUpdatedAt": 1600000000
            }

            return json.dumps(res)