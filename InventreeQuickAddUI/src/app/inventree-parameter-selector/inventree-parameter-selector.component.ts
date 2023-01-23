import { Component, OnInit } from '@angular/core';
import { InventreeQuickAddService } from '../inventree-quick-add.service';

const localStoragePartCategoryKey = "inventreePartCategory";
const localStorageStorageLocationKey = "inventreeStorageLocation";



@Component({
  selector: 'app-inventree-parameter-selector',
  templateUrl: './inventree-parameter-selector.component.html',
  styleUrls: ['./inventree-parameter-selector.component.less']
})
export class InventreeParameterSelectorComponent implements OnInit {

    partCategories: any[] = [];
    storageLocations: any[] = [];

    selectedStorageLocation: any;
    selectedPartCategory: any;

    constructor(private inventree: InventreeQuickAddService) {
        // Load previous category from localstorage
        const localStoragePartCategory = window.localStorage.getItem(localStoragePartCategoryKey);
        if(!!localStoragePartCategory) {
            const newPartCategory = Number(localStoragePartCategory);
            if(!isNaN(newPartCategory)) {
                this.selectedPartCategory = newPartCategory
            }
        }
        const localStorageStorageLocation = window.localStorage.getItem(localStorageStorageLocationKey);
        if(!!localStorageStorageLocation) {
            const newStorageLocation = Number(localStorageStorageLocation);
            if(!isNaN(newStorageLocation)) {
                this.selectedStorageLocation = newStorageLocation;
            }
        }
    }

    partCategoryChanged() {
        window.localStorage.setItem(localStoragePartCategoryKey, this.selectedPartCategory);
    }

    storageLocationChanged() {
        window.localStorage.setItem(localStorageStorageLocationKey, this.selectedStorageLocation);
    }

    ngOnInit(): void {
      this.inventree.partCategories().subscribe(partCategories => {
        console.info("Part categories", partCategories);
        this.partCategories = partCategories;
    })
    this.inventree.storageLocations().subscribe(storageLocations => {
          console.info("Storage locations", storageLocations);
        this.storageLocations = storageLocations;
      })
    }
}
