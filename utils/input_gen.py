import sys, os, random, glob, re

q = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])
s = int(sys.argv[4])
r = int(sys.argv[5])
f = int(sys.argv[6])
out_filepath = sys.argv[8] if len(sys.argv) > 8 else os.path.join(sys.path[0] +"/..", 'inputs')

#default for asp
lp_input_format = "lp"
lp_base_content = """#const n = {}.
#const l = {}.
#const s = {}.
#const r = {}.
#const f = {}.""".format(n,l,s,r,f)

#default for mzn
mzn_input_format = "dzn"
mzn_base_content = """n = {};
l = {};
s = {};
r = {};
f = {};""".format(n,l,s,r,f)

couples = [(i+1,j+1) for i in range(n) for j in range(n)]

#create input dir if not exists
os.makedirs(os.path.abspath(out_filepath), exist_ok=True)

#get current max input number of asp inputs (could either be for mzn)
current_inputs = glob.glob(out_filepath+"/*.{}".format(lp_input_format))
current_inputs = list(map(lambda x: int(re.findall('\d+', x)[0]), current_inputs))

current_max_input = 0
if current_inputs and len(current_inputs) > 0:
    current_max_input = max(current_inputs)

# create the same random instances for both lp and mzn inputs
for i in range(1+current_max_input,q+1+current_max_input):
    random.shuffle(couples)
    random_couples = couples[:f]

    #mzn
    out_content = mzn_base_content
    out_content += "\n"+"forbidden = ["
    for (j,l) in random_couples:
        out_content += "| {}, {}\n\t".format(j,l)
    out_content += "|];"
    
    with open(out_filepath+'/input{}.{}'.format(str(i), mzn_input_format), "w") as text_file:
        text_file.write(out_content)

    #lp
    out_content = lp_base_content
    for (j,l) in random_couples:
        out_content += "\n" + "val({}, {}, xxx).".format(j,l)
    
    with open(out_filepath+'/input{}.{}'.format(str(i), lp_input_format), "w") as text_file:
        text_file.write(out_content)