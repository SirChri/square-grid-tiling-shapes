$(document).ready(function () {
	var form = {
		id: "#solve-form"
	};

	//utils
	function generateGrid(rows, cols, cells) {
		var grid = "<div class='solgrid' style='grid-template-rows: repeat(" + rows + ", 1fr); grid-template-columns: repeat(" + rows + ", 1fr);'>";
		if (!cells) {
			for (let row = 1; row <= rows; row++) {
				for (let col = 1; col <= cols; col++) {
					grid += "<div class='selectable' data-row='" + row + "' data-col='" + col + "'></div>";
				}
			}
		} else {
			grid += cells;
		}
		return grid;
	}

	function download(filename, text) {
		var element = document.createElement('a');
		element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
		element.setAttribute('download', filename);

		element.style.display = 'none';
		document.body.appendChild(element);

		element.click();

		document.body.removeChild(element);
	}

	function enableCellSelection(n) {
		if (n > 49 || n < 1) {
			return;
		}

		form.forbiddenValues = {}

		$("#solution").empty();
		$("#solution").append(generateGrid(n, n));

		function toggleCell(cell) {
			var cellData = $(cell).data();
			var row = cellData.row
			var col = cellData.col
			var key = row + "_" + col;

			if (form.forbiddenValues[key]) {
				delete form.forbiddenValues[key];
				$(cell).removeClass('selected');
			} else {
				form.forbiddenValues[key] = {
					col: col,
					row: row
				}
				$(cell).addClass('selected');
			}
		}

		var isMouseDown = false;
		$("#solution .solgrid .selectable").mousedown(function () {
			isMouseDown = true;
			toggleCell(this);
			return false; // prevent text selection
		}).mouseover(function () {
			if (isMouseDown) {
				toggleCell(this);
			}
		});

		$(document).mouseup(function () {
			isMouseDown = false;
		});
	}

	//on n change, update the grid
	$("#grid-dimension").on("input", function () {
		if (this.value)
			enableCellSelection(parseInt(this.value))
	})

	//reset btn
	$(form.id).find('button[type="reset"]').on("click", function (event) {
		event.preventDefault();
		$(form.id).find("input").val("");
		form.forbiddenValues = {}
		$("#solution").empty();
	});


	$(form.id).find('button[type="reset-form"]').on("click", function (event) {
		event.preventDefault();
		var n = $("#grid-dimension").val();

		if (n) {
			n = parseInt(n)
			$("#solution").empty();
			form.forbiddenValues = {}
			$("#solution").append(generateGrid(n, n));

			enableCellSelection(n)
		}
	});

	//submit btn
	$(form.id).find('button[type="submit"]').on("click", function (event) {
		$(form.id).form("validate form");
		if (!$(form.id).form("is valid")) {
			return;
		}
		event.preventDefault();
		var forbiddenValuesRaw = form.forbiddenValues || {},
			forbiddenVals = [];

		for (const val in forbiddenValuesRaw) {
			forbiddenVals.push(forbiddenValuesRaw[val])
		}
		const data = {
			forbidden: forbiddenVals
		};
		$(form.id).serializeArray().forEach((field) => {
			data[field.name] = field.value;
		});
		$(form.id).addClass("loading");
		fetch('/api/solve', {
			method: "POST",
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		}).then((response) => {
			if (response.ok) {
				const r = response.json().then((data) => {
					var opt = data.opt,
						cost = data.cost,
						model = data.model,
						n = $("#grid-dimension").val(),
						cells = {},
						htmlcontent = "";

					for (const cell of model) {
						var x = cell.x,
							y = cell.y,
							val = cell.val;

						cells[x + "-" + y] = val;
					}

					for (let i = 1; i <= n; i++) {
						for (let j = 1; j <= n; j++) {
							var cell = cells[i + "-" + j],
								generalCls = cell.toLowerCase()[0];

							htmlcontent += '<div class="' + generalCls + ' ' + cell.toLowerCase() + '"></div>'
						}
					}

					$("#solution").empty();
					$("#solution").append(generateGrid(n, n, htmlcontent))
				});
			} else {
				throw Error(response.statusText);
			}
		}).then((data) => {
			$(form.id).removeClass("loading");
		}).catch((error) => {
			$(form.id).addClass('error');
			$(form.id).removeClass("loading");
			$(form.id).find('.message p').text(error.message);
			$(form.id).find('.message').show();
		});
	});

	//download input
	$(form.id).find('button[type="dwinput"]').on("click", function (event) {
		$(form.id).form("validate form");
		if (!$(form.id).form("is valid")) {
			return;
		}
		event.preventDefault();
		var forbiddenValuesRaw = form.forbiddenValues || {},
			forbiddenVals = [];

		for (const val in forbiddenValuesRaw) {
			forbiddenVals.push(forbiddenValuesRaw[val])
		}
		const data = {
			forbidden: forbiddenVals
		};
		$(form.id).serializeArray().forEach((field) => {
			data[field.name] = field.value;
		});
		$(form.id).addClass("loading");
		fetch('/api/files/input', {
			method: "POST",
			headers: {
				'Accept': '*/*',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		}).then((response) => {
			if (response.ok) {
				response.text().then((data) => download("input.lp", data))
			} else {
				throw Error(response.statusText);
			}
		}).then((data) => {
			$(form.id).removeClass("loading");
		}).catch((error) => {
			$(form.id).addClass('error');
			$(form.id).removeClass("loading");
			$(form.id).find('.message p').text(error.message);
			$(form.id).find('.message').show();
		});
	});

	//form validation
	$(form.id).form({
		fields: {
			n: {
				identifier: 'n',
				rules: [
					{
						type: 'integer[1..49]',
						prompt: 'Please enter an integer value from 1 to 49'
					}
				]
			},
			l: {
				identifier: 'l',
				rules: [
					{
						type: 'empty',
						prompt: 'You must specify a value for <i>l</i>'
					},
					{
						type: 'integer',
						prompt: 'Please enter an integer value'
					}
				]
			},
			r: {
				identifier: 'r',
				rules: [
					{
						type: 'empty',
						prompt: 'You must specify a value for <i>r</i>'
					},
					{
						type: 'integer',
						prompt: 'Please enter an integer value'
					}
				]
			},
			s: {
				identifier: 's',
				rules: [
					{
						type: 'empty',
						prompt: 'You must specify a value for <i>s</i>'
					},
					{
						type: 'integer',
						prompt: 'Please enter an integer value'
					}
				]
			}
		}
	});
});