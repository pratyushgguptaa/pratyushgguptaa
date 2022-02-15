import os
# import secrets
word = os.environ['WORD']

next = os.environ['NEXT']

for i in range(5):
    if(word[i] == next[i]):
        print('1', end='')
    else:
        print('0', end='')

print(len(word))
print(word)
