import sys, os, random, glob, re

q = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])
s = int(sys.argv[4])
r = int(sys.argv[5])
f = int(sys.argv[6])

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
if not os.path.exists(os.path.join(sys.path[0], 'inputs')):
    os.mkdir(os.path.join(sys.path[0], 'inputs'))

#get current max input number of asp inputs (could either be for mzn)
current_inputs = glob.glob(os.path.join(sys.path[0], 'inputs')+"/*.{}".format(lp_input_format))
current_inputs = map(lambda x: int(re.findall('\d+', x)[0]), current_inputs)

current_max_input = 0
if current_inputs:
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
    
    with open(os.path.join(sys.path[0], 'inputs/input{}.{}'.format(str(i), mzn_input_format)), "w") as text_file:
        text_file.write(out_content)

    #lp
    out_content = lp_base_content
    for (j,l) in random_couples:
        out_content += "\n" + "val({}, {}, xxx).".format(j,l)
    
    with open(os.path.join(sys.path[0], 'inputs/input{}.{}'.format(str(i), lp_input_format)), "w") as text_file:
        text_file.write(out_content)