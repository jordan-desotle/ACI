from sympy import *
from sympy import gcd as sm
from sympy import simplify as simp
from sympy import solve as sol
import matplotlib.pyplot as plt
import numpy as np
import collections

from sage.all import *
import sage.categories.all

from sage.categories.category_singleton import Category_singleton
from sage.misc.abstract_method import abstract_method
from sage.categories.fields import Fields

from sage.structure.element import coerce_binop



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

    def get_eq(self):
        return self.eq
    def reduce_mod_p(self, num):
        return (num % self.p)

    def equal_mod_p(self, num1, num2):
        return (self.reduce_mod_p(num1 - num2) == 0)

    def inverse_mod_p(self, num):
        if(self.reduce_mod_p(num) == 0):
            return None
        return pow(num, self.p - 2, self.p)

    def reduce_modulo_poly(self, poly, mod):
        print(poly)
        print(mod)
        remainder = prem(poly, mod)
        return remainder

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

    def reduce_coefficients(self, coeffs):
        #print("Before: " + str(coeffs))
        new_coeffs = []
        for i in coeffs:
            n = self.reduce_mod_p(i)
            new_coeffs.append(n)
        #print("After: " + str(new_coeffs))

        return new_coeffs

    def sage_cantor(self, d1, d2, eq, p_val):
        R = sage.all.PolynomialRing(GF(Integer(p_val)), names=('x',)); (x,) = R._first_ngens(1)
        D3 = sage.schemes.hyperelliptic_curves.jacobian_morphism.cantor_composition_simple(d1, d2, eq, Integer(2))
        D3_reduced = sage.schemes.hyperelliptic_curves.jacobian_morphism.cantor_reduction_simple(D3[0], D3[1], eq, 2)
        return D3_reduced

    def pseudo_random_nums(self, D3):
        u = D3[0]
        v = D3[1]
        roots = []
        
        roots.append(u.roots()[0][0])
        roots.append(u.roots()[1][0])
        random_num = v(x=roots[1])
        return random_num

    def fix_new_points(self, point_list):
        D1 = []
        D2 = []
        x1, y1 = point_list[0]
        x2, y2 = point_list[1]
        x3, y3 = point_list[2]
        x4, y4 = point_list[3]


        x1 = int(x1/2)
        x2 = int(x2-73)
        x3 = int(x3/3)
        x4 = int(x4-81)

        y1 = self.get_eq().subs(x, x1) % self.p
        y2 = self.get_eq().subs(x, x2) % self.p
        y3 = self.get_eq().subs(x, x3) % self.p
        y4 = self.get_eq().subs(x, x4) % self.p

        D1.append([x1, y1])
        D1.append([x2, y2])
        D2.append([x3, y3])
        D2.append([x4, y4])

        return [D1, D2] 

    def compare_points(self, point_list):

        counter_list = []
        for i in range (0, 4):

            counter_list.append(collections.Counter(point_list[i]))
        
        match = False
        for i in range (0, 4):
            for j in range (0, 4):
                if (counter_list[i] == counter_list[j]):
                    match = True
        return match

    def mumford_rep(self, D1, D2):
        divisors = [D1, D2]
        
        new_divisors = []
        for i in divisors:
            mum_rep = []
            # print(i)

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

            solved = sol(system_of_equations)
            
            # print(solved)

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
    def solve_for_new_points(self, x1, x2, coeffs):
        eq = 0
        y1 = 0 
        y2 = 0
        
        x = Symbol('x')
        degree = len(coeffs)
        for i in range(0, degree):
            eq = eq + coeffs[i]*x**(degree-(i+1))
        try: 
            y1 = eq.subs(x, x1)
            y2 = eq.subs(x, x2)
        except:
            valid = False
            i = 0
            while (valid == False):
                try:
                    temp_eq = 0
                    temp_coeffs = all_two_root_divs[-(i+1)][1].coefficients()
                    degree = len(temp_coeffs)
                    for i in range(0, degree):
                        temp_eq = temp_eq + temp_coeffs[i]*x**(degree-(i+1))
                    print("Equation: " + str(temp_eq))
                    temp_x1 = all_two_root_divs[-(i+1)][0].roots()[0][0]
                    temp_x2 = all_two_root_divs[-(i+1)][0].roots()[1][0]

                    y1 = temp_eq.subs(x, temp_x1)
                    y2 = temp_eq.subs(x, temp_x2)
                    valid = True
                except:
                    print("Didn't Work")
                    i += 1
            # y1 = int(eq)
            # y1 = int(eq)
        new_divisor = [[x1, y1], [x2, y2]]
        return new_divisor


    def cantors_algorithm(self, divisors, n, p_val):
        # print(divisors)

        divisor1 = divisors[0]
        divisor2 = divisors[1]

        u1, v1 = divisor1
        u2, v2 = divisor2

        e1, e2, c1, c2= symbols("e1 e2 c1 c2")
        need_num = False
        
        d1 = sm(u1, u2) #assigns the gcd of u1 and u2 to d1
        # print(d1)
        # print("E1, E2: " + str(solve(Eq(e1 * u1 + e2 * u2, d1), e1, e2)))
        d = sm(d1, v1 + v2) #assigns the gcd of d1 and v1+v2 to d (note, if the h(x) in your curve is not 0, add h to v1+v2)

        x = Symbol('x')

        #pulls the coefficients out of the Divisors for a later step (denoted by an *)
        u1_coeffs = poly(u1, x).all_coeffs()
        u2_coeffs = poly(u2, x).all_coeffs()   
        v1_coeffs = poly(v1, x).all_coeffs()
        v2_coeffs = poly(v2, x).all_coeffs()  
        d_coeffs = poly(d, x).all_coeffs()
        eq_coeffs = poly(self.eq, x).all_coeffs()



        v1v2 = v1+v2
        
        v1v2_coeffs = poly(v1v2, x).all_coeffs()  
        d1_coeffs = poly(d1, x).all_coeffs()
        if len(d1_coeffs) == 1:
            d1_coeffs.append(d1_coeffs[0])
            d1_coeffs[0] = 0

        
        #creates a Galois field for us to use sagemath's cantor functions in with x as a variable name.
        R = sage.all.PolynomialRing(GF(Integer(p_val)), names=('x',)); (x,) = R._first_ngens(1)


        # * lines 250-261 turn the divisors and curve into an object that sagemath can use.
        u1 = int(u1_coeffs[0])*x**2+int(u1_coeffs[1])*x+int(u1_coeffs[2])
        u2 = int(u2_coeffs[0])*x**2+int(u2_coeffs[1])*x+int(u2_coeffs[2])
        if (len(v1_coeffs) == 1):    
            v1 = int(v1_coeffs[0])
        else:
            v1 = int(v1_coeffs[0])*x+int(v1_coeffs[1])
        if (len(v2_coeffs) == 1):    
            v2 = int(v2_coeffs[0])
        else:
            v2 = int(v2_coeffs[0])*x+int(v2_coeffs[1])
        
        eq = eq_coeffs[0]*x**5 + eq_coeffs[1]*x**4 + eq_coeffs[2]*x**3 + eq_coeffs[3]*x**2 + eq_coeffs[4]*x + eq_coeffs[5]

        D1 = [u1, v1]
        D2 = [u2, v2]

        D3 = sage.schemes.hyperelliptic_curves.jacobian_morphism.cantor_composition_simple(D1, D2, eq, Integer(2))
        D3_reduced = sage.schemes.hyperelliptic_curves.jacobian_morphism.cantor_reduction_simple(D3[0], D3[1], eq, 2)


        d_arr = [D1, D2, D3]

        two_root_divs = []
        for i in range (0, n):
            
            #assigns the divisor that's two away from the iteration number to temp_d2
            # which is then plugged into cantor's algorithm with D1. 
            # example: on iteration 3, it will add D1 and D5
            temp_d2 = d_arr[i+2]
            D3_reduced = self.sage_cantor(D1, temp_d2, eq, p_val)

            #if the new D3 has two roots, there aren't already a full pair of two root divisors, and D3's v isn't an integer,
            # add D3 to the two root divisors list.
            if (len(D3_reduced[0].roots()) > 1 and len(two_root_divs) < 2):
                two_root_divs.append(D3_reduced)
                
            if (i == n-1):
                #if a full pair of two root divisors was never found, pull the 3rd and 2nd to last from the master list of 
                #two root divisors
                if (len(two_root_divs) < 2):
                
                    for j in range (0, (2 - len(two_root_divs))):
                        two_root_divs.append(all_two_root_divs[-(j+1)])
                    
                if (len(D3_reduced[0].roots()) < 2):
                    for j in range (0, n):
                        temp_d2 = d_arr[j]
                        D3_reduced = self.sage_cantor(temp_d2, D3_reduced, eq, p_val)
                        if(len(D3_reduced[0].roots()) > 1):
                            two_root_divs[1] = D3_reduced
                            break
                if (len(D3_reduced[0].roots()) < 2):
                    
                    if (type(D3_reduced[1]) == int):
                        if(D3_reduced[1] == 0):
                            random_num = D3_reduced[0].coefficients()[1]
                        else:

                            random_num = D3_reduced[1]
                    else:
                        if (len(D3_reduced[1].coefficients()) == 1):
                            random_num = D3_reduced[1].coefficients()[0]
                        elif (len(D3_reduced[1].coefficients()) == 2):
                            random_num = D3_reduced[1].coefficients()[1]
                else:
                    need_num = True


            d_arr.append(D3_reduced)
            

        length = len(d_arr) - 1
        
        new_points = []
        
        
        for i in two_root_divs:
            degree = len(i[1].coefficients())
            v3_coeffs = i[1].coefficients()
            x1 = i[0].roots()[0][0]
            x2 = i[0].roots()[1][0]
            new_points.append(self.solve_for_new_points(x1, x2, v3_coeffs))
        if (need_num == True):
            random_num = self.pseudo_random_nums(two_root_divs[1])
        return [random_num, new_points, two_root_divs]

