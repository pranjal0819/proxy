import json
import pdb

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import requests


class ProxyViewTests(TestCase):

    def setUp(self):
        self.proxy_url = reverse("proxy_view")
        self.valid_target_url = "https://example.com/api/resource"
        self.invalid_target_url = "https://invalid-url.com"

    @patch("requests.get")
    def test_missing_target_url(self, mock_get):
        """Test request with missing target_url parameter"""
        response = self.client.get(self.proxy_url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Target URL is required"})

    @patch("requests.get")
    def test_valid_get_request(self, mock_get):
        """Test valid GET request with target_url parameter"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = "mocked content"
        mock_get.return_value.headers = {"Content-Type": "text/plain"}

        response = self.client.get(self.proxy_url, {"target_url": self.valid_target_url, "key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"mocked content")
        self.assertEqual(response["Content-Type"], "text/plain")

    @patch("requests.post")
    def test_valid_post_request(self, mock_post):
        """Test valid POST request with target_url parameter"""
        mock_post.return_value.status_code = 201
        mock_post.return_value.content = '{"success": true}'
        mock_post.return_value.headers = {"Content-Type": "application/json"}

        response = self.client.post(
            f"{self.proxy_url}?target_url={self.valid_target_url}",
            json.dumps({"key": "value"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'{"success": true}')
        self.assertEqual(response["Content-Type"], "application/json")

    @patch("requests.put")
    def test_valid_put_request(self, mock_put):
        """Test valid PUT request with target_url parameter"""
        mock_put.return_value.status_code = 200
        mock_put.return_value.content = '{"updated": true}'
        mock_put.return_value.headers = {"Content-Type": "application/json"}

        response = self.client.put(
            f"{self.proxy_url}?target_url={self.valid_target_url}",
            json.dumps({"key": "value"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"updated": true}')
        self.assertEqual(response["Content-Type"], "application/json")

    @patch("requests.delete")
    def test_valid_delete_request(self, mock_delete):
        """Test valid DELETE request with target_url parameter"""
        mock_delete.return_value.status_code = 204
        mock_delete.return_value.content = ""
        mock_delete.return_value.headers = {"Content-Type": "text/plain"}

        response = self.client.delete(f"{self.proxy_url}?target_url={self.valid_target_url}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(response["Content-Type"], "text/plain")

    @patch("requests.get")
    def test_4xx_error_from_target(self, mock_get):
        """Test handling of 4xx error from target server"""
        mock_get.return_value.status_code = 404
        mock_get.return_value.content = "Not Found"

        response = self.client.get(self.proxy_url, {"target_url": self.valid_target_url})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Not Found")

    @patch("requests.get")
    def test_5xx_error_from_target(self, mock_get):
        """Test handling of 5xx error from target server"""
        mock_get.return_value.status_code = 500
        mock_get.return_value.content = "Internal Server Error"

        response = self.client.get(self.proxy_url, {"target_url": self.valid_target_url})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, b"Internal Server Error")

    @patch("requests.get")
    def test_network_error(self, mock_get):
        """Test network error handling (e.g., connection issues)"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        response = self.client.get(self.proxy_url, {"target_url": self.invalid_target_url})
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {"error": "Network error"})
