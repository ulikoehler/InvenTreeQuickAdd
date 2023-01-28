#!/usr/bin/env python3
import yaml
from inventree.api import InvenTreeAPI

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

def connect_to_inventree() -> InvenTreeAPI:
    """Connect to the Inventree server"""
    return InvenTreeAPI(
        config["inventree"]["url"],
        username=config["inventree"]["username"],
        password=config["inventree"]["password"],
    )
