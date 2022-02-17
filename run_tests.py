import os, subprocess, re, sys

my_path = os.path.abspath(os.path.dirname(__file__))
rootDir = os.path.join(my_path, "./inputs")

files = [os.path.relpath(os.path.join(dirpath, file), rootDir) for (dirpath, dirnames, filenames) in os.walk(rootDir) for file in filenames]

#create output dir if not exists
if len(files) > 0:  
    if not os.path.exists(os.path.join(sys.path[0], 'outputs')):
        os.mkdir(os.path.join(sys.path[0], 'outputs'))

for file in files:
    filename, file_extension = os.path.splitext(file)
    input_num = re.findall('\d+', file)[0]
    print("running {}{}".format(filename,file_extension))
    if file_extension == ".dzn":
        #run first with gecode
        bashCommand = "python {0}/visualizer/mzn_visualize.py gecode {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-gecode{2}.html".format(my_path,file,input_num)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
        #run with chuffed
        # bashCommand = "python {0}/visualizer/mzn_visualize.py chuffed {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-chuffed{2}.html".format(my_path,file,input_num)
        # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        # output, error = process.communicate()
        # print(output)
        #run first with gecode
        bashCommand = "python {0}/visualizer/mzn_visualize.py coin-bc {0}/main.mzn {0}/inputs/{1} {0}/outputs/mzn-coinbc{2}.html".format(my_path,file,input_num)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
    elif file_extension == ".lp":
        bashCommand = "python {0}/visualizer/asp_visualize.py {0}/main.lp {0}/inputs/{1} {0}/outputs/asp{2}.html".format(my_path,file,input_num)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)
    else:
        print("input file {} not recognized.".format(file))
