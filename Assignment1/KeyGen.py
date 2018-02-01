import random

m = int(input("Enter m: "))
n_list = list(range(1, 27))


class keyMatrix:

    def __init__(self, m):
        self.matrix = [0]
        self.m = m
        self.det = 0

    def initializeKeyMatrix(self):
        # initialize mxm matrix randomly b/w (1-26)
        self.matrix = [[random.choice(n_list) for x in range(self.m)] for y in range(self.m)]
        # calculate determinant
        self.det = self.calculateDet(self.matrix, 1) % 26

    def calculateDet(self, matrix, mul):
        width = len(matrix)
        if width == 1:
            return mul * matrix[0][0]
        else:
            sign = -1
            total = 0
            for i in range(width):
                m = []
                for j in range(1, width):
                    buff = []
                    for k in range(width):
                        if k != i:
                            buff.append(matrix[j][k])
                    m.append(buff)
                sign *= -1
                total += mul * self.calculateDet(m, sign * matrix[0][i])
            return total

    def printMatrix(self):
        print(self.matrix)

    def getDet(self):
        return self.det

    def isDetNonZero(self):
        return self.det != 0

    def isGcdOne(self, x, y):
        while (y):
            x, y = y, x % y
        return x == 1

    def isKeyMatrixInvertible(self):
        return self.isDetNonZero() and self.isGcdOne(self.det, 26)


# create a key object
k = keyMatrix(m)

# loop until k is invertible
while not k.isKeyMatrixInvertible():
    k.initializeKeyMatrix()

# k.printMatrix()
# print(k.getDet())
