# -*- coding: utf-8 -*-
"""
    Modified version of: halal-bot.py
    By: Matt Kearns & Ahmed Youssef 

    For POC/testing

    MOD1: Save all variables and rules via List for later reuse via Load.
          Added Help and changed Exit.

    Usage Instructions:

	1. Teach [-R/-L] Var = String
	
		Teaches the system the type and value of a variable.
		
	2. Teach Var = [True/False]
	
		Teaches the system the truth value of the variable.
		
	3. Teach Expression -> Var
	
		Teaches the system a new rule.
		
	4. List
	
		Lists the values of all root and learned variables, and
		lists all of the current rules and learned rules in the
		system.
		MOD1: Save all variables and rules to files.
		
	5. Learn
	
		Creates new rules based on rules already supplied in the system
		and updates the truth values of the variables based on the rules.
		
	6. Query Expression
	
		Query returns the truth value of the expression based on all of 
		the current rules and variables in the system.
		
	7. Why Expression
	
		Why gives an explanation of why the user-supplied expression is true
		or false given the current rules and variable values held by the
		system.

	8. Exit
	
                Exits program.

        9. Load

                Loads any saved vaiables and rules from files--overwrites all variables and
                rules in memory, so maybe use List before Load. 

	Key:
	
	-R = root variable
	-L = learned variable
	Var = user-defined variable name
	String = A string of the form "Today is Monday" or "Matt likes ice cream"
	Expression = Any valid expression of the form A&B->C or (!((A|B))&C)->D

   
"""

usage = """\
    Teach [-R/-L] Var = String 
    Teach Var = [True/False] 
    Teach Expression -> Var 
    List 
    Learn 
    Query Expression 
    Why Expression
    Exit
    Load \
"""

fVars = "simpVars.txt"
fRules = "simpRules.txt"
fMode = "w"

from collections import OrderedDict

class Variable:

    def __init__(self, value, truth, root):
        self.value = value
        self.truth = truth
        self.root = root

    def get_value(self):
        return self.value

    def get_truth(self):
        return self.truth

    def get_root(self):
        return self.root

    def set_truth(self, truth):
        self.truth = truth

    def __str__(self):
        return "{ value = " + self.value + ", truth = " + str(self.truth) + ", root = " + str(self.root) + " }"

    def __repr__(self):
        return str(self)

class Rule:

    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def get_antecedent(self):
        return self.antecedent

    def get_consequent(self):
        return self.consequent

    def __str__(self):
        return str(self.antecedent) + " -> " + str(self.consequent)

    def __repr__(self):
        return str(self)


def valid_rule(antecedent, consequent, variables):

    antecedent = antecedent.replace("(", " ( ")
    antecedent = antecedent.replace(")", " ) ")
    antecedent = antecedent.replace("&", " AND ")
    antecedent = antecedent.replace("|", " OR ")
    antecedent = antecedent.replace("!", " NOT ")
    antecedent = antecedent.split()

    for a in antecedent:
        if a not in ["(", ")", "AND", "OR", "NOT"]:
            if a not in variables:
                return False

    if consequent not in variables or variables[consequent].get_root():
        return False

    return True

def reset_learned(variables): 

    for key in variables:
        if not variables[key].get_root():
            variables[key].set_truth(False)

def is_fact(var, variables):

    if var in variables and variables[var].get_truth():
        return True
    else:
        return False

def format_rule(antecedent, consequent, variables, rules):

    valid = query_exp(consequent, variables, rules)

    antecedent = antecedent.replace("(", " ( ")
    antecedent = antecedent.replace(")", " ) ")
    antecedent = antecedent.replace("&", " AND ")
    antecedent = antecedent.replace("|", " OR ")
    antecedent = antecedent.replace("!", " NOT ")

    antecedent = antecedent.split()

    for i in range(len(antecedent)):
        if antecedent[i] not in ["(", ")", "AND", "OR", "NOT"]:
            antecedent[i] = variables[antecedent[i]].get_value()

    if antecedent[0] == "NOT":
        new_ant = str(antecedent[0]) + " "
    else:
        new_ant = str(antecedent[0])

    for a in range(1, len(antecedent)):
        if antecedent[a] in ["AND", "OR"]:
            new_ant += " " + str(antecedent[a]) + " "
        elif antecedent[a] == "NOT":
            new_ant += str(antecedent[a]) + " "
        else:
            new_ant += str(antecedent[a])

    antecedent = new_ant

    if valid:
        return "BECAUSE " + antecedent + " I KNOW THAT " + variables[consequent].get_value()
    else:
        return "BECAUSE IT IS NOT TRUE THAT " + antecedent + " I CANNOT PROVE THAT " + variables[consequent].get_value()

