import os
import secrets

words = []
with open('words.txt', 'r') as f:
    for line in f:
        words.append(line.strip())

print(len(words))
next = words[secrets.randbelow(len(words))]

f = open('secret.txt', 'w')
f.write(next.upper())
f.close()
