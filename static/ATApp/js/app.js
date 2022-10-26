var index_name = "";
var buy_sell = "";
var current_add_id = "";
var current_exit_id = "";
var current_add_qty = "";
var current_exit_qty = "";
var current_price = "";
var socket = "";

function roundTo(data){
    return Math.round((data + Number.EPSILON) * 100) / 100
}

function BuyPercent(initial_val,current_val){
    var percent =  ((current_val - initial_val) / initial_val) * 100;
    return roundTo(percent);
}
function SellPercent(initial_val,current_val){
    var percent =  ((initial_val - current_val) / initial_val) * 100;
    return roundTo(percent);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function get_stikes(symbol){
    var url = "http://127.0.0.1:8000/get_strikes/";
    $.ajax({  
        url: url,
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data : {
            'symbol':symbol
        },
        dataType: 'json',
        success: function(data) {
            var strikes = data.strikes;
            var select = document.getElementById('strike-options');
            document.getElementById('strike-options').innerText = null;
            var opt = document.createElement('option');
            opt.innerHTML = 'Select a Strike';
            select.appendChild(opt);
            for (var i = 0; i<strikes.length; i++){
                var opt = document.createElement('option');
                opt.value = strikes[i];
                opt.innerHTML = strikes[i];
                select.appendChild(opt);
            }
        },
        error: function(data) {
            console.log(data);
        }
    });
}

function niftyBuy()
{
    get_stikes('NIFTY');
    index_name = 'NIFTY';
    buy_sell = 'Buy';
    document.getElementById("order-model").style.height = "380px";
    document.getElementById("place-order").innerHTML = "Place Nifty Buy Order";
    document.getElementById("place-order").classList.remove('btn-danger');
    document.getElementById("place-order").classList.add('btn-success');
}

function niftyBuyOrderPlace(){
    var expiry = document.querySelector('input[name="expiry"]:checked').value;
    var stoploss = document.querySelector('input[name="stoploss"]:checked').value;
    var target = document.querySelector('input[name="target"]:checked').value;
    var side = document.querySelector('input[name="side"]:checked').value;
    console.log(expiry, stoploss, target, side);
}


function niftySell()
{
    get_stikes('NIFTY');
    index_name = 'NIFTY';
    buy_sell = 'Sell';
    document.getElementById("order-model").style.height = "380px";
    document.getElementById("place-order").innerHTML = "Place Nifty Sell Order";
    document.getElementById("place-order").classList.remove('btn-success');
    document.getElementById("place-order").classList.add('btn-danger');
    console.log('NIFTY SELL')
}

function bankniftyBuy()
{
    get_stikes('BANKNIFTY');
    index_name = 'BANKNIFTY';
    buy_sell = 'Buy';
    document.getElementById("order-model").style.height = "380px";
    document.getElementById("place-order").innerHTML = "Place Banknifty Buy Order";
    document.getElementById("place-order").classList.remove('btn-danger');
    document.getElementById("place-order").classList.add('btn-success');
}


function bankniftySell()
{
    get_stikes('BANKNIFTY');
    index_name = 'BANKNIFTY';
    buy_sell = 'Sell';
    document.getElementById("order-model").style.height = "380px";
    document.getElementById("place-order").innerHTML = "Place Banknifty Sell Order";
    document.getElementById("place-order").classList.remove('btn-success');
    document.getElementById("place-order").classList.add('btn-danger');
    console.log('BANKNIFTY SELL')
}

function cancelOrder()
{
    document.getElementById("order-model").style.height = "0px";
    document.getElementById("place-order").classList.remove('btn-danger');
    document.getElementById("place-order").classList.remove('btn-success');
}

function placeOrder(data){
    document.getElementById("order-model").style.height = "0px";
    document.getElementById("place-order").classList.remove('btn-danger');
    document.getElementById("place-order").classList.remove('btn-success');
    var url = "http://127.0.0.1:8000/place_order/";
    $.ajax({  
        url: url,
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data : {
            'name':data['name'],
            'expiry':data['expiry'],
            'strike':data['strike'],
            'quantity':data['quantity'],
            'side':data['side'],
            'stoploss':data['stoploss'],
            'target':data['target'],
            'type':data['type'],
        },
        dataType: 'json',
        success: function(data) {
            if(data.status == 'success'){
            get_today_positions();
            var x = document.getElementById("green-toast");
            var audio = new Audio('static/OptionApp/media/notification.mp3');
            audio.play();
            x.style.visibility = "visible";
            setTimeout(function(){ 
                x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
            }, 4000);
            }
            else{
                var x = document.getElementById("red-toast");
                x.style.visibility = "visible";
                setTimeout(function(){ 
                    x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                }, 4000);
            }
        },
        error: function(data) {
            console.log(data);
            var x = document.getElementById("red-toast");
            x.style.visibility = "visible";
            setTimeout(function(){ 
                x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
            }, 4000);
        }
    });
}

function add_model_popup(id){
    document.getElementById("addModel").style.display = "block";
    current_add_id = id;
    console.log(id)
    current_price = document.getElementById("ltp"+id).innerHTML;
    console.log(current_price)
}

function add_model_close(){
    document.getElementById("addModel").style.display = "none";
}

function exit_model_popup(id){
    document.getElementById("exitModel").style.display = "block";
    current_add_id = id;
    console.log(id)
    current_price = document.getElementById("ltp"+id).innerHTML;
    console.log(current_price)
}

function exit_model_close(){
    document.getElementById("exitModel").style.display = "none";
}


function addQuantity(){
    document.getElementById("addModel").style.display = "none";
    var quantity = document.getElementById("addquantity").value;
    var url = "http://127.0.0.1:8000/add_quantity/";
    $.ajax({  
        url: url,
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data : {
            'price':current_price,
            'quantity':quantity,
            'token':current_add_id
        },
        dataType: 'json',
        success: function(data) {
            if(data.status == 'success'){
                get_today_positions();
                var x = document.getElementById("blue-toast");
                x.style.visibility = "visible";
                var audio = new Audio('static/OptionApp/media/notification.mp3');
                audio.play();
                setTimeout(function(){ 
                    x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                }, 4000);
                }
                else{
                    var x = document.getElementById("red-toast");
                    x.style.visibility = "visible";
                    setTimeout(function(){ 
                        x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                    }, 4000);
                }
        },
        error: function(data) {
            console.log(data);
            var x = document.getElementById("red-toast");
            x.style.visibility = "visible";
            setTimeout(function(){ 
                x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
            }, 4000);
        }
    });
}

function exitQuantity(){
    document.getElementById("exitModel").style.display = "none";
    var quantity = document.getElementById("exitquantity").value;
    var url = "http://127.0.0.1:8000/exit_quantity/";
    $.ajax({  
        url: url,
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data : {
            'price':current_price,
            'quantity':quantity,
            'token':current_add_id
        },
        dataType: 'json',
        success: function(data) {
            if(data.status == 'success'){
                get_today_positions();
                var x = document.getElementById("blue-toast-exit");
                x.style.visibility = "visible";
                var audio = new Audio('static/OptionApp/media/notification.mp3');
                audio.play();
                setTimeout(function(){ 
                    x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                }, 4000);
                }
                else{
                    var x = document.getElementById("red-toast");
                    x.style.visibility = "visible";
                    setTimeout(function(){ 
                        x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                    }, 4000);
                }
        },
        error: function(data) {
            console.log(data);
            var x = document.getElementById("red-toast");
            x.style.visibility = "visible";
            setTimeout(function(){ 
                x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
            }, 4000);
        }
    });
}

function endTheDay(){
    var url = "http://127.0.0.1:8000/complete/";
    $.ajax({  
        url: url,
        type: 'GET',
        success: function(data) {
            if(data.status == 'success'){
                get_today_positions();
                var x = document.getElementById("green-toast-day");
                x.style.visibility = "visible";
                var audio = new Audio('static/OptionApp/media/notification.mp3');
                audio.play();
                setTimeout(function(){ 
                    x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                }, 4000);
                }
                else{
                    var x = document.getElementById("red-toast");
                    x.style.visibility = "visible";
                    setTimeout(function(){ 
                        x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
                    }, 4000);
                }
        },
        error: function(data) {
            console.log(data);
            var x = document.getElementById("red-toast");
            x.style.visibility = "visible";
            setTimeout(function(){ 
                x.style.visibility = x.style.visibility.replace("visible", "hidden"); 
            }, 4000);
        }
    });
}

// Websocket
function get_ltp(symbols,trade_data){
    // console.log("this is trade data", trade_data);
    // var ws =new  websocket('P502165', '094942383');
    // ws.connection();
    //   ws.on('connect', connectionOpen);
    //   function connectionOpen()
    //   {   
    //      ws.runScript(symbols, "mw");
    //   }
    // ws.on('tick', receiveTick);
    // function receiveTick(data)
    socket = new WebSocket('ws://127.0.0.1:8080/ws/tick/');
    socket.onopen = function(event){
        console.log("Connection open...");
    }
    socket.onmessage = function(event){
        var data = JSON.parse(event.data);
        data = data.data;
        var total_pnl = 0;
        for (var i = 0; i<data.length; i++){
            if('tk' in data[i]){
                var token = data[i]['tk'];
                var AStoken = 'AS'+token;
                var ABtoken = 'AB'+token;
                var CStoken = 'CS'+token;
                var CBtoken = 'CB'+token;
                if(token=='26000'){
                    document.getElementById('nifty-price').innerHTML = data[i]['ltp'];
                    document.getElementById('nifty-percentage-change').innerHTML = data[i]['change'];
                    continue;
                }
                else if(token=='26009'){
                    document.getElementById('banknifty-price').innerHTML = data[i]['ltp'];
                    document.getElementById('banknifty-percentage-change').innerHTML = data[i]['change'];
                    continue;
                }
                else{
                    //var price = data[i]['ltp'];
                    var Sltpid = 'ltp'+AStoken;
                    var Bltpid = 'ltp'+ABtoken;

                    var CSltpid = 'ltp'+CStoken;
                    var CBltpid = 'ltp'+CBtoken;

                    var Spnlid = 'pnl'+AStoken;
                    var Bpnlid = 'pnl'+ABtoken;

                    var Sperid = 'per'+AStoken;
                    var Bperid = 'per'+ABtoken;

                    var ltp = roundTo(parseFloat(data[i]['ltp']));

                    if((AStoken in trade_data) && (ABtoken in trade_data)){
                        var price = parseFloat(trade_data[AStoken]['price']);
                        var qty = parseInt(trade_data[AStoken]['quantity']);
                        var Spnl = (price*qty) - (ltp*qty);
                        var Sper = SellPercent(price,ltp)

                        var price = parseFloat(trade_data[ABtoken]['price']);
                        var qty = parseInt(trade_data[ABtoken]['quantity']);
                        var Bpnl = (ltp*qty) - (price*qty);
                        var Bper = BuyPercent(price,ltp)
                    }
                    else if((CStoken in trade_data) && (CBtoken in trade_data)){
                        var price = parseFloat(trade_data[CStoken]['price']);
                        var qty = parseInt(trade_data[CStoken]['quantity']);
                        var Spnl = (price*qty) - (ltp*qty);
                        var Sper = SellPercent(price,ltp)

                        var price = parseFloat(trade_data[CBtoken]['price']);
                        var qty = parseInt(trade_data[CBtoken]['quantity']);
                        var Bpnl = (ltp*qty) - (price*qty);
                        var Bper = BuyPercent(price,ltp)
                    }
                    else{
                        if(AStoken in trade_data){
                            var price = parseFloat(trade_data[AStoken]['price']);
                            var qty = parseInt(trade_data[AStoken]['quantity']);
                            var Spnl = (price*qty) - (ltp*qty);
                            var Sper = SellPercent(price,ltp)
                        }
                        else if(ABtoken in trade_data){
                            var price = parseFloat(trade_data[ABtoken]['price']);
                            var qty = parseInt(trade_data[ABtoken]['quantity']);
                            var Bpnl = (ltp*qty) - (price*qty);
                            var Bper = BuyPercent(price,ltp)
                        }
                        else if(CBtoken in trade_data){
                            var price = parseFloat(trade_data[CBtoken]['price']);
                            var qty = parseInt(trade_data[CBtoken]['quantity']);
                            var Bpnl = (ltp*qty) - (price*qty);
                            var Bper = BuyPercent(price,ltp)
                        }
                        else if(CStoken in trade_data){
                            var price = parseFloat(trade_data[CStoken]['price']);
                            var qty = parseInt(trade_data[CStoken]['quantity']);
                            var Bpnl = (ltp*qty) - (price*qty);
                            var Sper = BuyPercent(price,ltp)
                        }
                    }

                    if(document.getElementById(Sltpid)){
                        document.getElementById(Sltpid).innerHTML = data[i]['ltp'];
                        var Spnlhtml = document.getElementById(Spnlid);
                        var Sperhtml = document.getElementById(Sperid);
                        if(Spnl<0){
                            if(trade_data[AStoken]['status'] == 'Active'){
                                Spnlhtml.innerHTML = String(roundTo(Spnl));
                                if (isNaN(Sper)){
                                    Sperhtml.innerHTML = '0%';
                                }
                                else{
                                    Sperhtml.innerHTML = String(Sper)+'%';
                                }
                                Spnlhtml.className = '';
                                Sperhtml.className = '';
                                Spnlhtml.classList.add('red-pnl');
                                Sperhtml.classList.add('red-pnl');
                            }
                        }
                        else{
                            if(trade_data[AStoken]['status'] == 'Active'){
                                Spnlhtml.innerHTML = String(roundTo(Spnl));
                                if (isNaN(Sper)){
                                    Sperhtml.innerHTML = '0%';
                                }
                                else{
                                    Sperhtml.innerHTML = String(Sper)+'%';
                                }
                                Spnlhtml.className = '';
                                Sperhtml.className = '';
                                Spnlhtml.classList.add('green-pnl');
                                Sperhtml.classList.add('green-pnl');
                            }
                        } 
                    }
                    if(document.getElementById(Bltpid)){
                        document.getElementById(Bltpid).innerHTML = data[i]['ltp'];
                        var Bpnlhtml = document.getElementById(Bpnlid);
                        var Bperhtml = document.getElementById(Bperid);
                        if(Bpnl<0){
                            if(trade_data[ABtoken]['status'] == 'Active'){
                                Bpnlhtml.innerHTML = String(roundTo(Bpnl));
                                if (isNaN(Bper)){
                                    Bperhtml.innerHTML = '0%';
                                }
                                else{
                                    Bperhtml.innerHTML = String(Bper)+'%';
                                }
                                Bpnlhtml.className = '';
                                Bperhtml.className = '';
                                Bpnlhtml.classList.add('red-pnl');
                                Bperhtml.classList.add('red-pnl');
                            }
                        }
                        else{
                            if(trade_data[ABtoken]['status'] == 'Active'){
                                Bpnlhtml.innerHTML = String(roundTo(Bpnl));
                                if (isNaN(Bper)){
                                    Bperhtml.innerHTML = '0%';
                                }
                                else{
                                    Bperhtml.innerHTML = String(Bper)+'%';
                                }
                                Bpnlhtml.className = '';
                                Bperhtml.className = '';
                                Bpnlhtml.classList.add('green-pnl');
                                Bperhtml.classList.add('green-pnl');
                            }
                        } 
                    }

                    if(document.getElementById(CSltpid)){
                        document.getElementById(CSltpid).innerHTML = data[i]['ltp'];
                    }

                    if(document.getElementById(CBltpid)){
                        document.getElementById(CBltpid).innerHTML = data[i]['ltp'];
                    }

                    var total_pnl = 0;
                    Object.keys(trade_data).forEach(function(key) {
                        pnlId = 'pnl'+key;
                        total_pnl += parseFloat(document.getElementById(pnlId).innerHTML);
                    });
                    if (total_pnl<0){
                        document.getElementById('total-pnl').innerHTML = String(roundTo(total_pnl));
                        document.getElementById('total-pnl').className = '';
                        document.getElementById('total-pnl').classList.add('red-pnl');
                    }
                    else{
                        document.getElementById('total-pnl').innerHTML = String(roundTo(total_pnl));
                        document.getElementById('total-pnl').className = '';
                        document.getElementById('total-pnl').classList.add('green-pnl');
                    } 
                }
                
            }
        }
            

        if (data.length == 0){
            console.log('No data');
        
            }
    }
    socket.onerror = function(event){
        console.log("Websocket error ", event);
    }
    socket.onclose = function(event){
        console.log("Connection closed");
    }
}

function get_today_positions(){
    var url = "http://127.0.0.1:8000/all_positions/";
    $.ajax({  
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            try{
                data = JSON.parse(data.positions);
            }
            catch{
                console.log("Positions not found");
            }
            const tbody = document.getElementById('trdes-tbody');
            tbody.innerHTML = null;
            var trade_data = {}
            var ticker_tokens = "nse_cm|26000&nse_cm|26009";
            for(var i=0;i<data.length;i++){
                ticker_tokens = ticker_tokens+'&nse_fo|'+data[i]['token']
                if(data[i]['status']=='Active'){
                    var time_vals = data[i]['start_time'].split(' ')[1].split(':');
                    var final_time = time_vals[0]+':'+time_vals[1];
                    var half_quantity = data[i]['half_quantity']
                    if (half_quantity == ""){
                        var quantity = data[i]['quantity'];
                    }
                    else{
                        var quantity = data[i]['quantity'];
                        quantity = parseInt(quantity) - parseInt(half_quantity);
                    }
                    if(data[i]['order_type'].charAt(0)=='B'){
                        var order_type_class = 'buy-type';
                        var token = 'AB'+data[i]['token']
                        var ltp = 'ltp'+token
                        var pnl = 'pnl'+token
                        var per = 'per'+token
                        trade_data[token] = {
                            'quantity':String(quantity),
                            'price':data[i]['buy_price'],
                            'status':'Active',
                            'type':'Buy'
                        }
                    }
                    else{
                        var order_type_class = 'sell-type';
                        var token = 'AS'+data[i]['token']
                        var ltp = 'ltp'+token
                        var pnl = 'pnl'+token
                        var per = 'per'+token
                        trade_data[token] = {
                            'quantity':String(quantity),
                            'price':data[i]['sell_price'],
                            'status':'Active',
                            'type':'Sell'
                        }
                    }
                    var sl = data[i]['stoploss'].split('|');
                    var target = data[i]['target'].split('|');

                    tbody.innerHTML += `
                    <tr>
                        <td>`+final_time+`</td>
                        <td><span class='`+order_type_class+`'>`+data[i]['order_type']+`</span></td>
                        <td>`+data[i]['symbol']+`</td>
                        <td>`+quantity+`</td>
                        <td> <span class='open-status'>`+data[i]['status']+`</span></td>
                        <td id='`+token+`'>`+sl[0]+`<small>(`+sl[1]+`)</small></td>
                        <td>`+data[i]['buy_price']+`</td>
                        <td>`+data[i]['sell_price']+`</td>
                        <td>`+target[0]+`<small>(`+target[1]+`)</small></td>
                        <td id='`+ltp+`'>123.23</td>
                        <td class='' id='`+pnl+`'>123.23</td>
                        <td class='' id='`+per+`'>122.23%</td>
                        <td><span id='`+token+`' class='add-button' onclick='add_model_popup(this.id)'>Add</span></td>
                        <td><span id='`+token+`' class='exit-button' onclick='exit_model_popup(this.id)'>Exit</span></td>
                    </tr>
                    `
                }
                else{
                    var time_vals = data[i]['start_time'].split(' ')[1].split(':');
                    var final_time = time_vals[0]+':'+time_vals[1];
                    if(data[i]['order_type'].charAt(0)=='B'){
                        var order_type_class = 'buy-type-closed';
                        var token = 'CB'+data[i]['token']
                        var ltp = 'ltp'+token
                        var pnl = 'pnl'+token
                        var per = 'per'+token
                        
                        var buy_price = data[i]['buy_price'];
                        var full_exit_quantity = data[i]['full_exit_quantity']
                        if (full_exit_quantity == ""){
                            var quantity = data[i]['half_quantity'];
                            var sell_price = data[i]['half_exit_price'];
                        }
                        else{
                            var quantity = data[i]['full_exit_quantity'];
                            var sell_price = data[i]['sell_price'];
                        }
                        trade_data[token] = {
                            'quantity':String(quantity),
                            'price':data[i]['buy_price'],
                            'status':'Close',
                            'type':'Buy'
                        }
                        var pnl_amount = roundTo((parseFloat(sell_price) * parseInt(quantity)) - (parseFloat(buy_price)*parseInt(quantity)));
                        var per_amount = BuyPercent(parseFloat(buy_price), parseFloat(sell_price));
                        if (pnl_amount<0){
                            pnl_color_class = 'close-red-pnl';
                        }
                        else{
                            pnl_color_class = 'close-green-pnl';
                        }
                    }
                    else{
                        var order_type_class = 'sell-type-closed';
                        var token = 'CS'+data[i]['token']
                        var ltp = 'ltp'+token
                        var pnl = 'pnl'+token
                        var per = 'per'+token
                        
                        var sell_price = data[i]['sell_price'];
                        var full_exit_quantity = data[i]['full_exit_quantity']
                        if (full_exit_quantity == ""){
                            var quantity = data[i]['half_quantity'];
                            var buy_price = data[i]['half_exit_price'];
                        }
                        else{
                            var quantity = data[i]['full_exit_quantity'];
                            var buy_price = data[i]['buy_price'];
                        }
                        trade_data[token] = {
                            'quantity':String(quantity),
                            'price':data[i]['sell_price'],
                            'status':'Close',
                            'type':'Sell'
                        }
                        var pnl_amount = roundTo((parseFloat(sell_price)*parseInt(quantity)) - (parseFloat(buy_price)*parseInt(quantity)));
                        var per_amount = SellPercent(parseFloat(sell_price),parseFloat(buy_price));
                        if (pnl_amount<0){
                            pnl_color_class = 'close-red-pnl';
                        }
                        else{
                            pnl_color_class = 'close-green-pnl';
                        }
                    }
                    var sl = data[i]['stoploss'].split('|');
                    var target = data[i]['target'].split('|');
                    
                    tbody.innerHTML += `
                    <tr id='close-trades'>
                        <td>`+final_time+`</td>
                        <td> <span class='`+order_type_class+`'>`+data[i]['order_type']+`</span></td>
                        <td>`+data[i]['symbol']+`</td>
                        <td>`+quantity+`</td>
                        <td> <span class='close-status'>`+data[i]['status']+`</span></td>
                        <td id='`+token+`'>`+sl[0]+`<small>(`+sl[1]+`)</small></td>
                        <td>`+buy_price+`</td>
                        <td>`+sell_price+`</td>
                        <td>`+target[0]+`<small>(`+target[1]+`)</small></td>
                        <td id='`+ltp+`'>123.23</td>
                        <td class='`+pnl_color_class+`' id='`+pnl+`'>`+pnl_amount+`</td>
                        <td class='`+pnl_color_class+`' id='`+per+`'>`+per_amount+`%</td>
                        <td><span id='`+token+`' class='add-button' onclick='add_model_popup(this.id)'>Add</span></td>
                        <td><span id='`+token+`' class='exit-button' onclick='exit_model_popup(this.id)'>Exit</span></td>
                    </tr>
                    `
                }
            }
            tbody.innerHTML += `
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td><b>Total P&L</b></td>
                        <td><span id='total-pnl'>0.00</span></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    `
                   
            get_ltp(ticker_tokens,trade_data);
        },
        error: function(data) {
            console.log(data);
        }
    });
}

