import collections

def unpack(p = 0):
	def internal(x):
		return x[p]
	return internal

def unpack_single(x):
	return x[0]

def passthrough(*args):
	return args

class Parser:

	def __init__(self):
		self.rules = collections.defaultdict(list)

	def add_rule(self, name, contents, function = None):
		if function == None:
			if len(contents) == 1:
				function = unpack_single
			else:
				function = passthrough
		self.rules[name].append({
			'contents': contents,
			'function': function,
			'type': 'normal'
		})

	def add_atom(self, name, contents, function = unpack_single):
		self.rules[name].append({
			'contents': contents,
			'function': function,
			'type': 'atomic'
		})

	def print_rules(self):
		for rname, options in self.rules.items():
			print(rname)
			for i in options:
				print('   ', i)
			print()

	def parse(self, to_match, left, right, evaluate = False, trim = False):
		cache_key = (to_match, left, right)
		# print(to_match, left, right)
		if cache_key not in self.parse_cache:
			results = []
			for option in self.rules[to_match]:
				if option['type'] == 'atomic':
					if right - left == 1 and self.tokens[left] in option['contents']:
						results.append((option['function'] if evaluate else to_match, self.tokens[left]))
				elif option['type'] == 'normal':
					paths = [([], left)]
					for index, part in enumerate(option['contents']):
						next_paths = []
						for prev, limit in paths:
							for split in range(limit + 1, right - len(option['contents']) + index + 2):
								matched = self.parse(part, limit, split, evaluate, trim)
								if matched != None:
									next_paths.append((prev + [matched], split))
						paths = next_paths
					# Append to results
					for matched, end in paths:
						if matched != None and end == right:
							results.append((option['function'] if evaluate else to_match, matched))
			if len(results) == 0:
				self.parse_cache[cache_key] = [None]
			else:
				if trim:
					results = [results[0]]
				if evaluate:
					self.parse_cache[cache_key] = []
					for func, args in results:
						self.parse_cache[cache_key].append(func(args))
				else:
					self.parse_cache[cache_key] = results
				# print(to_match, ':', left, right)
				# for i in results:
				# 	print('   ', i)
				# print()
				if len(results) > 1:
					raise Exception('Ambiguous Parse Tree')
		return self.parse_cache[cache_key][0]

	def fullparse(self, tokens, master_rule, evaluate = False, trim = False):
		self.tokens = tokens[:]
		self.parse_cache = {}
		return self.parse(master_rule, 0, len(tokens), evaluate, trim)

if __name__ == '__main__':

	def eval_addition(x):
		if x[1] == '+':
			return x[0] + x[2]
		if x[1] == '-':
			return x[0] - x[2]

	def eval_multiplication(x):
		if x[1] == '*':
			return x[0] * x[2]
		if x[1] == '/':
			return x[0] / x[2]

	def eval_power(x):
		return x[0] ** x[2]

	parser = Parser()

	parser.add_atom('digit', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], lambda x: int(x[0]))
	parser.add_atom('operator_add', ['+', '-'])
	parser.add_atom('operator_mul', ['*', '/'])
	parser.add_atom('operator_power', ['^'])
	parser.add_atom('lpar', ['(', '[', '{'])
	parser.add_atom('rpar', [')', ']', '}'])

	parser.add_rule('number', ['digits'])
	parser.add_rule('number', ['operator_add', 'digits'], lambda x: x[1] if x[0] == '+' else -x[1])
	parser.add_rule('digits', ['digit'])
	parser.add_rule('digits', ['digits', 'digit'], lambda x: x[0] * 10 + x[1])

	parser.add_rule('addition', ['addition', 'operator_add', 'multiplication'], eval_addition)
	parser.add_rule('addition', ['multiplication'])

	parser.add_rule('multiplication', ['multiplication', 'operator_mul', 'power'], eval_multiplication)
	parser.add_rule('multiplication', ['power'])

	# a^b^c = a^(b^c)
	parser.add_rule('power', ['expression', 'operator_power', 'power'], eval_power)
	parser.add_rule('power', ['expression'])

	parser.add_rule('expression', ['lpar', 'addition', 'rpar'], unpack(1))
	parser.add_rule('expression', ['number'])

	parser.add_rule('master', ['addition'])

	parser.print_rules()

	code = input('> ')
	while code != '' and code != 'exit':
		if code == 'help' or code == '?':
			print("parser2.py by DXsmiley\nIn this example, you can type simple mathematical expressions.\nexample: 3 / (4 + 6 * 3)\n")
		else:
			tokens = list(code.replace(' ' , ''))
			print(parser.fullparse(tokens, 'master', True), '\n')
		code = input('> ')