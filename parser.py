from Grammar import *


class production_rule(object):
    """
        A Class that containes the constructed rules
        The rules are constructed in a form of a tree
        with the root having two child nodes
    """
    def __init__(self,  res, a, b):
        self.result = res
        self.rule_1 = a
        self.rule_2 = b

    # Get the result of the production of the two children
    @property
    def get_result(self):
        return self.result

    # Get the left child
    @property
    def get_left(self):
        return self.rule_1

    # Get the left child
    @property
    def get_right(self):
        return self.rule_2


class Cell(object):
    """
        A Cell class that is used to save the productions of each rule
    """

    # If this rule has previous productions, add to it. If not then the productions is empty.
    def __init__(self, production=None):
        if production:
            self.production = production
        else:
            self.production = []

    # Add  a new production for the cell
    def add_production(self, res, a, b):
        # Call the the production rule function to construnct the production for this rule
        self.production.append(production_rule(res,a,b))


    # Get all the results for all the productions for a specific cell
    @property
    def get_types(self):
        types = []
        for p in self.production:
            types.append(p.result)
        return types

    # Get the productions for a specific Cell
    @property
    def get_rules(self):
        return self.production




class Parser(object):
    """
        The Parser class that uses the grammar set pefore and the prduction rules generated,
        to parse the text and check if it fits in the gramar or not.
    """

    def __init__(self, grammar, sentence):

        # Breaking down the String into tokens to be parsed and checked
        self.tokens = sentence.split()

        # Number of tokens to be parsed
        self.length = len(self.tokens)

        # If there is no tokens Raise Error
        if self.length < 1:
            raise ValueError("The sentence could no be read")

        # Construct the parsing table as cells
        grammar.parsing_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]



    def parse(self, grammar, sentence):
        """
            Check the rules for each cell and token
        """

        for x, t in enumerate(self.tokens):
            # If there is no Rule then this word is not in the grammar.
            rules = grammar.check_rule(t)
            if rules == None:
                print("The word " + t + " is not in the grammar")
            else:
                # For each rule for this token add a production rule
                for rule in rules:
                    grammar.parsing_table[0][x].add_production(rule, production_rule(t, None, None), None)


        for l in range(2,self.length+1):
            for s in range(1,self.length-l+2):
                for p in range(1,l-1+1):

                    t1 = grammar.parsing_table[p-1][s-1].get_rules
                    t2 = grammar.parsing_table[l-p-1][s+p-1].get_rules

                    for a in t1:
                        for b in t2:
                            r = grammar.check_rule(str(a.get_result) + " " + str(b.get_result))

                            if r is not None:
                                for w in r:
                                    print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.get_result) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.get_result)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                    grammar.parsing_table[l-1][s-1].add_production(w,a,b)

        if  len(grammar.parsing_table[self.length-1][0].get_types) > 0:
            print("----------------------------------------")
            print('The sentence IS accepted in the language')
            print('Number of possible trees: ' + str(len(grammar.parsing_table[self.length-1][0].get_types)))
            print("----------------------------------------")
        else:
            print("--------------------------------------------")
            print('The sentence IS NOT accepted in the language')
            print("--------------------------------------------")

    #Print the CYK parse trable for the last sentence that have been parsed.
    def print_parse_table(self, grammar):
        try:
            from tabulate import tabulate
        except (ModuleNotFoundError,ImportError) as r:
            import subprocess
            import sys
            import logging
            logging.warning('To print the CYK parser table the Tabulate module is necessary, trying to install it...')
            subprocess.call([sys.executable, "-m", "pip", "install", 'tabulate'])

            try:
                from tabulate import tabulate
                logging.warning('The tabulate module has been instaled succesfuly!')

            except (ModuleNotFoundError,ImportError) as r:
                logging.warning('Unable to install the tabulate module, please run the command \'pip install tabulate\' in a command line')


        lines = []



        for row in reversed(grammar.parsing_table):
            l = []
            for cell in row:
                l.append(cell.get_types)
            lines.append(l)

        lines.append(self.tokens)
        print('')
        print(tabulate(lines))
        print('')
