from sympy import solve, symbols

a,b,c,d=symbols('a,b,c,d')
#4 Points on a Hyperelliptic Curve
p1 = [3,0]
p2 = [1,2]
p3 = [4,1]
p4 = [1,3]

#Systems of Equations to Solve for a,b,c,d
#y=ax^3+bx^2+cx+d
eq1 = a*((p1[0])*(p1[0])*(p1[0]))+b*(p1[0]**2)+c*p1[0]+d-p1[1]
print(eq1)

eq2 = a*((p2[0])*(p2[0])*(p2[0]))+b*(p2[0]**2)+c*p2[0]+d-p2[1]
print(eq2)

eq3 = a*((p3[0])*(p3[0])*(p3[0]))+b*(p3[0]**2)+c*p3[0]+d-p3[1]
print(eq3)

eq4 = a*((p4[0])*(p4[0])*(p4[0]))+b*(p4[0]**2)+c*p4[0]+d-p4[1]
print(eq4)

res = solve((eq1, eq2, eq3, eq4))
print(res) 