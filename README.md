# Plot

A python programs that plots points.

## Installation

1. Download the files and put them where you want.
2. Get svgwrite: `pip install svgwrite`

## Usage

`python -m plot "t, t | t [0, 10]"`

Add the flag `--w` to open the result image in your web browser.

`python -m plot --w "t, t | t [0, 10]"`

## Example

`r * sin(x), r * cos(x * 3) | x : [0, 2 * pi] | r : [1, 4, 4]`

![Example 1 Image](https://raw.githubusercontent.com/DXsmiley/Plot/master/example1.png)