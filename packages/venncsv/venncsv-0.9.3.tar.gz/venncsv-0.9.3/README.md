```
INSTALLATION

    $ pip3 install venncsv

HELP

    $ venncsv -h

USAGE

    $ venncsv [-h] [-V] [-v] [-y] [-n] [-o] [-q] [-A] [-O] [-X] [-M] [-W]

               x_csv y_csv

'$ venncsv x.csv y.csv' writes x_and_y.csv x_or_y.csv x_xor_y.csv x_minus_y.csv and y_minus_y.csv

Let's have two CSV files, say x.csv and y.csv. Each file contains a header plus zero or more rows.

File extensions must be underscore '.csv'. The two headers must be strictly equal.

Rows in input files are intended as two sets of strings, say x and y. No field splitting is done.

If we issue:

    $ venncsv -AOXMW x.csv y.csv

or simply:

    $ venncsv x.csv y.csv

then we generate five files, as follows:

    x_and_y.csv   = x & y, the intersection of x and y, the rows both in x and y
    x_or_y.csv    = x | y, the union of x and y, the rows in x or y or both
    x_xor_y.csv   = x ^ y, the exclusive union of x and y, the rows in x or y but not in both
    x_minus_y.csv = x - y, the difference between x and y, the rows in x but not in y
    y_minus_x.csv = y - x, the difference between y and x, the rows in y but not in x

                   ┌───────────┐
                   │ x - y     │
                 x │   ┌───────┼───┐
                   │   │ x & y │   │
                   └───┼───────┘   │ y
                       │     y - x │
                       └───────────┘

Sets x - y, x & y and y - x are the three wedges of the Venn diagram of sets x and y, and hence
the 'venncsv' name.

Output files can be selected by -A -O -X -M and -W flags, but if no such flag is given then all
five output files are written.

Trailing blanks in header and rows are stripped. Empty rows and duplicated rows are skipped.

Rows in output files are alphabetically sorted.

Input files can be prefixed by a path, but output files are always written in current directory.

Example:

    $ cat one.csv
    N
    4
    3
    2
    1
    $ cat two.csv
    N
    6
    5
    4
    3
    $ venncsv -vy one.csv two.csv
    4 rows <-- '/home/xxxx/one.csv'
    4 rows <-- '/home/xxxx/two.csv'
    2 rows --> '/home/xxxx/one_and_two.csv'
    6 rows --> '/home/xxxx/one_or_two.csv'
    4 rows --> '/home/xxxx/one_xor_two.csv'
    2 rows --> '/home/xxxx/one_minus_two.csv'
    2 rows --> '/home/xxxx/two_minus_one.csv'
    Open 2 input files and 5 output files for check and print or Quit? (o=open, q=quit) --> q
    $

POSITIONAL ARGUMENTS

  x_csv            1st input file
  y_csv            2nd input file

OPTIONAL ARGUMENTS

  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
  -v, --verbose    show what happens
  -y, --yes        overwrite existing output files (default: ask)
  -n, --no         don't overwrite existing output files (default: ask)
  -o, --open       at end open input and output files for check and print
                   (default: ask)
  -q, --quit       at end don't open input and output files for check and
                   print (default: ask)
  -A, --x-and-y    write x_and_y.csv = x.csv & y.csv
  -O, --x-or-y     write x_or_y.csv = x.csv | y.csv
  -X, --x-xor-y    write x_xor_y.csv = x.csv ^ y.csv
  -M, --x-minus-y  write x_minus_y.csv = x.csv - y.csv
  -W, --y-minus-x  write y_minus_x.csv = y.csv - x.csv
```
