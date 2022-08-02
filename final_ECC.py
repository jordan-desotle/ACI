import random
import os
from sympy import *
import math as m

red_color="\033[1;31m"
green_color="\033[1;32m"
yellow_color="\033[0;33m"
purple_color="\033[0;35m"
cyan_color="\033[0;36m"
blue_color="\033[0;34m"
white_color="\033[0;37m"


INF_POINT = None
PATH = './output'
FILE = '/output.txt'




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
		else:
			s = (self.reduce_mod_p(y1 - y2)) * (self.inverse_mod_p(x1 - x2))

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

	def return_random_points(self, num_points):
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

		coords_cp = coords
		length = self.p
		return_val = []
		for p in range(0, num_points):
			ind = random.randint(0, length)
			return_val.append(coords_cp[ind])
			del coords_cp[ind]

		print("Getting random points: ")

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
		return self.equal_mod_p(y**2, x**3 + self.a * x + self.b)

	def generate_psuedo_random_nums(self, num, point, counter):
		file = open(PATH + FILE, "w")
		c = counter
		p = point
		k = num
		while c > 0:
			p = self.multiply(k, p)
			k = p[1]
			c-=1
			bin_rep = bin(k).replace("0b", "")
			file.write(bin_rep + "\n")
			print('[{count:0>5}]: {y}'.format(count=counter-c, y=k, b=bin_rep))

def monobitTest():
	file = open(PATH + FILE, "r")
	total_result = 0
	c = 0
	for i in file:
		n = len(i)
		s = 0
		for j in i:
			if(j=="0"):
				s-=1
			elif(j=="1"):
				s+=1
		c+=1

		sobs = abs(s)/float(m.sqrt(n))
		p_val = m.erfc(m.fabs(sobs) / m.sqrt(n))
		total_result += p_val

		# print('[{count:0>5}]: Sum: {sum} Length: {len} Stat: {stat} PVal: {p}'.format(count=c, len=n, sum=s, stat=sobs, p=p_val))
	total_randomness = (total_result / c)*100
	print("Total Randomness: {r:.4}%".format(r=total_randomness))

		




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
    res = 1

    x = x % p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p

        y = y>>1
        x = (x * x) % p
     
    return res

def miillerTest(d, n):

    a = 2 + random.randint(1, n - 4)

    x = power(a, d, n)
 
    if (x == 1 or x == n - 1):
        return True;

    while (d != n - 1):
        x = (x * x) % n
        d *= 2

        if (x == 1):
            return False
        if (x == n - 1):
            return True

    return False

def isPrime(n):
	k = 4
     
	if (n <= 1 or n == 4):
		return False
	if (n <= 3):
		return True

	d = n - 1
	while (d % 2 == 0):
		d //= 2

	for i in range(k):
		if (miillerTest(d, n) == False):
			return False

	return True

def print_general_exchange():
	data = []

	general_text = "{color}A curve 'C' is picked and communicated between Bob and Alice{white}".format(color=yellow_color, white=white_color)
	data.append(["C", "C", "C"])
	update_data(general_text, data)
	input("")

	general_text = "{color}Alice and Bob both agree on a point on the curve 'C'.\nThis is known as the generator point 'G'{white}".format(color=yellow_color, white=white_color)
	data.append(["G", "G", "G"])
	update_data(general_text, data)
	input("")

	general_text = "{color}Alice and Bob now create their own private keys 'a' and 'b'{white}".format(color=yellow_color, white=white_color)
	data.append(["a", "", "b"])
	update_data(general_text, data)
	input("")

	general_text = "{color}Alice multiplies the generator point 'G' by her private key 'a' to get her public key 'aG'.\nShe then sends this to Bob{white}".format(color=yellow_color, white=white_color)
	data.append(["aG", "aG", "aG"])
	update_data(general_text, data)
	input("")

	general_text = "{color}Bob generates his public key the same way 'bG' and sends this to Alice{white}".format(color=yellow_color, white=white_color)
	data.append(["bG", "bG", "bG"])
	update_data(general_text, data)
	input("")

	general_text = "{color}With eachothers public keys, Alice and Bob can multiply them by their private keys to get the secret key\nThe point generated will be private to Alice and Bob due to their private keys being unknown{white}".format(color=yellow_color, white=white_color)
	data.append(["abG", "", "baG"])
	update_data(general_text, data)
	input("")

	general_text = "{color}With an unknown point to the Middle Man on the curve, Alice and Bob can choose to use either the X-value or the Y-value as their encryption key{white}".format(color=yellow_color, white=white_color)
	print(general_text)


def update_data(general_text, data):
	clear()
	print_boxs(data)
	print(general_text)

def print_boxs(data):
	min_leng = 20
	min_lines = 4
	for j in data:
		if(len(j) > min_leng):
			min_leng = len(j)
	min_leng += 4

	if(len(data)> min_lines):
		min_lines = len(data)

	names = ["Alice", "Middle Man", "Bob"]
	box = cyan_color

	print('{color}{name:^{length}}{space}'.format(name=names[0], length=min_leng+2, space=' '*5, color=green_color) + '{color}{name:^{length}}{space}'.format(name=names[1], length=min_leng+2, space=' '*5, color=red_color) + '{color}{name:^{length}}{space}'.format(name=names[2], length=min_leng+2, space=' '*5, color=green_color))
	print('{box_color}┌{line}┐{white}{space}'.format(line='─'*min_leng, space=' '*5, box_color=box, white=white_color)*3)
	if len(data) == 0:
		for i in range(0, min_lines):
			print('{box_color}│{white}{line}{box_color}│{white}{space}'.format(line=' '*min_leng, space=' '*5, box_color=box, white=white_color)*3)
		print('{box_color}└{line}┘{white}{space}'.format(line='─'*min_leng, space=' '*5, box_color=box, white=white_color)*3)
	else:
		cnt = 0
		for i in data:
			print('{box_color}│{white}{line:^{length}}{box_color}│{white}{space}'.format(line=str(i[0]), length=min_leng, space=' '*5, white=white_color, box_color=box) + '{box_color}│{white}{line:^{length}}{box_color}│{white}{space}'.format(line=str(i[1]), length=min_leng, space=' '*5, white=white_color, box_color=box) + '{box_color}│{white}{line:^{length}}{box_color}│{white}{space}'.format(line=str(i[2]), length=min_leng, space=' '*5, white=white_color, box_color=box))
			cnt += 1
		if(cnt < min_lines):
			for i in range(cnt, min_lines):
				print('{box_color}│{line}│{white}{space}'.format(line=' '*min_leng, space=' '*5, box_color=box, white=white_color)*3)
				cnt += 1
	print('{box_color}└{line}┘{white}{space}'.format(line='─'*min_leng, space=' '*5, box_color=box, white=white_color)*3)


def checkPath():
	if(not os.path.exists(PATH)):
		os.mkdir(PATH)
		print("Creating Directory")
		file = open(PATH + "/output.txt", "x")
	else:
		print("Directory already exists")
		if(os.path.exists(PATH + "/output.txt")):
			print("File already exists")
		else:
			print("Creating file")
			file = open(PATH + "/output.txt", "x")
	clear()

	



# Bitcoin values
p = 71226472761329746781570947201
a = 0
b = 7

# Bitcoin generator point
p1 = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)


testCurve = EllipticCurve(p, a, b)

checkPath()


# clear()
# print_Inp(p, a, b)
# print_general_exchange()
testCurve.generate_psuedo_random_nums(100, p1, 200)
# testCurve.generate_psuedo_random_nums(random.randint(0, p1[0]), p1, 200)

# monobitTest()