def format_goal(goal, variables):

    goal = goal.replace("(", " ( ")
    goal = goal.replace(")", " ) ")
    goal = goal.replace("&", " AND ")
    goal = goal.replace("|", " OR ")
    goal = goal.replace("!", " NOT ")

    goal = goal.split()

    for i in range(len(goal)):
        if goal[i] not in ["(", ")", "AND", "OR", "NOT"]:
            goal[i] = variables[goal[i]].get_value()

    if goal[0] == "NOT":
        new_goal = str(goal[0]) + " "
    else:
        new_goal = str(goal[0])

    for g in range(1, len(goal)):
        if goal[g] in ["AND", "OR"]:
            new_goal += " " + str(goal[g]) + " "
        elif goal[g] == "NOT":
            new_goal += str(goal[g]) + " "
        else:
            new_goal += str(goal[g])

    return new_goal

def solve(expression, variables):

    expression = expression.replace('(', '( ')
    expression = expression.replace(')', ' )')
    expression = expression.replace('&', ' and ')
    expression = expression.replace('|', ' or ')
    expression = expression.replace('!', 'not ')

    expression_list = expression.split()

    for i in range(len(expression_list)):
        if expression_list[i] not in ['not', 'or', 'and', '(', ')']:
            expression_list[i] = variables[expression_list[i]].get_truth()

    expression = str(expression_list[0]) + " "

    for i in range(1, len(expression_list)):
        expression += str(expression_list[i]) + " "

    return eval(expression)

def query_exp(expression, variables, rules, why=False):

    expression = expression.replace('(', '( ')
    expression = expression.replace(')', ' )')
    expression = expression.replace('&', ' and ')
    expression = expression.replace('|', ' or ')
    expression = expression.replace('!', 'not ')

    expression_list = expression.split()

    for i in range(len(expression_list)):
        if expression_list[i] not in ['not', 'or', 'and', '(', ')']:

            found = False

            for rule in rules:

                if rule.get_consequent() == expression_list[i]:
                    found = True
                    expression_list[i] = query_exp(rule.get_antecedent(), variables, rules)

            if not found:
                expression_list[i] = variables[expression_list[i]].get_truth()

    expression = str(expression_list[0]) + " "

    for i in range(1, len(expression_list)):
        expression += str(expression_list[i]) + " "

    return eval(expression)   

def why_exp(expression, variables, rules, start=False):

    result = list()

    if start and query_exp(expression, variables, rules):
        reasoning = "I THUS KNOW THAT "
    elif start:
        reasoning = "THUS I CANNOT PROVE "

    temp = expression.replace('(', '( ')
    temp = temp.replace(')', ' )')
    temp = temp.replace('&', ' and ')
    temp = temp.replace('|', ' or ')
    temp = temp.replace('!', 'not ')

    exp_list = temp.split()

    print(exp_list)

    for i in range(len(exp_list)):
        if exp_list[i] not in ['&', '|', '!', '(', ')']:
            exp_list[i] = variables[exp_list[i]].get_value()

    for x in exp_list:
        reasoning += str(x)

    reasoning = reasoning.replace('(', ' ( ')
    reasoning = reasoning.replace(')', ' ) ')
    reasoning = reasoning.replace('&', ' AND ')
    reasoning = reasoning.replace('|', ' OR ')
    reasoning = reasoning.replace('!', ' NOT ')

    result.append(reasoning)

    count = 0
    addition, count = simplify(expression, variables, rules, count)

    result.extend(addition)

    return result, count

