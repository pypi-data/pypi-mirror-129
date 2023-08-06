An NPM package for obfuscating scripts with Moonsec V3 (THIS IS NOT OFFICIAL)

Example:

```js
// Load moonsec
const msec = require('moonsec')
// Load fs (For file saving)
const fs = require('fs')

// Creates a client. new msec.Client(API Key)
const client = new msec.Client('your api key')


// Obfuscates a script. client.obfuscate(script, options, callback)
client.obfuscate('print("Hello World") MS_WATERMARK("Your watermark")', {
    "platform": "lua", // roblox (for excutors), lua (for things like repl), fivem (for fivem), robloxstudio (for server scripts)
    "maxsecurity": true, // Enables code optimization, uses more secure structures and increases security. Best when used with anti tamper. Not recommended on big scripts.
    "antitamper": true, // This uses loadstring or load, so your platform must support one of them. Uses a cool loader-like protection to ensure the safety of the VM as well as your code. File size might be 80kb more than usual.
    "constantprotection": true, // Encrypt constants and adds runtime integrity checks against deserializer/interpreter tampering.
    "requireprotection": false // Only for robloxstudio
}, async function(script, downloadurl) {
    console.log(downloadurl)
    await fs.writeFile('output.lua', script, function(err) {})
})
```