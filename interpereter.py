"""

	Constants:

		# These might be cut if they are too power hungry
		R : real numbers
		Z : integers
		N : natural numbers (positive integers)

		PI : pi
		P : ditto
		E : 2.8something

	Functions:

		# Should add to this list at some point
		sin : sine
		cos : cosine
		tan : tangent

		max : maximum
		min : minimum
		sum : summate
		prod : product

	Grammar Spec:

		master : iterator-list
		iterator-list : iterator-list "|" iterator
		iterator-list : tuple "|" iterator
		iterator : variable ":" tuple
		tuple : expression
		tuple : expression "," tuple
		forced-tuple : expression
		forced-tuple : expression "," tuple
		expression : range
		expression : set
		expression : addition
		range : "[" forced-tuple "]"
		range : "[~" forced-tuple "]"
		set : "{" tuple "}"
		addition : addition addition-operator multiplication
		addition : multiplication
		multiplication : multiplication multiplication-operator power
		multiplication : power
		power : peice "^" power # a^b^c = a^(b^c)
		peice : number
		peice : function
		peice : variable
		peice : bracketed-expression
		peice : contracted-multiplication
		function : variable "(" tuple ")"
		function : variable "()" # Will functions without arguments ever be used?
		function : variable "(" itertor-list ")" # This will come later
		bracketed-expression : "(" tuple ")"
		bracketed-expression : "(" iterator-list ")"
		variable : variable-name
		variable-name : letter character
		variable-name : letter
		character : letter
		character : digit
		addition-operator : "+"
		addition-operator : "-"
		multiplication-operator : "*"
		multiplication-operator : "/"
		# might confuse people... would be a nice shorthand for things though
		contracted-multiplication : number variable-name
		contracted-multiplication : number expression
		contracted-multiplication : number bracketed-expression

"""

from genericparser import Parser
import string
import math
import random
import data

# Utility

def frange(start, end, step = 1):
	i = start
	while i < end:
		yield i
		i += step

# Evaluation objects


class Master:

	def __init__(self, iterator_list):
		self.iterator_list = iterator_list

	def __repr__(self):
		return repr(self.iterator_list)

	def evaluate(self, variables):
		return self.iterator_list.evaluate(variables)

class IteratorList:

	def __init__(self, expression, iterator):
		self.iterator = iterator
		self.expression = expression

	def evaluate(self, variables):
		results = []
		for i in self.iterator.evaluate(variables):
			variables[self.iterator.variable.vname] = i
			item = self.expression.evaluate(variables)
			if isinstance(item, list):
				results += item
			else:
				results.append(item)
		return results

	def __repr__(self):
		return repr(self.expression) + ' | ' + repr(self.iterator)

class Iterator:

	def __init__(self, variable, generator):
		self.variable = variable
		self.generator = generator

	def evaluate(self, variables):
		return self.generator.evaluate(variables)

	def __repr__(self):
		return 'I(' + repr(self.variable) + ': ' + repr(self.generator) + ')'

class Variable:

	def __init__(self, vname):
		self.vname = vname

	def evaluate(self, variables):
		return variables.get(self.vname, 0)

	def __repr__(self):
		return self.vname

class Range:

	def __init__(self, my_tuple):
		self.my_tuple = my_tuple

	def evaluate(self, variables):
		parameters = self.my_tuple.evaluate(variables)
		num_param = len(parameters)
		start = 0
		end = 0
		intervals = 1000
		if num_param == 1:
			end = parameters[0]
		elif num_param == 2:
			start = parameters[0]
			end = parameters[1]
		elif num_param == 3:
			start = parameters[0]
			end = parameters[1]
			intervals = parameters[2]
		else:
			print('Wrong number of arguments for a range generator')
		step = (end - start) / intervals
		return list(frange(start, end, step))

	def __repr__(self):
		return 'R[' + repr(self.my_tuple) + ']'

class Set:

	def __init__(self, my_tuple):
		self.my_tuple = my_tuple

	def evaluate(self, variables):
		return list(self.my_tuple.evaluate(variables))

class Tuple:

	def __init__(self, peices, forced = False):
		self.peices = peices
		self.forced = forced

	def evaluate(self, variables):
		if len(self.peices) == 1 and not self.forced:
			return self.peices[0].evaluate(variables)
		else:
			return tuple(i.evaluate(variables) for i in self.peices)

	# def __str__(self):
	# 	return 'T(' + ', '.join(str(i) for i in self.peices) + ')'

	def __repr__(self):
		return 'T(' + ', '.join(str(i) for i in self.peices) + ')'

class Number:

	def __init__(self, value):
		self.value = value

	def evaluate(self, variables):
		return self.value

	def __repr__(self):
		return str(self.value)

class BinaryOperator:

	def __init__(self, left, right, operator):
		self.left = left
		self.right = right
		self.operator = operator

	def evaluate(self, variables):
		if self.operator == '+':
			return self.left.evaluate(variables) + self.right.evaluate(variables)
		elif self.operator == '-':
			return self.left.evaluate(variables) - self.right.evaluate(variables)
		elif self.operator == '*':
			return self.left.evaluate(variables) * self.right.evaluate(variables)
		elif self.operator == '/':
			return self.left.evaluate(variables) / self.right.evaluate(variables)
		elif self.operator == '^':
			return self.left.evaluate(variables) ** self.right.evaluate(variables)

	def __repr__(self):
		return 'B({} {} {})'.format(repr(self.left), self.operator, repr(self.right))

