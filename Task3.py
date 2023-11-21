INF = 10 ** 3

ans = 0

import numpy as np
def print_parameter_table(S, C, D):
    num_sources = len(S)
    num_destinations = len(D)

    # Print header
    print(f"{'Sources/Destinations':<20}", end="")
    for j in range(num_destinations):
        print(f"{'Destination ' + str(j + 1):<15}", end="")
    print("Supply")

    # Print separator line
    print("=" * 50)

    # Print cost matrix and supply vector
    for i in range(num_sources):
        print(f"{'Source ' + str(i + 1):<20}", end="")
        for j in range(num_destinations):
            print(f"{C[i][j]:<15}", end="")
        print(S[i])

    # Print separator line
    print("=" * 50)

    # Print demand vector
    print("Demand" + " " * 15, end="")
    for j in range(num_destinations):
        print(f"{D[j]:<15}", end="")
    print("\n")


def find_most_negative_element_coordinates(matrix):
    if not matrix or not matrix[0]:
        return None  # Empty matrix

    # Initialize variables to store the coordinates of the most negative element
    min_value = float('inf')
    min_coordinates = None

    # Iterate through each element in the matrix
    ok = 0
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if (value < 0):
                ok = 1
            # Check if the current value is smaller than the current minimum
            if value < min_value:
                min_value = value
                min_coordinates = (i, j)

    return min_coordinates, ok


def Russel(supply_vector, demand_vector, cost_matrix):
    col = [max(row) for row in cost_matrix]

    # print("Maximum elements from each row:", col)

    row = [max(column) for column in zip(*cost_matrix)]

    # print("Maximum elements from each column:", row)

    copied_matrix = [[element for element in row] for row in cost_matrix]

    n = len(copied_matrix)
    m = len(copied_matrix[0])
    for i in range(n):
        for j in range(m):
            copied_matrix[i][j] = copied_matrix[i][j] - (row[j] + col[i])
        #     print(copied_matrix[i][j], end=" ")
        # print()
    zero_matrix = [[0 for _ in range(m)] for _ in range(n)]
    ok = 1
    while (ok == 1):
        coordinates, ok = find_most_negative_element_coordinates(copied_matrix)
        if (ok == 0):
            break
        r = coordinates[0]
        c = coordinates[1]
        if (supply_vector[r] >= demand_vector[c]):
            zero_matrix[r][c] = demand_vector[c]
            supply_vector[r] = supply_vector[r] - demand_vector[c]
            demand_vector[c] = 0
            for i in range(n):
                copied_matrix[i][c] = 1
        else:
            zero_matrix[r][c] = supply_vector[r]
            demand_vector[c] = demand_vector[c] - supply_vector[r]
            supply_vector[r] = 0
            for i in range(m):
                copied_matrix[r][i] = 1

    # for i in range(n):
    #     for j in range(m):
    #         print(zero_matrix[i][j], end=" ")
    #     print()
    print("initial basic feasible solution and cost using Russell’s approximation method:")
    print_allocation(zero_matrix)

    s = 0
    for i in range(n):
        for j in range(m):
            s = s + zero_matrix[i][j] * cost_matrix[i][j]
    print("cost",s)
def findDiff(cost_matrix):
    rowDiff = []
    colDiff = []
    for i in range(len(cost_matrix)):
        arr = cost_matrix[i][:]
        arr.sort()
        rowDiff.append(arr[1] - arr[0])
    col = 0
    while col < len(cost_matrix[0]):
        arr = []
        for i in range(len(cost_matrix)):
            arr.append(cost_matrix[i][col])
        arr.sort()
        col += 1
        colDiff.append(arr[1] - arr[0])
    return rowDiff, colDiff
