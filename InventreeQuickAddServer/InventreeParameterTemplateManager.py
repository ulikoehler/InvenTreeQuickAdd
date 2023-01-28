#!/usr/bin/env python3
from inventree.api import InvenTreeAPI
from inventree.part import Parameter, ParameterTemplate
import requests

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
