import { DecodedPartInfo } from "./decoded-part-info";

export interface AddPartParameters {
    partNumber: string;
    /**
     * Inventree part category PK
     */
    category: number;
    /**
     * Inventree storage location PK
     */
    location: number;

    quantity: number;
    /**
     * Any metadata that has been read from the barcode
     */
    metadata?: DecodedPartInfo;
}
