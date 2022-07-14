from tabulate import tabulate
import random
import os

red_color="\033[1;31m"
green_color="\033[0;32m"
yellow_color="\033[0;33m"
purple_color="\033[0;35m"
cyan_color="\033[0;36m"
blue_color="\033[0;34m"
white_color="\033[0;37m"


# Represents an Elliptic Curve
class EllipticCurve:
	mult_table = []
	def __init__(self, p, a, b):
		self.p = p
		self.a = a
		self.b = b
		

	def gen_tables(self):

		for i in range (0, self.p):
			temp_arr = []
			for j in range(0, self.p):
				temp_int = (i*j)%self.p
				temp_arr.append(temp_int)
			self.mult_table.append(temp_arr)
	def print_table():
		print(self.mult_table)



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
			print("{red}Conditions for 'A':\nA >= 0, A < P{white}".format(red=red_color, white=white_color))
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
			print("{red}Conditions for 'B':\nB >= 0, B < P{white}".format(red=red_color, white=white_color))
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
inp = get_inp()

testCurve = EllipticCurve(inp[0], inp[1], inp[2])

testCurve.gen_tables()

print(tabulate(testCurve.mult_table))



















