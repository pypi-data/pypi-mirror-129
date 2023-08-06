# unitgen

Generate unit tests boilerplate code

This is a simple tool to generate boilerplate code for unit tests. It is for those developers who are not able to follow TDD (Test Driven Development) for few methods and want to write unit tests for them after writing the actual code.

All the test files are generated in a folder named "tests" if it does not exist.

Example:
examples/calci.py
```python
import math

class Calci:
    def __init__(self):
        print("Calci class created")

    def add(self, a, b=0):
        c = a + b
        return c

    def sub(self, a, b):
        return a - b


class StringCalci:
    def concat(self, a, b):
        return a + b

    def repeat(self, a, b):
        return a * b
```

Run unitgen from command line:
```bash
# View how to use unitgen
unitgen

# all files under examples directory are processed
unitgen examples

# Files calci.py and pay_handler.py are processed
unitgen examples/calci.py examples/pay_handler.py
```

Generated result:
tests/test_calci.py
```python

from unittest import TestCase
from examples.calci import Calci, StringCalci


class TestCalci(TestCase):
    def setUp(self):
        """ Set up objects for each test """
        
        self.calci = Calci()
    
    
    def test___init__(self):
        """ Test initialiser """
        self.obj = Calci()
    
    
    
    def test_add(self):
        
        a = None
        b = None
        actual_result = self.calci.add(a, b)
        expected_result = None
        self.assertEqual(actual_result, expected_result)
    
    
    
    def test_sub(self):
        
        a = None
        b = None
        actual_result = self.calci.sub(a, b)
        expected_result = None
        self.assertEqual(actual_result, expected_result)
    
    
    def tearDown(self):
        """ Destroy objects after each test """

class TestStringCalci(TestCase):
    def setUp(self):
        """ Set up objects for each test """
        
        self.string_calci = StringCalci()
    
    
    def test_concat(self):
        
        a = None
        b = None
        actual_result = self.string_calci.concat(a, b)
        expected_result = None
        self.assertEqual(actual_result, expected_result)
    
    def test_repeat(self):
        
        a = None
        b = None
        actual_result = self.string_calci.repeat(a, b)
        expected_result = None
        self.assertEqual(actual_result, expected_result)
    
    
    def tearDown(self):
        """ Destroy objects after each test """
```

Enjoy!

My Github profile: [susmitpy](https://www.github.com/susmitpy)

My Linkedin profile: [susmit vengurlekar](https://www.linkedin.com/in/susmit-vengurlekar/)

My Medium profile: [susmit.py](https://medium.com/@susmit.py)