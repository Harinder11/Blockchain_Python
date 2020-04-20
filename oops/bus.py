import vehicle

class Bus(vehicle.Vehicle):
    def __init__(self, speed=90):
        super().__init__(speed) #Calling base class constructor with added attributes otherwise it overwrites
        self.passengers = []

    def add_passengers(self, passenger):
        self.passengers.extend(passenger)

bus1 = Bus(110)
bus1.drive()
bus1.add_warning(['KO'])
print(bus1.show_warning())
bus1.add_passengers(['Hsk','Shruti','Koranga'])
print(bus1.passengers)