# Plot

A python programs that plots points.

## Installation

1. Download the files and put them where you want.
2. Get svgwrite: `pip install svgwrite`

## Usage

`python -m plot "t, t | t [0, 10]"`

Add the flag `--w` to open the result image in your web browser.

`python -m plot --w "t, t | t [0, 10]"`

## Examples

`1.5 * t, t * t | t : [0 - 2, 2]`

![Example 3 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example3.png)

`r * sin(a), r * cos(a * 3) | a : [0, 2 * pi] | r : [1, 4, 4]`

![Example 1 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example1.png)

`(r + sin(a * 6)) * cos(a), (r + sin(a * 6)) * sin(a), sin(a * 3) | a : [0, 2 * pi, 500] | r : [1, 3, 10]`

![Example 2 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example2.png)