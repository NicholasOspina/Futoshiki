#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
import itertools


def create_var_matrix(futo_grid, dom):
    var_grid = []
    vars = []
    for x in range(len(futo_grid)):
        row = []

        for y in range(0, len(futo_grid[x]), 2):
            temp_dom = dom.copy()
            if futo_grid[x][y] != 0:
                # new_var.assign(futo_grid[x][y])
                temp_dom = [futo_grid[x][y]]

            new_var = Variable("V({},{})".format(x+1, y // 2 +1), temp_dom)

            vars.append(new_var)
            row.append(new_var)

        var_grid.append(row)
    return var_grid, vars


def create_ineq_cons(futo_grid, var_grid, dom, i, j):

    new_con_ineq = Constraint("C(ineq {}, {})".format(i + 1, j // 2 + 1),
                              [var_grid[i][j // 2],
                               var_grid[i][j // 2 + 1]])
    sat_tuples_ineq = []

    for t in itertools.product(dom, dom):
        if (futo_grid[i][j + 1] == "<" and t[0] < t[1]) or (
                futo_grid[i][j + 1] == ">" and t[0] > t[1]):
            sat_tuples_ineq.append(t)

    # add the inequality constraints
    new_con_ineq.add_satisfying_tuples(sat_tuples_ineq)

    return new_con_ineq


def futoshiki_csp_model_1(futo_grid):# A!=B A!=C B!=D etc...

    highest_num = len(futo_grid) # numbers from 1 to len
    dom = [x+1 for x in range(highest_num)]

    var_grid, vars = create_var_matrix(futo_grid, dom)
    #var grid and vars now has all variables

    cons = []
    for i in range(len(futo_grid)): # iterate through all to find

        for j in range(0, len(futo_grid[i]), 2):

            # create the ineq con and add it where neccessary
            if j != len(futo_grid[i]) - 1 and (futo_grid[i][j + 1] == '>' or futo_grid[i][j + 1] == '<'):

                ineq_con = create_ineq_cons(futo_grid, var_grid, dom, i, j)
                cons.append(ineq_con)

            for k in range(j+2, len(futo_grid[i]), 2):

                # for 1, get (1,2), (1,3), 1,4)
                # We have a new constraint and variable

                new_con_row = Constraint("C({}, {})".format(i + 1, j // 2 + 1), [var_grid[i][j // 2], var_grid[i][k // 2]])
                new_con_col = Constraint("C({}, {})".format(j // 2 + 1, i + 1), [var_grid[j // 2][i], var_grid[k // 2][i]])
                #at most one for inequality since only through row

                sat_tuples_row = []
                sat_tuples_col = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:

                        sat_tuples_row.append(t)
                        sat_tuples_col.append(t)

                # row constraints
                new_con_row.add_satisfying_tuples(sat_tuples_row)
                cons.append(new_con_row)

                # add the col constraints
                new_con_col.add_satisfying_tuples(sat_tuples_col)
                cons.append(new_con_col)



    csp = CSP("Futoshiki1", vars)
    for c in cons:
        csp.add_constraint(c)

    return csp, var_grid


def futoshiki_csp_model_2(futo_grid): # A!=B!=C!=D

    dom = [x + 1 for x in range(len(futo_grid))]
    var_grid, vars = create_var_matrix(futo_grid, dom)



    # add all variables in a row to a constraint, same for col
    # will have
    # then do a check so that they are not all equal to each other
    cons = []
    for i in range(len(futo_grid)):  # iterate through all to find

        var_row = []
        var_col = []
        for j in range(0, len(futo_grid[i]), 2):
            # create the ineq con and add it where neccessary
            if j != len(futo_grid[i]) - 1 and (futo_grid[i][j + 1] == '>' or futo_grid[i][j + 1] == '<'):

                ineq_con = create_ineq_cons(futo_grid, var_grid, dom, i, j)
                cons.append(ineq_con)

            var_row.append(var_grid[i][j//2])
            var_col.append(var_grid[j//2][i])
        # get new constraints with all vars of its row or col
        new_con_row = Constraint("C(Row {})".format(i + 1), var_row)
        new_con_col = Constraint("C(Col {})".format(i + 1), var_col)

        # create the sup tuples for the constraint
        sat_tuples_row = []
        sat_tuples_col = []

        all_combinations_row = [var.domain() for var in var_row]
        all_combinations_row = itertools.product(*all_combinations_row)

        all_combinations_col = [var.domain() for var in var_col]
        all_combinations_col = itertools.product(*all_combinations_col)

        for t in all_combinations_row:
            t_set = set(t)
            if len(t_set) == len(t):
                sat_tuples_row.append(t)
        for t in all_combinations_col:
            t_set = set(t)
            if len(t_set) == len(t):
                sat_tuples_col.append(t)

        # row constraints
        new_con_row.add_satisfying_tuples(sat_tuples_row)
        cons.append(new_con_row)

        # add the col constraints
        new_con_col.add_satisfying_tuples(sat_tuples_col)
        cons.append(new_con_col)

    csp = CSP("Futoshiki2", vars)
    for c in cons:
        csp.add_constraint(c)

    return csp, var_grid


