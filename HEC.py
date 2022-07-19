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

		# equation = 51630*x**3 - 154890*x**2 + 154890*x - 51630
		# plt.scatter(x_values, y_values)
		# plt.show()


		print(x_values)
		print(y_values)

		x = Symbol("x")

		final_equation = 0
		for i in range(0,4):
			# print("I: " + str(i))
			product_of_tmp_equations = 1
			for j in range(0, 4):
				if(j!=i):
					print("X value [{i_val}]: {x_val_i}, X value [{j_val}]: {x_val_j}".format(i_val=i, x_val_i=x_values[i], j_val=j, x_val_j=x_values[j]))
					print("Coefficient: " + str(self.inverse_mod_p(x_values[i] - x_values[j])))
					tmp_eq = (x - 1) * self.inverse_mod_p(x_values[i] - x_values[j])
					# print("Temp: " + str(tmp_eq))
					# print("Coefficients: " + str(poly(tmp_eq).coeffs()))
					# print([prod(x**k for x, k in zip(poly(tmp_eq, x).gens, mon)) for mon in poly(tmp_eq, x).monoms()])

					# print("Monomials: " + str(poly(tmp_eq, x).monoms()))

					product_of_tmp_equations *= tmp_eq

					print("-"*20)
					print("Temp: " + str(tmp_eq))
					print("Product: " + str(product_of_tmp_equations))
					reduced_equation = self.reduce_equation_mod_p(product_of_tmp_equations)
					print("Reduced Equation: " + str(reduced_equation))
					print("-"*20)


			# print(product_of_tmp_equations)
			final_tmp = simplify(reduced_equation) * self.reduce_mod_p(y_values[i])
			final_tmp = self.reduce_equation_mod_p(expand(final_tmp))
			# print("Product: " + str(final_tmp))
			final_equation += final_tmp
			final_equation = self.reduce_equation_mod_p(final_equation)

		print("Sum of products: " + str(final_equation))
	

		# coeffs = poly(final_equation).all_coeffs()

		# find equal 


		# new_coeffs = []
		# for c in coeffs:

	def reduce_modulo_poly(self, poly, mod):
		print(poly)
		print(mod)

		remainder = prem(poly, mod)
		return remainder


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

	def reduce_equation_mod_p(self, equation):

		x = Symbol("x")
		coeffs = poly(equation, x).coeffs()
		monomials = [prod(x**k for x, k in zip(poly(equation, x).gens, mon)) for mon in poly(equation, x).monoms()]

		# print("Monomials: " + str(monomials))
		# print("Coefficients: " + str(coeffs))

		new_coeffs = self.reduce_coefficients(coeffs)

		y = 0
		ind = 0
		for i in monomials:
			y += i*new_coeffs[ind]
			ind += 1

		return y

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

	def reduce_coefficients(self, coeffs):
		#print("Before: " + str(coeffs))
		new_coeffs = []
		for i in coeffs:
			n = self.reduce_mod_p(i)
			new_coeffs.append(n)
		#print("After: " + str(new_coeffs))

		return new_coeffs


	def mumford_rep(self, D1, D2):
		divisors = [D1, D2]
		
		new_divisors = []
		for i in divisors:
			mum_rep = []
			print(i)

			x, y, a, b = symbols("x y a b")

			u = self.reduce_equation_mod_p(cancel((x-i[0][0])*(x-i[1][0])))
			# print(u)

			general_form = Eq(y, a*x + b)
			general_expression = a*x + b

			sub_1 = general_form.subs(y, i[0][1]).subs(x, i[0][0])
			sub_2 = general_form.subs(y, i[1][1]).subs(x, i[1][0])

			# # print(general_form)

			system_of_equations = []
			# # print(sub_1)
			# # print(sub_2)
			system_of_equations.append(sub_1)
			system_of_equations.append(sub_2)

			# print(system_of_equations)

			solved = solve(system_of_equations)
			print(solved)

			a_val = self.reduce_mod_p(solved[a])
			b_val = self.reduce_mod_p(solved[b])
			# # print("A: " + str(a_val))
			# # print("B: " + str(b_val))

			v = general_expression.subs(a, a_val).subs(b, b_val)

			# # print("v1: " + str(v1))
			# print(f'In Mumford Form, {i} = [{u}, {v}]')
			mum_rep.append(u)
			mum_rep.append(v)
			new_divisors.append(mum_rep)

		return new_divisors

	def cantors_algorithm(self, divisors):
		print(divisors)

		divisor1 = divisors[0]
		divisor2 = divisors[1]

		u1, v1 = divisor1
		u2, v2 = divisor2

		print("u1: " + str(u1) + ", v1: " + str(v1))
		print("u2: " + str(u2) + ", v2: " + str(v2))

		# d1 = self.reduce_modulo_poly(u1, u2)
		d1 = gcd(u1, u2)
		print("d1: " + str(d1))

		# e1 = d1 / 2 * u1
		# e2 = d1 / 2 * u2





		e1 = 1/2
		e2 = -1/2

		print("e1: " + str(e1))
		print("e2: " + str(e2))

		# d = self.reduce_modulo_poly(d1, v1 + v2)
		d = gcd(d1, v1 + v2)
		print("d: " + str(d))

		# # c1 = d / (2 * d1)
		# # c2 = d / (2*(v1 + v2))

		c1 = 3/8
		c2 = 1/16

		print("c1: " + str(c1))
		print("c2: " + str(c2))

		s1 = c1 * e1
		s2 = c1 * e2
		s3 = c2

		u = (u1 * u2) / d**2

		u = cancel(u)
		# u = self.reduce_equation_mod_p(u)
		v = simplify(self.reduce_modulo_poly((((s1*u1*v2)+(s2*u2*v1)+(s3*(v1*v2+(self.eq)))) / d), u))
		#v = simplify(sealf.reduce_modulo_poly((s1*u1*v2+s2*u2*v1), u))
		# print("v^2: " + str(simplify(cancel(v**2))))

		# # print("s1: " + str(s1))
		# # print("s2: " + str(s2))
		# # print("s3: " + str(s3))
		# # print("u: " + str(u))
		# # print("v: " + str(v))
		
		# print(self.eq)

		print("v:" + str(v))

		# u_prime = div((self.eq - simplify(cancel(v**2))), u)[0]
		# print("u': " + str(u_prime))

		# print("-v:" + str(-v))
		# v_prime = (div(-1*v, u_prime)[1])
		# print("v': " + str(v_prime))

		# # find multiplicitve inverse 

		while(degree(u) > 2):

			print("degree of u: " + str(degree(u)))

			u_prime = u_prime = div((self.eq - simplify(cancel(v**2))), u)[0]
			print("u': " + str(u_prime))
			print("-v mod u': " + str(Mod(-1*v, u_prime)))
			v_prime = (div(-1*v, u_prime)[1])


			print("u': " + str(u_prime))
			print("v': " + str(v_prime))

			u = u_prime
			v = v_prime

		# u = self.reduce_equation_mod_p(u)
		# v = self.reduce_equation_mod_p(v)

		print("u: " + str(u))
		print("v: " + str(v))


		# d1 = reduce_modulo_poly()


