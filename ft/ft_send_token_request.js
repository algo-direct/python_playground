const puppeteer = require('puppeteer');


const user_agent = 'Mozilla/5.0 (X11; CrOS x86_64 15183.14.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36';


const fs = require('fs')
const totp = require("/usr/local/lib/node_modules/totp-generator");
var Browser = require("/usr/local/lib/node_modules/zombie");
const api_key='895c86921eba455e90464fc8b4532e1c'
//const api_key='2023.da32b9591a634e0cbe227083b41f8b2b10b8c3229da8a810'
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

function sleep(s) {
	const ms = s * 1000;
    return new Promise(resolve => setTimeout(resolve, ms));
}



const generate_totp_at14th_second = async () => {
    let t = new Date();
    let to = new Date(t);
    let d = 0;
    console.log(`t = ${t},  mod: ${(t.getSeconds() % 30)}`)
    if ((t.getSeconds() % 30) > 24) {
    d = 10;
    //t.setSeconds(0);
    t.setSeconds(t.getSeconds() + d);
    let diff = t - to;
    console.log(`generate_totp_at14th_second: Added ${d} seconds to "${to}", will generate token at ${t}, gap is ${(t - to) / 1000} seconds`);
    await sleep(diff/1000);
    }
    return totp(`${totp_hash}`, { digits: 6 });
};



const __generate_totp_at14th_second = async () => {
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

	const browser = await puppeteer.launch({headless:true,
args: ['--no-sandbox'],
	});
	const page = await browser.newPage();
	page.setUserAgent(user_agent);
//	page.on('error', handlePageCrash(page));
// page.on('pageerror', handlePageCrash(page));
	page.on('console', msg => console.log('PAGE LOG:', msg.text()));
	page.on('request', request => {
		try{
	    console.log("************************ ===========================================")
            console.log('request : headers:' + request.headers());
            console.log('request : method:' + request.method());
            console.log('request : url:' + request.url());
	        }catch(e){}
	});
	page.on('response', async (response) => {
		try{
		console.log("===========================================" + response.url());
		
		//const r = await response.text();
		//console.log('Response : ' + r);
	        }catch(e){}
		});
	    let url = `https://auth.flattrade.in/?app_key=${api_key}`
	await page.goto(url);
/*
	url = 'https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending'
	    console.log(`url: ${url}`)
	await page.goto(url);

        await sleep(4);
	const extractedText = await page.$eval('*', (el) => el.innerText);
    console.log(extractedText);
	const body = await page.$("body")
	await page.screenshot({ path: 'click.jpeg', fullPage: true , type: "jpeg"});
        console.log("---------------- after click ------------ ");
        console.log("---------------- ------------ ");
	await browser.close();
        return 
*/

        //page.once('load', async () => {
	console.log('Page loaded!');
	await page.screenshot({ path: 'onload.jpeg', fullPage: true , type: "jpeg"});
        let path = '';
        let field_text = '';
        path = 'input[id=pwd]';
        field = await page.waitForSelector(path)
	filed_text = await field.evaluate(el => el.innerHTML)
        console.log(`path:${path} | field: ${field_text}`);
	elem_pwd = field
        await sleep(2);
        path = 'input[id=pan]';
        field = await page.waitForSelector(path)
	filed_text = await field.evaluate(el => el.innerHTML)
        console.log(`path:${path} | field: ${field_text}`);
	elem_pan = field
        await sleep(1);
        path = 'input[id=input-17]';
        field = await page.waitForSelector(path)
	filed_text = await field.evaluate(el => el.innerHTML)
        console.log(`path:${path} | field: ${field_text}`);
	elem_un = field
        await sleep(1);
        path = 'button[id=sbmt]';
        field = await page.waitForSelector(path)
	filed_text = await field.evaluate(el => el.innerHTML)
        console.log(`path:${path} | field: ${field_text}`);
	elem_btn = field
        await sleep(1);

        const filename = "up.txt"
        const content = fs.readFileSync(filename).toString().split('\n')
        await elem_un.type(content[0]);
        await sleep(1);
	filed_text = await elem_un.evaluate(el => el.innerHTML)
        console.log(`after fill un | ${filed_text}`);
        await elem_pwd.type(content[1]);
        await sleep(1);
	filed_text = await elem_pwd.evaluate(el => el.innerHTML)
        console.log(`after fill pwd | ${filed_text}`);
        console.log(`getting totp`);
        const totp = await generate_totp_at14th_second();
        console.log(`totp ${totp}`);
        await elem_pan.type(totp);
        await sleep(1);
	filed_text = await elem_pan.evaluate(el => el.innerHTML)
        console.log(`after fill pan | ${filed_text}`);
	await page.screenshot({ path: 'fill.jpeg', fullPage: true , type: "jpeg"});
        console.log("---------------- ------------ ");
	let js = "var buttons = document.getElementsByClassName('mdi-eye-off'); " +
                  "for(var i = 0; i < buttons.length; i++) { "+
                     "buttons[i].click();}"
        console.log("ev ---------------- ------------ ");
	await page.evaluate(js);
        console.log("ev2 ---------------- ------------ ");
        await sleep(1);
        console.log("ev3 ---------------- ------------ ");
	await page.screenshot({ path: 'last.jpeg', fullPage: true , type: "jpeg"});
        console.log("ev4 ---------------- ------------ ");
        console.log("ev5 ---------------- ------------ ");
        elem_btn.click();
        console.log("---------------- login clicked ------------ ");
        await sleep(1);
	await page.screenshot({ path: 'click.jpeg', fullPage: true , type: "jpeg"});
        console.log("---------------- after click ------------ ");
        console.log("---------------- ------------ ");
        await sleep(10);
	await page.screenshot({ path: 'last.jpeg', fullPage: true , type: "jpeg"});
	// if url remains same as https://auth.flattrade.in/?app_key=
	// error will be shown at document.getElementById("sbmt").nextSibling.nextSibling.nextSibling.children[0].innerHTML == " "
        const curl = await page.url();
        console.log(`curl: ${curl}`);
        if(curl.indexOf(url) != -1) {
		const errorDiv = await page.evaluate(() => document.getElementById("sbmt").nextSibling.nextSibling.nextSibling.children[0].innerHTML);
                console.log(`Failed to generate token, errorDiv: ${errorDiv}`);
	}
	await browser.close();
	//});
    // input-17
    // pwd
    // pan
    // sbmt

}


async function init() {
    getRequestCodeFromFlatTrade();
//	let o = await generate_totp_at14th_second();
//	console.log(`o: ${o}`)
    // let tk = await generate_totp_at14th_second();
    // console.log(tk); // prints an 6-digit token
    sleep(5)
}

init()
