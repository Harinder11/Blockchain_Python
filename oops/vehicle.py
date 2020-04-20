class Vehicle:
    def __init__(self, starting_top_speed = 100):     #Constructor
            self.max_speed = starting_top_speed           #instance attributes
            #self.warning = []                            #instance attributes
            self.__warning = []                           #Private instance attribute

    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warning.append(warning_text)

    def show_warning(self):
        return self.__warning
        
    def __repr__(self):
        print('Printing...')
        return 'Top Speed is {} and Warning is {}'.format(self.max_speed, self.__warning)
        
    def drive(self):
        print('Car speed is {}'.format(self.max_speed))