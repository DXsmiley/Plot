import sys
import webbrowser
import output
import interpereter
import os

# code = '0.2 * x , 0.35 * y | x : [0, 10, 10] | y : [0 , 10, 10]'
# code = '4 - a, a | a : [0, 10]'
# code = 'abs(5 * sin(a) - 1), 2 * cos(a * 3) | a : [0, 2 * pi]'
# code = input('> ')

shapes = []
codes = []

open_browser = False
show_parse_tree = False

for i in sys.argv[1:]:
	if i.startswith('--'):
		command = i[2:]
		if command == 'help':
			print("You called for help... but nobody came.")
		elif command == 'w':
			open_browser = True
		elif command == 'browser':
			open_browser = True
		elif command == 'parse-tree':
			show_parse_tree = True
		else:
			print('Unknown command:', command)
	else:
		codes.append(i)

for i in codes:
	shapes.append(interpereter.evaluate(i, show_parse_tree = show_parse_tree))

if len(shapes) > 0:
			
	output.writeToSVG('plot.temp', shapes, html_also = open_browser)

	if open_browser:
		# print('Opening in web browser...')
		url = os.path.abspath("plot.temp.html")
		webbrowser.open('file://' + url, new = 2)

else:

	print('Plotted no shapes')