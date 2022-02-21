from cgitb import text
import sys, json, re, subprocess, os, shutil

inputfile = sys.argv[1]
out_filepath = sys.argv[2] if len(sys.argv) > 2 else None

if not out_filepath:
    out_filepath = os.path.join(sys.path[0], 'output.html')
else:
    shutil.copyfile(os.path.join(sys.path[0], 'static.css'), os.path.dirname(os.path.abspath(out_filepath))+"/static.css")

n = 50
div_items = ""

with open(inputfile, "r") as text_file:
    for x in text_file:
        cells = x.split(" ")

        for cell in cells:
            cell = cell.strip()
            if cell:
                general_cls = cell.lower()[0]
                div_items += '<div class="'+general_cls+' '+cell.lower()+'"></div>'

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