from tabulate import tabulate
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



class HypEllipticCurve:

	def __init__(self, p):
		self.p = p

	def calculate_yy(self, new_x, exp):
		new_exp = exp.subs(x, new_x)

		yy = new_exp
		return yy
	def calculate_list(self, exp):
		yy_list =[]
		for i in range (0, self.p):
			yy_list.append(self.calculate_yy(i, exp))

		return yy_list
	def x_list(self):
		x_list = []
		for i in range(0, self.p):
			x_list.append(i)
		return x_list


def get_inp():

	good_P = False

	p = None
	

	print_Inp(p)
	while(not good_P):
		inp = None
		inp = int(input("Enter a value for P: "))
		if(isPrime(inp)):
			p = inp
			good_P = True
			print_Inp(p)
		else:
			print_Inp(p)
			print("{red}Conditions for 'P':\nP-value must be prime{white}".format(red=red_color, white=white_color))

	return p


# Prints input
def print_Inp(p):
	p_color = red_color

	if(not (p==None)):
		p_color = green_color


	clear()
	print('-'*30)
	print("{p_col}P: {p_val}{white}".format(p_val=p, p_col=p_color, white=white_color))
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


x = Symbol("x")
new_exp = x**5 - x**4 - (11*x)**3 +(9*x)**2 + 18 * x

inp = get_inp()
hec = HypEllipticCurve(inp)

print(hec.calculate_yy(20, new_exp))

point_list = []
point_list.append(hec.x_list())
point_list.append(hec.calculate_list(new_exp))

print(point_list[0])
print("\n")
print(point_list[1])
