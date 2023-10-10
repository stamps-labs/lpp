import numpy as np
import math

task = input("Enter the task ('min' for minize and 'max' for maximize): ")
assert task in ['min', 'max'], "The task must be either 'min' or 'max'"
n = int(input("Enter the number of variables: "))
m = int(input("Enter the number of constraints: "))

c = [int(x) for x in input("Enter the vector of coefficients of objective function: ").split()]
assert len(c) == n, "The length of vector of coefficients of objective function must be equal to number of variables"
print("Enter the matrix of coefficients of constraint function:")
A = [[int(x) for x in input().split()] for _ in range(m)]
assert len(A) == m and len(A[
                               0]) == n, "The shape of matrix of coefficients of constraint function must be equal (number of constraints x number of variables)"
b = [int(x) for x in input("Enter the vector of right-hand side numbers: ").split()]
assert len(b) == m, "The length of vector of right-hand side numbers must be equal to number of constraints"

precision = int(input("Enter the approximation accuracy (number of decimal digits): "))
if task == "min":
    c = [-1 * x for x in c]
if not(all(val >= 0 for val in b)):
    print("Vector b contains non-positive values the method is not applicable.")
    exit()

# Extract the last m rows by m columns of matrix A
identity_matrix = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
last_m_rows_m_columns = [row[-m:] for row in A[-m:]]
# last_m_rows_m_columns = [row[-m:] for row in A[-m:]]
# print(identity_matrix)
# print(last_m_rows_m_columns)
# Check if the extracted matrix is an identity matrix
if last_m_rows_m_columns != identity_matrix:
    print(f"The last {m} rows by {m} columns in matrix A do not form an identity matrix the method is not applicable.")
    exit()



def create_table(c, A, b):
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return xb + [z]
def vlaidate_improvment(tableau):
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])
def get_pivot_position(tableau):
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)

    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column


def aplly_row_opertaion(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier

    return new_tableau


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)
    print(round(tableau[-1][-1]*-1, precision))
    return solutions


def simplex(c, A, b):
    tableau = create_table(c, A, b)

    while vlaidate_improvment(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = aplly_row_opertaion(tableau, pivot_position)

    return get_solution(tableau)


solution = simplex(c, A, b)
print('solution: ',[round(elm, precision) for elm in solution[:-1]] )
