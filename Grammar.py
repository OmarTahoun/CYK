from parser import *

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

class Grammar(object):
    """This class containes the rules for the parsing that arre generated
    from the CFG given after converting it into CNF."""


    def __init__(self, filename):

        #initialising the grammar object with an empty dictionary
        self.rules = Dictlist()
        self.parsing_table = None
        self.length = 0

        #Reading the Rules from the grammar file
        #and constructing a map that maps each rule to it's origin
        for line in open(filename):
            x, y = line.split("->")
            self.rules[y.strip()] = x.strip()

        if len(self.rules) == 0:
            raise ValueError("No rules found in the grammar file!")

        self.show_rules()

    def show_rules(self):
        print("\nFile read Succesfully. The Rules found are: \n")

        for rule in self.rules:
            for x in self.rules[rule]:
                print(x + " --> " +rule)
        print()

    def check_rule(self,t):
        try:
            return self.rules[t]
        except KeyError as r:
            return None
