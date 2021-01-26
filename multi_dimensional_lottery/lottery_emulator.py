
# How long would it take to hit the lotto #?

from numpy import random as rand
#import pandas as pd
winning_ticket = [4, 26, 42, 50, 60, 24]
# This is the actual winning ticket: [4, 26, 42, 50, 60, 24]
one_slot = [i + 1 for i in range(70)]
bonus = [i + 1 for i in range(25)]
slot_gen = [one_slot for i in range(len(winning_ticket) - 1)] + [bonus]

print(winning_ticket)
print(slot_gen)


# combination = list of ints as combination
def mega_millions(combination, max_attempts = 1000):
    print("start")
    sorted_combo = sorted(combination[0:(len(combination) - 1)]) + [combination[-1]]
    print(sorted_combo)
    number_pool = [i + 1 for i in range(70)]
    bonus = [i + 1 for i in range(25)]
    try_again = True
    attempts = 0
    record = []
    while try_again == True and attempts <= max_attempts:
        attempts += 1
        test_pool = [i + 1 for i in range(70)]
        #print("test_pool len:", len(test_pool))
        test_combo = []
        for i in range(len(combination) - 1):
            rand_int = test_pool.pop(test_pool.index(rand.choice(test_pool)))
            test_combo.append(rand_int)
        test_combo.sort()
        test_combo.append(rand.choice(bonus))
        # print("Dimension:", attempts, "Winning ticket:", test_combo)

        if attempts % len(str(attempts))**5 == 0:
            print("Dimension:", attempts, "Winner:", test_combo)
            
        if test_combo == sorted_combo:
            print("Jackpot!", "Dimension", attempts, "has your winnings!")
            try_again = False
        else:
            # if test_combo in record:
            #     print("**DUPLICATE DRAW**", record.count(test_combo))
            # record.append(test_combo)
            test_pool = []

    return attempts
            

number_of_attempts = mega_millions(winning_ticket, 100000000)
#print(sorted(number_of_attempts[0]))



        




