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

#default for local search optimizer (https://github.com/vash96/optimization-challenges)
local_search_format = "txt"
local_search_base_content = "{}\n{} {} {} {}".format(n,s,r,l,f)

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

    #local_search
    out_content = local_search_base_content
    out_content += "\n"
    for (j,l) in random_couples:
        out_content += "{}, {}\n".format(j,l)
    
    with open(os.path.join(sys.path[0], 'inputs/input{}.{}'.format(str(i), local_search_format)), "w") as text_file:
        text_file.write(out_content)