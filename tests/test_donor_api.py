import unittest
from flask import Flask
from app import db, create_app

class DonorResourceTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_get_donor_list(self):
        response = self.client.get('/donors/')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your application logic
        
    def test_add_new_donor(self):
        data = {
            'name': 'John Doe',
            'age': 30,
            'blood_group': 'AB+',
            'email_id': 'johndoe@example.com'
        }
        
        response = self.client.post('/donors/', json=data)
        self.assertEqual(response.status_code, 201)
        # Add more assertions based on your application logic
        
if __name__ == '__main__':
    unittest.main()
