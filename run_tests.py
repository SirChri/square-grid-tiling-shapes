import os, subprocess, re, sys, json, ast

my_path = os.path.abspath(os.path.dirname(__file__))
rootDir = os.path.join(my_path, "./inputs")

files = [os.path.relpath(os.path.join(dirpath, file), rootDir) for (dirpath, dirnames, filenames) in os.walk(rootDir) for file in filenames]

#create output dir if not exists
if len(files) > 0:  
    if not os.path.exists(os.path.join(sys.path[0], 'outputs')):
        os.mkdir(os.path.join(sys.path[0], 'outputs'))

# useful to write output data times
with open(os.path.join(my_path, "./outputs/metadata.csv"), "w") as text_file: 
    #csv header 
    text_file.write("file,solver,n,l,s,r,f,time,cost,opt\n")      
    for file in files:
        filename, file_extension = os.path.splitext(file)
        input_num = re.findall('\d+', file)[0]
        print("running {}{}".format(filename,file_extension))
        if file_extension == ".dzn":
            #run first with gecode
            bashCommand = "python {0}/visualizer/mzn_visualize.py gecode {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-gecode{2}.html".format(my_path,file,input_num)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            out = ast.literal_eval(output)
            if out.has_key("time"):
                text_file.write("{},minizinc-gecode,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
            else:
                text_file.write("{},minizinc-gecode,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],"-","-","-"))
                

            #run with chuffed
            # bashCommand = "python {0}/visualizer/mzn_visualize.py chuffed {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-chuffed{2}.html".format(my_path,file,input_num)
            # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            # output, error = process.communicate()
            # print(output)
            #run first with gecode
            bashCommand = "python {0}/visualizer/mzn_visualize.py coin-bc {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-coinbc{2}.html".format(my_path,file,input_num)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            out = ast.literal_eval(output)
            if out.has_key("time"):
                text_file.write("{},minizinc-coinbc,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
            else:
                text_file.write("{},minizinc-coinbc,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],"-","-","-"))

        elif file_extension == ".lp":
            bashCommand = "python {0}/visualizer/asp_visualize.py {0}/main.lp {0}/inputs/{1} {0}/outputs/asp{2}.html".format(my_path,file,input_num)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if not error:
                try:
                    out = ast.literal_eval(output)
                    text_file.write("{},clingo,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
                except:
                    print(output)
        else:
            print("input file {} not recognized.".format(file))
