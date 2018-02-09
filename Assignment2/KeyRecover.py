ciphertext_file = "ciphertext.txt"
ciphertext = ' '.join((([line.rstrip('\n') for line in open(ciphertext_file)])[0]).split())

import pprint

print("\n-----ciphertext-----\n")
pprint.pprint(ciphertext)
print()

from collections import Counter

Words_Counter = Counter(x for x in ciphertext if not x.isspace())
print("\n-----most common words-----\n")
print(Words_Counter.most_common(5))
print("\n-----most common bigrams-----\n")
Bigram_Counter = Counter([ciphertext[i:i + 2] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 2]])
print(Bigram_Counter.most_common(5))
print("\n-----most common trigrams-----\n")
Trigram_Counter = Counter([ciphertext[i:i + 3] for i in range(len(ciphertext) - 1) if ' ' not in ciphertext[i:i + 3]])
print(Trigram_Counter.most_common(5))
