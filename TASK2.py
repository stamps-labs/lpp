import numpy
import numpy as np
from numpy.linalg import norm

task = input("Enter the task ('min' for minize and 'max' for maximize): ")
assert task in ['min', 'max'], "The task must be either 'min' or 'max'"
n = int(input("Enter the number of variables: "))
m = int(input("Enter the number of constraints: "))


c = [float(x) for x in input("Enter the vector of coefficients of objective function: ").split()]
assert len(c) == n, "The length of vector of coefficients of objective function must be equal to number of variables"
print("Enter the matrix of coefficients of constraint function:")
A = [[float(x) for x in input().split()] for _ in range(m)]
assert len(A) == m and len(A[
                               0]) == n, "The shape of matrix of coefficients of constraint function must be equal (number of constraints x number of variables)"
b = [float(x) for x in input("Enter the vector of right-hand side numbers: ").split()]
assert len(b) == m, "The length of vector of right-hand side numbers must be equal to number of constraints"
x = [float(x) for x in input("Enter the vector of initial interior solution ").split()]
precision = int(input("Enter the approximation accuracy (number of decimal digits): "))

x = np.array(x, float)
b = np.array(b, float)
A = np.array(A, float)
c = np.array(c, float)
if task == "min":
    c = [-1 * x for x in c]
if not (all(val >= 0 for val in b)):
    print("Vector b contains non-positive values the method is not applicable.")
    exit()
if not (all(val != 0 for val in x)) or  not(np.array_equal(A @ x  ,b)):
    print("The initial solution is wrong")
    exit()




def solve_with_interior_point_method(A_in, c_in, x_in,alpha):
    i = 1
    while True:
        v = x_in
        D = np.diag(x_in)

        AA = np.dot(A_in, D)
        cc = np.dot(D, c_in)
        I = np.eye(len(c_in))
        F = np.dot(AA, np.transpose(AA))
        FI = np.linalg.inv(F)
        H = np.dot(np.transpose(AA), FI)
        P = np.subtract(I, np.dot(H, AA))
        cp = np.dot(P, cc)
        nu = np.absolute(np.min(cp))
        y = np.add(np.ones(len(c_in), float), (alpha / nu) * cp)
        yy = np.dot(D, y)

        x_in = yy




        if norm(np.subtract(yy, v), ord=2) < 0.0001:
            break
        else:
            print("In iteration  ", i, " we have x = ", [round(elm, precision) for elm in x_in], "\n")
            i = i + 1


    print("In the last iteration  ", i, "  we have x=  \n", [round(elm, precision) for elm in x_in],"\n")
    if task=="max":
        print("the objective equal  \n", np.dot(c_in, x_in), "\n")
    else:
      print("the objective equal  \n", np.dot(c_in,x_in)*-1, "\n")


solve_with_interior_point_method(A, c, x,0.5)

solve_with_interior_point_method(A, c, x,0.9)
