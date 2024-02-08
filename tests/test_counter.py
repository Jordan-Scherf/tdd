from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""


class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        "It Should return an updated value"
        result = self.client.post('/counters/update')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        updatedResult = self.client.put('/counters/update')
        # I have no idea how to get the value out except with json
        self.assertEqual(updatedResult.json, {'update': 1})
        # now lets try to update without a counter existing
        doesntExist = self.client.put('/counter/Null')
        self.assertEqual(doesntExist.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_counter(self):
        "it should return the actual value in the counter"
        result = self.client.post('/counters/test')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        #Lets incrimiment the counter Twice
        self.client.put('/counters/test')
        self.client.put('/counters/test')
        # now lets check that the value of the counter should be 2
        testNumber = self.client.get('/counters/test').text
        self.assertEqual(int(testNumber), 2)
        # now lets try to get a counter that doesnt exist
    
    def test_delete_counter(self):
        "It should delete a counter after its created"
        result = self.client.post('/counters/deleteTest')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.delete('/counters/deleteTest')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        result = self.client.delete('/counters/deleteNotExist')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        