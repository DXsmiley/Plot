import svgwrite
import colorsys

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

	write_count = 0
	colour_min = min((p[2] for p in points if len(p) == 3), default = 0)
	colour_max = max(colour_min + 1, max((p[2] for p in points if len(p) == 3), default = 0))
	colour_range = colour_max - colour_min

	for p in points:
		if len(p) == 2:
			x, y = p
			c = colour_min
		elif len(p) == 3:
			x, y, c = p
		else:
			raise Exception('Invalid point {}'.format(p))
		c = (c - colour_min) / colour_range
		x = (x * scale) + (size / 2)
		y = (-y * scale) + (size / 2)
		r, g, b = colorsys.hsv_to_rgb(c, 1, 1)
		if 0 < x < size and 0 < y < size:
			svg.add(svg.circle(center = (x, y), r = 1, stroke = svgwrite.rgb(r * 255, g * 255, b * 255)))
			write_count += 1

	svg.save()

	if html_also:
		with open(filename + '.html', 'w') as f:
			f.write('<html><img src="plot.temp.svg" width={size} height={size}></html>'.format(size = 800))