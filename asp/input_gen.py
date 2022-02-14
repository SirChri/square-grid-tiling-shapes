import sys, os, random

q = int(sys.argv[1])
n = int(sys.argv[2])
l = int(sys.argv[3])
s = int(sys.argv[4])
r = int(sys.argv[5])
f = int(sys.argv[6])

base_content = """#const n = {}.
#const l = {}.
#const s = {}.
#const r = {}.
#const f = {}.""".format(n,l,s,r,f)

couples = [(i+1,j+1) for i in range(n) for j in range(n)]

for i in range(1,q+1):
    random.shuffle(couples)
    random_couples = couples[:f]
    out_content = base_content
    for (j,l) in random_couples:
        out_content += "\n" + "val({}, {}, xxx).".format(j,l)
    with open(os.path.join(sys.path[0], 'inputs/input'+str(i)+'.lp'), "w") as text_file:
        text_file.write(out_content)