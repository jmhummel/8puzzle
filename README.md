# 8puzzle
Python script for solving the classic "8-puzzle" game

This is a python script I developed for solving the tile sliding [8-puzzle game](https://en.wikipedia.org/wiki/15_puzzle).

## Capabilies

It has the option of using one of two heuristics: 

1. Manhatten ("taxi-cab") distance

2. Number of misplaced tiles.

It can also print the output in one of two formats:

1. Each state, including begining, intermediate and ending states.

2. List of moves made, where `r`,`l`,`u`,`d` signify right, left, up, and down respectively. 
This is the direction an adjecent tile to the open space (`0`) is moved.

## Input format
Input files are plain text, written as two lines: the start state and goal state.
States are space-deliniated. They must include the numbers 0-8, where `0` represents the empty space, and `1`-`8` the 8 tiles of the puzzle.
Here is an example of a properly formated state: 

```
1 2 0 3 4 5 6 7 8
```

I have included two puzzle files in the repository. `puzzle02.txt` is very simple, requiring only two moves, while `puzzle20.txt` can solved in a minumum of twenty moves.

## How to run

`8puzzle.py` reads from standard input, and takes two mandatory arguements: the heuristic to be used, and the output format.

The hueristic arguement will either be `1` for manhatten distance or `2` for number of misplaced tiles.

The output argument will either be `0` for action sequence or `1` for states.

## Example 
Here is an example of solving `puzzle02.txt` using the manhatten distance heuristic and output format of states:

### Input (`puzzle02.txt`)

```
1 2 0 3 4 5 6 7 8
0 1 2 3 4 5 6 7 8
```

### Command line

```
python 8puzzle.py 1 1 < puzzle02.txt
```

### Output

```
1 2 0 3 4 5 6 7 8
1 0 2 3 4 5 6 7 8
0 1 2 3 4 5 6 7 8
```