def determine_why(expression, variables, rules):

    valid = query_exp(expression, variables, rules)

    logic = list()

    logic.append(expression)

    done = False

    expression = expression.replace('(', ' ( ')
    expression = expression.replace(')', ' ) ')
    expression = expression.replace('&', ' & ')
    expression = expression.replace('|', ' | ')
    expression = expression.replace('!', ' ! ')

    exp_list = expression.split()

    while not done:

        done = True
        change = False

        for i in range(len(exp_list)):
            if exp_list[i] not in ['!', '|', '&', '(', ')'] and not variables[exp_list[i]].get_truth():
                for rule in rules:
                    if rule.get_consequent() == exp_list[i]:

                        exp_list[i] = rule.get_antecedent()

                        exp_list[i] = exp_list[i].replace('(', ' ( ')
                        exp_list[i] = exp_list[i].replace(')', ' ) ')
                        exp_list[i] = exp_list[i].replace('&', ' & ')
                        exp_list[i] = exp_list[i].replace('|', ' | ')
                        exp_list[i] = exp_list[i].replace('!', ' ! ')

                        exp_list[i] = exp_list[i].split()

                        exp_list = exp_list[:i] + exp_list[i] + exp_list[i+1:]
                        done = False
                        change = True
                        break
            if change:

                str_exp = str(exp_list[0])

                for i in range(1, len(exp_list)):
                    str_exp += str(exp_list[i])

                logic.append(str_exp)
                change = False

    return valid, logic


def get_diff(a, b):

    unique = ""

    a = a.replace('(', ' ( ')
    a = a.replace(')', ' ) ')
    a = a.replace('&', ' & ')
    a = a.replace('|', ' | ')
    a = a.replace('!', ' ! ')

    a = a.split()

    for i in a:
        if i not in b and i not in ['!', '|', '&', '(', ')']:
            unique = i

    return unique

if __name__ == "__main__":

    print("\n\t\tStart: Simpleton Expert System", end='\n\n')

    var_list = OrderedDict()
    rule_list = list()

    while True:

        teach_var = False
        set_root = False
        teach_rule = False
        list_knowledge = False
        learn = False
        query = False
        why = False
        myHelp = False
        myExit = False
        load_file = False
        index = None

        user_input = input("Enter command or Help: ").split('"')

        if user_input[0] == '': # Was exit now Help
            myHelp = True
            
        if user_input[0] == 'Exit':
            print("Exit\n")
            break

#        print(len(user_input))
#        print('\nuser_input: ' + str(user_input))
#        for ui in user_input:
#            print(ui)

        args = user_input[0].split()

#        print(len(args))
#        print('\nargs: ' + str(args))
#        for arg in args:
#            print(arg)

        if len(user_input) > 1:

            args.append(user_input[1])

            if len(args) != 5:
                continue

            teach_var = True

        if len(args) == 1:
            if args[0] == 'List':
                list_knowledge = True
            if args[0] == 'Learn':
                learn = True
            if args[0] == 'Help':
                myHelp = True
            if args[0] == 'Load':
                load_file = True

        if len(args) == 2:
            if args[0] == 'Query':
                query = True
            if args[0] == 'Why':
                why = True


        if not teach_var:

            for i in range(len(args)):

                if args[i] == '=':
                    set_root = True
                    index = i
                if args[i] == '->':
                    teach_rule = True
                    index = i
#                    print('teach_rule set true')

        if teach_var:

            var_defined = False

            for key in var_list:
                if key == args[2]:
                    print("\nVariable already defined.")
                    var_defined = True

            if var_defined:
                continue

            if args[1] == '-R':
                var_list[args[2]] = Variable(args[4], False, True)
            else:
                var_list[args[2]] = Variable(args[4], False, False)

        elif set_root:

            if args[1] not in var_list:
                print("\nVariable not defined.")
                continue

            if var_list[args[1]].get_root():
                if args[3] == 'true':
                    var_list[args[1]].set_truth(True)
                    reset_learned(var_list)
                elif args[3] == 'false':
                    var_list[args[1]].set_truth(False)
                    reset_learned(var_list)
                else:
                    print("\nInvalid assignment. Assign 'true' or 'false.'")
            else:
                print("\n" + str(args[1]) + " is not a root variable.")

        elif teach_rule:

            print('-In teach_rule...')

            antecedent = args[1]
            consequent = args[-1]

            if valid_rule(antecedent, consequent, var_list):
                rule_list.append(Rule(antecedent, consequent))
            else:
                print("Invalid rule use form: A&B -> C")
                continue

        elif list_knowledge:

            fMode = 'w'

            fv = open(fVars, fMode)

            print("\nWriting len(var_list) vars to file: " + str(len(var_list)))
            for var in var_list:
                print("var_list[var]: " + var + " ; value: " + var_list[var].get_value() + " ; truth: " + str(var_list[var].get_truth()) + " ; root: " + str(var_list[var].get_root()))
                fv.write(str(var) + ";" + str(var_list[var].get_value()) + ";" + str(var_list[var].get_truth()) + ";" + str(var_list[var].get_root()) +"\n")

            fv.close()

            fr = open(fRules, fMode)

            print("Writing len(rule_list) rules to file: " + str(len(rule_list)))
            for rule in rule_list:
                print("rule: antecedent: " + rule.get_antecedent() + " ; consequent: " + rule.get_consequent())
                fr.write(str(rule.get_antecedent()) + ";" + str(rule.get_consequent()) + "\n")    

            fr.close()
            
            print("\nRoot Variables:")
