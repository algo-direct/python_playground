const totp = require("totp-generator");
const crypto = require('crypto');
var querystring = require('querystring');
// var http = require('http');
var http = require('node:https');
var fs = require('fs');

// https://auth.flattrade.in/?app_key=817b42a19c3c4e2cb7b964a28ace809f

function send_request_to_get_token(

    request_code, api_key = '817b42a19c3c4e2cb7b964a28ace809f', api_secret_input = '2022.97ad1da690a44886842195e70ed6ee3d39cd920a50483575'

) {
    const input = api_key + request_code + api_secret_input;
    const api_secret = crypto.createHash('sha256').update(input).digest('hex');
    const req = {
        api_key, request_code, api_secret
    };

    var post_data = querystring.stringify(req);
  
    // https://authapi.flattrade.in/trade/apitoken
    // An object of options to indicate where to post to
    var post_options = {
        host: 'authapi.flattrade.in',
        port: '443',
        path: '/trade/apitoken',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': Buffer.byteLength(post_data)
        }
    };
  
    // Set up the request
    var post_req = http.request(post_options, function(res) {
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('Response: ' + chunk);
        });
    });

    post_req.on('error', (e) => {
        console.error(e);
      });
  
    // post the data
    post_req.write(post_data);
    post_req.end();
}

const request_code='1726242f1b18d1c4.31e880450ee86e3a1ac8c3fc2bb02a33fef5ab9450876e644be38e60ce707e27';
send_request_to_get_token(request_code)