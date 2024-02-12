######################################################################
# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# spell: ignore Rofrano jsonify restx dbname
"""
Product Store Service with UI
"""
from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app


######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# H O M E   P A G E
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# C R E A T E   A   N E W   P R O D U C T
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product = Product()
    product.deserialize(data)
    product.create()
    app.logger.info("Product with new id [%s] saved!", product.id)

    message = product.serialize()

    #
    # Uncomment this line of code once you implement READ A PRODUCT
    #
    # location_url = url_for("get_products", product_id=product.id, _external=True)
    location_url = "/"  # delete once READ is implemented
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# L I S T   A L L   P R O D U C T S
######################################################################

#
# PLACE YOUR CODE TO LIST ALL PRODUCTS HERE
#

def test_get_product_list(self):
    """It should Get a list of Products"""
    self._create_products(5)
    response = self.client.get(BASE_URL)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), 5)

######################################################################
# R E A D   A   P R O D U C T
######################################################################

#
# PLACE YOUR CODE HERE TO READ A PRODUCT
#

######################################################################
# U P D A T E   A   P R O D U C T
######################################################################

#
# PLACE YOUR CODE TO UPDATE A PRODUCT HERE
#
def test_update_product(self):
    """It should Update an existing Product"""
    # create a product to update
    test_product = ProductFactory()
    response = self.client.post(BASE_URL, json=test_product.serialize())
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # update the product
    new_product = response.get_json()
    new_product["description"] = "unknown"
    response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    updated_product = response.get_json()
    self.assertEqual(updated_product["description"], "unknown")
######################################################################
# D E L E T E   A   P R O D U C T
######################################################################


#
# PLACE YOUR CODE TO DELETE A PRODUCT HERE
#
def test_delete_product(self):
    """It should Delete a Product"""
    products = self._create_products(5)
    product_count = self.get_product_count()
    test_product = products[0]
    response = self.client.delete(f"{BASE_URL}/{test_product.id}")
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
    response = self.client.get(f"{BASE_URL}/{test_product.id}")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    new_count = self.get_product_count()
    self.assertEqual(new_count, product_count - 1)


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return product.serialize(), status.HTTP_200_OK

def test_get_product_not_found(self):
    """It should not Get a Product thats not found"""
    response = self.client.get(f"{BASE_URL}/0")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    data = response.get_json()
    self.assertIn("was not found", data["message"])

def test_query_by_name(self):
    """It should Query Products by name"""
    products = self._create_products(5)
    test_name = products[0].name
    name_count = len([product for product in products if product.name == test_name])
    response = self.client.get(
    BASE_URL, query_string=f"name={quote_plus(test_name)}")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), name_count)
    # check the data just to be sure
    for product in data:
     self.assertEqual(product["name"], test_name)

def test_query_by_category(self):
    """It should Query Products by category"""
    products = self._create_products(10)
    category = products[0].category
    found = [product for product in products if product.category == category]
    found_count = len(found)
    logging.debug("Found Products [%d] %s", found_count, found)

        # test for available
    response = self.client.get(BASE_URL, query_string=f"category={category.name}")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    data = response.get_json()
    self.assertEqual(len(data), found_count)
        # check the data just to be sure
    for product in data:
            self.assertEqual(product["category"], category.name)

def test_query_by_availability(self):
    """It should Query Products by availability"""
    products = self._create_products(10)
    available_products = [product for product in products if product.available is True]
    available_count = len(available_products)        
        # test for available
    response = self.client.get(
     BASE_URL, query_string="available=true")
     self.assertEqual(response.status_code, status.HTTP_200_OK)
     data = response.get_json()
     self.assertEqual(len(data), available_count)
        # check the data just to be sure
     for product in data:
            self.assertEqual(product["available"], True)