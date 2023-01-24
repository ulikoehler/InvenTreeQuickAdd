#!/usr/bin/env python3
from bottle import Bottle, run, response
from inventree.api import InvenTreeAPI
from inventree.stock import StockLocation
from inventree.part import PartCategory
import json

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

        @self.app.route('/api/inventree/add-part')
        def part_categories():
            response.content_type = 'application/json'
            return json.dumps([
              {"name": pathstring, "id": category.pk}
              for pathstring, category in self.part_categories_by_pathstring.items()
            ])

    def run(self):
        run(self.app, host='0.0.0.0', port=50949)

# Example usage
if __name__ == "__main__":
    server = InvenTreeQuickAddServer()
    server.run()
