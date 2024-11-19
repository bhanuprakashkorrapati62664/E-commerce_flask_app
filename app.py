from flask import Flask, render_template
from pymongo import MongoClient
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

user_name = os.getenv('user_name')
password = os.getenv('password')

MONGODB_USERNAME = quote_plus(user_name)
MONGODB_PASSWORD = quote_plus(password)
client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.cnpj6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
print(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.cnpj6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['shop_db']
products_collection = db['products']

products = [
    {
        "name": "Picture1",
        "tag": "Electronics",
        "price": 25.99,
        "image_path": "static/images/product1.jpg"
    },
    {
        "name": "Bluetooth Speaker",
        "tag": "Electronics",
        "price": 45.50,
        "image_path": "static/images/product2.jpg"
    },
]
insert_result = products_collection.insert_many(products)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    products_data = list(products_collection.find())
    return render_template('products.html', products=products_data)

if __name__ == '__main__':
    app.run(debug=True)
