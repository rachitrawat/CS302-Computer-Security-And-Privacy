import pprint
import random

m = int(input("Enter m: "))
n_list = list(range(1, 27))


class KeyMatrix:

    def __init__(self, m):
        self.matrix = [0]
        self.m = m
        self.det = 0
        # determinant of permutation matrix
        self.count = 0

    def initialize(self):
        # initialize mxm matrix randomly b/w (1-26)
        self.matrix = [[random.choice(n_list) for x in range(self.m)] for y in range(self.m)]
        # calculate determinant
        self.det = self.calculateDet()

    def calculateDet(self):

        # LU decomposition
        # det A = det P * det L * det U
        # O(n^3) [Naive Laplace Expansion took O(n!)]

        P, L, U = self.lu_decomposition(self.matrix)

        # print("P:")
        # pprint.pprint(P)
        #
        # print("L:")
        # pprint.pprint(L)
        #
        # print("U:")
        # pprint.pprint(U)

        prod1, prod2 = 1, 1

        for i in range(self.m):
            # product of diagonal elements
            prod1 *= (L[i][i])
            prod2 *= (U[i][i])

        return round(((-1) ** self.count * prod1 * prod2) % 26)

    def mult_matrix(self, M, N):
        """Multiply square matrices of same dimension M and N"""

        # Converts N into a list of tuples of columns
        tuple_N = list(zip(*N))

        # Nested list comprehension to calculate matrix multiplication
        return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n)) for col_n in tuple_N] for row_m in M]

    def pivot_matrix(self, M):
        """Returns the pivoting matrix for M, used in Doolittle's method."""
        m = len(M)
        # Create an identity matrix, with floating point values
        id_mat = [[float(i == j) for i in range(m)] for j in range(m)]

        # Rearrange the identity matrix such that the largest element of
        # each column of M is placed on the diagonal of of M
        for j in range(m):
            row = max(range(j, m), key=lambda i: abs(M[i][j]))
            if j != row:
                # count the number of swaps it takes to get to the identity matrix
                self.count += 1
                # Swap the rows
                id_mat[j], id_mat[row] = id_mat[row], id_mat[j]
        return id_mat

    def lu_decomposition(self, A):
        """Performs an LU Decomposition of A (which must be square)
        into PA = LU. The function returns P, L and U."""
        n = len(A)

        # Create zero matrices for L and U
        L = [[0.0] * n for i in range(n)]
        U = [[0.0] * n for i in range(n)]

        # Create the pivot matrix P and the multipled matrix PA
        P = self.pivot_matrix(A)
        PA = self.mult_matrix(P, A)

        # Perform the LU Decomposition
        for j in range(n):
            # All diagonal entries of L are set to unity
            L[j][j] = 1.0

            # LaTeX: u_{ij} = a_{ij} - \sum_{k=1}^{i-1} u_{kj} l_{ik}
            for i in range(j + 1):
                s1 = sum(U[k][j] * L[i][k] for k in range(i))
                U[i][j] = PA[i][j] - s1

            # LaTeX: l_{ij} = \frac{1}{u_{jj}} (a_{ij} - \sum_{k=1}^{j-1} u_{kj} l_{ik} )
            for i in range(j, n):
                s2 = sum(U[k][j] * L[i][k] for k in range(j))
                L[i][j] = (PA[i][j] - s2) / U[j][j]

        return (P, L, U)

    def printDetails(self):
        print('Key:')
        pprint.pprint(self.matrix)
        print('Determinant:', self.det)

    def isGcdOne(self, x, y):
        # Euclidean Algorithm
        while (y):
            x, y = y, x % y
        return x == 1

    def isInvertible(self):
        return self.det != 0 and self.isGcdOne(self.det, 26)

    def writeToFile(self):
        file = open('key.txt', 'w')
        for row in self.matrix:
            for element in row:
                file.write("%s\n" % element)


# create a key object
k = KeyMatrix(m)

# loop until k is invertible
while not k.isInvertible():
    k.initialize()

k.printDetails()
k.writeToFile()
