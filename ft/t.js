
const fs = require('fs')
const totp = require("/usr/local/lib/node_modules/totp-generator");
var Browser = require("/usr/local/lib/node_modules/zombie");
const api_key='2023.da32b9591a634e0cbe227083b41f8b2b10b8c3229da8a810'
const totp_hash="V66RE47RI74LO7S7I5LPZ3J6Y7IIWOR6"
const token = totp(`${totp_hash}`, { digits: 6 });
console.log(token); // prints an 6-digit token

const inspect = obj => {
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            console.log(`${prop}: ${obj[prop]}`)
        }
    }
}

//   inspect(token)
// console.log('%O',); // prints an 8-digit token

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const generate_totp_at14th_second = async () => {
    let t = new Date();
    let to = new Date(t);
    let d = 0;
    if (t.getSeconds() < 30) {
        d = 44;
    }
    else {
        d = 74;
    }
    t.setSeconds(0);
    t.setSeconds(d);
    let diff = t - to;
    console.log(`generate_totp_at14th_second: Added ${d} seconds to "${to}", will generate token at ${t}, gap is ${(t - to) / 1000} seconds`);
    await sleep(diff);
    return totp(`${totp_hash}`, { digits: 6 });
};

async function getRequestCodeFromFlatTrade() {
    let user_agent = 'Mozilla/5.0 (X11; CrOS x86_64 15183.14.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36';
    let browser = new Browser({
        userAgent: user_agent, debug: true,
	    //maxWait: 12000000,
        waitDuration: '20s',
    });

    browser.debug = true
    browser.pipeline.addHandler(function (browser, request, response) {
        // Log the response body
	console.log("************************ ===========================================")
        console.log('request : ' + JSON.stringify(request));
	console.log("===========================================")
        console.log('Response : ' + JSON.stringify(response));
	//return new Promise(function(resolve) {
    //setTimeout(resolve, 100);
  //});
    //sleep(500);
	    return response;
    });
    // let url = 'https://www.google.com';
    let url = `https://google.com`
    console.log(`url: ${url}`)
    browser.visit(url,  function (error) {
        console.log("#######----------------");
        if (error) {
            console.log("****** Error In Browser:", error);
           // return { error };
        }
        console.log("---------------- loaded page: ");
        browser.dump();
        // await sleep(5 * 1000);
        console.log("---------------- ------------ ");

    });
    // input-17
    // pwd
    // pan
    // sbmt

}

async function init() {
    getRequestCodeFromFlatTrade();
    // let tk = await generate_totp_at14th_second();
    // console.log(tk); // prints an 6-digit token
    sleep(5)
}

init()