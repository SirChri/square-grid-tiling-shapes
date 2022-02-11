from cgitb import text
import sys, json, re, subprocess, os

mainfile = sys.argv[1]
inputfile = sys.argv[2]

bashCommand = 'minizinc {} {} -O2 --solver gecode --time-limit 300000 -p12 -f --output-mode json -s --soln-separator "" --search-complete-msg ""'.format(mainfile, inputfile)
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
jsondata = re.sub(r'^\%.*\n?', '', output, flags=re.MULTILINE).strip()[:-5]
statsdata = {}

for line in output.splitlines():
    if(line.startswith("%%%mzn-stat: ")):
        line = line.replace("%%%mzn-stat: ", "")
        key = line.split("=")[0]
        val = line.split("=")[1]
        statsdata[key] = val

data = json.loads(jsondata)


## Input file read
textarea_input = ""
with open(inputfile, "r") as text_file:
    textarea_input += '<textarea disabled="disabled" class="input-textarea">'
    for x in text_file:
        textarea_input += x
    textarea_input += '</textarea>'

## Data handling
n = 0
div_items = ""

## Time
stats = "<ul>"
for key in statsdata:
    value = statsdata[key]
    stats += "<li><b>"+key+"</b>: "+str(value)+" sec</li>"
stats += "</ul>"

for arr in data["Board"]:
    n = len(arr)
    for j in arr:
        val = j["e"]
        general_cls = val.lower()[0]
        div_items += '<div class="'+general_cls+' '+val.lower()+'"></div>'

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
                    """+stats+"""
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
with open(os.path.join(sys.path[0], 'main.html'), "w") as text_file:
    text_file.write(out_content)