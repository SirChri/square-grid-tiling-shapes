import 'semantic-ui-css/semantic.css';
import 'semantic-ui-css/semantic';
import './style.css'
import Form from './form'
import page from 'page';

const container = document.querySelector(".solve-form");
const form = new Form();

page('/', index);
page('*', notfound);

function index() {
    $(container).empty();
    form.attach(container);

    $("#grid-dimension").on("input", function () {
        var n = this.value;
        form.forbiddenValues = {}

        $(".solution").empty();
        $(".solution").append(generateGrid(n, n));

        $(".solution .solgrid .selectable").on("click", function () {
            var cellData = $(this).data();
            var row = cellData.row
            var col = cellData.col
            var key = row+"_"+col;

            if (form.forbiddenValues[key]) {
                delete form.forbiddenValues[key];
                $(this).removeClass('selected');
            } else {
                form.forbiddenValues[key] = {
                    col: col,
                    row: row
                }
                $(this).addClass('selected');
            }
        });
    })
}
function generateGrid(rows, cols) {
    var grid = "<div class='solgrid' style='grid-template-rows: repeat(" + rows + ", 1fr); grid-template-columns: repeat(" + rows + ", 1fr);'>";
    for (let row = 1; row <= rows; row++) {
        for (let col = 1; col <= cols; col++) {
            grid += "<div class='selectable' data-row='" + row + "' data-col='" + col + "'></div>";
        }
    }
    return grid;
}

function notfound() {
    $(container).empty();
}

page.start();