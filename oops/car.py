
# speed = 120

# class Car:
#     max_speed = 100   #class attributes
#     warning = []      #class attributes
#     def drive(self):
#         print('Maximum car speed is {}'.format(self.max_speed))
#         #print('Hey hi speed is {}'.format(speed))
# car1 = Car()
# car1.drive()
# Car.max_speed = 140
# car1.warning.append('Harinder') #still refering to the class attribute

# car2 = Car()
# car2.drive()
# print(car2.warning)             #still refering to the class attribute

'''
Private Attributes can be only accessed within the class not from outside.
Public Attributes/Instance attributes can be accessed from outside the class.
Private attributes can be defined as self.__attributename
'''
from vehicle import Vehicle
class Car(Vehicle):
    #This all is in Vehicel Class
    # def __init__(self, starting_top_speed = 100):     #Constructor
    #     self.max_speed = starting_top_speed           #instance attributes
    #     #self.warning = []                            #instance attributes
    #     self.__warning = []                           #Private instance attribute

    # def add_warning(self, warning_text):
    #     if len(warning_text) > 0:
    #         self.__warning.append(warning_text)

    # def show_warning(self):
    #     return self.__warning
    
    # def __repr__(self):
    #     print('Printing...')
    #     return 'Top Speed is {} and Warning is {}'.format(self.max_speed, self.__warning)
    
    # def drive(self):
    #     print('Car speed is {}'.format(self.max_speed))

    def ShowOff(self):
        print('My car is really fast')

car1=Car()
car1.drive()
car1.add_warning(['hsk'])
print(car1.show_warning())
#car1.warning.append('FromCar1')   #As warning is a public Attribute 
#car1.warning.append('FromCar1')   #Can be accessed from outside as __warnign is private
#print(car1.warning)

print(car1)  #This automatically calls __repr__ method from the class Car.

car2 = Car(200)
car2.drive()
#print(car2.warning)
