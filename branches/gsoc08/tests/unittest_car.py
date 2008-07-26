import unittest

import pygame
from pygame.locals import *

import libcarcode.car

class testCar(unittest.TestCase):
    """ Test case for car class """
    
    def setUp(self):
        pygame.mixer.init()
        self.car = libcarcode.car.Car()
    
    def testEngine(self):
        # Test default initial engine state
        self.assertEqual(self.car.running,  True)
        
        # Test setting engine on
        self.car.engine_off()
        self.assertEqual(self.car.running,  False)
        
        # Test setting engine off
        self.car.engine_on()
        self.assertEqual(self.car.running,  True)
        
        # Test switching engine state
        self.car.flip_engine()
        self.assertEqual(self.car.running,  False)
        
    def testGear(self):
        # Test default initial gear state
        self.assertEqual(self.car.forward_gear,  True)
        
        # Test setting gear reverse
        self.car.set_gear_reverse()
        self.assertEqual(self.car.forward_gear,  False)
        
        # Test setting gear forward
        self.car.set_gear_forward()
        self.assertEqual(self.car.forward_gear,  True)
        
        # Test switching gear state
        self.car.flip_gear()
        self.assertEqual(self.car.forward_gear,  False)
        
    def testSteerLeft(self):
        self.car.accelerate()
        
        # Steer left
        self.car.steer_left()
        self.assert_(self.car.angle > 0)
    
    def testSteerLeft370(self):
        self.car.accelerate()
        
        # Steer over 360 degrees
        self.car.steer_left(370)
        self.assert_(self.car.angle == 10)
        
    def testSteerLeftReverse(self):
        self.car.accelerate()
        self.car.set_gear_reverse()
        
        # Steer left in reverse gear
        self.car.steer_left(7)
        self.assert_(self.car.angle == 353)

    def testSteerRight(self):
        self.car.accelerate()
        
        # Steer left
        self.car.steer_right()
        self.assert_(self.car.angle == 353)
    
    def testSteerRight370(self):
        self.car.accelerate()
        
        # Steer over 360 degrees
        self.car.steer_right(-370)
        self.assert_(self.car.angle == 350)
        
    def testSteerRightReverse(self):
        self.car.accelerate()
        self.car.set_gear_reverse()
        
        # Steer left in reverse gear
        self.car.steer_right()
        self.assert_(self.car.angle == 7)
        
def suite():
    """ Create a test suite from test cases """
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testCar))
    
    return suite
