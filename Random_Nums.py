import random
import os
from sympy import *

red_color="\033[1;31m"
green_color="\033[0;32m"
yellow_color="\033[0;33m"
purple_color="\033[0;35m"
cyan_color="\033[0;36m"
blue_color="\033[0;34m"
white_color="\033[0;37m"


INF_POINT = None


# Represents an Elliptic Curve
class EllipticCurve:
	def __init__(self, p, a, b):
		self.p = p
		self.a = a
		self.b = b


	def addition(self, point1, point2):
		if (point1 == INF_POINT):
			return point2
		if (point2 == INF_POINT):
			return point1

		(x1, y1) = point1
		(x2, y2) = point2

		# Checks for vertical points
		if(self.equal_mod_p(x1, x2) and self.equal_mod_p(y1, -y2)):
			return INF_POINT

		# Calculate s-value
		if(self.equal_mod_p(x1, x2) and self.equal_mod_p(y1, y2)):
			# Adding point to itself
			s = (self.reduce_mod_p(3 * x1**2 + self.a)) * (self.inverse_mod_p(2 * y1))
			#s = (self.reduce_mod_p(3 * x1**2 + self.a)) / (self.reduce_mod_p(2 * y1))
		else:
			s = (self.reduce_mod_p(y1 - y2)) * (self.inverse_mod_p(x1 - x2))
			#s = (self.reduce_mod_p(y1 - y2)) / (self.reduce_mod_p(x1 - x2))

		s2 = self.reduce_mod_p(y1 - s * x1)

		x3 = self.reduce_mod_p(s**2 - x1 - x2)
		y3 = self.reduce_mod_p(-s * x3 - s2)

		new_point = (x3, y3)

		return new_point


	def reduce_mod_p(self, num):
		return (num % self.p)

	def equal_mod_p(self, num1, num2):
		return (self.reduce_mod_p(num1 - num2) == 0)

	def inverse_mod_p(self, num):
		if(self.reduce_mod_p(num) == 0):
			return None
		return pow(num, self.p - 2, self.p)

	# returns random points on the curve. only works for small p-values
	def return_random_points(self, num_points):

		# implement algorith to determine the total number of points
		if(num_points > 2):
			num_points = 2
			print("Can only return 2 points at this time")
		if(num_points <= 0):
			num_points = 1
			print("Number of points to be returned must be greater than 0")

		x, a, b= symbols("x a b")
		equation = x**3 + a*x + b
		equation = equation.subs(a, self.a).subs(b, self.b)
		solutions = []
		for i in range(0, self.p):
			final_equation = equation
			final_equation = final_equation.subs(x, i)
			yy = final_equation%self.p
			solutions.append(yy)

		coords = []
		for x in range(0,self.p):
			for j in range(0,self.p):
				tmp = []
				if((j**2)%self.p == solutions[x]):
					tmp.append(x)
					tmp.append(j)
					coords.append(tmp)
		# print(coords)

		coords_cp = coords
		length = self.p
		return_val = []
		for p in range(0, num_points):
			ind = random.randint(0, length)
			return_val.append(coords_cp[ind])
			del coords_cp[ind]

		return return_val



	def multiply(self, k, P):
		Q = INF_POINT
		while k != 0:
			if k & 1 != 0:
				Q = self.addition(Q, P)
			P = self.addition(P, P)
			k >>= 1
		return Q

	def check_point(self, point):
		(x, y) = point
		# print("Y^2%P: " + str(self.reduce_mod_p(y*y)))
		#print(self.reduce_mod_p(x**3 + self.a * x + self.b))
		return self.equal_mod_p(y**2, x**3 + self.a * x + self.b)




# Gathers input from user
def get_inp():
	good_A = False
	good_B = False
	good_P = False

	p = None
	a = None
	b = None

	print_Inp(p, a, b)
	while(not good_P):
		inp = None
		inp = int(input("Enter a value for P: "))
		if(isPrime(inp)):
			p = inp
			good_P = True
			print_Inp(p, a, b)
		else:
			print_Inp(p, a, b)
			print("{red}Conditions for 'P':\nP-value must be prime{white}".format(red=red_color, white=white_color))
	while(not good_A):
		# print_Inp(p, a, b)
		inp = None
		inp = int(input("Enter a value for A: "))
		if((inp < 0) or (inp >= p)):
			print_Inp(p, a, b)
			good_A = True
			# print("{red}Conditions for 'A':\nA >= 0, A < P{white}".format(red=red_color, white=white_color))
		else:
			a = inp
			good_A = True
			print_Inp(p, a, b)
	while(not good_B):
		# print_Inp(p, a, b)
		inp = None
		inp = int(input("Enter a value for B: "))
		if((inp < 0) or (inp >= p)):
			print_Inp(p, a, b)
			good_B = True
			# print("{red}Conditions for 'B':\nB >= 0, B < P{white}".format(red=red_color, white=white_color))
			# print_Inp(p, a, b)
		else:
			b = inp
			good_B = True
			print_Inp(p, a, b)

	return p, a, b


# Prints input
def print_Inp(p, a, b):
	p_color = red_color
	a_color = red_color
	b_color = red_color

	if(not (p==None)):
		p_color = green_color
	if(not (a==None)):
		a_color = green_color
	if(not (b==None)):
		b_color = green_color

	clear()
	print('-'*30)
	print("{p_col}P: {p_val}\n{a_col}A: {a_val}\n{b_col}B: {b_val}{white}".format(p_val=p, a_val=a, b_val=b, p_col=p_color, a_col=a_color, b_col=b_color, white=white_color))
	print('-'*30)

def clear():
	command = ('clear' if os.name =='posix' else 'cls')
	os.system(command)



def power(x, y, p):
     
    # Initialize result
    res = 1
     
    # Update x if it is more than or
    # equal to p
    x = x % p
    while (y > 0):
         
        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p
 
        # y must be even now
        y = y>>1 # y = y/2
        x = (x * x) % p
     
    return res

def miillerTest(d, n):
     
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4)
 
    # Compute a^d % n
    x = power(a, d, n)
 
    if (x == 1 or x == n - 1):
        return True;
 
    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n
        d *= 2

        if (x == 1):
            return False
        if (x == n - 1):
            return True
 
    # Return composite
    return False

def isPrime(n):

	k = 4
     
    # Corner cases
	if (n <= 1 or n == 4):
		return False
	if (n <= 3):
		return True

	# Find r such that n =
	# 2^d * r + 1 for some r >= 1
	d = n - 1
	while (d % 2 == 0):
		d //= 2

	# Iterate given number of 'k' times
	for i in range(k):
		if (miillerTest(d, n) == False):
			return False

	return True



# Get input from user
# inp = get_inp()
# p = inp[0]
# a = inp[1]
# b = inp[2]

# # Bitcoin values
# p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
# a = 0
# b = 7
# # Bitcoin generator point
# p1 = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)


p = 7
a = 3
b = 2
p1 = (2, 3)
p2 = (4, 6)

testCurve = EllipticCurve(p, a, b)
print(testCurve.return_random_points(2))

# p1 = (55, 22) # true
# print(testCurve.check_point(p1))
# p1 = (53, 53) # true
# print(testCurve.check_point(p1))
# p1 = (53, 26) # true
# print(testCurve.check_point(p1))
# p1 = (54, 22) # false
# print(testCurve.check_point(p1))
# p1 = (32, 9) # true
# print(testCurve.check_point(p1))
# p1 = (17, 22) # false
# print(testCurve.check_point(p1))



# print(testCurve.addition(p1, p2))
# print(testCurve.check_point(p2))









