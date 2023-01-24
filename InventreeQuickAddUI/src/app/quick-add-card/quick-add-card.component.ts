import { Component, ViewChild } from '@angular/core';
import { InventreeParameterSelectorComponent } from '../inventree-parameter-selector/inventree-parameter-selector.component';
import { InventreePartNumberInputComponent } from '../inventree-part-number-input/inventree-part-number-input.component';
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

    constructor(private inventree: InventreeQuickAddService) {
    }

    save() { // Save button clicked
        console.log('Saved!');
    }
}
