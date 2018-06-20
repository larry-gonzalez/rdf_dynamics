lattice.py
==========
*   Compute a lattice (of sets) with the subset relation
*   It returns only the direct subsets
*   It includes the emptyset as the top of the lattice
*   It does not include supremum of all sets as the bottom


Dependencies:
-------------
*   python2 or python3


How to use it:
--------------
*    python lattice.py input_file lattice_output performance_output


It assumes:
-----------
*   input_file must contain one list or set per line
*   the elements in those lists or sets must be numbers (recommended) or strings


Example
-------
*   One list per line
*   The elements in those lists are numbers
*   Each line is going to be evaluated in python (eval(line))
```
$ more example.txt
[1]
[2]
[3]
[4]
[1, 2]
[1, 3]
[1, 2, 3]
[1, 3, 4]
```


Execution
---------
$ python3.5 lattice.py example.txt out1.txt out2.txt


Output1
-------
*   each line represent an edge in the lattice (set tab set)
*   it includes only direct subsets (in the example there is non edge between {1} and {1,2,3})
*   it does not include edges to the supremum (there is no edge to {1,2,3,4})
```
$ more out1.txt
{}	{1}
{}	{2}
{}	{3}
{}	{4}
{1}	{1, 2}
{1}	{1, 3}
{2}	{1, 2}
{3}	{1, 3}
{4}	{1, 3, 4}
{1, 2}	{1, 2, 3}
{1, 3}	{1, 3, 4}
{1, 3}	{1, 2, 3}
```


Output2
-------
*   Tab separated file with three columns
*   First two columns: levels been compared at the time
*   A level *i* is the set of sets that have *i* elements
*   The sum of the third column is the total time spent
```
$ more out2.txt
1	0	7.867813110351562e-06
2	1	9.059906005859375e-06
2	0	2.1457672119140625e-06
3	2	6.9141387939453125e-06
3	1	7.3909759521484375e-06
3	0	1.6689300537109375e-06
$
```


Performance
-----------
*   It depends on the number of sets
*   It depends on the distribution of the number of elements of those sets
*   For 2,004,910 sets with 3,276 elements, it took 06:57:59 to compute a lattice
*   For 2,118,109 sets with 3,492 elements, it took 07:51:07
