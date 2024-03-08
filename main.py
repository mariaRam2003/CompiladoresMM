from lexer_parser import Yalex
from lexer_graphic import display_expression_tree
from lexer_shunting import infix_postfix
from lexer_tree import get_tree

import sys


analizador = Yalex(sys.argv[1])
regex = analizador.get_regex()
display_expression_tree(get_tree(infix_postfix(regex)), regex)