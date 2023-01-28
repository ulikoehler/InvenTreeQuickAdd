#!/usr/bin/env python3
from inventree.company import Company, SupplierPart, ManufacturerPart
from inventree.part import Part
from InventreeCompanyManager import InvenTreeCompanyManager


class InventreeSupplierPartManager(object):
    def __init__(self, api, supplier_manager: InvenTreeCompanyManager):
        self.api = api
        self.supplier_manager = supplier_manager

    def create_supplier_part(self, supplier: str, part: Part, template: dict):
        """Create a supplier part, linking a part and a supplier together"""
        template["supplier"] = self.supplier_manager[supplier].pk
        template["part"] = part.pk
        # Create supplier part
        return SupplierPart.create(self.api, template)
