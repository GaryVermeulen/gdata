#
# 1st attempt at using Pyke with Simpleton
#

# Straight from examle
#
from pyke import knowledge_engine, krb_traceback, goal

# Compile and load .krb files in same directory that I'm in (recursively).
engine = knowledge_engine.engine(__file__)

##fc_goal = goal.compile('family.how_related($person1, $person2, $relationship)')
fc_goal = goal.compile('words.how_related($n1, $v1, $relationship)')

# Forward chaing test
#
def fc_test(person1 = 'Mary'):
    '''
        This function runs the forward-chaining example (fc_example.krb).
    '''
    engine.reset()      # Allows us to run tests multiple times.

    start_time = time.time()
    engine.activate('fc_example')  # Runs all applicable forward-chaining rules.
    fc_end_time = time.time()
    fc_time = fc_end_time - start_time

    print("doing proof...")
    with fc_goal.prove(engine, n1=n1) as gen:
        for vars, plan in gen:
            print("%s, %s are %s" % \
                    (n1, vars['v1'], vars['relationship']))
    prove_time = time.time() - fc_end_time
    print()
    print("done.")
    engine.print_stats()
    print("fc time %.2f, %.0f asserts/sec" % \
          (fc_time, engine.get_kb('nva').get_stats()[2] / fc_time))

