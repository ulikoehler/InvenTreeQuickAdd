import { Component } from '@angular/core';

@Component({
  selector: 'app-inventree-part-number-input',
  templateUrl: './inventree-part-number-input.component.html',
  styleUrls: ['./inventree-part-number-input.component.less']
})
export class InventreePartNumberInputComponent {
    public partNumber: string = '';
}
