import unittest
import unittest_car

# Load all test suites
carsuite = unittest_car.suite()

#Create main test suite
suite = unittest.TestSuite()

#add all tests to main suite
suite.addTest(carsuite)

# Run Unittest
unittest.TextTestRunner(verbosity=2).run(suite)
