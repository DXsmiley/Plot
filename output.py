import svgwrite
import colorsys
import data

def writeShape(shape, params):
	if isinstance(shape, list):
		for i in shape:
			writeShape(i, params)
	elif isinstance(shape, tuple):
		if len(shape) == 2:
			x, y = shape
			c = 0
		elif len(shape) == 3:
			x, y, c = shape
		else:
			raise Exception('Invalid point {}'.format(shape))
		x = (x * params['scale']) + (params['size'] / 2)
		y = (-y * params['scale']) + (params['size'] / 2)
		c = (c - params['colour_min']) / params['colour_range']
		if 0 < x < params['size'] and 0 < y < params['size']:
			r, g, b = colorsys.hsv_to_rgb(c, 1, 1)
			params['svg'].add(params['svg'].circle(center = (x, y), r = 1, stroke = svgwrite.rgb(r * 255, g * 255, b * 255)))
	elif isinstance(shape, data.Line):
		for (x1, y1), (x2, y2) in zip(shape.points[:-1], shape.points[1:]):
			x1 = (x1 * params['scale']) + (params['size'] / 2)
			y1 = (-y1 * params['scale']) + (params['size'] / 2)
			x2 = (x2 * params['scale']) + (params['size'] / 2)
			y2 = (-y2 * params['scale']) + (params['size'] / 2)
			if 0 < x1 < params['size'] and 0 < y1 < params['size'] and 0 < x2 < params['size'] and 0 < y2 < params['size']:
				params['svg'].add(params['svg'].line((x1, y1), (x2, y2), stroke = svgwrite.rgb(255, 0, 0)))
	else:
		print('Cannot plot type', type(shape))

def parseShapes(shape):
	vals = {
		'colour_min': 0,
		'colour_max': 1
	}
	if isinstance(shape, list):
		for i in shape:
			p = parseShapes(i)
			vals['colour_min'] = min(vals['colour_min'], p.get('colour_min', 0))
			vals['colour_max'] = max(vals['colour_max'], p.get('colour_max', 1))
		return vals
	elif isinstance(shape, tuple):
		if len(shape) == 3:
			vals['colour_max'] = shape[2]
			vals['colour_min'] = shape[2]
	return vals

def writeToSVG(filename, points, html_also = True):

	size = 800
	scale = 60
	tick_frequency = 1
	svg = svgwrite.Drawing(filename + '.svg', profile = 'tiny')

	axis_colour = svgwrite.rgb(200, 200, 200)

	svg.add(svg.line((size / 2, 0), (size / 2, size), stroke = axis_colour))
	svg.add(svg.line((0, size / 2), (size, size / 2), stroke = axis_colour))

	for i in range(0, size // 2, scale * tick_frequency):
		a = size / 2 + i
		b = size / 2
		svg.add(svg.line((a, b - 3), (a, b + 3), stroke = axis_colour))
		svg.add(svg.line((b - 3, a), (b + 3, a), stroke = axis_colour))
		a = size / 2 - i
		svg.add(svg.line((a, b - 3), (a, b + 3), stroke = axis_colour))
		svg.add(svg.line((b - 3, a), (b + 3, a), stroke = axis_colour))

	params = parseShapes(points)
	params['colour_range'] = params['colour_max'] - params['colour_min']
	params['size'] = 800
	params['scale'] = 60
	params['svg'] = svg

	# colour_min = min((p[2] for p in points if len(p) == 3), default = 0)
	# colour_max = max(colour_min + 1, max((p[2] for p in points if len(p) == 3), default = 0))
	# colour_range = colour_max - colour_min

	writeShape(points, params)

	svg.save()

	if html_also:
		with open(filename + '.html', 'w') as f:
			f.write('<html><img src="plot.temp.svg" width={size} height={size}></html>'.format(size = 800))