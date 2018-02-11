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
trigrams_common = "THE, ING, AND, HER, ERE, ENT, THA, NTH, WAS, ETH, FOR, DTH"
bigrams_common_lst = (bigrams_common.replace(' ', '').lower().split(','))
trigrams_common_lst = (trigrams_common.replace(' ', '').lower().split(','))


def pprintText(header, text):
    print("\n-----" + header + "-----")
    pprint.pprint(text)


def getOverview(ciphertext):
    Letters_Counter = Counter(x for x in ciphertext if not x.isspace())
    print("\n-----most common letters-----")
    print(Letters_Counter.most_common(10))
    print("\n-----most common bigrams-----")
    Bigram_Counter = Counter(
        [ciphertext[i:i + 2] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 2]])
    print(Bigram_Counter.most_common(10))
    print("\n-----most common trigrams-----")
    Trigram_Counter = Counter(
        [ciphertext[i:i + 3] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 3]])
    print(Trigram_Counter.most_common(10))
    return Letters_Counter, Bigram_Counter, Trigram_Counter


def getDummyString(str):
    slist = list(str)
    for i, c in enumerate(slist):
        if slist[i] != ' ':
            slist[i] = '-'
    return ''.join(slist)


def refreshMapping():
    global plaintext_str, ciphertext_char_lst, plaintext_char_lst, plaintext_lst, count

    for index, val in enumerate(ciphertext_char_lst):
        # post analysis: o maps to o
        if val != ' ' and (val != k_dict[val] or val == 'o'):
            plaintext_char_lst[index] = k_dict[val]

    plaintext_str = ''.join(plaintext_char_lst)
    plaintext_lst = plaintext_str.split()
    plaintext_char_lst = list(plaintext_str)
    pprintText("mapping " + str(count), (plaintext_str))
    count += 1

    if count == 8:
        f = open("plaintext.txt", 'w')
        f.write(plaintext_str)
        f.close()


# Read ciphertext
ciphertext_file = "ciphertext.txt"
ciphertext_str = ' '.join((([line.rstrip('\n') for line in open(ciphertext_file)])[0]).split())
ciphertext_lst = ciphertext_str.split()
ciphertext_char_lst = list(ciphertext_str)

# pprint
pprintText("ciphertext", ciphertext_str)

# get counter objects
LC, BC, TC = getOverview(ciphertext_str)

# str with non-space chars replaced with '-'
plaintext_str = (getDummyString(ciphertext_str))
plaintext_lst = plaintext_str.split()
plaintext_char_lst = list(plaintext_str)

# count to keep track of mapping no
count = 1

# get single letters in cipher text (=> a or i in English)
tmplst = []
for element in ciphertext_lst:
    if len(element) == 1 and element not in tmplst:
        tmplst.append(element)

pprintText("most common single letter words", tmplst)
# Guess (n=>a, v=>i)
k_dict['n'] = 'a'
k_dict['v'] = 'i'
print("Swap: " + 'n' + " with " + 'a')
print("Swap: " + 'v' + " with " + 'i')
refreshMapping()

pprintText("most common trigram containing a", "abz")
# Guess "abz" => "and"
# (b=>n, z=>d)
k_dict['b'] = 'n'
k_dict['z'] = 'd'
print("Swap: " + 'b' + " with " + 'n')
print("Swap: " + 'z' + " with " + 'd')
refreshMapping()

pprintText("2 most common letters", "u, p")
# Guess
# (u=>e, p=>t)
k_dict['u'] = 'e'
k_dict['p'] = 't'
print("Swap: " + 'u' + " with " + 'e')
print("Swap: " + 'p' + " with " + 't')
refreshMapping()

pprintText("most common trigrams", "tge")
# Guess tge => the
# (g=>h, t=>r)
k_dict['g'] = 'h'
print("Swap: " + 'g' + " with " + 'h')
refreshMapping()

pprintText("Guess ij and eayth", "is and earth")
# (j=>s, y => r
k_dict['j'] = 's'
k_dict['y'] = 'r'
print("Swap: " + 'j' + " with " + 's')
print("Swap: " + 'y' + " with " + 'r')
refreshMapping()

pprintText("Guess at--s-here", "atmosphere")
# (e=>m, o=>o, w=> p)
k_dict['e'] = 'm'
k_dict['w'] = 'p'
print("Swap: " + 'e' + " with " + 'm')
print("Swap: " + 'w' + " with " + 'p')
refreshMapping()

pprintText("Guess s-spended", "suspended")
pprintText("Guess parti--es", "particles")
pprintText("Guess nitr--en", "nirtogen")
pprintText("Guess 'en-ir-nmenta-", "environmental")
# (k=>u, c=>t, l=> s)
k_dict['k'] = 'u'
k_dict['t'] = 'c'
k_dict['s'] = 'l'
k_dict['x'] = 'g'
k_dict['m'] = 'v'
print("Swap: " + 'k' + " with " + 'u')
print("Swap: " + 't' + " with " + 'c')
print("Swap: " + 's' + " with " + 'l')
print("Swap: " + 'x' + " with " + 'g')
print("Swap: " + 'm' + " with " + 'v')

pprintText("Guess -ecause", "because")
pprintText("Guess -ith-ut-", "without")
pprintText("Guess e-ist", "exist")
pprintText("Guess in-luences", "influences")
pprintText("Guess water we drin-", "water we drink")
pprintText("Guess water we -uiet", "quiet")
pprintText("gra-ing in the pasture", "grazing")
pprintText("-olly life", "jollu")
k_dict['i'] = 'b'
k_dict['r'] = 'y'
k_dict['c'] = 'w'
k_dict['q'] = 'x'
k_dict['a'] = 'f'
k_dict['f'] = 'k'
k_dict['l'] = 'q'
k_dict['d'] = 'z'
k_dict['h'] = 'j'
print("Swap: " + 'i' + " with " + 'b')
print("Swap: " + 'r' + " with " + 'y')
print("Swap: " + 'c' + " with " + 'w')
print("Swap: " + 'q' + " with " + 'x')
print("Swap: " + 'a' + " with " + 'f')
print("Swap: " + 'f' + " with " + 'k')
print("Swap: " + 'l' + " with " + 'q')
print("Swap: " + 'd' + " with " + 'z')
print("Swap: " + 'h' + " with " + 'j')
refreshMapping()

import collections

# convert key dict to string
key_map = {v: k for k, v in k_dict.items()}
od = collections.OrderedDict(sorted(key_map.items()))
key_list = []
for key, value in od.items():
    temp = ord(value) - 97
    key_list.append(temp)

key_str = (' '.join(str(x) for x in key_list))
f = open("key.txt", 'w')
f.write(str(key_str))  # write key to file
f.close()
