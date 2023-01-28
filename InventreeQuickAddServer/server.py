#!/usr/bin/env python3
import json
import os
import re

import digikey
import requests
import structlog
from Config import config, connect_to_inventree
from InventreeParameterTemplateManager import InventreeParameterTemplateManager
from InventreeCompanyManager import InvenTreeManufacturerManager, InvenTreeSupplierManager
from bottle import Bottle, request, response, run
from digikey.v3.productinformation import (KeywordSearchRequest,
                                           KeywordSearchResponse, PidVid,
                                           ProductDetails)

from inventree.part import Parameter, ParameterTemplate, Part, PartCategory
from inventree.stock import StockItem, StockLocation
from InventreeSupplierPartManager import InventreeSupplierManufacturerPartManager

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
        self.inventree = connect_to_inventree()
        self.init_routes()
        self.find_stock_locations()
        self.find_part_categories()
        # Setup distributor API interfaces
        self.setup_digikey()
        self.parameter_templates = InventreeParameterTemplateManager(self.inventree)
        self.suppliers = InvenTreeSupplierManager(self.inventree)
        self.manufacturers = InvenTreeManufacturerManager(self.inventree)
        self.supplier_manufacturer_parts = InventreeSupplierManufacturerPartManager(self.inventree, self.suppliers, self.manufacturers)

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

    def create_part_parameter_if_not_exists(self, part: Part, template: ParameterTemplate, value: str) -> bool:
        """

        Returns:
            bool: if the parameter was created or not
        """
        try:
            Parameter.create(self.inventree, {
                'part': part.pk,
                'template': template.pk,
                'data': value
            })
            return True # Created
        except requests.exceptions.HTTPError as ex:
            if "The fields part, template must make a unique set".lower() in str(ex).lower():
                # This means this part already has the relevant parameter => ignore
                return False
            else:
                # Something else went wrong - re-raise ex
                raise ex

    def add_parameters_to_part(self, part: Part, part_info: PartInfo):
        """Import parameters from part_info to part"""
        if part_info.package:
            if self.create_part_parameter_if_not_exists(part, self.parameter_templates.package, part_info.package):
                self.logger.info("Creating package parameter", part=part_info.mpn, value=part_info.package)
        if part_info.datasheet:
            if self.create_part_parameter_if_not_exists(part, self.parameter_templates.datasheet, part_info.datasheet):
                self.logger.info("Creating datasheet parameter", part=part_info.mpn, value=part_info.datasheet)
        if part_info.manufacturer:
            if self.create_part_parameter_if_not_exists(part, self.parameter_templates.manufacturer, part_info.manufacturer):
                self.logger.info("Creating manufacturer parameter", part=part_info.mpn, value=part_info.manufacturer)

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

            # Search for part number
            metadata = data["metadata"]
            # Fetch location and category from database
            # These are only selectable from EXISTING locations and categories
            category = PartCategory(self.inventree, data["category"])
            location = StockLocation(self.inventree, data["location"])

            part_info: PartInfo = PartInfo()
            part_info.mpn = data["partNumber"]

            # Search on DigiKey
            digikey_result = self.search_digikey(part_info.mpn)
            # Try to find exactly matching MPNs
            if digikey_result.exact_manufacturer_products_count > 0:
                # Copy part properties only from the first exact match
                product: ProductDetails = digikey_result.exact_manufacturer_products[0]
                part_info.description = product.detailed_description
                part_info.datasheet = product.primary_datasheet

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

            # Add supplier parts
            for product in digikey_result.exact_manufacturer_products:
                self.logger.info("Creating DigKey supplier part", mpn=part_info.mpn, sku=product.digi_key_part_number)
                self.supplier_manufacturer_parts.create_supplier_part("Digi-Key", part, {
                    "SKU": product.digi_key_part_number,
                    "link": product.product_url
                })
                # Create manufacturer part
                self.supplier_manufacturer_parts.create_manufacturer_part(product.manufacturer.value, part, {
                    "MPN": part_info.mpn,
                })


            # Add the part to the stock

            response.content_type = 'application/json'
            return {"status": "ok"}

    def run(self):
        run(self.app, host='0.0.0.0', port=50949)

# Example usage
if __name__ == "__main__":
    server = InvenTreeQuickAddServer()
    server.run()
