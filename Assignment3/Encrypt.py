import math
import random

import rsa.pem
from pyasn1.codec.der import decoder
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


def Encrypt(q, g, h, plain_text):
    r = random.randint(2, q - 1)  # r ∈ {2, . . . , q − 1}
    c1 = square_and_multiply(g, r, q)  # c1 = g^r mod q
    c2 = (plain_text * square_and_multiply(h, r, q)) % q  # C2 = (h^r × m) mod q

    return c1, c2


# Read Public Key
with open("PK") as f:
    temp = f.readlines()
pem_key = ''.join(temp)
der = rsa.pem.load_pem(pem_key, 'PUBLIC KEY')
(priv, _) = decoder.decode(der, asn1Spec=AsnPubKey())
q = int(priv['q'])
g = int(priv['g'])
h = int(priv['h'])

# read Plaintext
with open("plaintext") as f:
    temp = f.readlines()
plain_text = int([x.strip() for x in temp][0])

# write ciphertext c1,c2
c1, c2 = Encrypt(q, g, h, plain_text)
file = open('ciphertext', 'w')
file.write("%s" % str(c1) + " " + str(c2))
