from flask import Flask, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.cnpj6.mongodb.net/shop_db?retryWrites=true&w=majority")
db = client['shop_db']
products_collection = db['products']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    products_data = list(products_collection.find())
    return render_template('products.html', products=products_data)

if __name__ == '__main__':
    app.run(debug=True)