p = 11
c1 = 1
c2 = -4
c3 = -14
c4 = 36
c5 = 45
c6 = 0





# c1 = 1
# c2 = 0
# c3 = 3
# c4 = 2
# c5 = 0
# c6 = 3



# p = 5

# p1 = (3,0)
# p2 = (1,2)

# p3 = (4,1)
# p4 = (3,0)


# D1 = [p1, p2]
# D2 = [p3, p4]
x = Symbol("x")

print(prem(x**2 + 7*x + 10, 11))

print(prem(x**2 + 4*x + 4, x))



# new_divisors = [[x**2 + 7*x + 10, x + 9], [x**2 + 10, 7*x + 9]]
new_divisors = [[x**2 - 4*x + 3, -4*x + 12], [x**2 -6*x + 5, -2*x + 10]]

print(gcd(new_divisors[0][0], new_divisors[1][0]))

hec = HyperEllipticCurve(p, c1, c2, c3, c4, c5, c6)
# new_divisors = hec.mumford_rep(D1, D2)
# hec.calculate_cubic_equation(D1, D2)

hec.cantors_algorithm(new_divisors)


# ________________________________________________________

# p = 23

# c1 = 1
# c2 = -1
# c3 = -11
# c4 = 9
# c5 = 18
# c6 = 0

# hec = HyperEllipticCurve(p, c1, c2, c3, c4, c5, c6)
# coords = hec.solve_for_coords()
# hec.plot_points(coords)

# p1 = (1, 19)
# p2 = (8, 1)
# p3 = (11, 1)
# p4 = (17, 11)

# # print(hec.check_point(p1))
# # print(hec.check_point(p2))
# # print(hec.check_point(p3))
# # print(hec.check_point(p4))

# D1 = [p1, p2]
# D2 = [p3, p4]

# hec.calculate_cubic_equation(D1, D2)

