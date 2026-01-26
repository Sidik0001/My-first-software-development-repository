
'''
Unit 7 - Guess the Number Game

'''

import random

print('''

Welcome to Guess the Number Game!

      The rules are simple you provide a number and I will let you know 
      how correct your guess is within 7 attempts. 

''')

low_bound =int(input('Please enter the lower bound rumber:\n'))
high_bound =int(input('Please enter the highr bound rumber:\n'))

print('You should have 7 attempts to guess correctly the number')
print(f'Great! Now let me guess a number in this range {low_bound,high_bound}')

num = random.randint(low_bound, high_bound)

total = 7  # total number of opportunities

gc= 0 # guesses counter

while gc < total:
    gc +=1 # incrementing the guess number
    user_guess = int(input('Enter your guess:\n'))

    if user_guess == num:
        print(f'Congratulations! You guessed the right number, which was {num}')
        break
    elif gc >= total and user_guess != num:
        print(f'Sorry you lost the game! The right number was {num}')
    elif user_guess < num:
        print('You guessed lower than the number.')
    elif user_guess > num:
        print('You guessed higher than the number.')
    

print('Thanks for playing the game!')

