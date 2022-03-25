import $ from 'jquery';

const htmlTemplate = () => `
<form class="ui form">
<div class="field">
  <label>Grid dimension</label>
  <input id="grid-dimension" type="number" class="numfield" pattern="[0-9]*" name="n" placeholder="6">
</div>
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
  <div class="ui error message">
    <div class="header">Error</div>
    <p>Placeholder for error message.</p>
  </div>
  <button class="ui button" type="submit">Submit</button>
</form>
`;
class Form {
    constructor() {
        this.mainElement = document.createElement('div');
        $(this.mainElement).html(htmlTemplate());
    }
    attach(containerElement) {
        $(containerElement).append(this.mainElement);
        // these settings should be here, if not they will not work because the DOM is not mounted
        $(this.mainElement).find('.error').hide();
        $(this.mainElement).find('button[type="submit"]').click(this.submit.bind(this));
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
        fetch('/api/solve', {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then((response) => {
            if (response.ok) {
                return response.json();
            } else
                throw Error(response.statusText);
        }).then((data) => {
            $(this.mainElement).find('form input').val("");
        }).catch((error) => {
            $(this.mainElement).find('form').addClass('error');
            $(this.mainElement).find('form .message p').text(error.message);
            $(this.mainElement).find('form .message').show();
        });
    }
}

export default Form;