
import collections
import json
import pickle
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

# def unlimited_arguments(*args, **kargs): 
#     print(args)
#     print(kargs)
#     for k, arg in kargs.items():
#         print(k, arg)
    
# unlimited_arguments(1,2,3,4,5, name='HSK', age=27, city='Haldwani', country ='India') 



'''
difference between json and pickle, there is no data loss in pickle.
below eg. shows pickle outputs Ordereddict as well whereas json does not. Advantage of json is we can read the output data in pickle its binary.
'''
ord_dict = collections.OrderedDict([('name','HSK'),('age',30),('country','India')])
print('ordered dictionary is:',ord_dict)
#OrderedDict([('name', 'HSK'), ('age', 30), ('country', 'India')])
str_normal = ('This is harinder \n and I am from UK')
json_str = json.dumps(ord_dict)
print('json_str is:',json_str)
#json_str is: {"name": "HSK", "age": 30, "country": "India"}
json_pyobj = json.loads(json_str)
print('json_pyobj is:',json_pyobj)

pickle_str = pickle.dumps(ord_dict)
print('pickle_str is:', pickle_str)
#pickle_str is: b'\x80\x04\x95K\x00\x00\x00\x00\x00\x00\x00\x8c\x0bcollections\x94\x8c\x0bOrderedDict\x94\x93\x94)R\x94(\x8c\x04name\x94\x8c\x03HSK\x94\x8c\x03age\x94K\x1e\x8c\x07country\x94\x8c\x05India\x94u.'
pickle_pyobj = pickle.loads(pickle_str)
print('pickle_pyobj is:', pickle_pyobj)