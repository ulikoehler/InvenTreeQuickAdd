import { Component } from '@angular/core';
import { AutocompleteResult } from '../autocomplete-result';
import { InventreeQuickAddService } from '../inventree-quick-add.service';

@Component({
  selector: 'app-inventree-part-number-input',
  templateUrl: './inventree-part-number-input.component.html',
  styleUrls: ['./inventree-part-number-input.component.less']
})
export class InventreePartNumberInputComponent {
    public partNumber: string = '';

    mpnSuggestions: AutocompleteResult[] = [];

    constructor(private inventree: InventreeQuickAddService) {
    }

    autocomplete(event: any) {
        console.log("Autocomplete", event);
        this.inventree.autocompleteMPN(event.query).subscribe(suggestions => {
            this.mpnSuggestions = suggestions;
            console.log("Autocomplete response", suggestions);
        });
    }
}