class Function:

	def __init__(self, variable, arguments):
		self.variable = variable
		self.arguments = arguments

	def evaluate(self, variables):
		function_object = self.variable.evaluate(variables)
		parameters = self.arguments.evaluate(variables)
		return function_object(*parameters)

	def __repr__(self):
		return 'F:{}({})'.format(repr(self.variable), repr(self.arguments))

# Setup the grammer and things

parser = Parser()

for i in '|:,[](){}^.-':
	parser.add_atom(i, [i])

parser.add_atom('addition-operator', ['+', '-'])
parser.add_atom('multiplication-operator', ['*', '/'])

parser.add_rule('master', ['iterator-list'], lambda x: Master(x[0]))
parser.add_rule('master', ['expression'], lambda x: Master(x[0]))
parser.add_rule('iterator-list', ['iterator-list', '|', 'iterator'], lambda x: IteratorList(x[0], x[2]))
parser.add_rule('iterator-list', ['tuple', '|', 'iterator'], lambda x: IteratorList(x[0], x[2]))
parser.add_rule('iterator', ['variable', ':', 'tuple'], lambda x: Iterator(x[0], x[2]))
parser.add_rule('tuple', ['tuple-peice'], lambda x: Tuple(x[0]))
parser.add_rule('tuple', ['expression'], lambda x: Tuple(x))
parser.add_rule('forced-tuple', ['tuple-peice'], lambda x: Tuple(x[0], forced = True))
parser.add_rule('forced-tuple', ['expression'], lambda x: Tuple(x, forced = True))
parser.add_rule('tuple-peice', ['expression', ',', 'expression'], lambda x: [x[0], x[2]])
parser.add_rule('tuple-peice', ['expression', ',', 'tuple-peice'], lambda x: [x[0]] + x[2])
parser.add_rule('expression', ['range'])
parser.add_rule('expression', ['set'])
parser.add_rule('expression', ['addition'])
# parser.add_rule('expression', ['number'])
parser.add_rule('range', ['[', 'forced-tuple', ']'], lambda x: Range(x[1]))
parser.add_rule('set', ['{', 'forced-tuple', '}'], lambda x: Set(x[1]))

# Mathematical expression
make_binary_op = lambda x : BinaryOperator(x[0], x[2], x[1])
parser.add_rule('addition', ['addition', 'addition-operator', 'multiplication'], make_binary_op)
parser.add_rule('addition', ['multiplication'])
parser.add_rule('multiplication', ['multiplication', 'multiplication-operator', 'power'], make_binary_op)
parser.add_rule('multiplication', ['power'])
parser.add_rule('power', ['peice', '^', 'power'], make_binary_op)
parser.add_rule('power', ['peice'])
parser.add_rule('peice', ['number'])
parser.add_rule('peice', ['variable'])
parser.add_rule('peice', ['function'])
parser.add_rule('peice', ['bracketed-expression'])
parser.add_rule('bracketed-expression', ['(', 'tuple', ')'], lambda x: x[1])
parser.add_rule('bracketed-expression', ['(', 'iterator-list', ')'], lambda x: x[1])
parser.add_rule('function', ['variable', '(', 'forced-tuple', ')'], lambda x: Function(x[0], x[2]))

# Numbers
parser.add_atom('digit', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
# parser.add_rule('number', ['operator_add', 'digits'], lambda x: x[1] if x[0] == '+' else -x[1])
parser.add_rule('digits', ['digit'])
parser.add_rule('digits', ['digits', 'digit'], lambda x: x[0] + x[1])
parser.add_rule('number', ['digits'], lambda x : Number(int(x[0])))
parser.add_rule('number', ['-', 'digits'], lambda x : Number(- int(x[1])))
make_decimal = lambda n, a, b: Number(n * (int(a) + int(b) / (10 ** len(b))))
parser.add_rule('number', ['digits', '.', 'digits'], lambda x : make_decimal(1, x[0], x[2]))
parser.add_rule('number', ['-', 'digits', '.', 'digits'], lambda x : make_decimal(-1, x[1], x[3]))

# Variable names
join_strings = lambda x: ''.join(x)
parser.add_atom('letter', list(string.ascii_letters))
parser.add_rule('character', ['letter'])
parser.add_rule('character', ['digit'])
parser.add_rule('characters', ['character'])
parser.add_rule('characters', ['character', 'characters'], join_strings)
parser.add_rule('variable-name', ['letter', 'characters'], join_strings)
parser.add_rule('variable-name', ['letter'])
parser.add_rule('variable', ['variable-name'], lambda x : Variable(x[0]))

def process_points(points, function):
	out = []
	for i in points:
		if len(i) == 2:
			x, y = function(i[0], i[1])
			out.append((x, y))
		elif len(i) == 3:
			x, y = function(i[0], i[1])
			c = c[2]
			out.append((x, y, c))
		else:
			out.append(i)
	return out

def function_scale(amount, points):
	return process_points(points, lambda x, y: (x * amount, y * amount))

def function_kick(amount, points):
	k = lambda x, y: (x + random.uniform(-1, 1) * amount, y + random.uniform(-1, 1) * amount)
	return process_points(points, k)

def function_line(points):
	return [data.Line(points)]

def evaluate(code, show_parse_tree = False):
	constants = {
		'pi': math.pi,
		'e': math.e,
		'sin': math.sin,
		'cos': math.cos,
		'tan': math.tan,
		'max': max,
		'min': min,
		'abs': abs,
		'scale': function_scale,
		'kick': function_kick,
		'line': function_line
	}
	tokens = list(code.replace(' ', ''))
	structure = parser.fullparse(tokens, 'master', True)
	if structure == None:
		raise Exception('Parse Failed')
	if show_parse_tree:
		print(structure)
	return structure.evaluate(constants)