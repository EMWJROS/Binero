# Binero
![A binero](https://github.com/EMWJROS/Binero/blob/main/Binero.png)

The squares are to be filled with zeros and ones. Each row and column shall contain the same number of ones and zeros. There must not be more than two zeros or ones in line, regardless of direction. Each column must be unique. The same holds for the rows.

## My solution

The following algorithm goes back to a sudoku-solving program that I wrote in 2005 when
I first heard of Sudoku. My original idea was only to use the `prune()` function (see below) but I quickly realised that this was not enough and I had to implement the `find_solitaries()` function that rapidly reduces the number of unknowns in the puzzle. I have since then adapted the solution to Kakkuro and Tec-to-nic puzzles and now to Binero.

## Algorithm

The code works by keeping track of the possible values of each square on the grid and
each row and column and iteratively combining the information in them.

`box` is an array where each element is a bitmap with one bit for the possibility of '0' and one bit for '1'. In total, each element can have three values: 1 (meaning the corresponding square holds a '0'), 2 (a '1') or 3 (both values are possible). (NB: 0 is not used.)

The restrictions on the number of ones and zeros in each row and column only allow for 34
possible rows and columns in an 8x8 solved Binero. `zone_values` is a list of binary strings that represent these 34 different combinations.

`row` and `col` are vectors of indices to `zone_values` showing which possibilities that
exist for the specific rows and columns. These are initialised to all possible values: 
[0, 1, ... 33].

The solution starts by transferring the information in `puzzle`, which is the given puzzle
in a more human-readable form, to `box`. Since now some squares have attained known values, all assignments for rows and columns are no longer possible. The `prune()` function updates `row` and `col` and discards row and column assignments that no longer are possible. (The name is borrowed from chess programming where you *prune* the tree of possible moves.)

The next step basically feedbacks the information from `row` and `col` into`box`. Firstly,
the `find_solitaries()` function checks whether any row or column now has only one possible assignment (a *solitary*). If it finds that, it updates `box` accordingly. Then it proceeds by aggregating all the information in e.g. one specific row. If it finds that all the possible assignments of that row require the second column to be a '1', it updates `box` accordingly, and similiarly for the columns.

This should now have reduced the number of unknown squares. The `prune()` and `find_solitaries()` functions are then repeated over and over again until no further improvement can be seen. If the number of unknowns is then 0, the puzzle is solved.
