
if (!window.proto) {
	console.log("Proto not initialized");
} else {
	console.log("Proto initialized");
}

proto = {
	renderDefinition: function(defObject) {
		var text = "";

		// Parse over each definition
		for (var j = 0; j < defObject['defs'].length; j++) {
			var definition = defObject['defs'][j],
				meaning = "";

			meaning += "<span class='meaning-number'>" + (j + 1) + ".</span>";
			meaning += "<span class='meaning-meaning'>" + definition['glosses'].join('; ') + "</span>";

			text += "<div class='meaning-definition'>" + meaning + "</div>";
		}

		return; ext
	},

	/**
	 * Takes in a special furigana string in the format specified by the project
	 * at https://github.com/Doublevil/JmdictFurigana, then spits out html 
	 * that uses <ruby> tags to show the furigana of each kanji.
	 * @param  {String} furi Specially formatted furigana string.
	 * @return {String}      HTML of the rendered furigana.
	 */
	renderFuri: function(furi) {
			// Splits the string into data
		var parts    = furi.split("|"),
			// The kanji headword
			head     = parts[0],
			// The furigana parts with indices
			furigana = parts[2].split(";");

		// Turns the kanji and reading into
		// ruby html syntax
		var rubify = function(kanji, reading) {
			return "<ruby><rb>" + kanji + "</rb><rp>(</rp><rt>" + reading + "</rt><rp>)</rp></ruby>";
		};

		var furiReplace = [];
		// Iterate over the furigana and come up
		// with the replacements
		for (var i = 0; i < furigana.length; i++) {
			// Divides the indices and the reading
			parts = furigana[i].split(":");

			// Have more than one index
			if (parts[0].includes("-")) {
				var range = parts[0].split("-"),
					startIndex = parseInt(range[0]),
					endIndex = parseInt(range[1]);

				// Generate the indices array
				var indices = [];
				for (var j = startIndex; j <= endIndex; j++) {
					indices.push(j);
				}

				furiReplace.push({
					'indices': indices,
					'html': rubify(head.substring(startIndex, endIndex + 1),parts[1])
				});
			}
			// Just replaces one kanji
			else {
				var index = parseInt(parts[0]);
				furiReplace.push({
					'indices': [index],
					'html': rubify(head[index], parts[1])
				});
			}
		}


		// Makes the final string
		var html = "";
		// Iterate over the kanji reading
		for (var i = 0; i < head.length; i++) {
			var added = false;

			// Iterate over the replace array
			for (var j = 0; j < furiReplace.length; j++) {
				var indices = furiReplace[j]['indices'];
				// If we find this index in the replacement
				if (indices.indexOf(i) != -1) {
					html += furiReplace[j]['html'];
					i = indices[indices.length - 1];
					added = true;
					break;
				}
			}

			if (added) {
				continue;
			}

			html += head[i];
		}

		return html;
	},
	
	/**
	 * Renders information on a word to the DOM, prioritizing the most
	 * common reading. 
	 * @param  {String} defString     Definition string JSON as output by 
	 *                                proto's card builder.
	 * @param  {String} readingString Reading string JSON as output by proto's
	 *                                card builder.
	 * @return {None}               Just modifies the DOM; no return value.
	 */
	render: function(defString, readingString) {

	}
};





function switchStroke() {
	var head   = document.getElementById("head"),
		stroke = document.getElementById("stroke");

	if (head.style.display == "none") {
		stroke.style.display = "none";
		head.style.display = "block";
	} else {
		head.style.display = "none";
		stroke.style.display = "block";
	}
}