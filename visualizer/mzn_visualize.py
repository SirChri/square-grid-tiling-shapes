from cgitb import text
import sys, json, re, subprocess, os, shutil

solver = sys.argv[1]
mainfile = sys.argv[2]
inputfile = sys.argv[3]
out_filepath = sys.argv[4] if len(sys.argv) > 4 else None

if not out_filepath:
    out_filepath = os.path.join(sys.path[0], 'output.html')
else:
    shutil.copyfile(os.path.join(sys.path[0], 'static.css'), os.path.dirname(os.path.abspath(out_filepath))+"/static.css")

bashCommand = 'minizinc {} {} -O2 --solver {} --time-limit 300000 -p12 -f --output-mode json -s --soln-separator "" --search-complete-msg "OPTIMUM"'.format(mainfile, inputfile, solver)
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
jsondata = re.sub(r'^\%.*\n?|^\"\"|^\"OPTIMUM\"', '', output, flags=re.MULTILINE).strip()
statsdata = {}

if error:
    print("an error has eccurred: {}".format(error))
    exit(1)

optimum_found = False
for line in output.splitlines():
    if(line.strip() == '\"OPTIMUM\"'):
        optimum_found = True

    if(line.startswith("%%%mzn-stat: ")):
        line = line.replace("%%%mzn-stat: ", "")
        key = line.split("=")[0]
        val = line.split("=")[1]
        statsdata[key] = val

#output
vis_output = {}

#put some data into the output
vis_output["opt"] = optimum_found

## Input file read
textarea_input = ""
with open(inputfile, "r") as text_file:
    textarea_input += '<textarea disabled="disabled" class="input-textarea">'
    for x in text_file:
        if x.strip().replace(" ", "").startswith("n="):
            vis_output["n"] = re.findall('\d+', x)[0]
        elif x.strip().replace(" ", "").startswith("l="):
            vis_output["l"] = re.findall('\d+', x)[0]
        elif x.strip().replace(" ", "").startswith("r="):
            vis_output["r"] = re.findall('\d+', x)[0]
        elif x.strip().replace(" ", "").startswith("s="):
            vis_output["s"] = re.findall('\d+', x)[0]
        elif x.strip().replace(" ", "").startswith("f="):
            vis_output["f"] = re.findall('\d+', x)[0]
        textarea_input += x
    textarea_input += '</textarea>'

## Data handling
n = 0
div_items = ""

if jsondata != "=====UNKNOWN=====" and jsondata != "" and jsondata != "=====ERROR=====":
    data = json.loads(jsondata)
    vis_output["cost"] = data["obj"]
else:
    print(vis_output)
    exit(1)

## Time
vis_output["time"] = 0
stats = "<ul>"
for key in statsdata:
    if key == "flatTime" or key == "solveTime":
        vis_output["time"] += float(statsdata[key])
    value = statsdata[key]
    stats += "<li><b>"+key+"</b>: "+str(value)+"</li>"
stats += "<li>Optimum found: "+str(optimum_found)+"</li>"
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
with open(out_filepath, "w") as text_file:
    text_file.write(out_content)

print(vis_output)