import random

import rsa.pem
from pyasn1.codec.der import encoder
from pyasn1.type import univ, namedtype


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


class PrivateKey(object):
    def __init__(self, a=None):
        self.a = a


class PublicKey(object):
    def __init__(self, q=None, g=None, h=None):
        self.q = q
        self.g = g
        self.h = h


def rabinMiller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2  # discard remainder
        t += 1

    for trials in range(11):  # try to falsify num's primality 11 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def isPrime(num):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling rabinMiller().

    if (num < 2):
        return False  # 0, 1, and negative numbers are not prime

    # About 1/3 of the time we can quickly determine if num is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabinMiller(), but unlike rabinMiller() is not guaranteed to
    # prove that a number is prime.
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                 991, 997]

    if num in lowPrimes:
        return True

    # See if any of the low prime numbers can divide num
    for prime in lowPrimes:
        if num % prime == 0:
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    return rabinMiller(num)


def generateLargePrime(keysize=300):
    # Return a random prime number of keysize bits in size.
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if isPrime(num) and isPrime(2 * num + 1):
            return num


def square_and_multiply(x, c, n):
    # z=x^c mod n
    c = '{0:b}'.format(c)  # convert exponent to binary
    z = 1
    l = len(c)

    for i in range(0, l):
        z = z ** 2 % n
        if c[i] == "1":
            z = (z * x) % n

    return int(z)


# finds a primitive root for prime p
# this function was implemented from the algorithm described here:
# http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root(p):
    if p == 2:
        return 1
    # the prime divisors of p-1 are 2 and (p-1)/2 because
    # p = 2x + 1 where x is a prime
    p1 = 2
    p2 = (p - 1) // p1

    # test random g's until one is found that is a primitive root mod p
    while 1:
        g = random.randint(2, p - 1)
        # g is a primitive root if for all prime factors of p-1, p[i]
        # g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not (square_and_multiply(g, (p - 1) // p1, p) == 1):
            if not square_and_multiply(g, (p - 1) // p2, p) == 1:
                return g


p = generateLargePrime()
q = (2 * p) + 1

# Primitive root of a prime number n is an integer r between[1, n-1] such that
# the values of r^x(mod n) where x is in range[0, n-2] are different.
# g is the generator
g = find_primitive_root(q)

# set g as quadratic residue mod q
g = square_and_multiply(g, 2, q)

a = random.randint(2, (q - 1) - 1)  # {2,3,....o(g)-1}
h = square_and_multiply(g, a, q)

print("p: ", p)
print("q: ", q)
print("g: ", g)
print("a: ", a)
print("h: ", h)

PK = PublicKey(q, g, h)
SK = PrivateKey(a)
# write public key in ans.1 PEM scheme
# Create the ASN object
asn_key = AsnPubKey()
asn_key.setComponentByName('q', PK.q)
asn_key.setComponentByName('g', PK.g)
asn_key.setComponentByName('h', PK.h)
encoder.encode(asn_key)
pem_key = rsa.pem.save_pem(encoder.encode(asn_key), 'PUBLIC KEY')
with open('PK', 'wb') as w:
    w.write(pem_key)

# write secret key
file = open('SK', 'w')
file.write("%s" % SK.a)
