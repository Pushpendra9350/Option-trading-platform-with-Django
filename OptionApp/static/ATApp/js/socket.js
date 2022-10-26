var imported = document.createElement('script');
imported.src = 'https://cdnjs.cloudflare.com/ajax/libs/pako/1.0.11/pako_inflate.js';
document.head.appendChild(imported);

let triggers = {
	"connect": [],
	"tick": []
};
var conn = null;
function websocket(clientcode, feedtoken, script, task)
{
	
	var x=0;
	var feed_token = feedtoken;
	var client_code = clientcode;
	var strwatchlistscrips = script;//"nse_cm|2885";
	var task =task;//'mw'; 
	var conn = new WebSocket('wss://wsfeeds.angelbroking.com/NestHtml5Mobile/socket/stream');//('wss://omnefeeds.angelbroking.com/NestHtml5Mobile/socket/stream');

	this.connection = function (){
		return new Promise((resolve, reject) => {
		if (client_code === null || feed_token === null) 
			return "client_code or feed_token is missing";

		

		conn.onopen = function(e) { 

			var _req = '{"task":"cn","channel":"","token":"' + feed_token + '","user":"' + client_code + '","acctid":"' + client_code + '"}'; 

			var result = conn.send(_req);

			trigger("connect", [result]);

			/*
			setInterval(function () {
				var _hb_req = '{"task":"hb","channel":"","token":"' + feed_token + '","user": "' + client_code + '","acctid":"' + client_code + '"}';
				conn.send(_hb_req);
			}, 60000);
			*/

		}; 
		conn.onmessage = function(e) {

			let strData = atob(e.data);
			
			// Convert binary string to character-number array
			var charData = strData.split('').map(function (x) { return x.charCodeAt(0); });

			// Turn number array into byte-array
			var binData = new Uint8Array(charData);

			// Pako magic
			var result = _atos(pako.inflate(binData));

			//console.log(result);
			trigger("tick", [result]);
			
		};


		conn.onerror = function (evt) {
			console.log("error::", evt);

		};
		conn.onclose = function (evt) {
			console.log("Socket closed");
			trigger("tick",['Socket Closed']);
		};
	});
	}

	this.runScript = function (script, task) {
		  
          if (task === null)
           return "task is missing";
          if (task === "mw" || task === "sfi" || task === "dp") {
               var strwatchlistscrips = script;   //"nse_cm|2885&nse_cm|1594&nse_cm|11536";
               var _req = '{"task":"' + task + '","channel":"' + strwatchlistscrips + '","token":"' + feed_token + '","user": "' + client_code + '","acctid":"' + client_code + '"}';
               conn.send(_req);
          } else return "Invalid task provided";
     };


	this.on = function (e, callback) {
      	if (triggers.hasOwnProperty(e)) {
           triggers[e].push(callback);
      	}
    };

    this.close = function () {
          ws.close()
     }

}

function _atos(array) {
     var newarray = [];
     try {
          for (var i = 0; i < array.length; i++) {
               newarray.push(String.fromCharCode(array[i]));
          }
     } catch (e) { }

     return newarray.join('');
}



function trigger(e, args) {
     if (!triggers[e]) return
     for (var n = 0; n < triggers[e].length; n++) {
          triggers[e][n].apply(triggers[e][n], args ? args : []);
     }
}