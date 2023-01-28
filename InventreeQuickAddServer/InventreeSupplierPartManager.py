#!/usr/bin/env python3
from inventree.company import SupplierPart, ManufacturerPart
from inventree.part import Part
from InventreeCompanyManager import InvenTreeSupplierManager, InvenTreeManufacturerManager
import requests
import structlog
class InventreeSupplierManufacturerPartManager(object):
    def __init__(self, api, suppliers: InvenTreeSupplierManager, manufacturers: InvenTreeManufacturerManager):
        self.api = api
        self.suppliers = suppliers
        self.manufacturers = manufacturers
        self.logger = structlog.get_logger()


    def create_supplier_part_if_not_exists(self, template):
        try:
            return SupplierPart.create(self.api, template)
        except requests.HTTPError as ex:
            if "must make a unique set".lower() in str(ex).lower():
                self.logger.debug("Supplier part already exists", template=template)
                # Ignore this error but fetch the template from the DB
                return SupplierPart.list(self.api, part=template["part"], supplier=template["supplier"], SKU=template["SKU"])[0]
            else:
                # Other exception, re-raise
                raise ex

    def create_manufacturer_part_if_not_exists(self, template):
        try:
            return ManufacturerPart.create(self.api, template)
        except requests.HTTPError as ex:
            if "must make a unique set".lower() in str(ex).lower():
                self.logger.debug("Manufacturer part already exists", template=template)
                # Ignore this error but fetch the template from the DB
                return ManufacturerPart.list(self.api, part=template["part"], manufacturer=template["manufacturer"], MPN=template["MPN"])[0]
            else:
                # Other exception, re-raise
                raise ex

    def create_supplier_part(self, supplier: str, part: Part, template: dict):
        """Create a supplier part, linking a part and a supplier together"""
        template["supplier"] = self.suppliers[supplier].pk
        template["part"] = part.pk
        # Create supplier part if not exists
        return self.create_supplier_part_if_not_exists(template)

    def create_manufacturer_part(self, manufacturer: str, part: Part, template: dict):
        """Create a manufacturer part, linking a part and a manufacturer together"""
        template["manufacturer"] = self.manufacturers[manufacturer].pk
        template["part"] = part.pk
        # Create supplier part
        return self.create_manufacturer_part_if_not_exists(template)
