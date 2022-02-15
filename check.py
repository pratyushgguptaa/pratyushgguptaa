import os
import secrets
# word = os.environ['WORD']

# next = os.environ['NEXT']

# for i in range(5):
#     if(word[i] == next[i]):
#         print('1', end='')
#     else:
#         print('0', end='')

words = []
with open('words.txt', 'r') as f:
    for line in f:
        words.append(line.strip())

print(len(words))
next = words[secrets.randbelow(len(words))]

f = open('secret.txt', 'w')
f.write(next.upper())
f.close()

# print(len(word))
# print(word)
