import sys, json;

class Cell:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val

data = json.load(sys.stdin); 
cells = {}
n = 0

rawres = data["Result"]
nmodels = json.dumps(data["Models"])
time = json.dumps(data["Time"])
div_items = ""
div_info = json.dumps(data)

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


print("""<html>
<head>
<link rel="stylesheet" href="static.css">
</head>
<body>
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

<div class="body">
<div class="split left">
sdssdd
"""+div_info+"""
</div>
<div class="split right">
<div class="grid">
"""+div_items+"""
</div>
</div>
</div>
</body>
</html>""")