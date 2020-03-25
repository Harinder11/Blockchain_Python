
#With Global keyword

name = "HSK"

def get_name():
    global name
    name = input('Your name please')

get_name()
print(name)

"""
#Without global keyword
name = "HSK"

def get_name():
    name = input('Your name please')

get_name()
print(name)
"""