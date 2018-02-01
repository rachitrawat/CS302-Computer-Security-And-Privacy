import random

m = int(input("Enter m: "))
n_list = list(range(1, 27))


class keyMatrix:

    def __init__(self, m):
        self.matrix = []
        self.m = m

    def initializeKeyMatrix(self):
        # initialize mxm matrix randomly b/w (1-26)
        self.matrix = [[random.choice(n_list) for x in range(self.m)] for y in range(self.m)]

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
            print(total)
            return total

    def printMatrix(self):
        print(self.matrix)

    def isDetNonZero(self):
        if self.calculateDet(self.matrix, 1) != 0:
            return True
        else:
            return False
    #
    # def isInvertible(self):


# create an mxm matrix object
k = keyMatrix(m)

k.initializeKeyMatrix()
k.printMatrix()

print(k.isDetNonZero())