document.addEventListener("DOMContentLoaded", function(event) {
    get_today_positions();
    //get_ltp();
    var order_form = document.getElementById("order-form");
    // var buttone = document.getElementById("clickme");
    // buttone.addEventListener("click", function(event){
    //     event.preventDefault();
    //     document.getElementById("addModel").style.display = "block";
    // });

    order_form.addEventListener("submit", function(event){
        event.preventDefault();
        var expiry = document.querySelector('input[name="expiry"]:checked').value;
        var stoploss = document.querySelector('input[name="stoploss"]:checked').value;
        var target = document.querySelector('input[name="target"]:checked').value;
        var side = document.querySelector('input[name="side"]:checked').value;
        var strike = document.getElementById('strike-options').value;
        var quantity = document.getElementById('quantity').value;
        // Create objects
        if (strike != 'Select a Strike'){
            if(quantity != '0'){
                var order_data = {
                    'name':index_name,
                    'expiry':expiry,
                    'stoploss':stoploss,
                    'target':target,
                    'side':side,
                    'strike':strike,
                    'quantity':quantity,
                    'type':buy_sell
                }
                placeOrder(order_data)
            }
            else{
                alert('Please enter quantity');
            }
        }
        else{
            alert('Please select a strike')
        }
    });
});

window.addEventListener("click", function(event) {
    var addModel = document.getElementById("addModel")
    var exitModel = document.getElementById("exitModel")
        if (event.target == addModel) {
            addModel.style.display = "none";
        }
        if (event.target == exitModel) {
            exitModel.style.display = "none";
        }
    
});

