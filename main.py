import time
import random

with open('text.txt', 'r') as file:
    text = file.read()

sentences = text.split('.')
sentences = [sentence.strip() for sentence in sentences[:-1]]

perfect = 0
correct = 0
wrong = 0
total = 0
max_time = 4

def correct_answer():
    print("\nPARABÉNS")
    global correct
    correct += 1

def wrong_answer(txt):
    print('\n'+ txt)
    global wrong
    wrong += 1

while (True):
    print('\nprepare-se para digitar')
    time.sleep(1)

    start = time.time()

    cur_phrase = sentences.pop(random.randint(0, len(sentences)-1))
    print(cur_phrase)
    typed = input()

    finish = time.time()

    time_total = finish - start
    print('\ntempo máximo: ' + str(max_time))
    print('tempo total: ' + "{:.2f}".format(time_total))

    time.sleep(1)
    
    if typed == cur_phrase:
        if time_total < max_time:
             correct_answer()
        else:
            wrong_answer('melhore seu tempo...')
    else:
        wrong_answer('as frases não combinam...')

    time.sleep(1)

    total += 1
    if len(sentences) <= 0: break

print('\nCORRECT: ' + str(correct))
print('WRONG: ' + str(wrong))