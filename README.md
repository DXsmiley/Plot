# Plot

A python programs that plots points.

## Installation

1. Download the files and put them where you want.
2. Get svgwrite: `pip install svgwrite`

## Usage

`python -m plot [options] command...`

Example:

`python -m plot --w "t, t + 2 | t : [~1]"`

### Options

All flags should be prefixed with `--`.

| Flag       | Action                                  |
| ---------- | --------------------------------------- |
| help       | Show this help.                         |
| w, browser | Open the output in the default browser  |
| parse-tree | Prints the parse tree                   |

### Command Syntax

TODO: Write a tutorial.

## Examples

`1.5 * t, t ^ 2 | t : [-2, 2]`

![Example 3 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example3.png)

`r * sin(a), r * cos(a * 3) | a : [0, 2 * pi] | r : [1, 4, 4]`

![Example 1 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example1.png)

`(r + sin(a * 6)) * cos(a), (r + sin(a * 6)) * sin(a), sin(a * 3) | a : [0, 2 * pi, 500] | r : [1, 3, 10]`

![Example 2 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example2.png)

	line((sin(t) * t * 0.1, cos(t) * t * 0.1 | t : [0, 12 * pi]))
	line((sin(0-t) * t * 0.1, cos(0-t) * t * 0.1 | t : [0, 12 * pi]))

![Example 4 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example4.png)