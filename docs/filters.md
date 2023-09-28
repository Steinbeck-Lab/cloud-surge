
Surge has the facility to remove molecules which contain certain substructures using the
-B option. The argument of -B is a list of numbers separated by commas without spaces.
For example, -B2,3,8. Each number indicates a set of substructures that are forbidden.
You can use -B more than once, for example -B2,4,6 is the same as -B4 -B6,2. We
will describe the meaning of each number separately. In some cases it is necessary to
understand the distinction between rings and cycles, as explained in Section 5.
In the pictures, a circle represents any type of atom, a simple join matches any bond,
a double join matches a double or triple bond, and a triple join matches only a triple
bond. Many of the families below were inspired by MOLGEN [3].
-B1 Rings of length up to 7 have no triple bonds. This is equivalent to cycles of length
up to 7 having no triple bonds.
-B2 Consider rings of length r and s which share one bond (i.e. fused rings). Let e be
the common bond and let f be any bond belonging to one of the rings and sharing
exactly one atom with e. In the cases {r, s} = {3, 3}, {3, 4} and {3, 5}, both e and
f must be single bonds. In the cases {r, s} = {3, 6}, {4, 4} and {4, 5}, f must be a
8
single bond.
-B3 Consider rings of length r and s which share two bonds. Let e be one of the shared
bonds and let f be a bond belonging to one of the rings and sharing exactly one
atom with e. In the cases {r, s} = {4, 4}, {4, 5}, {4, 6}, {5, 5} and {5, 6}, both e
and f must be single bonds.
-B4 Consider two rings of length 6 that share three bonds. Then any bond which lies in
one of the rings and has exactly one atom in the other ring must be a single bond.
-B5 No atom has two double or triple bonds unless it is also bonded to some other
non-hydrogen atom.
9
-B6 No atom in a ring of length up to 8 has two double bonds unless it is also bonded
to some other non-hydrogen atom.
-B7 These are forbidden: two atoms with four common neighbours, and three atoms
with three common neighbours.
-B8 These are forbidden: a cycle of length 5 having an atom bonded to each of the other
4 atoms, a set of 4 atoms all bonded to each other sharing one bond with a cycle of
length 4.
-B9 Every atom lies on at most one ring of length 3 or 4. Equivalently, every atom lies
on at most one cycle of length 3 or 4.