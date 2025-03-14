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

class TokenData:
    def DummySession() -> str:
        return "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MWI5NjNjMWI3YjZkMTE5IiwianRpIjoxNzA1NTMyMTE3MSwic3ViIjoiMDAwMDAwMDAwMDAwMDAwMCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMubmludGVuZG8uY29tIiwiaWF0IjowMDAwMDAwMDAwLCJzdDpzY3AiOlswLDgsOSwxNywyM10sImV4cCI6OTk5OTk5OTk5OSwidHlwIjoic2Vzc2lvbl90b2tlbiJ9.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    def DummyAccess() -> str:
        return "eyJraWQiOiIxMTZlODk3Ny1lYTFlLTQwMzEtOWEzYi1mNWMwNTM4OTQyZjQiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYWNjb3VudHMubmludGVuZG8uY29tLzEuMC4wL2NlcnRpZmljYXRlcyJ9.eyJhYzpzY3AiOlswLDgsOSwxNywyM10sImlhdCI6MDAwMDAwMDAwMCwianRpIjoiYjdhNjUzMjQtNDc3Zi00MjQyLWJiOGYtNmQ2MGJkODAwYWUzIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5uaW50ZW5kby5jb20iLCJhYzpncnQiOjY0LCJ0eXAiOiJ0b2tlbiIsImF1ZCI6IjcxYjk2M2MxYjdiNmQxMTkiLCJleHAiOjk5OTk5OTk5OTksInN1YiI6ImRlYWRiZWVmZGVhZGJlZWYifQ==.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    def DummyID() -> str:
        return "eyJraWQiOiJhNGNiZmZiNS0xMDU3LTQ0MTItYmZmZS1mNTc0M2I5NjQ2NDgiLCJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYWNjb3VudHMubmludGVuZG8uY29tLzEuMC4wL2NlcnRpZmljYXRlcyJ9.eyJ0eXAiOiJpZF90b2tlbiIsImF0X2hhc2giOiJPdXdNZ3dCZkc3SUkxODJYOG1TRHpBIiwiZXhwIjo5OTk5OTk5OTk5LCJzdWIiOiJkZWFkMDAwMDAwMDBiZWVmIiwiYXVkIjoiNzFiOTYzYzFiN2I2ZDExOSIsImNvdW50cnkiOiJVUyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMubmludGVuZG8uY29tIiwiaWF0IjowMDAwMDAwMDAwLCJqdGkiOiIyMGUyMWIxNy1iMTk2LTQwN2UtYTMzNS1hYzAzYTlkNjI3NzcifQ==.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    def DummyV1ID() -> str:
        return "deadbeefdeadbeef"
    
    def V1Layout() -> str:
        lines = [
            "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>",
            '<map>',
            f'<string name="SessionToken">{TokenData.DummySession()}</string>',
            '<string name="AccessToken"></string>',
            '<string name="IDToken"></string>',
            '</map>'
        ]

        return "".join(lines)
    
    def Path() -> str:
        return "/data/data/com.nintendo.znca/shared_prefs/TokenData.xml"

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
    
    def V2Layout(accessToken: str, id: int) -> str:
        userInfo = {
            "id": id,
            "nsaId": "deadbeefdeadbeef",
            "imageUri": "https://cdn-image-e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com/1/249afd3869c8e31d",
            "name": "Client",
            "supportId": "0000-0000-0000-0000-0000-0",
            "isChildRestricted": False,
            "etag": "\"deadbeefdeadbeef\"",
            "links": {
                "nintendoAccount": {
                    "membership": {
                        "active": True
                    }
                },
                "friendCode": {
                    "regenerable": True,
                    "regenerableAt": 1600000000,
                    "id": "0000-0000-0000"
                }
            },
            "permissions": {
                "presence": "FRIENDS"
            },
            "presence": {
                "state": "OFFLINE",
                "updatedAt": 0,
                "logoutAt": 0,
                "game": {}
            }
        }

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
            f'<string name="CoralUserKeyV2">{json.dumps(userInfo, separators=(',', ':')).replace('"', "&quot;")}</string>',
            f'<long name="CoralAccessTokenExpiredAtKeyV2" value="{int(time.time() + 7000)}"/>',
            f'<string name="CoralAccessTokenKeyV2">{accessToken}</string>'
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
    
    def AppletLaunchURL() -> str:
        return "https://s.nintendo.com/av5ja-lp1/znca/game/4834290508791808"


class ServerResponse:
    class Header:
        def APITokens(contentLength: int) -> dict:
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
        
        def ListWebServices() -> dict:
            return {
                "date": datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT'),
                "content-type": "application/json",
                "vary": "Accept-Encoding",
                "vary": "origin",
                "server": "gunicorn",
                "allow": "POST, OPTIONS",
                "x-frame-options": "DENY",
                "x-content-type-options": "nosniff",
                "referrer-policy": "same-origin",
                "cross-origin-opener-policy": "same-origin",
                "content-encoding": "gzip",
                "via": "1.1 google"
            }

    class Body:
        def APITokens(idToken: str, accessToken: str) -> str:
            res = {
                "token_type": "Bearer",
                "id_token": idToken,
                "scope": [
                    "openid",
                    "user",
                    "user.birthday",
                    "user.mii",
                    "user.screenName"
                ],
                "access_token": accessToken,
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
        
        def ListWebServices() -> str:
            res = {
                "status": 0,
                "result": [
                    {
                        "id": 4834290508791808,
                        "uri": "https://api.lp1.av5ja.srv.nintendo.net",
                        "customAttributes": [
                            {
                                "attrValue": "true",
                                "attrKey": "verifyMembership"
                            },
                            {
                                "attrValue": "true",
                                "attrKey": "deepLinkingEnabled"
                            },
                            {
                                "attrValue": "true",
                                "attrKey": "fullScreen"
                            },
                            {
                                "attrValue": "000000",
                                "attrKey": "appNavigationBarBgColor"
                            },
                            {
                                "attrValue": "000000",
                                "attrKey": "appStatusBarBgColor"
                            }
                        ],
                        "whiteList": [
                            "*.av5ja.srv.nintendo.net",
                            "c.nintendo.com/splatoon3-tournament"
                        ],
                        "name": "Splatoon 3",
                        "imageUri": "https://cdn.znc.srv.nintendo.net/gameWebServices/n84dab60/n84dab60/images/usEn/banner.png"
                    }
                ],
                "correlationId": "deadbeef-dead-dead-dead-deadbeefdead-deadbeef"
            }
            
            return json.dumps(res)
