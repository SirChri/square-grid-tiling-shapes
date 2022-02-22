import os, subprocess, re, sys, json, ast

my_path = os.path.abspath(os.path.dirname(__file__))
parent_path = my_path + "/.."
inputs_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(parent_path, "./inputs")
outputs_path = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(parent_path, "./outputs")

rootDir = inputs_path

files = [file for file in next(os.walk(rootDir))[2] if file.endswith('.dzn') or file.endswith('.lp')]

print(outputs_path)
#create output dir if not exists
if len(files) > 0:  
    os.makedirs(outputs_path, exist_ok=True)

# useful to write output data times
with open(os.path.join(outputs_path, "./metadata.csv"), "w") as text_file: 
    #csv header 
    text_file.write("file,solver,n,l,s,r,f,time,cost,opt\n")      
    for file in files:
        filename, file_extension = os.path.splitext(file)
        input_num = re.findall('\d+', file)[0]
        print("running {}{}".format(filename,file_extension))
        if file_extension == ".dzn":
            #run first with gecode
            bashCommand = "python3 {0}/visualizer/mzn_visualize.py gecode {0}/main.mzn {4}/{1} {3}/mzn-gecode{2}.html".format(parent_path,file,input_num,outputs_path,inputs_path)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode('utf-8')
            out = ast.literal_eval(output)
            if "time" in out:
                text_file.write("{},minizinc-gecode,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
            else:
                text_file.write("{},minizinc-gecode,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],"-","-","-"))
                

            #run with chuffed
            # bashCommand = "python3 {0}/visualizer/mzn_visualize.py chuffed {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-chuffed{2}.html".format(parent_path,file,input_num)
            # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            # output, error = process.communicate()
            # print(output)

            #run first with gecode
            bashCommand = "python3 {0}/visualizer/mzn_visualize.py coin-bc {0}/main.mzn {4}/{1} {3}/mzn-coinbc{2}.html".format(parent_path,file,input_num,outputs_path,inputs_path)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode('utf-8')
            out = ast.literal_eval(output)
            if "time" in out:
                text_file.write("{},minizinc-coinbc,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
            else:
                text_file.write("{},minizinc-coinbc,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],"-","-","-"))

        elif file_extension == ".lp":
            try:
                bashCommand = "python3 {0}/visualizer/asp_visualize.py {0}/main.lp {4}/{1} {3}/asp{2}.html".format(parent_path,file,input_num,outputs_path,inputs_path)
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                output = output.decode('utf-8')
                
                if not error:
                    out = ast.literal_eval(output)
                    text_file.write("{},clingo,{},{},{},{},{},{},{},{}\n".format(filename,out["n"],out["l"],out["s"],out["r"],out["f"],out["time"],out["cost"],out["opt"]))
            except:
                print("something went wrong with file {}".format(file))
        else:
            print("input file {} not recognized.".format(file))
