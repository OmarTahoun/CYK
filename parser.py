from Grammar import *
class production_rule(object):
    def __init__(self,  res, a, b):
        self.result = res
        self.rule_1 = a
        self.rule_2 = b

    @property
    def get_result(self):
        return self.result

    @property
    def get_left(self):
        return self.rule_1

    @property
    def get_right(self):
        return self.rule_2


class Cell(object):
    def __init__(self, production=None):
        if production:
            self.production = production
        else:
            self.production = []

    def add_production(self, res, a, b):
        self.production.append(production_rule(res,a,b))

    @property
    def get_types(self):
        types = []
        for p in self.production:
            types.append(p.result)
        return types

    @property
    def get_rules(self):
        return self.production

class Parser(object):
    def __init__(self, grammar, sentence):
        self.tokens = sentence.split()
        self.length = len(self.tokens)

        if self.length < 1:
            raise ValueError("The sentence could no be read")
        grammar.parsing_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]

    def parse(self, grammar, sentence):
        for x, t in enumerate(self.tokens):
            rules = grammar.check_rule(t)
            if rules == None:
                print("The word " + t + " is not in the grammar")
            else:
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