def vogel(supply, demand, cost_matrix):
    n = len(cost_matrix)
    m = len(cost_matrix[0])
    INF = 10 ** 3

    ans = 0

    num_rows = len(supply)
    num_cols = len(demand)
    # loop runs until both the demand and the supply is exhausted
    allocations = [[0] * num_cols for _ in range(num_rows)]
    while max(supply) != 0 or max(demand) != 0:
        # finding the row and col difference
        row, col = findDiff(cost_matrix)
        # finding the maxiumum element in row difference array
        maxi1 = max(row)
        # finding the maxiumum element in col difference array
        maxi2 = max(col)

        # if the row diff max element is greater than or equal to col diff max element
        if (maxi1 >= maxi2):
            for ind, val in enumerate(row):
                if (val == maxi1):
                    # finding the minimum element in cost_matrix index where the maximum was found in the row difference
                    mini1 = min(cost_matrix[ind])
                    for ind2, val2 in enumerate(cost_matrix[ind]):
                        if (val2 == mini1):
                            # calculating the min of supply and demand in that row and col
                            mini2 = min(supply[ind], demand[ind2])
                            ans += mini2 * mini1
                            # subtracting the min from the supply and demand
                            allocations[ind][ind2] = mini2
                            supply[ind] -= mini2
                            demand[ind2] -= mini2
                            # if demand is smaller then the entire col is assigned max value so that the col is eliminated for the next iteration
                            if (demand[ind2] == 0):
                                for r in range(n):
                                    cost_matrix[r][ind2] = INF
                            # if supply is smaller then the entire row is assigned max value so that the row is eliminated for the next iteration
                            else:
                                cost_matrix[ind] = [INF for i in range(m)]
                            break
                    break
        # if the row diff max element is greater than col diff max element
        else:
            for ind, val in enumerate(col):
                if (val == maxi2):
                    # finding the minimum element in cost_matrix index where the maximum was found in the col difference
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, cost_matrix[j][ind])

                    for ind2 in range(n):
                        val2 = cost_matrix[ind2][ind]
                        if val2 == mini1:
                            # calculating the min of supply and demand in that row and col
                            mini2 = min(supply[ind2], demand[ind])
                            ans += mini2 * mini1
                            # subtracting the min from the supply and demand
                            allocations[ind2][ind] = mini2
                            supply[ind2] -= mini2
                            demand[ind] -= mini2
                            # if demand is smaller then the entire col is assigned max value so that the col is eliminated for the next iteration
                            if (demand[ind] == 0):
                                for r in range(n):
                                    cost_matrix[r][ind] = INF
                            # if supply is smaller then the entire row is assigned max value so that the row is eliminated for the next iteration
                            else:
                                cost_matrix[ind2] = [INF for i in range(m)]
                            break
                    break


    print("Initial Basic Feasible Solution and cost  using Vogel’s approximation method ")
    print_allocation(allocations)
    print("cost:", ans)
def north_west_corner(cost_matrix, supply, demand):
    num_suppliers = len(supply)
    num_consumers = len(demand)

    # Initialize the allocation matrix with zeros
    allocation = [[0 for _ in range(num_consumers)] for _ in range(num_suppliers)]

    # Initialize indices for suppliers and consumers
    i, j = 0, 0

    # Iterate until all supply and demand are exhausted
    while i < num_suppliers and j < num_consumers:
        # Find the minimum between supply[i] and demand[j]
        quantity = min(supply[i], demand[j])

        # Allocate the quantity to the current cell
        allocation[i][j] = quantity

        # Update supply and demand
        supply[i] -= quantity
        demand[j] -= quantity

        # Move to the next row or column based on which is exhausted first
        if supply[i] == 0:
            i += 1
        else:
            j += 1

    return allocation


def print_allocation(allocation):
    print("[")
    for row in allocation:
        print(row,' , ')
    print("]")


if __name__ == "__main__":
    supply = [float(x) for x in input("enter the vector of coefficients of supply - S.   ").split()]
    assert len(supply) == 3, "The length of this vector must be 3"
    assert all(x >= 0 for x in
               supply), "All elements in the supply vector must be greater than or equal to zero the method is not applicable."
    print("Enter the matrix of coefficients of costs - C.")
    cost_matrix = [[float(x) for x in input().split()] for _ in range(3)]
    assert all(x > 0 for row in cost_matrix for x in
               row), "All elements in the cost matrix must be greater than  zero the method is not applicable."
    assert len(cost_matrix) == 3 and len(cost_matrix[
                                             0]) == 4, "The shape of matrix of coefficients of constraint function must be equal (number of sources x number of destenations)"
    demand = [float(x) for x in input("Enter the vector of coefficients of demand - D   ").split()]
    assert len(demand) == len(cost_matrix[0]), "The length of this vector must be 4"
    assert all(x >= 0 for x in
               demand), "All elements in the demand vector must be greater than or equal to zero the method is not applicable."

    # cost_matrix = [
    #     [5, 4, 2, 7],
    #     [3, 2, 9, 6],
    #     [8, 7, 4, 2]
    # ]
    #
    # supply = [30, 50, 20]
    # demand = [40, 30, 30, 20]
    # print (supply)
    supplyN = supply[:]
    supplyV = supply[:]
    supplyR = supply[:]
    demandN = demand[:]
    demandV = demand[:]
    demandR = demand[:]
    cost_matrixN = [row[:] for row in cost_matrix]
    cost_matrixV = [row[:] for row in cost_matrix]
    cost_matrixR = [row[:] for row in cost_matrix]
    print_parameter_table(supply, cost_matrix, demand)
    print("The problem is unbalanced." if sum(supply) != sum(demand) else "The problem is balanced.")

    allocation = north_west_corner(cost_matrixN, supplyN, demandN)
    s=0

    print("Initial Basic Feasible Solution and cost  using north-west corner method")
    # print_parameter_table(supply, allocation, demand)
    print_allocation(allocation)
    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            s = s + allocation[i][j] * cost_matrix[i][j]
    print("cost:",s)
    vogel(supplyV,demandV,cost_matrixV)
    Russel(supplyR, demandR, cost_matrixR)

