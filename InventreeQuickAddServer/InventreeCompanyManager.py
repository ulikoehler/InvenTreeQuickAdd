#!/usr/bin/env python3
from inventree.company import Company, SupplierPart, ManufacturerPart
import requests
import yaml
import structlog
from Config import *
import tempfile
from urllib.parse import urlsplit
import os.path

class InvenTreeCompanyManager(object):
    def __init__(self, api):
        self.api = connect_to_inventree()
        self.logger = structlog.get_logger()
        self.standard_suppliers = {}
        # Create suppliers & manufacturers from Suppliers.yml
        with open("Suppliers.yml", "r") as infile:
            _config = yaml.safe_load(infile)
        self.default_currency = _config["config"]["currency"]
        self.suppliers_config = {
            supplier["name"]: supplier
            for supplier in _config["suppliers"]
        }

    def set_company_image(self, company: Company, image_url: str):
        # Get extension from image_url
        path = urlsplit(image_url).path
        extension = os.path.splitext(path)[-1] # e.g. ".jpg"
        # Create named temporary file
        with tempfile.NamedTemporaryFile(suffix=extension) as image_file:
            # Download image to temporary file
            image_file.write(requests.get(image_url).content)
            # Upload image to InvenTree
            company.uploadImage(image_file.name)
            # Delete temporary file
            image_file.close()

    def create_standard_supplier(self, template):
        # Suppliers always get assigned a default of manufacturer=False, supplier=True, customer=False
        template["is_manufacturer"] = False if "is_manufacturer" not in template else template["is_manufacturer"]
        template["is_supplier"] = True if "is_supplier" not in template else template["is_supplier"]
        template["is_customer"] = False if "is_customer" not in template else template["is_customer"]
        template["currency"] = self.default_currency if "currency" not in template else template["currency"]

        # Download remote image
        image_url = None
        if "remote_image" in template:
            image_url = template["remote_image"]
            del template["remote_image"]

        self.standard_suppliers[template["name"]] =  self.create_supplier_if_not_exists(template)
        # Add image, if any
        if image_url:
            self.set_company_image(self.standard_suppliers[template["name"]], image_url)

    def __getitem__(self, key):
        if key not in self.standard_suppliers:
            # Create supplier
            self.create_standard_supplier(self.suppliers_config[key])
        return self.standard_suppliers[key]

    def create_supplier_if_not_exists(self, template: dict):
        # Try to find existing company
        existing_companies = Company.list(self.api, name=template["name"])
        if len(existing_companies) > 0:
            return existing_companies[0]
        self.logger.info("Supplier does not exist, creating...", supplier=template["name"])
        # else: Create new company
        return Company.create(self.api, template)

if __name__ == "__main__":
    api = connect_to_inventree()
    company_manager = InvenTreeCompanyManager(api)
    # Create all suppliers (normally they are created on-demand)
    for name, template in company_manager.suppliers_config.items():
        company_manager.create_standard_supplier(template)
