import unittest
import os
os.environ['TESTING'] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "<h1>Adam G. Emerson</h1>" in html
        assert '<div class="profile">' in html
        assert '<ul class="menu">' in html


    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_response = response.get_json()
        self.assertIn("timeline_posts", json_response)
        self.assertEqual(len(json_response["timeline_posts"]), 0)
        
        # Add multiple timeline posts
        self.client.post('/api/timeline_post', data={
            "name": "Alice",
            "email": "alice@example.com",
            "content": "First post"
        })
        self.client.post('/api/timeline_post', data={
            "name": "Bob",
            "email": "bob@example.com",
            "content": "Second post"
        })
        
        # Check the GET API again
        response = self.client.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        json_response = response.get_json()
        self.assertEqual(len(json_response["timeline_posts"]), 2)
        self.assertEqual(json_response["timeline_posts"][0]['name'], "Bob")
        self.assertEqual(json_response["timeline_posts"][1]['name'], "Alice")
        self.assertEqual(json_response["timeline_posts"][0]['content'], "Second post")
        self.assertEqual(json_response["timeline_posts"][1]['content'], "First post")


    def test_timeline_page(self):
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert "<h1>Timeline</h1>" in html
        assert '<form id="timeline-form">' in html

    def test_malformed_timeline_post(self):
        # POST request with missing name
        response = self.client.post('/api/timeline_post', data={
            "email": "john@example.com", "content": "Hello, world, I'm John Doe!"}
        )
        assert response.status_code == 400
        # Check response body
        html = response.get_data(as_text=True)
        print(html)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe", "email": "john@example.com", "content": ""}
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello, world, I'm John Doe!"}
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
        