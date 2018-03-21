### Lattice File
*   Every line contain: a number, a tab, zero o more numbers separated by spaces.
*   Every number represent a Characteristic Set ID (from all_charsets.txt file)
*   Example: `0\t1 2\n` means that there are two edges: [0,1] and [0,2]
*   Example: `2\t\n` means that 2 is a leaf node.
*   Example: `7\t58 419 92\n` means that there are three edges: [7,58], [7,419], [7,92]

