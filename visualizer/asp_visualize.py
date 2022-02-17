from cgitb import text
import sys, json, os
import subprocess
import shutil
    
class Cell:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val

mainfile = sys.argv[1]
inputfile = sys.argv[2]
out_filepath = sys.argv[3] if len(sys.argv) > 3 else None

if not out_filepath:
    out_filepath = os.path.join(sys.path[0], 'output.html')
else:
    shutil.copyfile(os.path.join(sys.path[0], 'static.css'), os.path.dirname(os.path.abspath(out_filepath))+"/static.css")

bashCommand = "clingo {} {} --parallel 10 --quiet=1 --out-hide-aux --outf=2 --time-limit=300 --warn none --configuration=frumpy".format(mainfile, inputfile)
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if error:
    print("an error has eccurred: {}".format(error))
    exit(1)

data = json.loads(output)

try: 

    ## Input file read
    textarea_input = ""
    with open(inputfile, "r") as text_file:
        textarea_input += '<textarea disabled="disabled" class="input-textarea">'
        for x in text_file:
            textarea_input += x
        textarea_input += '</textarea>'

    ## Data handling
    cells = {}
    n = 0
    div_items = ""
    div_info = "" #json.dumps(data)

    rawres = data["Result"]

    ## Time
    time = "<ul>"
    for key in data["Time"]:
        value = data["Time"][key]
        time += "<li><b>"+key+"</b>: "+str(value)+"</li>"
    time += "</ul>"

    ## Models
    models = "<ul>"
    for key in data["Models"]:
        value = data["Models"][key]
        models += "<li><b>"+key+"</b>: "+str(value)+"</li>"
    models += "</ul>"

    for rowval in data["Call"][0]["Witnesses"][0]["Value"]:
        aux = rowval.split("(")[1].split(")")[0]
        row = aux.split(",")[0]
        col = aux.split(",")[1]
        val = aux.split(",")[2]

        n = max(n, int(col))
        cells[row+"-"+col] = Cell(row,col,val)

    for i in range(1,n+1):
        for j in range(1,n+1):
            cell = cells[str(i)+"-"+str(j)]
            general_cls = cell.val.lower()[0]
            div_items += '<div class="'+general_cls+' '+cell.val.lower()+'"></div>'

    out_content = """
    <html>
        <head>
            <title>Output</title>
            <link rel="stylesheet" href="static.css">
            <style>
                .grid {
                display: grid; 

                grid-template-rows: repeat("""+str(n)+""", 1fr);
                grid-template-columns: repeat("""+str(n)+""", 1fr);
                
                gap: 0px;
                /*margin-top: 60px;*/
                height: 95%;
                }
            </style>
        </head>
        <body>
            <div class="body">
                <div class="split left">
                    <div class="program-instance">
                        <h2>Program instance</h2>
                        """+textarea_input+"""
                    </div>

                    <div class="sol-statistics">
                        <h2>Solution statistics</h2>
                        <h3>Time</h3>
                        """+time+"""
                        
                        <h3>Models</h3>
                        """+models+"""
                    </div>
                </div>
                <div class="split right">
                    <div class="grid">
                        """+div_items+"""
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    with open(out_filepath, "w") as text_file:
        text_file.write(out_content)
except:
    raise Exception('Something went wrong while searching the solution: '+json.dumps(data))