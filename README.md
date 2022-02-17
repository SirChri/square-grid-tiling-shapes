# Square grid tiling with shapes
## Problem
Consider an x n chessboard (n is given in input). You have *l* "L" pieces, *s* "square" pieces, and *r* "rectangle" pieces (see figure, the size of the rectangle is 3 x 1, the square is 2 x 2, the biggest side of the "L" are of size 2). *l*, *s*, *r* are given in input. The goal is to fill the chessboard with the pieces in such a way to minimize the remaining free cells. The additional requirement is that some *f* cells of the chessboard are already occupied (this is also given in input). See the example in figure (grey cells are occupied/forbidden). 

![Problem definition](def1.png?raw=true)

## Input generator
The file `input_gen.py` is used to generate random instances of both minizinc and asp "methods".\\
It takes 6 int parameters as input:\\
>> `python input_gen.py q n l s r f`
where:\\
* `q`: is the number of istances that we would like to create randomly;
* `n`: is the board dimension
* `l`: number of 2x2 ls
* `s`: number of 2x2 squares
* `r`: number of 1X3 rectangles
* `f`: number of forbidden cells (chosen randomly)
The output files will then be saved in the `./inputs/` folder.

## Run all input instances
The script `run_tests.py` effectively runs all the instances for minizinc and asp through their respective visualizers.\\It doesn't take any parameter on input and stores the outputs files in the `./outputs/` folder.
