
const logger = require('./logger')(__filename);
const process_util = require('./process_util')(logger);
const iv_utils = require('./iv_utils');
var request = require('/usr/local/lib/node_modules/request');
var WebSocketClient = require('websocket').client;
var fs = require('fs');
const md_file_name = `md/ft_md_${iv_utils.dateTimeToString(new Date())}.txt`;
console.log(`md_file_name:`, md_file_name)
const md_file_stream = fs.createWriteStream(md_file_name, {
	flags: 'a'
})


var reconnectInterval = 1000 * 2;

const token = fs.readFileSync('token.txt', 'utf8');
logger.info(`token: ${token}`)

const stateType = {
	init: "init",
	connecting: "connecting",
	connected: "connected",
	disconnecting: "disconnecting",
	subscribingTouchline: "subscribingTouchline",
	subscribingDepth: "subscribingDepth",
	subscribed: "subscribed",
};

var shuttingDown = false;

function shouldShutdown() {
	const now = new Date();
	logger.info(`${now}`)
	if (now.getHours() > 15) {
		logger.info(`shouldShutdown returning true`)
		return true;
	}
	if (now.getHours() < 15) {
		logger.info(`shouldShutdown returning  false`)
		return false;
	}
	if (now.getHours() == 15) {
		if (now.getMinutes() > 30) {
			logger.info(`shouldShutdown returning true`)
			return true;
		}
		else {
			logger.info(`shouldShutdown returning false`)
			return false;
		}
	}
}

let ctx = {
	client: null,
	state: stateType.init,
	reconnectInProgress: false
};

