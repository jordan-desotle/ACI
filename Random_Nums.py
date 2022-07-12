import random
import os

red_color="\033[1;31m"
green_color="\033[0;32m"
yellow_color="\033[0;33m"
purple_color="\033[0;35m"
cyan_color="\033[0;36m"
blue_color="\033[0;34m"
white_color="\033[0;37m"


#Represents elliptic curves
class EllipticCurve:
	def __init__(self, p, a, b):
		self.p = p
		self.a = a
		self.b = b



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
		if(is_Prime(inp)):
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

	os.system("clear")
	print('-'*30)
	print("{p_col}P: {p_val}\n{a_col}A: {a_val}\n{b_col}B: {b_val}{white}".format(p_val=p, a_val=a, b_val=b, p_col=p_color, a_col=a_color, b_col=b_color, white=white_color))
	print('-'*30)



 
def is_Prime(n):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
 
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(8):#number of trials 
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True  




# Get input from user
inp = get_inp()


testCurve = EllipticCurve(inp[0], inp[1], inp[2])





















