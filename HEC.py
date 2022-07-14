from sympy import *
import matplotlib.pyplot as plt
import numpy as np

# HyperElliptic Curve Cryptography


def plot_points(coords):
	x_coords = []
	y_coords = []

	for i in range(0, len(coords)):
		print(coords[i])
		x_coords.append(coords[i][0])
		y_coords.append(coords[i][1])
	# print(x_coords)
	# print(y_coords)

	plt.scatter(x_coords, y_coords)

	plt.show()


def solve_for_coords(p):

	# results in (x**5 + 3*x**3 + 2*x**2 + 3) or x^5 + 3x^3 + 2x^2 + 3
	c1_val = 1
	c2_val = 0
	c3_val = 3
	c4_val = 2
	c5_val = 0
	c6_val = 3

	c1, c2, c3, c4, c5, c6, x = symbols("c1 c2 c3 c4 c5 c6 x")
	equation = c1*x**5 + c2*x**4 + c3*x**3 + c4*x**2 + c5*x + c6


	subs_equation = equation.subs(c1, c1_val).subs(c2, c2_val).subs(c3, c3_val).subs(c4, c4_val).subs(c5, c5_val).subs(c6, c6_val)

	print(subs_equation)

	solutions = []
	for i in range(0, p):
		final_equation = subs_equation
		final_equation = final_equation.subs(x, i)
		yy = final_equation%p
		solutions.append(yy)
	# print(solutions)

	coords = []
	for x in range(0,p):
		for j in range(0,p):
			tmp = []
			if((j**2)%p == solutions[x]):
				tmp.append(x)
				tmp.append(j)
				coords.append(tmp)

	print(coords)
	return coords



# usr_inp = inp()
# usr_inp = get_inp()
#generate_tables(usr_inp[0])
#print_tables()

p = 5
coords = solve_for_coords(p)
plot_points(coords)

