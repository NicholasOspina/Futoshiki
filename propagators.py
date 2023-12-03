#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''

    pruned = []
    # something was just assigned need to check all constraints
    if not newVar:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    for const in constraints:
        if const.get_n_unasgn() == 1:  # unassgn or total?
            
            curr_var = const.get_unasgn_vars()
            curr_var = curr_var[0]
            for value in curr_var.cur_domain():  # loop through all possible values
                curr_var.assign(value)  # assign value and check if works with new value
                # what are pruned variables
                #pruned = var.cur_domain().copy - value  # all pruned, only need to keep track of this var
                # want to prune everything that conflicts with assignment

                vals = []  # to hold things to be checked
                for var in const.get_scope():  # gets all variables
                    vals.append(var.get_assigned_value())
                if not const.check(vals):  # check if works
                    if (curr_var, value) not in pruned:
                        pruned.append((curr_var, value))
                        curr_var.prune_value(value)
                        do_prune = True
                curr_var.unassign()
            # check variables effected to see if DWO
            if curr_var.cur_domain_size() == 0:
                return False, pruned

    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    if not newVar:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    pruned = []
    queue = constraints.copy()

    while queue: # while there are still constraints, look to see if they satisfy
        curr_con = queue[0] #we have curr_con constraint
        queue.pop(0)  # pop item

        vars = curr_con.get_unasgn_vars()
        #go through all variables and its possible values, prune when needed
        for var in vars:

            for value in var.cur_domain():  # loop through all possible values
                if not curr_con.has_support(var, value):
                    if (var, value) not in pruned:
                        pruned.append((var, value))
                        queue.extend(csp.get_cons_with_var(var))  # queue
                        var.prune_value(value)

            if var.cur_domain_size() == 0:
                return False, pruned

    return True, pruned

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    minimum = (float('inf'), None)
    for var in vars:
        size = var.cur_domain_size()
        if minimum[0] > size:
            minimum = (size, var)
    return minimum[1]
