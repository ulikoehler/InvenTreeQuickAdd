import { Component, OnInit } from '@angular/core';
import { InventreeQuickAddService } from '../inventree-quick-add.service';

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
    }

    partCategoryChanged() {

    }

    storageLocationChanged() {

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
