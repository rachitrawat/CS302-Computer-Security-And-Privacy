import numpy as np


def generate_key():
    f = open("key.txt", 'w')
    key = str((np.random.permutation(26)).tolist())  # create a random permutation and convert to string
    key = key[1:-1]  # remove the last and first ch - '(' and  ')'
    key = key.replace(',', '')  # remove all the spaces
    f.write(str(key))  # write key to file
    f.close()


generate_key()