#            f.write("Root Variables:\n")
            for key in var_list:
                if var_list[key].get_root():
                    print("\t" + key + " = " + '"' + var_list[key].get_value() + '"')
#                    f.write("\t" + key + " = " + '"' + var_list[key].get_value() + '"\n')
            print("\nLearned Variables:")
#            f.write("Learned Variables:\n")
            for key in var_list:
                if not var_list[key].get_root():
                    print("\t" + key + " = " + '"' + var_list[key].get_value() + '"')
#                    f.write("\t" + key + " = " + '"' + var_list[key].get_value() + '"\n')
            print("\nFacts:")
#            f.write("Facts:\n")
            for key in var_list:
                if var_list[key].get_truth():
                    print("\t" + key)
#                    f.write("\t" + key + "\n")

            print("\nRules:")
#            f.write("Rules:\n")
            for rule in rule_list:
                print("\t" + rule.__str__())
#                f.write("\t" + rule.__str__() + "\n")
                
#            f.close()
            
        elif learn:

            for rule in rule_list:
                if solve(rule.get_antecedent(), var_list):
                    var_list[rule.get_consequent()].set_truth(True)
                else:
                    var_list[rule.get_consequent()].set_truth(False)


        elif query:

            print("\n" + str(query_exp(args[1], var_list, rule_list)))

        elif why: 

            valid, logic = determine_why(args[1], var_list, rule_list)

            print("\n" + str(valid))

            fact_list = list()

            for step in logic:

                step = step.replace("(", " ( ")
                step = step.replace(")", " ) ")
                step = step.replace("&", " & ")
                step = step.replace("|", " | ")
                step = step.replace("!", " ! ")

                step = step.split()

                for i in step:
                    if i not in ["(", ")", "&", "|", "!"] and i not in fact_list and var_list[i].get_root():
                        fact_list.append(i)

            for fact in fact_list:

                if var_list[fact].get_truth():
                    print("I KNOW THAT " + var_list[fact].get_value())
                else:
                    print("I KNOW IT IS NOT TRUE THAT " + var_list[fact].get_value())

            i = len(logic)-1

            while i >= 0:

                if i > 0:

                    con = get_diff(logic[-2], logic[-1])
                    ant = ""

                    for rule in rule_list:
                        if rule.get_consequent() == con:
                            ant = rule.get_antecedent()

                    print(format_rule(ant, con, var_list, rule_list))

                else:

                    if valid:
                        print("I THUS KNOW THAT", format_goal(logic[0], var_list))
                    else:
                        print("THUS I CANNOT PROVE", format_goal(logic[0], var_list))

                i -= 1
                logic.pop()        

        elif myHelp:
            
            print('Valid Commands Are:\n' + usage)

        elif load_file:

            fMode = 'r'
            
            rule_list.clear()
            var_list.clear()

            fv = open(fVars, fMode)

            for v in fv:
                v = v.strip('\n')
                v = v.split(';')

                var_list[v[0]] = Variable(v[1], v[2], v[3])

            fv.close()

            fr = open(fRules, fMode)

            for r in fr:
                r = r.strip('\n')
                r = r.split(';')

                antecedent = r[0]
                consequent = r[1]
                
                rule_list.append(Rule(antecedent, consequent))

            fr.close()
            
        else:
            print("\nUnknown Command.")

        print("\n.\n")
    #
        print('len(args): ' + str(len(args)))
        for arg in args:
            print('args[arg]: ' + str(arg))
    
        print("len(var_list): " + str(len(var_list)))
        for var in var_list:
            print("var_list[var]: " + var + " ; value: " + var_list[var].get_value() + " ; truth: " + str(var_list[var].get_truth()) + " ; root: " + str(var_list[var].get_root()))
            print("> " + var_list[var].__str__() + " <\n")

        print("len(rule_list): " + str(len(rule_list)))
        for rule in rule_list:
            print("rule_list[rule]: " + rule.__str__())

    print("--------------------\n")
    
