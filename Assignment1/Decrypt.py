import pprint
from math import ceil, log

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
        self.det = self.calculateDet(self.matrix)
        self.det_mod = self.det % 26
        self.det_inv = self.getDetInverse(self.det_mod, 26)
        self.matrix_inv = self.getMatrixInverse(self.matrix)
        # determinant of permutation matrix
        self.count = 0

    def calculateDet(self, m):

        # LU decomposition
        # det A = det P * det L * det U
        # O(n^3) [Naive Laplace Expansion takes O(n!)]

        P, L, U = self.lu_decomposition(m)

        # print("P:")
        # pprint.pprint(P)
        #
        # print("L:")
        # pprint.pprint(L)
        #
        # print("U:")
        # pprint.pprint(U)

        prod1, prod2 = 1, 1

        for i in range(len(m)):
            # product of diagonal elements
            prod1 *= (L[i][i])
            prod2 *= (U[i][i])

        return round(((-1) ** self.count * prod1 * prod2))

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
        print('Determinant:', self.det_mod)
        print('Determinant Inverse:', self.det_inv)
        # print('K Inverse:', self.matrix_inv)

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

    def transposeMatrix(self, m):
        return list(map(list, list(zip(*m))))

    def getMatrixMinor(self, m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    def getMatrixInverse(self, m):
        determinant = self.det_inv
        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[(m[1][1] * determinant), (-1 * m[0][1] * determinant)],
                    [(-1 * m[1][0] * determinant), (m[0][0] * determinant)]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * self.calculateDet(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = round((cofactors[r][c] * determinant))
        return cofactors


def printMatrix(matrix):
    for line in matrix:
        print("\t".join(map(str, line)))


def ikjMatrixProduct(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C


def subtract(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def strassenR(A, B):
    """
        Implementation of the strassen algorithm.
    """
    n = len(A)
    LEAF_SIZE = 8
    if n <= LEAF_SIZE:
        return ikjMatrixProduct(A, B)
    else:
        # initializing the new sub-matrices
        newSize = int(n / 2)
        a11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]

        b11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]

        aResult = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        bResult = [[0 for j in range(0, newSize)] for i in range(0, newSize)]

        # dividing the matrices in 4 sub-matrices:
        for i in range(0, newSize):
            for j in range(0, newSize):
                a11[i][j] = A[i][j]  # top left
                a12[i][j] = A[i][j + newSize]  # top right
                a21[i][j] = A[i + newSize][j]  # bottom left
                a22[i][j] = A[i + newSize][j + newSize]  # bottom right

                b11[i][j] = B[i][j]  # top left
                b12[i][j] = B[i][j + newSize]  # top right
                b21[i][j] = B[i + newSize][j]  # bottom left
                b22[i][j] = B[i + newSize][j + newSize]  # bottom right

        # Calculating p1 to p7:
        aResult = add(a11, a22)
        bResult = add(b11, b22)
        p1 = strassenR(aResult, bResult)  # p1 = (a11+a22) * (b11+b22)

        aResult = add(a21, a22)  # a21 + a22
        p2 = strassenR(aResult, b11)  # p2 = (a21+a22) * (b11)

        bResult = subtract(b12, b22)  # b12 - b22
        p3 = strassenR(a11, bResult)  # p3 = (a11) * (b12 - b22)

        bResult = subtract(b21, b11)  # b21 - b11
        p4 = strassenR(a22, bResult)  # p4 = (a22) * (b21 - b11)

        aResult = add(a11, a12)  # a11 + a12
        p5 = strassenR(aResult, b22)  # p5 = (a11+a12) * (b22)

        aResult = subtract(a21, a11)  # a21 - a11
        bResult = add(b11, b12)  # b11 + b12
        p6 = strassenR(aResult, bResult)  # p6 = (a21-a11) * (b11+b12)

        aResult = subtract(a12, a22)  # a12 - a22
        bResult = add(b21, b22)  # b21 + b22
        p7 = strassenR(aResult, bResult)  # p7 = (a12-a22) * (b21+b22)

        # calculating c21, c21, c11 e c22:
        c12 = add(p3, p5)  # c12 = p3 + p5
        c21 = add(p2, p4)  # c21 = p2 + p4

        aResult = add(p1, p4)  # p1 + p4
        bResult = add(aResult, p7)  # p1 + p4 + p7
        c11 = subtract(bResult, p5)  # c11 = p1 + p4 - p5 + p7

        aResult = add(p1, p3)  # p1 + p3
        bResult = add(aResult, p6)  # p1 + p3 + p6
        c22 = subtract(bResult, p2)  # c22 = p1 + p3 - p2 + p6

        # Grouping the results obtained in a single matrix:
        C = [[0 for j in range(0, n)] for i in range(0, n)]
        for i in range(0, newSize):
            for j in range(0, newSize):
                C[i][j] = c11[i][j]
                C[i][j + newSize] = c12[i][j]
                C[i + newSize][j] = c21[i][j]
                C[i + newSize][j + newSize] = c22[i][j]
        return C


# Strassen's Algorithm O(n^2.80) [Naive multiplication is O(n^3)]
def strassen(A, B):
    # print(A, B)
    assert type(A) == list and type(B) == list
    assert len(A) == len(A[0]) == len(B) == len(B[0])

    # Make the matrices bigger so that you can apply the strassen
    # algorithm recursively without having to deal with odd
    # matrix sizes
    nextPowerOfTwo = lambda n: 2 ** int(ceil(log(n, 2)))
    n = len(A)
    m = nextPowerOfTwo(n)
    APrep = [[0 for i in range(m)] for j in range(m)]
    BPrep = [[0 for i in range(m)] for j in range(m)]
    for i in range(n):
        for j in range(n):
            APrep[i][j] = A[i][j]
            BPrep[i][j] = B[i][j]
    CPrep = strassenR(APrep, BPrep)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = round(CPrep[i][j]) % 26
    return C


# create a key object
k = getKey()
k_obj = KeyMatrix(k)
cipher_matrix_flat = getCipher()
# print(cipher_matrix_flat)
k_obj.printDetails()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


cipher_matrix = (list(chunks(cipher_matrix_flat, len(k[0]))))
temp = []

# convert cipher text matrix to square
for i in range(len(k[0])):
    temp.append(0)

msg_matrix = []

for i in range(len(cipher_matrix)):
    x = [cipher_matrix[i]]
    for i in range(len(k[0]) - 1):
        x.append(temp)
    msg_matrix.append(strassen(x, k_obj.matrix_inv)[0])

# make a flat list out of msg matrix
flat_list = [item for sublist in msg_matrix for item in sublist]

msg_text = ''.join([to_alpha_map[x] for x in flat_list])
print("plaintext:", msg_text)
with open("output.txt", "w") as text_file:
    text_file.write(msg_text)
