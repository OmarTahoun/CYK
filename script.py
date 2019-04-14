from Grammar import *
from parser import *
my_grammar = Grammar("test.txt")
my_parser = Parser(my_grammar, 'astronomers saw stars with ears')


my_parser.parse(my_grammar, 'astronomers saw stars with ears')
my_parser.print_parse_table(my_grammar)