function reconnect() {
	if (ctx.reconnectInProgress) {
		return;
	}
	ctx.reconnectInProgress = true;
	setTimeout(() => { ctx.reconnectInProgress = false; }, reconnectInterval * 5);
	logger.info("reconnect #######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	ctx.state = stateType.init;
	setTimeout(handleNextEvent, reconnectInterval);
}

const nseTOP100 = "NSE|13#NSE|22#NSE|25#NSE|3563#NSE|15083#NSE|6066#NSE|10217#NSE|8110#NSE|1270#NSE|157#NSE|236#NSE|19913#NSE|5900#NSE|16669#NSE|317#NSE|16675#NSE|305#NSE|4668#NSE|404#NSE|383#NSE|526#NSE|10604#NSE|2181#NSE|547#NSE|10794#NSE|685#NSE|694#NSE|20374#NSE|15141#NSE|14732#NSE|772#NSE|10940#NSE|881#NSE|910#NSE|6545#NSE|4717#NSE|10099#NSE|1232#NSE|7229#NSE|4244#NSE|1333#NSE|467#NSE|9819#NSE|1348#NSE|1363#NSE|2303#NSE|1394#NSE|1330#NSE|4963#NSE|21770#NSE|18652#NSE|1660#NSE|1624#NSE|13611#NSE|29135#NSE|5258#NSE|13751#NSE|1594#NSE|11195#NSE|11723#NSE|1922#NSE|17818#NSE|11483#NSE|9480#NSE|2031#NSE|4067#NSE|10999#NSE|23650#NSE|11630#NSE|17963#NSE|2475#NSE|24184#NSE|14413#NSE|2664#NSE|14977#NSE|2535#NSE|2885#NSE|17971#NSE|21808#NSE|3273#NSE|4204#NSE|3103#NSE|3150#NSE|3045#NSE|3351#NSE|11536#NSE|3432#NSE|3456#NSE|3426#NSE|3499#NSE|13538#NSE|3506#NSE|3518#NSE|11287#NSE|11532#NSE|10447#NSE|18921#NSE|3063#NSE|3787#NSE|5097"

function processShutdown() {
	md_file_stream.end();
	process.exit(0);
}

function handleErrorAndDisconnect(error) {
	logger.error(error);
	if (ctx.client) {
		ctx.client.close();
	}
	ctx.state = stateType.init;
	ctx.reconnectInProgress = false;
	logger.info("handleErrorAndDisconnect #######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
	logger.info("#######################################################################################################################")
}

function handleNextEvent(connection, msgstr) {
	logger.info(`state: ${ctx.state}, c:${!!connection}, m: ${!!msgstr}`)
	if (shuttingDown) { return; }
	if (shouldShutdown()) {
		shuttingDown = true;
		setTimeout(processShutdown, reconnectInterval);
		return;
	}
	if (ctx.state === stateType.init) {
		const url = "wss://piconnect.flattrade.in/PiConnectWSTp/"
		let client = new WebSocketClient();
		ctx.client = client
		registerCB(ctx.client);
		ctx.client.connect(url);
		ctx.state = stateType.connecting
		return;
	}
	else if (ctx.state === stateType.connecting) {
		ctx.state = stateType.connected;
		sendConnectRequest(connection);
		return;
	}
	else if (ctx.state === stateType.connected) {
		let msg = JSON.parse(msgstr);
		if (msg.t !== "ck" && msg.s !== "OK") {
			handleErrorAndDisconnect("FT protocol connect request failed!!");
			return;
		}
		ctx.state = stateType.subscribingTouchline;
		subscribeTouchline(connection);
		return;
	}
	else if (ctx.state === stateType.subscribingTouchline) {
		let msg = JSON.parse(msgstr);
		if (msg.t === "tf") { return; }
		if (msg.t === "df") { return; }
		if (msg.t !== "tk") {
			logger.error("FT protocol subscribeTouchline request failed!!");
			//handleErrorAndDisconnect("FT protocol subscribeTouchline request failed!!");
		}
		ctx.state = stateType.subscribingDepth;
		subscribeDepth(connection);
		return;
	}
	else if (ctx.state === stateType.subscribingDepth) {
		let msg = JSON.parse(msgstr);
		if (msg.t === "tf") { return; }
		if (msg.t === "df") { return; }
		if (msg.t !== "dk") { //TODO: count 100 dk before changing state
			logger.error("FT protocol subscribeDepth request failed!!");
			// handleErrorAndDisconnect("FT protocol subscribeDepth request failed!!");
		}
		ctx.state = stateType.subscribed;
		logger.info("##################################### SUBSCRIBED ###########################################")
		return;
	}

}

function subscribeTouchline(connection) {
	// NOTE: there is a BUG in FT API, you must need to send # in k field
	logger.info(`subscribeTouchline ${!!connection}  ${connection && connection.connected}`)
	if (connection.connected) {
		logger.info(`a2`)
		const req = {
			t: "t",
			k: "NSE|22#NSE|NIFTY", // NOTE: there is a BUG in FT API, you must need to send # in k field
		};
		const reqs = JSON.stringify(req);
		logger.info(`subscribeTouchline reqs:${reqs}`)
		connection.sendUTF(reqs);
	}
	else {
		logger.info(`subscribeTouchline error ${!!connection}  ${connection && connection.connected}`)
		handleErrorAndDisconnect("TCP connection is not connected !!")
	}

}

function subscribeDepth(connection) {
	logger.info(`b1 ${!!connection}  ${connection && connection.connected}`)
	if (connection.connected) {
		const req = {
			t: "d",
			k: nseTOP100
			// "NSE|22#NSE|3456",
		};
		connection.sendUTF(JSON.stringify(req));
	}
	else {
		handleErrorAndDisconnect("TCP connection is not connected !!")
		logger.info(`b3 ${!!connection}  ${connection && connection.connected}`)
	}

}

function sendConnectRequest(connection) {
	if (connection.connected) {
		const req = {
			t: "c",
			uid: "FT009375",
			actid: "FT009375",
			source: "API",
			susertoken: token
		};
		const rs = JSON.stringify(req);
		logger.info(`connect request: ${rs}`);
		connection.sendUTF(rs);
	}
	else {
		logger.error("TCP connection is not connected !!")
	}
}

function registerCB(client) {
	client.on('connectFailed', function (error) {
		logger.info('connectFailed: ' + error.toString());
		reconnect();
	});
	client.on('connect', function (connection) {
		logger.info('WebSocket Client Connected');
		connection.on('error', function (error) {
			logger.info("Connection Error: " + error.toString());
			reconnect();
		});
		connection.on('close', function () {
			logger.info('echo-protocol Connection Closed');
			reconnect();
		});
		connection.on('message', function (message) {
			if (message.type === 'utf8') {
				if (ctx.state !== stateType.subscribed) {
					logger.info("Received: '" + message.utf8Data + "'");
					handleNextEvent(connection, message.utf8Data)
				}
				md_file_stream.write("\n");
				md_file_stream.write("MD_at_t_" + iv_utils.dateTimeToString(new Date()));
				md_file_stream.write("\n");
				md_file_stream.write(message.utf8Data);
			}
			else {
				logger.error("Received non utf8 msg");
			}
		});
		handleNextEvent(connection);
	});
}

setTimeout(handleNextEvent, reconnectInterval);
