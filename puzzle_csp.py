#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = caged_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the FunPuzz puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. caged_csp_model (worth 25/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with FunPuzz cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(fpuzz_grid):
    ##IMPLEMENT
    n = fpuzz_grid[0][0]
    dom = []
    for i in range(n):
        dom.append(i + 1)

    vars = []
    for i in dom:
        vars_col = []
        for j in dom:
            vars_col.append(Variable("Cell{}{}".format(i, j), dom))
        vars.append(vars_col)

    sat_tup = []
    for t in itertools.permutations(dom, 2):
        sat_tup.append(t)

    cons = []
    for r in range(len(dom)):
        for c in range(len(dom)):
            for i in range(c+1, len(dom)):
                con = Constraint("{}, {}".format(vars[r][c].name, vars[r][i].name), [vars[r][c], vars[r][i]])
                con.add_satisfying_tuples(sat_tup)
                cons.append(con)
            for j in range(r+1, len(dom)):
                con = Constraint("{}, {}".format(vars[r][c].name, vars[j][c].name), [vars[r][c], vars[j][c]])
                con.add_satisfying_tuples(sat_tup)
                cons.append(con)

    vrb = []
    for v in vars:
        vrb += v

    csp = CSP("{}-binary_ne_grid".format(n), vrb)
    for c in cons:
        csp.add_constraint(c)
    return csp, vars


def nary_ad_grid(fpuzz_grid):
    ##IMPLEMENT 
    n = fpuzz_grid[0][0]
    dom = []
    for i in range(n):
        dom.append(i + 1)

    sat_tup = []
    for t in itertools.permutations(dom, len(dom)):
        sat_tup.append(t)

    vars = []
    cons = []
    for i in dom:
        vars_col = []
        for j in dom:
            vars_col.append(Variable("Cell{}{}".format(i, j), dom))
        con = Constraint("R{}".format(i), vars_col)
        con.add_satisfying_tuples(sat_tup)
        cons.append(con)
        vars.append(vars_col)

    for j in range(len(dom)):
        c = []
        for i in range(len(dom)):
            c.append(vars[i][j])
        con = Constraint("C{}".format(j+1), c)
        con.add_satisfying_tuples(sat_tup)
        cons.append(con)

    vrb = []
    for v in vars:
        vrb += v

    csp = CSP("{}ary_ad_grid".format(n), vrb)
    for con in cons:
        csp.add_constraint(con)
    return csp, vars


def split_digit(n, vrbs):
    n1 = n / 10
    n1 = int(n1)
    n2 = n % 10
    return vrbs[n1-1][n2-1]


def caged_csp_model(fpuzz_grid):
    ##IMPLEMENT
    n = fpuzz_grid[0][0]

    dom = []
    for i in range(n):
        dom.append(i + 1)

    csp, vars = nary_ad_grid(fpuzz_grid)

    for i in range(1, len(fpuzz_grid)):
        if len(fpuzz_grid[i]) == 2:
            v = split_digit(fpuzz_grid[i][0], vars)
            v.assign(fpuzz_grid[i][1])
        else:
            sat_tup = []
            vs = []
            ops = fpuzz_grid[i][-1]
            targ = fpuzz_grid[i][-2]
            for j in range(len(fpuzz_grid[i]) - 2):
                v = split_digit(fpuzz_grid[i][j], vars)
                vs.append(v)
            for t in itertools.product(dom, repeat=len(vs)):
                if ops == 0 and t not in sat_tup:
                    if sum(t) == targ:
                        for comb in itertools.permutations(t, len(t)):
                            if comb not in sat_tup:
                                sat_tup.append(comb)
                elif ops == 1 and t not in sat_tup:
                    res = t[0]
                    for num in range(1, len(t)):
                        res -= t[num]
                    if res == targ:
                        for comb in itertools.permutations(t, len(t)):
                            if comb not in sat_tup:
                                sat_tup.append(comb)
                elif ops == 2 and t not in sat_tup:
                    res = t[0]
                    for num in range(1, len(t)):
                        res /= t[num]
                    if res == targ:
                        for comb in itertools.permutations(t, len(t)):
                            if comb not in sat_tup:
                                sat_tup.append(comb)
                elif ops == 3 and t not in sat_tup:
                    res = t[0]
                    for num in range(1, len(t)):
                        res *= t[num]
                    if res == targ:
                        for comb in itertools.permutations(t, len(t)):
                            if comb not in sat_tup:
                                sat_tup.append(comb)

            con = Constraint("Cage{}".format(i), vs)
            con.add_satisfying_tuples(sat_tup)
            csp.add_constraint(con)

    return csp, vars


if __name__ == '__main__':

    csp, var_array = binary_ne_grid([[4]])
    for c in csp.get_all_cons():
        print(c)
