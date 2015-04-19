//cookie nuskaitymo sprendimas pagal http://stackoverflow.com/a/5639455/552214
(function(){
    var cookies;

    function readCookie(name,c,C,i){
        if(cookies){ return cookies[name]; }

        c = document.cookie.split('; ');
        cookies = {};

        for(i=c.length-1; i>=0; i--){
           C = c[i].split('=');
           cookies[C[0]] = C[1];
        }

        return cookies[name];
    }

    window.readCookie = readCookie; // or expose it however you want
})();

function encode(text, key)
    {
        cipher = ""
        for (var i in text)
            cipher += String.fromCharCode(text[i].charCodeAt(0) + key);
        console.log(key)
        return cipher;
    }

function decode(cipher, key)
    {
        text = "";
        for (var i in cipher)
            text += String.fromCharCode(cipher[i].charCodeAt(0) - key);
        return text;
    }

function xmlhttpPost(strURL)
{
    var xmlHttpReq = false;
    if (window.XMLHttpRequest)
        xmlHttpReq = new XMLHttpRequest();
    else if (window.ActiveXObject)
        xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP")

    xmlHttpReq.open("POST", strURL, true);
    xmlHttpReq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlHttpReq.onreadystatechange = function()
    {
        if (xmlHttpReq.readyState == 4)
            updatepage(xmlHttpReq.responseText);
    }
    xmlHttpReq.send(getquerystring());
}

function getquerystring()
{
    var form = document.forms["f1"];
    var word = form.word.value;
    var qstr = "action=request&query=" + encode(word, parseInt(window.readCookie("key").replace(/"/g, ""))%26);
    return qstr;
}

function updatepage(str)
{
    document.getElementById("result").innerHTML = decode(str, parseInt(window.readCookie("key").replace(/"/g, ""))%26);
}