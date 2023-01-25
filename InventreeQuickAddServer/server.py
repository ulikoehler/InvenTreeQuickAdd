#!/usr/bin/env python3
from bottle import Bottle, run, response, request
from inventree.api import InvenTreeAPI
from inventree.stock import StockLocation
from inventree.part import PartCategory
import json

import digikey
import os
from digikey.v3.productinformation import KeywordSearchRequest

import yaml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

class InvenTreeQuickAddServer(object):
    def __init__(self):
        self.app = Bottle()
        self.inventree = InvenTreeAPI(config["inventree"]["server"], username=config["inventree"]["username"], password=config["inventree"]["password"])
        self.init_routes()
        self.find_stock_locations()
        self.find_part_categories()
        # Setup distributor API interfaces
        self.setup_digikey()

    def setup_digikey(self):
        if "digikey" in config:
            os.makedirs(config["digikey"]["storage_path"], exist_ok=True)
            os.environ['DIGIKEY_CLIENT_ID'] = config["digikey"]["client_id"]
            os.environ['DIGIKEY_CLIENT_SECRET'] = config["digikey"]["client_secret"]
            os.environ['DIGIKEY_CLIENT_SANDBOX'] = str(config["digikey"]["client_sandbox"])
            os.environ['DIGIKEY_STORAGE_PATH'] = config["digikey"]["storage_path"]

    def search_digikey(self, part_number: str):
        search_request = KeywordSearchRequest(keywords=part_number, record_count=10)
        result = digikey.keyword_search(body=search_request)
        return result

    def find_stock_locations(self) -> dict:
        all_stock_locations = StockLocation.list(self.inventree)

        # Dict of part categories by name
        # (e.g. 'OpAmps')
        self.stock_locations_by_name = {
            category["name"]: category
            for category in all_stock_locations
        }
        # Dict of part categories by public key (e.g. 7)
        self.stock_locations_by_pk = {
            category.pk: category
            for category in all_stock_locations
        }
        # Dict of part categories by hierarchical path
        # (e.g. 'Office/Spart parts box')
        self.stock_locations_by_pathstring = {
            category.pathstring: category
            for category in all_stock_locations
        }

    def find_part_categories(self) -> dict:
        all_categories = PartCategory.list(self.inventree)

        # Dict of part categories by name
        # (e.g. 'OpAmps')
        self.part_categories_by_name = {
            category["name"]: category
            for category in all_categories
        }
        # Dict of part categories by public key (e.g. 7)
        self.part_categories_by_pk = {
            category.pk: category
            for category in all_categories
        }
        # Dict of part categories by hierarchical path
        # (e.g. 'Electronics-Components/ICs/OpAmps')
        self.part_categories_by_pathstring = {
            category.pathstring: category
            for category in all_categories
        }

    def init_routes(self):
        """Initialize all routes"""
        @self.app.route('/api/inventree/storage-locations')
        def storage_locations():
            response.content_type = 'application/json'
            return json.dumps([
              {"name": pathstring, "id": location.pk}
              for pathstring, location in self.stock_locations_by_pathstring.items()
            ])

        @self.app.route('/api/inventree/part-categories')
        def part_categories():
            response.content_type = 'application/json'
            return json.dumps([
              {"name": pathstring, "id": category.pk}
              for pathstring, category in self.part_categories_by_pathstring.items()
            ])

        @self.app.route('/api/inventree/add-part', method='POST')
        def add_part():
            data = request.json

            print(data)
            # Search for part number
            metadata = data["metadata"]
            # Fetch location and category from database
            category = PartCategory(self.inventree, data["category"])
            location = StockLocation(self.inventree, data["location"])

            partNumber = data["partNumber"]

            print(f"Searching for part {partNumber} in category {category.name}")
            # Search on DigiKey
            digikey_result = self.search_digikey(data["partNumber"])
            print(digikey_result)
            response.content_type = 'application/json'
            return {"status": "ok"}

    def run(self):
        run(self.app, host='0.0.0.0', port=50949)

# Example usage
if __name__ == "__main__":
    server = InvenTreeQuickAddServer()
    server.run()
