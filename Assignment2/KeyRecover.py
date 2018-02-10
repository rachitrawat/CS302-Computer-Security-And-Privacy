import pprint
from collections import Counter

alpha = 'abcdefghijklmnopqrstuvwxyz'
k_dict = dict([(alpha[i], alpha[i]) for i in range(len(alpha))])

letter_freq = {'a': 8.55, 'k': 0.81, 'u': 2.68,
               'b': 1.60, 'l': 4.21, 'v': 1.06,
               'c': 3.16, 'm': 2.53, 'w': 1.83,
               'd': 3.87, 'n': 7.17, 'x': 0.19,
               'e': 12.10, 'o': 7.47, 'y': 1.72,
               'f': 2.18, 'p': 2.07, 'z': 0.11,
               'g': 2.09, 'q': 0.10,
               'h': 4.96, 'r': 6.33,
               'i': 7.33, 's': 6.73,
               'j': 0.22, 't': 8.94
               }

bigrams_common = "TH, HE, IN, ER, AN, RE, ED, ON, ES, ST, EN, AT, TO, NT, HA, ND, OU, EA, NG, AS, OR, TI, IS, ET, IT, AR, TE, SE, HI, OF"
trigrams_common = "THE, ING, AND, HER, ERE, ENT, THA, NTH, WAS, ETH,FOR, DTH"
bigrams_common_lst = (bigrams_common.replace(' ', '').lower().split(','))
trigrams_common_lst = (trigrams_common.replace(' ', '').lower().split(','))


def pprintText(header, text):
    print("\n-----" + header + "-----")
    pprint.pprint(text)


def getOverview(ciphertext):
    Letters_Counter = Counter(x for x in ciphertext if not x.isspace())
    print("\n-----most common letters-----")
    print(Letters_Counter.most_common(5))
    print("\n-----most common bigrams-----")
    Bigram_Counter = Counter(
        [ciphertext[i:i + 2] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 2]])
    print(Bigram_Counter.most_common(5))
    print("\n-----most common trigrams-----")
    Trigram_Counter = Counter(
        [ciphertext[i:i + 3] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 3]])
    print(Trigram_Counter.most_common(5))
    print()
    return Letters_Counter, Bigram_Counter, Trigram_Counter


def replaceChar(cipher_lst, plain_lst, char1, char2):
    for n, i in enumerate(ciphertext_str):
        if i == char1:
            cipher_lst[n] = char2
            plain_lst[n] = char2
    return ''.join(cipher_lst), ''.join(plain_lst)


def getDummyString(str):
    slist = list(str)
    for i, c in enumerate(slist):
        if slist[i] != ' ':
            slist[i] = '-'
    return ''.join(slist)


# Read ciphertext
ciphertext_file = "ciphertext.txt"
ciphertext_str = ' '.join((([line.rstrip('\n') for line in open(ciphertext_file)])[0]).split())

# pprint
pprintText("ciphertext", ciphertext_str)

# get counter objects
LC, BC, TC = getOverview(ciphertext_str)

# str with non-space chars replaced with '-'
plaintext = (getDummyString(ciphertext_str))

# replace most common character with 'e'
pprintText("'e' replaced text",
           replaceChar(list(ciphertext_str), list(plaintext), [x[0] for x in LC.most_common(1)][0], 'e'))
