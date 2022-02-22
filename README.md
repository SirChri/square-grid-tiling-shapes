# Square grid tiling with shapes
## Problem definition
Consider an n x n chessboard (n is given in input). You have *l* "L" pieces, *s* "square" pieces, and *r* "rectangle" pieces (see figure, the size of the rectangle is 3 x 1, the square is 2 x 2, the biggest side of the "L" are of size 2). *l*, *s*, *r* are given in input. The goal is to fill the chessboard with the pieces in such a way to minimize the remaining free cells. The additional requirement is that some *f* cells of the chessboard are already occupied (this is also given in input). See the example in figure (grey cells are occupied/forbidden). 

![Problem definition](relation/images/def1.png?raw=true)

## Solutions
The models that solve this problem are `main.lp` for ASP/clingo and `main.mzn` for minizinc.\
They are tested with:\
-  minizinc 2.5.5 (coin-bc 2.10.5/1.17.5 and gecode 6.3.0)
-  clingo 5.5.1

## Visualizers
Both ested with python 3.10.2.\

### Minizinc visualizer
You can view the output formatted as HTML running the `./visualizer/mzn_visualizer.py` with takes the following parameters:
* `solver`: one of `gecode` or `coinbc`;
* `main_file`: the `main.mzn` file;
* `input_file`: the `input.dzn` file;
* `output_file` (OPT): the html file where the output will be written (e.g. `./outputs/out1.html`). If not specified, the output will be saved in `./visualizer/output.html`.
### ASP visualizer
You can view the output formatted as HTML running the `./visualizer/asp_visualizer.py` with takes the following parameters:
* `main_file`: the `main.lp` file;
* `input_file`: the `input.lp` file;
* `output_file` (OPT): the html file where the output will be written (e.g. `./outputs/out1.html`). If not specified, the output will be saved in `./visualizer/output.html`. 

## Utils
Both tested with python 3.10.2.
### Input generator
The file `utils/input_gen.py` is used to generate random instances of both minizinc and asp "methods".\
It takes 6 int parameters as input:\
>> `python3 utils/input_gen.py q n l s r f output_path`
where:\\
* `q`: is the number of istances that we would like to create randomly;
* `n`: is the board dimension
* `l`: number of 2x2 ls
* `s`: number of 2x2 squares
* `r`: number of 1X3 rectangles
* `f`: number of forbidden cells (chosen randomly)
* `output_path` (OPT): relative or absoulte path of where the inputs will be generated. If not specified, the output will be `./inputs/` folder.
If the `output_path` folders don't exist, it will take care of creating them recursively;
### Run all input instances
The script `utils/run_tests.py` effectively runs all the instances for minizinc and asp through their respective visualizers.\
It takes two optional parameters:
* `input_path` (OPT): the folder where the inputs are located;
* `output_path` (OPT): the folder where the outputs (of the visualizers) will be saved;
If the `output_path` folders don't exist, it will take care of creating them recursively;

## Usage examples
Fast usage:
```bash
#create 2 instances
python3 ./utils/input_gen.py 2 8 10 10 10 5 ./inputs 
#run the visualizers/solvers
python3 ./utils/run_tests.py ./inputs ./outputs
```

Single usage:
```bash
#create 2 instances
python3 ./utils/input_gen.py 2 8 10 10 10 5 ./inputs 

#run only asp visualizer on one instance
python3 visualizer/asp_visualize.py main.lp inputs/inputi.lp outputs/asp1.html
```