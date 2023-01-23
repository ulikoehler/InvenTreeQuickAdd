export interface DecodedPartInfo {
    RawBarcode: string;
    Quantity?: number;
    DistributorPartNumber?: string;
    ManufacturerPartNumber?: string;
    OrderPosition?: number;
    CustomerOrderNumber?: string;
    CustomerOrderDescription?: string;
    CustomerPartNumber?: string;
    Revision?: string; // Chip revision
    LotNumber?: string;
    /**
     * TI:
     *  - TKY - full turnkey processing
     *  - NTY - non turnkey processing
     *  - SWR - special work request (engineering material)
     */
    TurnkeyProcessingType?: string;
    Manufacturer?: string;
    CountryOfOrigin?: string;
    CountryOfWaferFab?: string;
    LocationOfWaferFab?: string;
    LocationOfAssemblySite?: string;
    CountryOfAssemblySite?: string;
    /**
     * TI: Always 0033317
     */
    WorldwideISOSupplierID?: string;
    DateCode?: string;
    PartID?: string; // Supplier-specific
    LoadID?: string; // Supplier-specific
    SupplierURL?: string; // Supplier-specific URL for this part
    Distributor?: string; // DigiKey, Mouser, LCSC, TME, ...
    DistributorWarehouseRemark?: string; // Remarks about picking & sorting process
}
