from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Configuration
USERNAME = "d5900938-be95-4412-95b3-50b11983e13e"
PASSWORD = "90fa0de5-250a-4e99-bd65-85b1854d9c82"
BASE_URL = "http://102.33.60.228:9183/getResources"

SALES_REPS_URL = f"{BASE_URL}/sales_reps"
PRODUCTS_URL = f"{BASE_URL}/products"
CUSTOMERS_URL = f"{BASE_URL}/customers"

@app.route('/sales_reps', methods=['GET'])
def get_sales_reps():
    """
    Fetch all sales reps and return a cleaned list.
    """
    try:
        response = requests.get(
            SALES_REPS_URL,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Accept": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            sales_reps = [
                {
                    "rep_code": rep.get("rep_code"),
                    "name": rep.get("name"),
                    "email": rep.get("email"),
                    "uri": rep.get("@uri")
                }
                for rep in data.get("sales_reps", [])
            ]
            return jsonify({"sales_reps": sales_reps}), 200
        else:
            return jsonify({
                "error": f"HTTP {response.status_code}",
                "message": response.reason,
                "details": response.text
            }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500


@app.route('/products', methods=['GET'])
def get_products():
    """
    Fetch products and return only the product_code values.
    """
    try:
        response = requests.get(
            PRODUCTS_URL,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Accept": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            product_codes = [
                product.get("product_code")
                for product in data.get("products", [])
                if product.get("product_code")
            ]
            return jsonify({"product_codes": product_codes}), 200
        else:
            return jsonify({
                "error": f"HTTP {response.status_code}",
                "message": response.reason,
                "details": response.text
            }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500


@app.route('/customers', methods=['GET'])
def get_customer_accounts():
    """
    Fetch customers and return only account_number values.
    """
    try:
        response = requests.get(
            CUSTOMERS_URL,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Accept": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            account_numbers = [
                customer.get("account_number")
                for customer in data.get("customers", [])
                if customer.get("account_number")
            ]
            return jsonify({"account_numbers": account_numbers}), 200
        else:
            return jsonify({
                "error": f"HTTP {response.status_code}",
                "message": response.reason,
                "details": response.text
            }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500


@app.route('/')
def home():
    return "Flask API is running. Endpoints: /sales_reps, /products, /customers"


if __name__ == '__main__':
    app.run(debug=True)
