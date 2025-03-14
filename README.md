# NSOBox - An Experimental Sandbox Server For F-Token Synthesis
This project aims to allow non-NSO (Nintendo Switch Online) clients to connect to the Nintendo Game APIs by generating F-Tokens for arbitrary clients.

## Context
Nintendo has cut down on unofficial API access in recent times by forcing login requests to be accompanied by a `f` parameter. It is unknown how exactly this parameter is generated, and the code to do so is heavily obfuscated and contains primitive debugging detection.

While annoying, it was still possible to work around by hooking the application with Frida. This allowed for a server to be established between the app and clients. The hook would then generate valid F tokens, which were sent back to the clients.

Unfortunately, Nintendo has implemented Google's `pairipcore` library, which features much more advanced debugging detection and the old Frida server approach is no longer viable.

## A New Solution
By manipulating the Nintendo Switch Online's local storage and network activity, it is still possible to force an instance of the app into generating arbitrary F tokens.

This project provides a server for accepting incoming F-Token requests and controlling an Android device to fulfill them.

## Prerequisites
- A **rooted** Android Device/Redroid Container in developer mode.
    - The latest version of Nintendo Switch Online must be installed.
        - Needs to have been started at least once - does not need to be logged in.
        - Must have root access disabled (i.e. Magisk DenyList or similar).
    - Your MITMProxy Certificate must be installed to the system store.
    - ADB Shell must have superuser permissions.
- [MITMProxy](https://mitmproxy.org/) and [ADB](https://developer.android.com/tools/adb) installed on the hosting computer.
- A Python 3.10+ environment with the `requests` and `mitmproxy` packages installed.
    - See [requirements.txt](requirements.txt)

#### If you have the proper setup, you should be able to perform the following steps:
- Running `adb devices` in any Terminal should return a list containing your device ID.
```shell
~> adb devices
List of devices attached
89WX0J2UJ       device
```
- Running `adb shell "su -c 'echo Hello'"` should return like so:
```shell
~>  adb shell "su -c 'echo Hello'"
Hello
```
- If you receive an error message, ensure that you've granted Shell superuser rights in your root manager.
- Running `mitmproxy` in any Terminal should start MITMProxy. If you followed the Android setup guide properly, you should be able to see all the traffic coming from the Android device.
    - If you don't observe any traffic, try opening a webpage in Chrome and ensuring you have your proxy settings properly set.
    - If you see SSL errors, make sure that you installed your unique MITMProxy certificate into the Android system store correctly.

## Setup
If you were successfully able to run all of the prerequisite steps, you should now be able to start and run the Python server.

This Python server will establish a MITMProxy instance and start an HTTP server to accept incoming requests. The ports of which can be customized at the top of the [Server.py](src/Server.py) file. By default, they are as follows:
```python
# Configuration
HTTP_SERVER_HOST = "0.0.0.0"
HTTP_SERVER_PORT = 8000

MITM_SERVER_HOST = "0.0.0.0"
MITM_SERVER_PORT = 8080
```
You can start the server just by running `python Server.py` from the [src](src/) directory.
```shell
~/NSOBox/src> python Server.py
[*] Starting HTTP Server...
[*] Starting MITM Proxy...
```

The server supports both types of F Token generation.

#### Generation Method 1

The first F token required to gain a `webApiServerCredential` from `https://api-lp1.znc.srv.nintendo.net/v3/Account/Login` can be generated using the following GET request:
```shell
# For F1 Tokens | id_token from https://accounts.nintendo.com/connect/1.0.0/api/token
GET http://localhost:8000/F1?id_token=[id_token]
```

F1 tokens can then be used to get a `webApiServerCredential` from `https://api-lp1.znc.srv.nintendo.net/v3/Account/Login`.

#### Generation Method 2
The second F token required to gain `GameWebServiceToken` from `https://api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken` can be generated using the following GET request:
```shell
# For F2 Tokens | webApiServerCredential from https://api-lp1.znc.srv.nintendo.net/v3/Account/Login
GET http://localhost:8000/F2?web_api_token=[webApiServerCredential]
```
A `GameWebServiceToken` can be used to access game specific APIs, such as Splatnet.
#### Results
When successful, the server will return an `application/json` payload containing the following information:
```json
{
  "timestamp": 1700000000000,
  "requestId": "20f8b70c-3e63-4800-b490-64347c23b0a3",
  "f": "deb416eaa8c61f4d18f84f7c1f1e4d9562a1b53f7..."
}
```
In the event of an error, the server will return a non-200 status code and an `application/text` payload containing an error message.

## WIPs
- Upgrading Networking Infrastructure
- Ease of Access Improvements
