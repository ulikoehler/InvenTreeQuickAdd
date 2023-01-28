#!/usr/bin/env python3
from inventree.company import Company, SupplierPart, ManufacturerPart
import requests
import yaml
import structlog

class InvenTreeCompanyManager(object):
    def __init__(self, api):
        self.api = api
        self.logger = structlog.get_logger()
        self.standard_suppliers = {}

    def create_standard_suppliers(self):
        with open("Suppliers.yml", "r") as infile:
            self._suppliers_config = yaml.safe_load(infile)
        self.logger.info("Creating standard suppliers")
        for supplier in self._suppliers_config.suppliers:
            # Suppliers always get assigned a default of manufacturer=False, supplier=True
            supplier["is_manufacturer"] = False
            supplier["is_supplier"] = True

            self.standard_suppliers[supplier["name"]] =  self.create_supplier_if_not_exists(supplier)

    def __getitem__(self, key):
        return self.standard_suppliers[key]

    def get_or_create_digikey(self):
        """Create the DigiKey Company with standard parameters"""
        self.create_supplier_if_not_exists({
        })

    def get_or_create_mouser(self):
        """Create the Mosuer supplier with standard parameters"""

    def create_supplier_if_not_exists(self, template: dict):
        try:
            return Company.create(self.api, template)
        except requests.HTTPError as ex:
            if "Supplier with this Name already exists".lower() in str(ex).lower():
                # Ignore this error but fetch the template from the DB
                return Company.list(self.api, name=template["name"])[0]
            else:
                # Other exception, re-raise
                raise ex
