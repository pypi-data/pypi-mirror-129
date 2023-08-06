A package for obfuscating scripts with Moonsec V3 (THIS IS NOT OFFICIAL)

Example:

```py
from moonsec import Obfuscator as Msec

Msec.login('api key')

def obfuscationCallback(script, downloadurl):
    print(downloadurl)
    open('output.lua', 'wb').write(script)

Msec.obfuscate("print('Hello World') MS_WATERMARK('Your watermark')", {
    "platform": "lua", # roblox (for excutors), lua (for things like repl), fivem (for fivem), robloxstudio (for server scripts)
    "maxsecurity": True, # Enables code optimization, uses more secure structures and increases security. Best when used with anti tamper. Not recommended on big scripts.
    "antitamper": True, # This uses loadstring or load, so your platform must support one of them. Uses a cool loader-like protection to ensure the safety of the VM as well as your code. File size might be 80kb more than usual.
    "constantprotection": True, # Encrypt constants and adds runtime integrity checks against deserializer/interpreter tampering.
    "requireprotection": False # Only for robloxstudio
}, obfuscationCallback)
```