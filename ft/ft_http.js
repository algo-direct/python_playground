
var request = require('/usr/local/lib/node_modules/request');

const token='ec03209c1d533b6e9b49c70c2bb80bc9a482ea2165810707a014d3569ce9fc04';

function doRequest(url, data) {
	const headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    ,'Content-Type' : 'application/x-www-form-urlencoded'
};
  return new Promise(function (resolve, reject) {
   request({url: url,
    method: "POST",
    headers: headers,
    //headers: {
    //    "content-type": "application/json",
    //    },
    body: data
    //form: data
   }, function (error, res, body) {
//	       console.log(`res: ${JSON.stringify(res)} error: ${error}, body: ${JSON.stringify(body)}`);
      if (!error && res.statusCode === 200) {
        resolve({res, body});
      } else {
        reject(error);
      }
    });
  });
}

const symbolToToken = {
"SBIN-EQ": "3045",
"TATAMOTORS-EQ": "3456"
};

function seconds_since_epoch(d){ return Math.floor( d.getTime() / 1000 ); }
function date_delta(d, dt){
	d.setDate(d.getDate() + dt);
	return d;
}

function getEODChartData(symbol) {
    return () => { return {url: 'https://piconnect.flattrade.in/PiConnectTP/EODChartData',
	jData:  {uid: 'FT009375', symbol: "NSE:" + symbol, 
		from: "" + seconds_since_epoch(date_delta(new Date(), -1)),
		//st:  seconds_since_epoch(date_delta(new Date(), -1)),
		tp: "" + seconds_since_epoch(new Date()),
		//et:  seconds_since_epoch(new Date()),
//		intrv: "5"
	}
    }};
}


function getTPSeries(symbol) {
    return () => { return {url: 'https://piconnect.flattrade.in/PiConnectTP/TPSeries',
	jData:  {uid: 'FT009375', exch: 'NSE', token: "" + symbolToToken[symbol], 
		st: "" + seconds_since_epoch(date_delta(new Date(), -1)),
		//st:  seconds_since_epoch(date_delta(new Date(), -1)),
		et: "" + seconds_since_epoch(new Date()),
		//et:  seconds_since_epoch(new Date()),
		intrv: "5" }
    }};
}


function getTopListName() {
    return {url: 'https://piconnect.flattrade.in/PiConnectTP/TopListName',
	jData:  {uid: 'FT009375', exch: "NSE"}
    };
}

function getMaxPayoutAmount() {
    return {url: 'https://piconnect.flattrade.in/PiConnectTP/GetMaxPayoutAmount',
	jData:  {uid: 'FT009375', actid: 'FT009375'}
    };
}


function getGetBrokerMsg() {
    return {url: 'https://piconnect.flattrade.in/PiConnectTP/GetBrokerMsg',
	jData:  {uid: 'FT009375'}
    };
}

function getUserDetails() {
    return {url: 'https://piconnect.flattrade.in/PiConnectTP/UserDetails',
	jData:  {uid: 'FT009375'}
    };
}

function getSearchScrip() {
    return {url: 'https://piconnect.flattrade.in/PiConnectTP/SearchScrip',
	jData:  {uid: 'FT009375', stext: "SBI", exch: "NSE"}
    };
}


async function main(fx) {
const {url,jData}=fx()
const data = `jData=${JSON.stringify(jData)}&jKey=${token}`;
console.log(`url: ${url}`);
console.log(`data: ${data}`);
const resp = await doRequest(url, data);
console.log(`resp: ${JSON.stringify(resp)}`);
}

//main(getEODChartData("TATAMOTOTS-EQ"))
//main(getTopListName)
main(getGetBrokerMsg)
  .then(results => console.log("all done", results)) // <- receives result
  .catch(console.error) // <- handles error;
