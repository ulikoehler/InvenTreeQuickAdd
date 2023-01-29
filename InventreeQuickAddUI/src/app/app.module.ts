import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BarcodeScannerComponent } from './barcode-scanner/barcode-scanner.component';

import { HttpClientModule } from '@angular/common/http';
import { CardModule } from 'primeng/card';
import { DropdownModule } from 'primeng/dropdown';
import { SelectButtonModule } from 'primeng/selectbutton';
import { InventreeParameterSelectorComponent } from './inventree-parameter-selector/inventree-parameter-selector.component';
import { InventreePartNumberInputComponent } from './inventree-part-number-input/inventree-part-number-input.component';

import { AutoFocusModule } from 'primeng/autofocus';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import {InputNumberModule} from 'primeng/inputnumber';
import {AutoCompleteModule} from 'primeng/autocomplete';

import { QuickAddCardComponent } from './quick-add-card/quick-add-card.component';

import { InventreeQuantityInputComponent } from './inventree-quantity-input/inventree-quantity-input.component';

@NgModule({
  declarations: [
    AppComponent,
    BarcodeScannerComponent,
    InventreeParameterSelectorComponent,
    InventreePartNumberInputComponent,
    QuickAddCardComponent,
    InventreeQuantityInputComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    CardModule,
    InputNumberModule,
    ButtonModule,
    AutoCompleteModule,
    AutoFocusModule,
    InputTextModule,
    SelectButtonModule,
    DropdownModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
