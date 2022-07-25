
from sympy import *
import matplotlib.pyplot as plt
import numpy as np
from sage.all import *



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


    def cantors_algorithm(self, divisors):
        # print(divisors)

        divisor1 = divisors[0]
        divisor2 = divisors[1]

        u1, v1 = divisor1
        u2, v2 = divisor2

        e1, e2, c1, c2= symbols("e1 e2 c1 c2")

        d1 = gcd(u1, u2)
        # print("E1, E2: " + str(solve(Eq(e1 * u1 + e2 * u2, d1), e1, e2)))
        d = gcd(d1, v1 + v2)

        u1 = self.reduce_equation_mod_p(u1)
        u2 = self.reduce_equation_mod_p(u2)

        d1 = self.reduce_mod_p(d1)
        d = self.reduce_mod_p(d)

        # print(f"gcd({u1}, {u2}): {d1}, gcd({d1}, {v1} + {v2}): {d}, u1: {u1}, u2: {u2}")
        # print("C1, C2: " + str(solve(Eq(c1 * d1 + c2 *(v1 + v2), d), c1, c2)))

        e_dict = solve(Eq(e1 * u1 + e2 * u2, d1), e1, e2)
        print(e_dict)
        e_dict = solve(Eq(e1 * u1 + e2 * u2, d1), e2, e1)
        print(e_dict)

        e1_val = solve((-e1*x**2 - 7*e1*x - 10*e1 + 1)/(x**2 + 10))[0][e1]
        print(e1_val)

        e2_val = solve((-e2*x**2 - 10*e2 + 1)/(x**2 + 7*x + 10))[0][e2]
        print(e2_val)
        
        # e1_val = 1/(2*u1)
        # e2_val = 1/(2*u2)

        # e1_eq = solve(Eq(e1 * u1 + e2 * u2, d1), e1, e2)
        # print(e1_eq[0])
        # print(solve((e1_eq[0])))


        # print(solve((-e1*x**2 - 7*e1*x - 10*e1 + 1)/(x**2 + 10), e1))
        # e_dict = solve(Eq(e1 * u1 + e2 * u2, d1), e1, e2)
        c_dict = solve(Eq(c1 * d1 + c2 *(v1 + v2), d), c1, c2)

       

        # print(e_dict)
        # print(c_dict)

        # print(simplify(e_dict[0][0]))

        # print(self.reduce_equation_mod_p(cancel(u1 * u2)))

        # e1_val = e_dict[e1]
        # e2_val = e_dict[e2]
        c1_val = c_dict[c1]
        c2_val = c_dict[c2]

        



        print(f"e1: {e1_val}, e2: {e2_val}, c1: {c1_val}, c2: {c2_val}")

        s1 = (c1_val * e1_val)
        s2 = (c1_val * e2_val)
        s3 = c2_val

        u = (u1 * u2) / d**2

        # Need to find a way to call xgcd() from sage math


        u = self.reduce_equation_mod_p(cancel(u))
        print(u)
        # v = simplify(self.reduce_modulo_poly((((s1*u1*v2)+(s2*u2*v1)+(s3*(v1*v2+(self.eq)))) / d), u))
        v = div(self.reduce_equation_mod_p(s1*u1*v2+s2*u2*v1), u)[1]

        print(v)
        while(degree(u) > 2):

            u_prime = u_prime = div((self.eq - simplify(cancel(v**2))), u)[0]
            v_prime = (div(-1*v, u_prime)[1])

            u = u_prime
            v = v_prime

        u = monic(u)

        u = self.reduce_equation_mod_p(u)
        v = self.reduce_equation_mod_p(v)
        print("u3: " + str(u))
        print("v3: " + str(v))




p = 11
c1 = 1
c2 = 0
c3 = 3
c4 = 7
c5 = 1
c6 = 2

x = Symbol("x")

new_divisors = [[x**2 + 7*x + 10, x + 9], [x**2 + 10, 7*x + 9]]

hec = HyperEllipticCurve(p, c1, c2, c3, c4, c5, c6)
hec.cantors_algorithm(new_divisors)

