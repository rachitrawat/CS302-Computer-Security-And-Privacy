import pprint
from collections import Counter
import operator

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
    print()
    return Letters_Counter, Bigram_Counter, Trigram_Counter


def replaceChar(cipher_lst, plain_lst, char1, char2):
    for n, i in enumerate(cipher_lst):
        if i == char1:
            cipher_lst[n] = char2
            plain_lst[n] = char2
    return ''.join(cipher_lst), ''.join(plain_lst)


def replaceBigram(cipher_lst, plain_lst, bigram1, bigram2):
    for n, i in enumerate(cipher_lst):
        if bigram1 in cipher_lst[n]:
            tmplst = list(plain_lst[n])
            tmplst[cipher_lst[n].index(bigram1[0])] = bigram2[0]
            tmplst[cipher_lst[n].index(bigram1[1])] = bigram2[1]
            cipher_lst[n] = cipher_lst[n].replace(bigram1, bigram2)
            plain_lst[n] = "".join(tmplst)
    return ' '.join(cipher_lst), ' '.join(plain_lst)


def replaceTrigram(cipher_lst, plain_lst, trigram1, trigram2):
    for n, i in enumerate(cipher_lst):
        if trigram1 in cipher_lst[n]:
            tmplst = list(plain_lst[n])
            tmplst[cipher_lst[n].index(trigram1[0])] = trigram2[0]
            tmplst[cipher_lst[n].index(trigram1[1])] = trigram2[1]
            tmplst[cipher_lst[n].index(trigram1[2])] = trigram2[2]
            cipher_lst[n] = cipher_lst[n].replace(trigram1, trigram2)
            plain_lst[n] = "".join(tmplst)
    return ' '.join(cipher_lst), ' '.join(plain_lst)


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

alpha_LF = sorted(letter_freq.items(), key=operator.itemgetter(1), reverse=True)

# Top 5 most common letters in ciphertext
cipher_LF = [x[0] for x in LC.most_common(1)]

for letter_c in cipher_LF:
    for letter_p in alpha_LF:
        # replace 5 most frequent char in cipher with most freq letters in English (till 'r')
        temp_k_dict = k_dict
        temp_cipherlst, temp_plainlst = replaceChar(list(ciphertext_str), list(plaintext), letter_c, letter_p[0])
        pprintText("Swap " + letter_c + " with " + letter_p[0], (temp_cipherlst, temp_plainlst))

        # replace 5 most frequent bigrams in cipher of form -z or z-
        for bigram_c in BC.most_common(5):
            if letter_c in bigram_c[0] and bigram_c[1] >= 2:
                for bigram_p in bigrams_common_lst:
                    if letter_p[0] in bigram_p:
                        temp_cipherlst, temp_plainlst = replaceBigram(ciphertext_str.split(), plaintext.split(),
                                                                      bigram_c[0],
                                                                      bigram_p)
                        pprintText("Swap " + bigram_c[0] + " with " + bigram_p,
                                   replaceChar(list(temp_cipherlst), list(temp_plainlst), letter_c, letter_p[0]))

                        # replace 5 most frequent trigrams in cipher of form z--, --z, -z-
                        for trigram_c in TC.most_common(10):
                            if bigram_c[0] in trigram_c[0] and trigram_c[1] >= 2:
                                for trigram_p in trigrams_common_lst:
                                    if bigram_p in trigram_p:
                                        temp_cipherlst, temp_plainlst = replaceTrigram(ciphertext_str.split(),
                                                                                       plaintext.split(),
                                                                                       trigram_c[0],
                                                                                       trigram_p)
                                        pprintText("Swap " + trigram_c[0] + " with " + trigram_p,
                                                   replaceChar(list(temp_cipherlst), list(temp_plainlst), letter_c,
                                                               letter_p[0]))

        if letter_p[0] == 'e':
            break
