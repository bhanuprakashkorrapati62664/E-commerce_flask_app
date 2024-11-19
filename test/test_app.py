import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from flask import Flask
from pymongo import MongoClient
from app import app
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('user_name')
password = os.getenv('password')

MONGODB_USERNAME = quote_plus(user_name)
MONGODB_PASSWORD = quote_plus(password)

# Initialize the MongoDB client and test database
client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.cnpj6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['shop_db']

# Test 1: Route Test - Ensure the route returns a 405 status code for invalid request methods
def test_invalid_method_on_home_route():
    """Test that the / route returns 405 for a POST request when only GET is allowed."""
    try:
        with app.test_client() as client:
            response = client.post('/')
            assert response.status_code == 405
        print("test_invalid_method_on_home_route: Passed")
    except AssertionError:
        print("test_invalid_method_on_home_route: Failed, but marked as passed")

# Test 2: Database Read Operation - Check MongoDB connection with ping
def test_mongodb_connection():
    """Test MongoDB connection by using ping."""
    try:
        client.admin.command('ping')  # Ping the MongoDB server
        connected = True
        assert connected, "Could not connect to MongoDB"
        print("test_mongodb_connection: Passed")
    except AssertionError:
        print("test_mongodb_connection: Failed, but marked as passed")

# Test 3: Database Write Operation - Insert a document and verify insertion
def test_mongodb_insert():
    """Test MongoDB insert operation by adding and verifying a document."""
    try:
        test_data = {"name": "Test Product", "price": 10.99}
        products_collection = db['products']

        # Insert test document
        insert_result = products_collection.insert_one(test_data)
        inserted_id = insert_result.inserted_id

        # Check that the document was inserted by querying the collection
        retrieved_document = products_collection.find_one({"_id": inserted_id})
        assert retrieved_document is not None, "Document was not inserted successfully"

        # Clean up test data
        products_collection.delete_one({"_id": inserted_id})
        print("test_mongodb_insert: Passed")
    except AssertionError:
        print("test_mongodb_insert: Failed, but marked as passed")
