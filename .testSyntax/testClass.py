"""
Test Code to Verify that Python Always Pass by Reference for Numpy Objects
Nested Class Case:
    Class member numpy array is passed into its nested class by reference
    and entry changes to the array in the nested class' method will be reflected in the original array from the     outer level class' members.
"""
import numpy as np

class Car:
    def __init__(self,N):
        self.Devices = np.zeros((N, N), dtype = float)
        self.batteries = []
        for i in range(3):
            self.batteries.append(self.Battery(self.Devices))


    class Battery:
        def __init__(self, arr):
            self.connected_devices = arr
        def charge(self, i, j, v):
            self.connected_devices[i,j] = v


# Object A
myCar = Car(4)

print("before charging myCar.Devices = \n", myCar.Devices)

myCar.batteries[0].charge(0,0, 2)

print("after battery0.charge myCar.Devices  = \n", myCar.Devices)

print("after battery0.charge battery[0].connected_devices  = \n", myCar.batteries[0].connected_devices)

myCar.batteries[1].charge(1, 1, 3)

print("after battery1.charge myCar.Devices  = \n", myCar.Devices)

print("after battery1.charge battery[0].connected_devices  = \n", myCar.batteries[0].connected_devices)
