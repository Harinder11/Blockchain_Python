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

print(average(3, get_userinput()))