p = 11
c1 = 1
c2 = 0
c3 = 3
c4 = 7
c5 = 1
c6 = 2

random_nums = []

FILE = "random_nums.txt"
x = Symbol("x")
# p_val = 20988936657440586486151264256610222593863921 #144 bit | trial 1(Hyperelliptic) + 2(Elliptic) 
# p_val = 237512715131811281324243117391942323623 # 128 bit | trial 3(Hyperelliptic) + 4(Elliptic)
# p_val = 115792089237316195423570985008687907853269984665640564039457584007908834671663 # 256 bit | trial 5(Hyperelliptic) + 6(Elliptic)
# p_val = 6957596529882152968992225251835887181478451547013  # 160 bit | trial 7(Hyperelliptic) + 8(Elliptic)
# p_val = 71226472761329746781570947201  # 96 bit | trial 9(Hyperelliptic) + 10(Elliptic)
p_val= 997

new_divisors = [[x**2 + 7*x + 10, x + 9], [x**2 + 10, 7*x + 9]]
n = 100
random_num = 0
all_two_root_divs = []

hec = HyperEllipticCurve(p, c1, c2, c3, c4, c5, c6)
for i in range(0, 200):

    cantors_results = []
    # Assigns the random_num returned from cantors_algorithm to new_num
    cantors_results = hec.cantors_algorithm(new_divisors, n, p_val)
    new_num = cantors_results[0]
    new_points = []
    
    #assigns the points for the new starting divisors to new_D1 and new_D2 respectively
    new_D1 = cantors_results[1][0]
    new_D2 = cantors_results[1][1]
    
    #puts the new divisors into muford representation
    new_divisors = hec.mumford_rep(new_D1, new_D2)

    #In the even that the number is less than 10000000000000000000000000000000000000, 
    #this does point addition again until its high enough.
    while (new_num < 10000000000000000000000000):
        cantors_results = hec.cantors_algorithm(new_divisors, n, p_val)
        new_num = cantors_results[0]
        new_points = []
        
        new_D1 = cantors_results[1][0]
        new_D2 = cantors_results[1][1]
        new_divisors = hec.mumford_rep(new_D1, new_D2)
    print(str(i+1) + ": " + str(new_num))

    #Adds the new random number to random_nums
    random_nums.append(new_num)

    #adds the two root divisors from the last iteration to a master list
    # in case a future iteration doesn't produce enough
    for j in cantors_results[2]:
        all_two_root_divs.append(j)
        

file = open(FILE, "w")
for i in random_nums:
    # file.write(bin(i).replace("0b", "") + "\n")
    file.write(str(i) + "\n")


