var fixConjugation = function(id,string) {
	var conjugations = string.split(",");
	var total = ""
	var appendline = function(text) {
		total = total + text + ", ";
	}
	for (var i = 0; i < conjugations.length; i++) {
		if (i == conjugations.length-1) {
			total = total + conjugations[i];
		} else {
			total = total + conjugations[i] + ", ";
		}
	}
	var current = document.getElementById(id).innerHTML;
	document.getElementById(id).innerHTML = current + total;
}

fixConjugation('impf',"{{Imperfective_Conj}}");
fixConjugation('pf',"{{Perfective_Conj}}");