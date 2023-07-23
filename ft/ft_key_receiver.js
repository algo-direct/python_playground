const fs = require('fs');
var express = require('/usr/local/lib/node_modules/express');
var app = express();
var request = require('/usr/local/lib/node_modules/request');
const { createHash } = require('crypto');

const api_key='895c86921eba455e90464fc8b4532e1c'
const api_secret='2023.da32b9591a634e0cbe227083b41f8b2b10b8c3229da8a810'

function doRequest(url, data) {
  return new Promise(function (resolve, reject) {

   request({url: url,
    method: "POST",
    headers: {
        "content-type": "application/json",
        },
    json: data
   }, function (error, res, body) {
      if (!error && res.statusCode === 200) {
        resolve({res, body});
      } else {
        reject(error);
      }
    });
  });
}

// This responds with "Hello World" on the homepage
app.get('/', function (req, res) {
   console.log('ft_key_receiver: ' + "Got a GET request for the homepage");
   res.send('Hello GET');
})

// This responds a GET request for the /list_user page.
app.get('/ftsk', async function (req, res) {
   console.log('ft_key_receiver: ' + `Got a GET request for ${req.originalUrl}`);
   console.log('ft_key_receiver: ' + `query ${JSON.stringify(req.query)}`);
   console.log('ft_key_receiver: ' + `query.code ${req.query.code}`);
   request_code=req.query.code
   url=`https://authapi.flattrade.in/trade/apitoken`
   api_secret_hash_input=`${api_key}${request_code}${api_secret}`
   api_secret_hash=createHash('sha256').update(api_secret_hash_input).digest('hex');
   const body = {
      "api_key":`${api_key}`,
      "request_code": `${request_code}`,
	   "api_secret":`${api_secret_hash}`
   }
   console.log('ft_key_receiver: ' + `api_key: ${api_key}`)
   console.log('ft_key_receiver: ' + `request_code: ${request_code}`)
   console.log('ft_key_receiver: ' + `api_secret: ${api_secret}`)
   console.log('ft_key_receiver: ' + `api_secret_hash: ${api_secret_hash}`)
   console.log('ft_key_receiver: ' + `body: ${JSON.stringify(body)}`)
   const resp = await doRequest(url, body);
   console.log('ft_key_receiver: ' + `resp: ${JSON.stringify(resp)}`);
   fs.writeFileSync('token.json', `${JSON.stringify(resp, undefined, 2)}`);
   fs.writeFileSync('token.txt', `${resp["body"]["token"]}`);
   res.send(`${JSON.stringify(resp, undefined, 2)}`);
})

var server = app.listen(8080, function () {
   var host = server.address().address
   var port = server.address().port
   console.log('ft_key_receiver: ' + "Example app listening at http://%s:%s", host, port)
})
