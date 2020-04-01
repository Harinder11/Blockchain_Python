"""
While calling the function whatever argument we pass has 
preference over the default argument.

"""

# def average(first_number, second_number = 6):
#     print('first number is', first_number)
#     print('second number is', second_number)
#     avg = (first_number + second_number)/2
#     return avg

# def get_userinput():
#     return int(input("please enter your nummber"))

# #In this case it will take the default argument that is 6
# print(average(3))

# #Here the function average will take the second argument from get_userinput()
# print(average(3, get_userinput()))

""" 
*args: using this we can pass multiple arguments without indicating the function in prior
*args: can have unlimited unnamed arguments, and returns a tuple
**kargs: can have unlimited named arguments and return a dictionary
"""
# def unlimited_arguments(*args): #*args creates a tuple of arguments that are passed
#     print(args)
#     for arg in args:
#         print(arg)
    
# unlimited_arguments(1,2,3,4,5) #Multiple arguments passed

# def unlimited_arguments(*args, **kargs): 
#     print(args)
#     for arg in args:
#         print(arg)
    
# unlimited_arguments(*[1,2,3,4,5]) #This will unpack the list, its same as unlimited_arguments(1,2,3,4,5)

def unlimited_arguments(*args, **kargs): 
    print(args)
    print(kargs)
    for k, arg in kargs.items():
        print(k, arg)
    
unlimited_arguments(1,2,3,4,5, name='HSK', age=27, city='Haldwani', country ='India') 