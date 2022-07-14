from sympy import *
import matplotlib.pyplot as plt
import numpy as np

# HyperElliptic Curve Cryptography


class HyperEllipticCurve:
	def __init__(self, p, c1_inp, c2_inp, c3_inp, c4_inp, c5_inp, c6_inp):
		self.p = p
		self.c1 = c1_inp
		self.c2 = c2_inp
		self.c3 = c3_inp
		self.c4 = c4_inp
		self.c5 = c5_inp
		self.c6 = c6_inp

		c1, c2, c3, c4, c5, c6, x = symbols("c1 c2 c3 c4 c5 c6 x")
		equation = c1*x**5 + c2*x**4 + c3*x**3 + c4*x**2 + c5*x + c6
		self.eq = equation.subs(c1, self.c1).subs(c2, self.c2).subs(c3, self.c3).subs(c4, self.c4).subs(c5, self.c5).subs(c6, self.c6)

		print(self.eq)

	def solve_for_coords(self):
		solutions = []
		x = Symbol("x")
		for i in range(0, p):
			final_equation = self.eq
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

	def calculate_cubic_equation(self, D1, D2):
		# print(D1)
		# print(D2)

		p1, p2 = (D1[0], D1[1])
		p3, p4 = (D2[0], D2[1])

		# need array of x and y values
		x_values = [p1[0], p2[0], p3[0], p4[0]]
		y_values = [p1[1], p2[1], p3[1], p4[1]]

		print(x_values)
		print(y_values)

		x = Symbol("x")

		equations = []
		for i in range(0,4):
			# print("I: " + str(i))
			product_of_tmp_equations = 1
			for j in range(0, 4):
				if(j!=i):
					#print("X value [{i_val}]: {x_val_i}, X value [{j_val}]: {x_val_j}".format(i_val=i, x_val_i=x_values[i], j_val=j, x_val_j=x_values[j]))
					#print("Coefficient: " + str(self.inverse_mod_p(x_values[i] - x_values[j])))
					tmp_eq = (x - 1) * self.inverse_mod_p(x_values[i] - x_values[j])
					# print(tmp_eq)
					product_of_tmp_equations *= tmp_eq
			print(product_of_tmp_equations)
			final_tmp = simplify(product_of_tmp_equations)
			print(final_tmp)



	def plot_points(self, coords):
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

	def reduce_mod_p(self, num):
		return (num % self.p)

	def equal_mod_p(self, num1, num2):
		return (self.reduce_mod_p(num1 - num2) == 0)

	def inverse_mod_p(self, num):
		if(self.reduce_mod_p(num) == 0):
			return None
		return pow(num, self.p - 2, self.p)

	def check_point(self, point):
		(x, y) = point
		x_sym = Symbol("x")
		equation = self.eq.subs(x_sym, x)
		return self.equal_mod_p(y**2, equation)



p = 23

# p = 5
# c1 = 1
# c2 = 0
# c3 = 3
# c4 = 2
# c5 = 0
# c6 = 3

# p1 = (3,0)
# p2 = (1,2)
# p3 = (4,1)
# p4 = (1,3)

c1 = 1
c2 = -1
c3 = -11
c4 = 9
c5 = 18
c6 = 0

hec = HyperEllipticCurve(p, c1, c2, c3, c4, c5, c6)
coords = hec.solve_for_coords()
hec.plot_points(coords)


p1 = (1, 19)
p2 = (8, 1)
p3 = (11, 1)
p4 = (17, 11)

# print(hec.check_point(p1))
# print(hec.check_point(p2))
# print(hec.check_point(p3))
# print(hec.check_point(p4))

D1 = [p1, p2]
D2 = [p3, p4]

hec.calculate_cubic_equation(D1, D2)

