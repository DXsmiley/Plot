import sys
import webbrowser
import output
import interpereter
import os

HELP_STRING = """
plot [options] command...
Options:
    --help         Show this help
    --w            Open the output in the default browser
    --browser      ''
    --parse-tree   Prints the parse tree
"""

shapes = []
codes = []

open_browser = False
show_parse_tree = False

for i in sys.argv[1:]:
	if i.startswith('--'):
		command = i[2:]
		if command == 'help':
			print(HELP_STRING)
		elif command == '?':
			print(HELP_STRING)
		elif command == 'w':
			open_browser = True
		elif command == 'browser':
			open_browser = True
		elif command == 'parse-tree':
			show_parse_tree = True
		else:
			print('Unknown command:', command)
	elif i == '-help' or i == '?' or i == '-?':
		print(HELP_STRING)
	else:
		if i == '-help':
			print("Interpereted '-help' as a plot command. Use '--help' for actual help.")
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