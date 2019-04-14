var changeButton = document.getElementById('change-button');

var hira = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわゐゑをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽやゆよ";

var rando = function() {
	return Math.floor(Math.random() * hira.length);
}
var update = function() {
	var text = "";
	for (var i = 0; i < 10; i++) {
		text += hira[rando()]
	}
	document.getElementById('prompt').innerHTML = text;
}

changeButton.onclick = update;
changeButton.touchstart = update;

update();