from pyasn1.codec.der import decoder
import rsa.pem
from pyasn1.type import univ, namedtype

with open("PK.txt") as f:
    temp = f.readlines()


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


pem_key = ''.join(temp)
der = rsa.pem.load_pem(pem_key, 'PUBLIC KEY')
(priv, _) = decoder.decode(der, asn1Spec=AsnPubKey())
q = int(priv['q'])
g = int(priv['g'])
h = int(priv['h'])

print(q, g, h)
