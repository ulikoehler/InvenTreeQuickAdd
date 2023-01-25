#!/usr/bin/env python3
import json
import os
import re

import digikey
import requests
import structlog
import yaml
from bottle import Bottle, request, response, run
from digikey.v3.productinformation import (KeywordSearchRequest,
                                           KeywordSearchResponse, PidVid,
                                           ProductDetails)
from inventree.api import InvenTreeAPI
from inventree.part import Parameter, ParameterTemplate, Part, PartCategory
from inventree.stock import StockItem, StockLocation

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

class InventreeParameterTemplateManager(object):
    def __init__(self, api: InvenTreeAPI):
        self.api = api
        self.datasheet = self.create_parameter_template_if_not_exists({'name' : 'Datasheet'})
        self.package = self.create_parameter_template_if_not_exists({'name' : 'Package'})
        self.manufacturer = self.create_parameter_template_if_not_exists({'name' : 'Manufacturer'})

    def create_parameter_template_if_not_exists(self, template: dict) -> ParameterTemplate:
        try:
            return ParameterTemplate.create(self.api, template)
        except requests.HTTPError as ex:
            if "part parameter template with this Name already exists".lower() in str(ex).lower():
                # Ignore this error but fetch the template from the DB
                return ParameterTemplate.list(self.api, name=template["name"])[0]
            else:
                # Other exception, re-raise
                raise ex

class PartInfo(object):
    """Abstract part info, indepent of the source"""
    mpn: str = None
    description: str = None
    datasheet: str = None
    package: str = None
    manufacturer: str = None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

class InvenTreeQuickAddServer(object):
    def __init__(self):
        self.logger = structlog.get_logger()

        self.app = Bottle()
        self.inventree = InvenTreeAPI(config["inventree"]["server"], username=config["inventree"]["username"], password=config["inventree"]["password"])
        self.init_routes()
        self.find_stock_locations()
        self.find_part_categories()
        # Setup distributor API interfaces
        self.setup_digikey()
        self.parameter_templates = InventreeParameterTemplateManager(self.inventree)

    def setup_digikey(self):
        if "digikey" in config:
            os.makedirs(config["digikey"]["storage_path"], exist_ok=True)
            os.environ['DIGIKEY_CLIENT_ID'] = config["digikey"]["client_id"]
            os.environ['DIGIKEY_CLIENT_SECRET'] = config["digikey"]["client_secret"]
            os.environ['DIGIKEY_CLIENT_SANDBOX'] = str(config["digikey"]["client_sandbox"])
            os.environ['DIGIKEY_STORAGE_PATH'] = config["digikey"]["storage_path"]

    def create_inventree_parameter_templates(self):
        """Create parameter templates for the parameters we read out"""

    def search_digikey(self, part_number: str) -> KeywordSearchResponse:
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

    def get_or_create_part(self, partInfo: PartInfo, category_pk: int):
        """Get or create a part"""
        # Check if the part already exists
        try:
            return Part.list(self.inventree, name_regex=re.escape(partInfo.mpn))[0]
        except IndexError:
            print(f"Creating part {partInfo.mpn}, does not exist yet")
            # Part does not exist, create it
            return Part.create(self.inventree, {
                'name': partInfo.mpn,
                'description': partInfo.description,
                'category': category_pk
            })

    def add_parameters_to_part(self, part: Part, part_info: PartInfo):
        """Import parameters from part_info to part"""
        if part_info.package:
            self.logger.info("Creating package parameter", part=part_info.mpn, value=part_info.package)
            Parameter.create(self.inventree, {
                'part': part.pk,
                'template': self.parameter_templates.package.pk,
                'data': part_info.package
            })
        if part_info.datasheet:
            self.logger.info("Creating datasheet parameter", part=part_info.mpn, value=part_info.datasheet)
            Parameter.create(self.inventree, {
                'part': part.pk,
                'template': self.parameter_templates.datasheet.pk,
                'data': part_info.datasheet
            })
        if part_info.manufacturer:
            self.logger.info("Creating manufacturer parameter", part=part_info.mpn, value=part_info.manufacturer)
            Parameter.create(self.inventree, {
                'part': part.pk,
                'template': self.parameter_templates.manufacturer.pk,
                'data': part_info.manufacturer
            })

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

            part_info: PartInfo = PartInfo()
            part_info.mpn = data["partNumber"]

            # Search on DigiKey
            digikey_result = self.search_digikey(part_info.mpn)
            # Try to find exactly matching MPNs
            if digikey_result.exact_manufacturer_products_count > 0:
                # Exact match on manufacturer part number
                product: ProductDetails = digikey_result.exact_manufacturer_products[0]
                part_info.description = product.detailed_description
                part_info.datasheet = product.primary_datasheet
                part_info["Manufacturer"] = product.manufacturer.value
                for parameter in product.parameters:
                    if parameter.parameter == "Supplier Device Package":
                        part_info.package = parameter.value
            elif digikey_result.exact_digi_key_product is not None:
                # Exact match on DigiKey part number
                pass # TODO

            ###
            # Create the part in InvenTree
            ###
            part = self.get_or_create_part(part_info, category.pk)
            self.add_parameters_to_part(part, part_info)
            # Add the part to the stock

            print(part_info)

            response.content_type = 'application/json'
            return {"status": "ok"}

    def run(self):
        run(self.app, host='0.0.0.0', port=50949)

# Example usage
if __name__ == "__main__":
    server = InvenTreeQuickAddServer()
    server.run()
