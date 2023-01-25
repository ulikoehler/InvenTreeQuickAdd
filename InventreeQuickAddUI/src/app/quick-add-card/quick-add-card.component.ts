import { Component, ViewChild } from '@angular/core';
import { AddPartParameters } from '../add-part-parameters';
import { InventreeParameterSelectorComponent } from '../inventree-parameter-selector/inventree-parameter-selector.component';
import { InventreePartNumberInputComponent } from '../inventree-part-number-input/inventree-part-number-input.component';
import { InventreeQuantityInputComponent } from '../inventree-quantity-input/inventree-quantity-input.component';
import { InventreeQuickAddService } from '../inventree-quick-add.service';

@Component({
  selector: 'app-quick-add-card',
  templateUrl: './quick-add-card.component.html',
  styleUrls: ['./quick-add-card.component.less']
})
export class QuickAddCardComponent {
    @ViewChild(InventreeParameterSelectorComponent)
    private parameterSelector = {} as InventreeParameterSelectorComponent;

    @ViewChild(InventreePartNumberInputComponent)
    private partNumberInput = {} as InventreePartNumberInputComponent;

    @ViewChild(InventreeQuantityInputComponent)
    private quantityInput = {} as InventreeQuantityInputComponent;

    constructor(private inventree: InventreeQuickAddService) {
    }

    save() { // Save button clicked
        console.log('Saved!');
        const part: AddPartParameters = {
            partNumber: this.partNumberInput.partNumber,
            quantity: this.quantityInput.quantity,
            location: this.parameterSelector.selectedStorageLocation,
            category: this.parameterSelector.selectedPartCategory,
            metadata: {
                // TODO
            }
        };
        this.inventree.addPart(part).subscribe((data) => {
            console.log("Add part response", data);
        });
    }
}
