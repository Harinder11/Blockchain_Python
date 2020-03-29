"""
While calling the function whatever argument we pass has 
preference over the default argument.

"""

def average(first_number, second_number = 6):
    print('first number is', first_number)
    print('second number is', second_number)
    avg = (first_number + second_number)/2
    return avg

def get_userinput():
    return int(input("please enter your nummber"))

#In this case it will take the default argument that is 6
print(average(3))

#Here the function average will take the second argument from get_userinput()
print(average(3, get_userinput()))