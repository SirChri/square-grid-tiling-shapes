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

        $("#solution").empty();
        $("#solution").append(generateGrid(n, n));

        $("#solution .solgrid .selectable").on("click", function () {
            var cellData = $(this).data();
            var row = cellData.row
            var col = cellData.col
            var key = row + "_" + col;

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

    form.addEventListener("reset", function () {
        $("#solution").empty();
    })

    form.addEventListener("submit", function (data) {
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
    })
}
/**
 * 
 * @param {int} rows 
 * @param {int} cols 
 * @returns 
 */
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

function notfound() {
    $(container).empty();
}

page.start();