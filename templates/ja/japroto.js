
if (!window.proto) {
	window.proto = {
		meanings: {
			"MA": "martial arts term",
			"X": "rude or X-rated term (not displayed in educational software)",
			"abbr": "abbreviation",
			"adj-i": "i-adjective",
			"adj-ix": "i-adjective (yoi/ii class)",
			"adj-na": "na-adjective",
			"adj-no": "nouns which may take the genitive case particle `no'",
			"adj-pn": "pre-noun adjectival (rentaishi)",
			"adj-t": "`taru' adjective",
			"adj-f": "noun or verb acting prenominally",
			"adv": "adverb (fukushi)",
			"adv-to": "adverb taking the `to' particle",
			"arch": "archaism",
			"ateji": "ateji (phonetic) reading",
			"aux": "auxiliary",
			"aux-v": "auxiliary verb",
			"aux-adj": "auxiliary adjective",
			"Buddh": "Buddhist term",
			"chem": "chemistry term",
			"chn": "children's language",
			"col": "colloquialism",
			"comp": "computer terminology",
			"conj": "conjunction",
			"cop-da": "copula",
			"ctr": "counter",
			"derog": "derogatory",
			"eK": "exclusively kanji",
			"ek": "exclusively kana",
			"exp": "expressions (phrases, clauses, etc.)",
			"fam": "familiar language",
			"fem": "female term or language",
			"food": "food term",
			"geom": "geometry term",
			"gikun": "gikun (meaning as reading) or jukujikun (special kanji reading)",
			"hon": "honorific or respectful (sonkeigo) language",
			"hum": "humble (kenjougo) language",
			"iK": "word containing irregular kanji usage",
			"id": "idiomatic expression",
			"ik": "word containing irregular kana usage",
			"int": "interjection (kandoushi)",
			"io": "irregular okurigana usage",
			"iv": "irregular verb",
			"ling": "linguistics terminology",
			"m-sl": "manga slang",
			"male": "male term or language",
			"male-sl": "male slang",
			"math": "mathematics",
			"mil": "military",
			"n": "noun (common) (futsuumeishi)",
			"n-adv": "adverbial noun (fukushitekimeishi)",
			"n-suf": "noun, used as a suffix",
			"n-pref": "noun, used as a prefix",
			"n-t": "noun (temporal) (jisoumeishi)",
			"num": "numeric",
			"oK": "word containing out-dated kanji",
			"obs": "obsolete term",
			"obsc": "obscure term",
			"ok": "out-dated or obsolete kana usage",
			"oik": "old or irregular kana form",
			"on-mim": "onomatopoeic or mimetic word",
			"pn": "pronoun",
			"poet": "poetical term",
			"pol": "polite (teineigo) language",
			"pref": "prefix",
			"proverb": "proverb",
			"prt": "particle",
			"physics": "physics terminology",
			"rare": "rare",
			"sens": "sensitive",
			"sl": "slang",
			"suf": "suffix",
			"uK": "word usually written using kanji alone",
			"uk": "word usually written using kana alone",
			"unc": "unclassified",
			"yoji": "yojijukugo",
			"v1": "-ru verb",
			"v1-s": "-ru verb - kureru special class",
			"v2a-s": "Nidan verb with 'u' ending (archaic)",
			"v4h": "Yodan verb with `hu/fu' ending (archaic)",
			"v4r": "Yodan verb with `ru' ending (archaic)",
			"v5aru": "-u verb - -aru special class",
			"v5b": "-u verb with `bu' ending",
			"v5g": "-u verb with `gu' ending",
			"v5k": "-u verb with `ku' ending",
			"v5k-s": "-u verb - Iku/Yuku special class",
			"v5m": "-u verb with `mu' ending",
			"v5n": "-u verb with `nu' ending",
			"v5r": "-u verb with `ru' ending",
			"v5r-i": "-u verb with `ru' ending (irregular verb)",
			"v5s": "-u verb with `su' ending",
			"v5t": "-u verb with `tsu' ending",
			"v5u": "-u verb with `u' ending",
			"v5u-s": "-u verb with `u' ending (special class)",
			"v5uru": "-u verb - Uru old class verb (old form of Eru)",
			"vz": "-ru verb - zuru verb (alternative form of -jiru verbs)",
			"vi": "intransitive verb",
			"vk": "Kuru verb - special class",
			"vn": "irregular nu verb",
			"vr": "irregular ru verb, plain form ends with -ri",
			"vs": "noun or participle which takes the aux. verb suru",
			"vs-c": "su verb - precursor to the modern suru",
			"vs-s": "suru verb - special class",
			"vs-i": "suru verb - irregular",
			"kyb": "Kyoto-ben",
			"osb": "Osaka-ben",
			"ksb": "Kansai-ben",
			"ktb": "Kantou-ben",
			"tsb": "Tosa-ben",
			"thb": "Touhoku-ben",
			"tsug": "Tsugaru-ben",
			"kyu": "Kyuushuu-ben",
			"rkb": "Ryuukyuu-ben",
			"nab": "Nagano-ben",
			"hob": "Hokkaido-ben",
			"vt": "transitive verb",
			"vulg": "vulgar expression or word",
			"adj-kari": "`kari' adjective (archaic)",
			"adj-ku": "`ku' adjective (archaic)",
			"adj-shiku": "`shiku' adjective (archaic)",
			"adj-nari": "archaic/formal form of na-adjective",
			"n-pr": "proper noun",
			"v-unspec": "verb unspecified",
			"v4k": "Yodan verb with `ku' ending (archaic)",
			"v4g": "Yodan verb with `gu' ending (archaic)",
			"v4s": "Yodan verb with `su' ending (archaic)",
			"v4t": "Yodan verb with `tsu' ending (archaic)",
			"v4n": "Yodan verb with `nu' ending (archaic)",
			"v4b": "Yodan verb with `bu' ending (archaic)",
			"v4m": "Yodan verb with `mu' ending (archaic)",
			"v2k-k": "Nidan verb (upper class) with `ku' ending (archaic)",
			"v2g-k": "Nidan verb (upper class) with `gu' ending (archaic)",
			"v2t-k": "Nidan verb (upper class) with `tsu' ending (archaic)",
			"v2d-k": "Nidan verb (upper class) with `dzu' ending (archaic)",
			"v2h-k": "Nidan verb (upper class) with `hu/fu' ending (archaic)",
			"v2b-k": "Nidan verb (upper class) with `bu' ending (archaic)",
			"v2m-k": "Nidan verb (upper class) with `mu' ending (archaic)",
			"v2y-k": "Nidan verb (upper class) with `yu' ending (archaic)",
			"v2r-k": "Nidan verb (upper class) with `ru' ending (archaic)",
			"v2k-s": "Nidan verb (lower class) with `ku' ending (archaic)",
			"v2g-s": "Nidan verb (lower class) with `gu' ending (archaic)",
			"v2s-s": "Nidan verb (lower class) with `su' ending (archaic)",
			"v2z-s": "Nidan verb (lower class) with `zu' ending (archaic)",
			"v2t-s": "Nidan verb (lower class) with `tsu' ending (archaic)",
			"v2d-s": "Nidan verb (lower class) with `dzu' ending (archaic)",
			"v2n-s": "Nidan verb (lower class) with `nu' ending (archaic)",
			"v2h-s": "Nidan verb (lower class) with `hu/fu' ending (archaic)",
			"v2b-s": "Nidan verb (lower class) with `bu' ending (archaic)",
			"v2m-s": "Nidan verb (lower class) with `mu' ending (archaic)",
			"v2y-s": "Nidan verb (lower class) with `yu' ending (archaic)",
			"v2r-s": "Nidan verb (lower class) with `ru' ending (archaic)",
			"v2w-s": "Nidan verb (lower class) with `u' ending and `we' conjugation (archaic)",
			"archit": "architecture term",
			"astron": "astronomy, etc. term",
			"baseb": "baseball term",
			"biol": "biology term",
			"bot": "botany term",
			"bus": "business term",
			"econ": "economics term",
			"engr": "engineering term",
			"finc": "finance term",
			"geol": "geology, etc. term",
			"law": "law, etc. term",
			"mahj": "mahjong term",
			"med": "medicine, etc. term",
			"music": "music term",
			"Shinto": "Shinto term",
			"shogi": "shogi term",
			"sports": "sports term",
			"sumo": "sumo term",
			"zool": "zoology term",
			"joc": "jocular, humorous term",
			"anat": "anatomical term"
		},
		stripTag: function(tag) {
			return tag.substring(5,tag.length - 1);
		},
		renderDefinition: function(defObject) {
			var text = "";

			// Parse over each definition
			for (var j = 0; j < defObject['defs'].length; j++) {
				var definition = defObject['defs'][j],
					meaning = "";

				meaning += "<span class='meaning-number'>" + (j + 1) + ".</span>";
				meaning += "<span class='meaning-meaning'>" + definition['glosses'].join('; ');

				var posTags = definition['pos'],
					posTagMeanings = [];
				for (var i = 0; i < posTags.length; i++) {
					posTagMeanings.push(this.meanings[this.stripTag(posTags[i])]);
				}

				meaning += "<span class='meaning-info'>" + posTagMeanings.join(', ') + '</span>';


				meaning += "</span>";

				text += "<div class='meaning-definition'>" + meaning + "</div>";
			}

			for (var j = 0; j < defObject['readings'].length; j++) {
				var reading = defObject['readings'][j];
				text += "<a href='http://jisho.org/search/" + reading['kanji'] + "'>" + reading['kanji'] + "</a>【" + reading['kana'] + "】";
				// text += reading['kanji'] + "【" + reading['kana'] + "】";
			}

			return text;
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
		render: function(headword, defString, readingString) {
			if (readingString == '') {
				readingString = '[]';
			}

			var head     = document.getElementById("head"),
			    stroke   = document.getElementById("stroke"),
				def      = document.getElementById("def"),
				defs     = JSON.parse(defString),
				readings = JSON.parse(readingString),
				mainDef  = defs[0],
				mainReading = defs[0]['readings'][0];

			var found = false;
			// Look for the right pronunciation
			for (var i = 0; i < defs.length; i++) {
				var definition = defs[i];
				for (var j = 0; j < definition['readings'].length; j++) {
					var reading = definition['readings'][j];

					// If this matches the kanji headword
					if (reading['kanji'] == headword) {
						// Look for readings
						for (var k = 0; k < readings.length; k++) {
							var parts = readings[k].split('|');
							if (parts[0] == mainReading['kanji'] &&
								parts[1] == mainReading['kana']) {
								head.innerHTML = this.renderFuri(readings[k]);
								stroke.innerHTML = mainReading['kanji'];
								found = true;
								break;
							}
						}
					}
					else if ((reading['kana'] == headword) && 
							 (reading['kanji'] == '')) {
						head.innerHTML = headword;
						stroke.innerHTML = headword;
						found = true;
						break;
					}
					if (found) {
						break;
					}
				}

				if (found) {
					break;
				}
			}

			if (!found) {
				head.innerHTML = headword;
				stroke.innerHTML = headword;
			}
			

			var definitionHTML = "";
			for (var i = 0; i < defs.length; i++) {
				definitionHTML += this.renderDefinition(defs[i]);
			}
			def.innerHTML = definitionHTML;
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
}
