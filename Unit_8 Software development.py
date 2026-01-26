'''

Unit 8 Software Development

Recursion Example: Fibonacci Sequence
'''


def Fib(n):
    '''
    This function is a typical case of recursion where a function calls itself 
    as long as the base case is not reached or fullfilled.
    Using return usually helps exit a function with a value or output, but in
    this case another fixed and valid condition must exist for exiting the recursion 
    otherwise it will either hit the maximum recursion (failing) or run indefinitely like a 'while True' loop without a break.
    '''

    if n<=2: # Base case allowing to exit the recursion
        return 1
    else:
        return Fib(n-1) + Fib(n-2)
    
print(Fib(9))

# for i in range(14): # loop
#     print(Fib(i))


print('Fibonacci sequence using dictionary comprehension:\n')

x={f'Fib{i}':Fib(i) for i in range(1,14)}

print(x)





