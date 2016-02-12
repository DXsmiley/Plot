import copy

# A line is made of many points

class Line:

	def __init__(self, points):
		self.points = copy.deepcopy(points)

# A mesh is made of many lines of the same length

class Mesh:

	def __init__(self, lines, solid = False):
		self.lines = copy.deepcopy(lines)

# Unused point class

class Point:

	def __init__(self, x, y, colour = 0):
		self.x = x
		self.y = y
		self.colour = 0