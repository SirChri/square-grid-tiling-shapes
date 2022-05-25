# Square grid tiling with shapes
## Problem definition
Consider an n x n chessboard (n is given in input). You have *l* "L" pieces, *s* "square" pieces, and *r* "rectangle" pieces (see figure, the size of the rectangle is 3 x 1, the square is 2 x 2, the biggest side of the "L" are of size 2). *l*, *s*, *r* are given in input. The goal is to fill the chessboard with the pieces in such a way to minimize the remaining free cells. The additional requirement is that some *f* cells of the chessboard are already occupied (this is also given in input). See the example in figure (grey cells are occupied/forbidden). 

![Problem definition](relation/images/def1.png?raw=true)

## Solutions
The models that solve this problem are `main.lp` for ASP/clingo and `main.mzn` for minizinc.\
They are tested with:
-  minizinc 2.5.5 (coin-bc 2.10.5/1.17.5 and gecode 6.3.0)
-  clingo 5.5.1

## Interactive solver
I wrote a node site that relies on [clingojs](https://github.com/dousto/clingojs) to give the user an interactive solver.

![Site solver](preview.gif?raw=true)

#### Requirements
In order to set up and run the tool you must have the following softwares (platform independant):
- [nodejs](https://nodejs.org/it/download/) tested with version >=v16.15.0
- [clingo](https://potassco.org/clingo/), tested with version >=5.4.0

On **windows** *clingo* is available [here (5.4.0)](https://github.com/potassco/clingo/releases/download/v5.4.0/clingo-5.4.0-win64.zip) (you can also check if there are newer versions directly on their github page), it is portable and does not require any install procedure, indeed you only have to unzip it. *Nodejs* is downloadable from their [site](https://nodejs.org/it/download/), I suggest to get the Windows installer (.msi) one and install it on your pc.\
On **macos** you can find them on homebrew. (`brew install node && brew install clingo`) \
On **ubuntu/linux** you should be able to find them directly on the official repository. (`sudo apt install gringo nodejs`)


#### Setup and run
- Edit the `routes/config.js` file according to your node/clingo setup/configuration.\
Below you can find a config example for every major operating system. You can choose from one of them:

```javascript
//WINDOWS
module.exports = {
    //it is important to escape backslashes 
    // clingo exe path
    clingo_path: "C:\\Users\\clondero\\Downloads\\clingo-5.4.0-win64\\clingo.exe",
    // main asp file
    main_file_path: "C:\\Users\\clondero\\Downloads\\square-grid-tiling-shapes-main\\main.lp" 
};
```
```javascript
// MAC OS
module.exports = {
    clingo_path: '/opt/homebrew/bin/clingo',
    main_file_path: '/Users/christian/Documents/Git/square-grid-tiling-shapes/main.lp'
};
```
```javascript
// LINUX/UBUNTU
module.exports = {
    clingo_path: '/usr/bin/clingo',
    main_file_path: '/Users/christian/Documents/Git/square-grid-tiling-shapes/main.lp'
};
```
- Open the terminal (or cmd/powershell on windows), position the command (`cd ...`) on the project root folder and run the following commands:
    - `npm install`
    - `npm start`
- open your browser at `http://localhost:3000` and enjoy.

### Notes
Developed and tested with `node v16.15.0` and `node v17.7.2`.\
Tested on Windows 10, Ubuntu 18.04 and macOS Monterey 12.3.1.
