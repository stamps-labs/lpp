from pprint import pprint

def dot(a, b):
    assert len(a) == len(b), "The length of a and b must match"
    return sum([a_i * b_i for a_i, b_i in zip(a, b)])


def solve_lpp(n, m, c, A, b, task='min'):
    # Right hand side must be positive
    if any([b_i < 0 for b_i in b]):
        print("The method is not applicable!")
        return None, None
    
    # For maximization task just multiply objective by -1 and minimize it
    if task == 'max':
        c = [-c_i for c_i in c]
    
    # Find basis as column of 0 but one 1.
    basis = [-1] * m
    for col in range(n):
        column = [A[row][col] for row in range(m)]
        if column.count(0) == m - 1 and column.count(1) == 1:
            basis[column.index(1)] = col
    if any([basis_i < 0 for basis_i in basis]):
        print("There are no identity in matrix of coefficients")
    c_b = [c[basis_i] for basis_i in basis]


    minima = float('inf')
    solution = [0 for col in range(n)]

    while True:
        # Calculate delta to know solution is optimal or to find leading column
        delta_b = dot(c_b, b)
        delta = []
        for col in range(n):
            column = [A[row][col] for row in range(m)]
            delta.append(dot(c_b, column) - c[col])
        
        # if there are no positive values in delta, solution is optimal
        if max(delta) <= 0:
            minima = delta_b
            for i, basis_i in enumerate(basis):
                solution[basis_i] = b[i]
            if task == 'min':
                return minima, solution
            else:
                return -minima, solution

        # Find leading column, row and element
        leading_column = delta.index(max(delta))
        column = [A[row][leading_column] for row in range(m)]
        ratio = [b_i / column_i if column_i != 0 else -1 for b_i, column_i in zip(b, column)]
        leading_row = ratio.index(min(filter(lambda x: x > 0, ratio)))
        leading_element = A[leading_row][leading_column]
        
        # Calculate new A, b and c.
        new_A = [[float('inf') for col in range(n)] for row in range(m)]
        new_b = [float('inf') for row in range(m)]
        new_c = [float('inf') for col in range(n)]

        for col in range(n):
            new_A[leading_row][col] = A[leading_row][col] / leading_element
        new_b[leading_row] = b[leading_row] / leading_element
        
        for col in range(n):
            for row in range(m):
                if row == leading_row:
                    continue
                new_A[row][col] = A[row][col] - A[row][leading_column] * new_A[leading_row][col]
        for row in range(m):
            if row == leading_row:
                continue
            new_b[row] = b[row] - A[row][leading_column] * new_b[leading_row]
        for col in range(n):
            new_c[col] = c[col] - c[leading_column] * new_A[leading_row][col]

        # replace old A, b and c with new ones and go to next iteration.
        A = new_A
        b = new_b
        c = new_c
        c_b[leading_row] = c[leading_column]
        basis[leading_row] = leading_column


def main():
    task = input("Enter the task ('min' for minize and 'max' for maximize): ")
    assert task in ['min', 'max'], "The task must be either 'min' or 'max'"
    n = int(input("Enter the number of variables: "))
    m = int(input("Enter the number of constraints: " ))

    c = [int(x) for x in input("Enter the vector of coefficients of objective function: ").split()]
    assert len(c) == n, "The length of vector of coefficients of objective function must be equal to number of variables"
    print("Enter the matrix of coefficients of constraint function:")
    A = [[int(x) for x in input().split()] for _ in range(m)]
    assert len(A) == m and len(A[0]) == n, "The shape of matrix of coefficients of constraint function must be equal (number of constraints x number of variables)"
    b = [int(x) for x in input("Enter the vector of right-hand side numbers: ").split()]
    assert len(b) == m, "The length of vector of right-hand side numbers must be equal to number of constraints"
    
    precision = int(input("Enter the approximation accuracy (number of decimal digits): "))

    optima, solution = solve_lpp(n, m, c, A, b, task)
    
    if optima:
        if task == 'min':
            print("Minima: ", round(optima, precision))
        else: 
            print("Maxima: ", round(optima, precision))
        print("Solution: ", [round(elem, precision) for elem in solution])


if __name__ == '__main__':
    main()