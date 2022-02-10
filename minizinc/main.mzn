% Square (1 way):
%   a)
%       S11  S12
%       S13  S14
% 
% Rectangle (2 ways):
%   a) 
%       R11  R12  R13
%   b)
%       R21
%       R22
%       R23
%
% L (4 ways):
%   a)
%       L11
%       L12  L13
%   b)
%       L22  L21
%       L23
%   c)
%       L33  L32
%            L31
%   d)
%            L43
%       L41  L42
% 
% 

include "globals.mzn";

%% Input parameters
int: n;
int: f;
int: s;
int: r;
int: l;
enum CellValues = {XXX, EEE, S11, S12, S13, S14, R11, R12, R13, R21, R22, R23, 
                    L11, L12, L13, L21, L22, L23, L31, L32, L33, L41, L42, L43};
enum Coordinates = {X, Y};
array[1..f, Coordinates] of 1..n: forbidden;    %% List of forbidden cells of the form (forbidden[i][1], forbidden[i][2])

array[1..n, 1..n] of var CellValues: Board;     %% CSP target: assign cells to pieces
var 0..(n*n - f): obj;        %% COP objective function to be minimized: number of cells not assigned





%% Forbidden constraints:
%% 1) All Board cells in forbidden are made XXX
%% 2) Only Board cells in forbidden are made XXX
constraint % 1)
forall(i in 1..f) (
    Board[ forbidden[i, X], forbidden[i, Y] ] == XXX
);

constraint % 2)
count_eq(Board, XXX, f);



%% Number of tiles for each type
%% the domain limits the max number
var 0..s: n_squares;
var 0..r: n_rects;
var 0..l: n_ls;        
var 0..n*n: area;

%% Limit the number of (pieces of) squares to be exactly n_squares
constraint
forall(i in S11..S14) (
    count_eq(Board, i, n_squares)
);

%% Limit the number of (pieces of) rectangles to be exactly n_rectangles
constraint
count(Board, R11) + count(Board, R21) == n_rects /\
forall(i in R12..R13) ( count(Board, i) == count(Board, R11) ) /\
forall(i in R22..R23) ( count(Board, i) == count(Board, R21) );

%% Limit the number of (pieces of) ls to be exactly n_ls
constraint
sum(i in [L11, L21, L31, L41]) ( count(Board, i) ) == n_ls /\
forall(i in [L11, L21, L31, L41], j in 1..2) (
    count(Board, i+j) == count(Board, i)
);

constraint
area == 4*n_squares + 3*n_rects + 3*n_ls /\
obj == n*n - f - area;

constraint
count_eq(Board, EEE, obj);


%% Correct form constraints
constraint
forall(x, y in 1..n where Board[x, y] != XXX /\ Board[x, y] != EEE) (
    (Board[x, y] == S11 <->                 Square1(x, y)) /\
    (Board[x, y] == S12 <-> y>1 /\          Square1(x, y-1)) /\
    (Board[x, y] == S13 <-> x>1 /\          Square1(x-1, y)) /\
    (Board[x, y] == S14 <-> x>1 /\ y>1 /\   Square1(x-1, y-1)) /\

    (Board[x, y] == R11 <->                 Rect1(x, y)) /\
    (Board[x, y] == R12 <-> y>1 /\          Rect1(x, y-1)) /\
    (Board[x, y] == R13 <-> y>2 /\          Rect1(x, y-2)) /\

    (Board[x, y] == R21 <->                 Rect2(x, y)) /\
    (Board[x, y] == R22 <-> x>1 /\          Rect2(x-1, y)) /\
    (Board[x, y] == R23 <-> x>2 /\          Rect2(x-2, y)) /\

    (Board[x, y] == L11 <->                 LL1(x, y)) /\
    (Board[x, y] == L12 <-> x>1 /\          LL1(x-1, y)) /\
    (Board[x, y] == L13 <-> x>1 /\ y>1 /\   LL1(x-1, y-1)) /\

    (Board[x, y] == L21 <->                 LL2(x, y)) /\
    (Board[x, y] == L22 <-> y<n /\          LL2(x, y+1)) /\
    (Board[x, y] == L23 <-> x>1 /\ y<n /\   LL2(x-1, y+1)) /\

    (Board[x, y] == L31 <->                 LL3(x, y)) /\
    (Board[x, y] == L32 <-> x<n /\          LL3(x+1, y)) /\
    (Board[x, y] == L33 <-> x<n /\ y<n /\   LL3(x+1, y+1)) /\

    (Board[x, y] == L41 <->                 LL4(x, y)) /\
    (Board[x, y] == L42 <-> y>1 /\          LL4(x, y-1)) /\
    (Board[x, y] == L43 <-> x<n /\ y>1 /\   LL4(x+1, y-1))
);



%% Optimize
solve :: seq_search([
	int_search(Board, first_fail, indomain_random, complete)
])
minimize obj;


%% Output
output ["Solution found has \(obj) empty cells\n\n"] ++
        [show(Board[x, y]) ++ if y==n then "\n" else "  " endif | x, y in 1..n];

%% Helper predicates
predicate Square1(var int: x, var int: y) = (
    x<n /\ y<n /\
    Board[x, y]     == S11 /\ Board[x, y+1]     == S12 /\
    Board[x+1, y]   == S13 /\ Board[x+1, y+1]   == S14
);

predicate Rect1(var int: x, var int: y) = (
    y<=n-2 /\
    Board[x, y] == R11 /\ Board[x, y+1] == R12 /\ Board[x, y+2] == R13
);


predicate Rect2(var int: x, var int: y) = (
    x<=n-2 /\
    Board[x, y]     == R21 /\ 
    Board[x+1, y]   == R22 /\ 
    Board[x+2, y]   == R23
);

predicate LL1(var int: x, var int: y) = (
    x<n /\ y<n /\
    Board[x, y]     == L11 /\
    Board[x+1, y]   == L12 /\ Board[x+1, y+1] == L13
);

predicate LL2(var int: x, var int: y) = (
    x<n /\ y>1 /\
    Board[x, y-1]   == L22 /\ Board[x, y]     == L21 /\
    Board[x+1, y-1] == L23
);

predicate LL3(var int: x, var int: y) = (
    x>1 /\ y>1 /\
    Board[x-1, y-1] == L33 /\   Board[x-1, y]   == L32 /\ 
                                Board[x, y]     == L31
);

predicate LL4(var int: x, var int: y) = (
    x>1 /\ y<n /\
                            Board[x-1, y+1] == L43 /\
    Board[x, y] == L41 /\   Board[x, y+1]   == L42
);
