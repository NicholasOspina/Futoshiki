# Futoshiki
Futoshiki game solver utilizing Forward Checking, Back Propagation, and Constraint Satisfaction

Given an input of a constraint satisfaction problem such as Futoshiki, find a solution for the board using either Forward Checking or a Constraint Satisfaction approach with Generalized Arc Constraint.

It was tested using the autotester.py and was able to successfully find the correct solution for a Futoshiki board and the N-Queens problem(as a baseline for constraint satisfaction).

# Futoshiki Solving
Utilized a CSP model, either a model with several binary constraints or one with 1 multi-variable constraint to brute force different solutions to the board, and then the Forward Checking and Generalized Arc Constraint algorithms would be able to use that solution set to determine if they are on the right track. 



