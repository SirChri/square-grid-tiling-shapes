import $ from 'jquery';

const htmlTemplate = () => `
<form class="ui form">
<div class="field">
  <label>Grid dimension</label>
  <input id="grid-dimension" type="number" class="numfield" pattern="[0-9]*" name="n" placeholder="6">
</div>
<div class="three fields">
<div class="field">
  <label>Number of ls</label>
  <input type="number" class="numfield" pattern="[0-9]*" name="l" placeholder="5">
</div>
<div class="field">
  <label>Number of squares</label>
  <input type="number" class="numfield" pattern="[0-9]*" name="s" placeholder="5">
</div>
<div class="field">
  <label>Number of rectangles</label>
  <input type="number" class="numfield" pattern="[0-9]*" name="r" placeholder="5">
</div>
</div>
  <div class="ui error message">
    <div class="header">Error</div>
    <p>Placeholder for error message.</p>
  </div>
  <button class="ui button" type="submit">Submit</button>
  <button class="ui button" type="reset">Reset</button>
  <button class="ui button" type="dwinput">Download input</button>
</form>
`;

function download(filename, text) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);
  
	element.style.display = 'none';
	document.body.appendChild(element);
  
	element.click();
  
	document.body.removeChild(element);
  }

class Form {
	constructor() {
		this.mainElement = document.createElement('div');
		$(this.mainElement).html(htmlTemplate());
		this.listeners = {};
	}
	emit(method, payload = null) {
		const callback = this.listeners[method];
		if (typeof callback === 'function') {
			callback(payload);
		}
	}
	addEventListener(method, callback) {
		this.listeners[method] = callback;
	}
	removeEventListener(method) {
		delete this.listeners[method];
	}
	attach(containerElement) {
		$(containerElement).append(this.mainElement);
		// these settings should be here, if not they will not work because the DOM is not mounted
		$(this.mainElement).find('.error').hide();
		$(this.mainElement).find('button[type="submit"]').on("click", this.submit.bind(this));
		$(this.mainElement).find('button[type="reset"]').on("click", this.reset.bind(this));
		$(this.mainElement).find('button[type="dwinput"]').on("click", this.downloadinput.bind(this));
	}
	reset(event) {
		event.preventDefault();
		$(this.mainElement).find('form input').val("");
		if (this.listeners["reset"]) {
			this.emit("reset")
		}
	}
	downloadinput(event) {
		event.preventDefault();
		var forbiddenValuesRaw = this.forbiddenValues || {},
			forbiddenVals = [];

		for (const val in forbiddenValuesRaw) {
			forbiddenVals.push(forbiddenValuesRaw[val])
		}
		const data = {
			forbidden: forbiddenVals
		};
		$(this.mainElement).find('form').serializeArray().forEach((field) => {
			data[field.name] = field.value;
		});
		$(this.mainElement).find("form").addClass("loading");
		fetch('/api/download/input', {
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
			$(this.mainElement).find("form").removeClass("loading");
		}).catch((error) => {
			$(this.mainElement).find('form').addClass('error');
			$(this.mainElement).find("form").removeClass("loading");
			$(this.mainElement).find('form .message p').text(error.message);
			$(this.mainElement).find('form .message').show();
		});
	}
	submit(event) {
		event.preventDefault();
		var forbiddenValuesRaw = this.forbiddenValues || {},
			forbiddenVals = [];

		for (const val in forbiddenValuesRaw) {
			forbiddenVals.push(forbiddenValuesRaw[val])
		}
		const data = {
			forbidden: forbiddenVals
		};
		$(this.mainElement).find('form').serializeArray().forEach((field) => {
			data[field.name] = field.value;
		});
		$(this.mainElement).find("form").addClass("loading");
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
					if (this.listeners["submit"]) {
						this.emit("submit", data)
					}
					return data;
				});
			} else {
				if (this.listeners["submitErr"]) {
					this.emit("submitErr", response)
				}
				throw Error(response.statusText);
			}
		}).then((data) => {
			$(this.mainElement).find("form").removeClass("loading");
		}).catch((error) => {
			$(this.mainElement).find('form').addClass('error');
			$(this.mainElement).find("form").removeClass("loading");
			$(this.mainElement).find('form .message p').text(error.message);
			$(this.mainElement).find('form .message').show();
		});
	}
	onAfterSubmit() {

	}
}

export default Form;