import pprint

alpha = 'abcdefghijklmnopqrstuvwxyz'
to_num_map = dict([(alpha[i], i * 1) for i in range(len(alpha))])
to_alpha_map = {v: k for k, v in to_num_map.items()}


def getKey():
    key = []
    with open("key.txt") as f:
        temp = f.readlines()
    # remove null character
    temp = [x.strip().split() for x in temp]
    for row in temp:
        key = key + [list(map(int, row))]
    return key


def getCipher():
    msg = []
    with open("ciphertext.txt") as f:
        temp = f.readlines()
    # remove null character
    temp = [x.strip() for x in temp]
    print("ciphertext:", ''.join(temp))
    # convert to num
    return [to_num_map[x] for x in list(''.join(temp))]


class KeyMatrix:

    def __init__(self, matrix):
        self.matrix = matrix
        self.m = len(matrix[0])
        self.det = self.calculateDet()
        self.det_inv = self.getDetInverse(self.det, 26)
        # determinant of permutation matrix
        self.count = 0

    def calculateDet(self):

        # LU decomposition
        # det A = det P * det L * det U
        # O(n^3) [Naive Laplace Expansion takes O(n!)]

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
        self.count = 0
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
        print('Determinant Inverse:', self.det_inv)

    def getDetInverse(self, det, mod):

        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)

        def modinv(a, m):
            g, x, y = egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')
            else:
                return x % m

        return modinv(det, mod)


# create a key object
k = KeyMatrix(getKey())
k.printDetails()
