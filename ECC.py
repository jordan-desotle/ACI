from sympy import *
import matplotlib.pyplot as plt
import numpy as np

# Elliptic Curve Cryptography


# Tables storing mod values
multiplicitive_table = []
additive_table = []


def plot_points(coords, inp):
	x_coords = []
	y_coords = []

	a = inp[1]
	b = inp[2]


	for i in range(0, len(coords)):
		print(coords[i])
		x_coords.append(coords[i][0])
		y_coords.append(coords[i][1])

	print(x_coords)
	print(y_coords)

	plt.scatter(x_coords, y_coords)
	# y, x = np.ogrid[-5:5:100j, -5:5:100j]
	# plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])

	plt.show()

# def plot_curve(inp):

	
	
# 	plt.show()


# Get values to calculate mod tables
# def inp():
# 	good_A = False
# 	good_B = False
# 	good_P = False

# 	while(not good_P):
# 		p = int(input("Enter a value for P: "))
# 		if(p > 1):
# 			for i in range(2, p):
# 				if((p % i) == 0):
# 					print("Number must be prime")
# 					break
# 			else:
# 				good_P = True
# 	while(not good_A):
# 		a = int(input("Enter a value for A: "))
# 		if((a < 0) or (a >= p)):
# 			print("Conditions for 'A':\nA >= 0, A < P")
# 		else:
# 			good_A = True
# 	while(not good_B):
# 		b = int(input("Enter a value for B: "))
# 		if((b < 0) or (b >= p)):
# 			print("Conditions for 'B':\nB >= 0, B < P")
# 		else:
# 			good_B = True

# 	return p, a, b

def get_inp():
	good_A = False
	good_B = False
	good_P = False

	p = int(input("Enter a value for P: "))
	while(not good_A):
		a = int(input("Enter a value for A: "))
		if((a < 0) or (a >= p)):
			print("Conditions for 'A':\nA >= 0, A < P")
		else:
			good_A = True
	while(not good_B):
		b = int(input("Enter a value for B: "))
		if((b < 0) or (b >= p)):
			print("Conditions for 'B':\nB >= 0, B < P")
		else:
			good_B = True

	return p, a, b

def generate_tables(p):

	for i in range(0, p):
		tmp_arr = []
		for j in range(0, p):
			tmp = (i + j) % p
			tmp_arr.append(tmp)
		additive_table.append(tmp_arr)

	for i in range(0, p):
		tmp_arr = []
		for j in range(0, p):
			tmp = (i * j) % p
			tmp_arr.append(tmp)
		multiplicitive_table.append(tmp_arr)

def generate_coords(p, sols):


	coords = []
	for x in range(0,p):
		print("X: " + str(x) + ", Y^2: " + str(sols[x]))
		for j in range(0,p):
			tmp = []
			if((j*j)%p == sols[x]):
				# print("X: " + str(x) + ", Y: " + str(j))
				tmp.append(x)
				tmp.append(j)
				coords.append(tmp)

	# print(coords)

	return coords

	# coords = []
	# for i in range(0, p):
	# 	for s in sols:
	# 		print("X: " + str(i) + ", Y^2: " + str(s) + )
	# 		if((i*i)%p == s):
	# 			print({i, s})
	# 			coords.append({i, s})
	# print(coords)
		



def print_tables():

	for i in additive_table:
		tmp = ""
		for j in i:
			tmp += str(j) + ' '
		print(tmp)

	print("\n")

	for i in multiplicitive_table:
		tmp = ""
		for j in i:
			tmp += str(j) + ' '
		print(tmp)

	# print(additive_table)
	# print(multiplicitive_table)

def solve_for_yy(inp):

	x, a, b = symbols("x a b")

	# equation = input("Enter an equation: ")
	# new_equation = sympify(equation, evaluate=False)


	new_equation = x**3 + a*x + b
	# print(type(new_equation))
	#new_equation = ""

	new_equation = new_equation.subs(a, inp[1])
	new_equation = new_equation.subs(b, inp[2])

	print(new_equation)

	solutions = []
	# # plug in x and solve
	for i in range(0, inp[0]):
		final_equation = new_equation

		final_equation = final_equation.subs(x, i)
		#print(final_equation)

		yy = Symbol('yy')
		# solve_equation = Eq(final_equation, yy)
		equation1 = Eq(final_equation, yy)
		
		sol = ((solve(equation1, yy))[0] % inp[0])
		
		print('[{count:0>8}] Solution for (Y^2 = ({count})^3 + ({a_val})({count}) + {b_val}) mod({p_val}): {sol_val}'.format(count=i, a_val=inp[1], b_val=inp[2], p_val=inp[0], sol_val=str(sol)))
		solutions.append(sol)

	return solutions



	

# usr_inp = inp()
usr_inp = get_inp()
generate_tables(usr_inp[0])
print_tables()
solutions = solve_for_yy(usr_inp)
coords = generate_coords(usr_inp[0], solutions)
plot_points(coords, usr_inp)
# plot_curve(usr_inp)






