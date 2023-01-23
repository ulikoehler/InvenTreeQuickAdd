
import { Result, BarcodeFormat } from '@zxing/library';
import { Injectable } from '@angular/core';
import {DecodedPartInfo} from './decoded-part-info';

@Injectable({
    providedIn: 'root'
})
export class BarcodeValueDecoderService {

    constructor() { }

    /**
     * Parse standard DataMatrix based codes such as TI
     */
    parseDataMatrix(text: string, parts: string[], distributor: string): DecodedPartInfo {
        const info: DecodedPartInfo = {Distributor: distributor, RawBarcode: text};
        for (const part of parts) {
            if (part.startsWith("4L")) { // Country of origin
                info.CountryOfOrigin = part.substring(2);
            } else if (part.startsWith("Q")) {
                info.Quantity = Number(part.substring(1));
            } else if (part.startsWith("K")) {
                info.CustomerOrderNumber = part.substring(1);
            } else if (part.startsWith("P")) {
                if(distributor == "Mouser") {
                    info.CustomerPartNumber = part.substring(1);
                } else {
                    info.DistributorPartNumber = part.substring(1);
                }
            } else if (part.startsWith("1P")) {
                info.ManufacturerPartNumber = part.substring(2);
            } else if (part.startsWith("14K")) {
                info.OrderPosition = Number(part.substring(3));
            } else if (part.startsWith("1V")) {
                info.Manufacturer = part.substring(2);
            } else if (part.startsWith("2P")) {
                info.Revision = part.substring(2);
            } else if (part.startsWith("31T")) {
                info.LotNumber = part.substring(3);
            } else if (part.startsWith("4W")) {
                info.TurnkeyProcessingType = part.substring(2);
            } else if (part.startsWith("20L")) {
                info.LocationOfWaferFab = part.substring(3);
            } else if (part.startsWith("21L")) {
                info.CountryOfWaferFab = part.substring(3);
            } else if (part.startsWith("22L")) {
                info.LocationOfAssemblySite = part.substring(3);
            } else if (part.startsWith("23L")) {
                info.CountryOfAssemblySite = part.substring(3);
            } else if (part.startsWith("V")) {
                info.WorldwideISOSupplierID = part.substring(1);
            } else if (part.startsWith("D")) {
                info.DateCode = part.substring(1);
            } else if (part.startsWith("12Z")) {
                info.PartID = part.substring(3);
            } else if (part.startsWith("13Z")) {
                info.LoadID = part.substring(3);
            } else {
                console.info(`Unknown DataMatrix entry: ${part}`);
            }
        }
        return info;
    }

    parseTME(text: string, parts: string[]): DecodedPartInfo {
        const info: DecodedPartInfo = {Distributor: "TME", RawBarcode: text};
        for (const part of parts) {
            if (part.startsWith("http")) {
                // The entire part is an URL
                info.SupplierURL = part;
            } else if (part == "RoHS") {
                // At the moment, ignore this
            }
            const [key, value] = part.split(":");
            if (key == "QTY") {
                info.Quantity = Number(value);
            } else if (key == "PN") {
                info.CustomerPartNumber = value;
            } else if (key == "MPN") {
                info.CustomerPartNumber = value;
            } else if (key == "CPO") {
                info.CustomerOrderDescription = value;
            } else if (key == "MFR") {
                info.Manufacturer = value;
            } else if (key == "PO") {
                info.CustomerOrderNumber = value;
            } else {
                console.info(`Unknown TME key: ${key}=${value}`);
            }
        }
        return info;
    }

    parseLCSC(text: string): DecodedPartInfo {
        // Remove "{" and "}" at either end
        if (text.startsWith("{")) {
            text = text.substring(1);
        }
        if (text.endsWith("}")) {
            text = text.substring(0, text.length - 1);
        }
        // Split!
        const parts = text.split(",");

        const info: DecodedPartInfo = {Distributor: "LCSC", RawBarcode: text};
        for (const part of parts) {
            const [key, value] = part.split(":");
            if(key == "pbn") {
                info.DistributorWarehouseRemark = value
            } else if(key == "on") {
                // Customer order number
                info.CustomerOrderNumber = value;
            } else if(key == "cc") {
                // ???
            } else if(key == "pdi") {
                // ???
            }  else if(key == "hp") {
                // ???
            } else if(key == "pc") {
                // LCSC part number
                info.DistributorPartNumber = value;
            } else if(key == "qty") {
                // LCSC part number
                info.Quantity = Number(value);
            } else if(key == "pc") {
                // LCSC part number
                info.DistributorPartNumber = value;
            } else if(key == "pm") {
                // Manufacturer part number
                info.ManufacturerPartNumber = value;
            } else if(key == "wc") {
                // ?? country of origin?
                info.CountryOfOrigin = value;
            }
        }
        return info;
    }

    decodeBarcode(result: Result): any {
        const text = result.getText();
        if (result.getBarcodeFormat() == BarcodeFormat.DATA_MATRIX) {
            // DigiKey or Mouser!
            if (text.startsWith(">[)>06")) {
                // MOUSER codes are just separated by \x1D
                const parts = text.split("\x1D");
                return this.parseDataMatrix(text, parts, "Mouser");
            } else if (text.startsWith("[)>")) { // DigiKey or TI, same format
                const primaryParts = text.split("\x1E");
                const data = primaryParts[1];
                // primaryParts[0] == '[)>'
                const isTexasInstruments = data.includes("V0033317");
                return this.parseDataMatrix(text, data.split("\x1D"), isTexasInstruments ? "TexasInstruments" : "DigiKey");
            }
        } else if (result.getBarcodeFormat() == BarcodeFormat.QR_CODE) {
            // TME or LCSC
            if (text.startsWith("{")) { // LCSC
                return this.parseLCSC(text);
            } else if (text.startsWith("QTY:")) { // TME
                const parts = text.split(" ");
                return this.parseTME(text, parts);
            }
        }
        return null;
    }
}
