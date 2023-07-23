
var fs = require('fs');
const fn = "OpenAPIScripMaster.json"
const d = JSON.parse(fs.readFileSync(fn,{ encoding: 'utf8' }))
let buf = ""
d.forEach((s) => {
    buf += JSON.stringify(s)
    buf += "\n"
}); 
fs.writeFileSync(`sym.json`, buf);
