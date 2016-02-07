import svgwrite

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

	for x, y in points:
		cx = (x * scale) + (size / 2)
		cy = (-y * scale) + (size / 2)
		if 0 < cx < size and 0 < cy < size:
			svg.add(svg.circle(center = (cx, cy), r = 1, stroke = svgwrite.rgb(255, 0, 0)))
			write_count += 1

	svg.save()

	if html_also:
		with open(filename + '.html', 'w') as f:
			f.write('<html><img src="plot.temp.svg" width={size} height={size}></html>'.format(size = 800))