import string
import sys


def encrypt(plaintext, key):
    ciphertext = ''
    for ch in plaintext:
        ascii_ch = ord(ch) - 97
        enc_ascii_ch = key[ascii_ch]
        enc_ch = chr(enc_ascii_ch + 97)
        ciphertext += enc_ch
    return ciphertext


key_file = "key.txt"
message_file = "message.txt"

key = (([line.rstrip('\n') for line in open(key_file)])[0]).split()
key = [int(k) for k in key]

paragraphs = [line.rstrip('\n') for line in open(message_file)]
f = open('plaintext.txt', 'w')
for para in paragraphs:
    para = para.lower()
    exclude = set(string.punctuation)
    para = ''.join(ch for ch in para if ch not in exclude)
    f.write(para + '\n')
f.close()

paragraphs = [line.rstrip('\n') for line in open('plaintext.txt')]
f = open('ciphertext.txt', 'w')
for para in paragraphs:
    enc_para = ''
    for word in para.split(' '):
        enc_word = encrypt(word, key)
        enc_para += enc_word + ' '
    f.write(enc_para + '\n')
f.close()

print("-------------- Done --------------")
