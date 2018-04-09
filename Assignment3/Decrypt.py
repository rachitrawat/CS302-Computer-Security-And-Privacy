import rsa.pem
from pyasn1.codec.der import decoder
from pyasn1.type import univ, namedtype
import math


class AsnPubKey(univ.Sequence):
    """ASN.1 contents of DER encoded public key:
    PublicKey ::= SEQUENCE {
         q           INTEGER,  -- q
         g           INTEGER,  -- g
         h           INTEGER,  -- h

    """

    componentType = namedtype.NamedTypes(
        namedtype.NamedType('q', univ.Integer()),
        namedtype.NamedType('g', univ.Integer()),
        namedtype.NamedType('h', univ.Integer())

    )


def square_and_multiply(x, c, n):
    # z=x^c mod n
    c = '{0:b}'.format(c)  # convert exponent to binary
    z = 1
    l = len(c)

    for i in range(0, l):
        z = (math.pow(z, 2)) % n
        if c[i] == "1":
            z = (z * x) % n

    return int(z)


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''


def multiplicative_inverse(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicative inverse of a mod b
    #      or      j = multiplicative inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterative Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo original b
    if ly < 0:
        ly += oa  # If neg wrap modulo original a
    # return a , lx, ly  # Return only positive values
    return lx


def Decrypt(c1, c2, a, q):
    t1 = square_and_multiply(c1, a, q)
    t1_inv = multiplicative_inverse(t1, q)
    t2 = (c2 * t1_inv) % q
    return t2


# read c1, c2
with open("ciphertext") as f:
    temp = f.readlines()[0].split()
c1 = int(temp[0])
c2 = int(temp[1])

# read secret key
with open("SK") as f:
    temp = f.readlines()
a = int(temp[0])
print("a: ", a)

# Read Public Key
with open("PK") as f:
    temp = f.readlines()
pem_key = ''.join(temp)
der = rsa.pem.load_pem(pem_key, 'PUBLIC KEY')
(priv, _) = decoder.decode(der, asn1Spec=AsnPubKey())
q = int(priv['q'])
g = int(priv['g'])
h = int(priv['h'])
print("q: ", q)
print("g: ", g)
print("h: ", h)

plain_text = Decrypt(c1, c2, a, q)
file = open('output_plaintext', 'w')
file.write("%s" % str(plain_text))
print("Ciphertext: ", str(c1) + " " + str(c2))
print("Plaintext: ", str(plain_text))
