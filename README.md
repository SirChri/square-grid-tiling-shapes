# Square grid tiling with shapes
## Problem definition
Consider an n x n chessboard (n is given in input). You have *l* "L" pieces, *s* "square" pieces, and *r* "rectangle" pieces (see figure, the size of the rectangle is 3 x 1, the square is 2 x 2, the biggest side of the "L" are of size 2). *l*, *s*, *r* are given in input. The goal is to fill the chessboard with the pieces in such a way to minimize the remaining free cells. The additional requirement is that some *f* cells of the chessboard are already occupied (this is also given in input). See the example in figure (grey cells are occupied/forbidden). 

![Problem definition](relation/images/def1.png?raw=true)

## Solutions
The models that solve this problem are `main.lp` for ASP/clingo and `main.mzn` for minizinc.\
They are tested with:\
-  minizinc 2.5.5 (coin-bc 2.10.5/1.17.5 and gecode 6.3.0)
-  clingo 5.5.1

## Interactive solver
I wrote a node site that relies on [clingojs](https://github.com/dousto/clingojs) to give the user an interactive solver. Some can set up the node server in a few steps:
1. change the `routes/config.js` file with the exact paths
1. `npm install`
1. `npm start`
1. open your browser at `https://localhost:3000` and enjoy.

![Site solver](preview.gif?raw=true)

### Notes
Developed and tested with `node v17.7.2`.