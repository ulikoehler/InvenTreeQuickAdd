import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { BarcodeScannerComponent } from './barcode-scanner/barcode-scanner.component';

import {SelectButtonModule} from 'primeng/selectbutton';
import {DropdownModule} from 'primeng/dropdown';
import { InventreeParameterSelectorComponent } from './inventree-parameter-selector/inventree-parameter-selector.component';
import { HttpClientModule } from '@angular/common/http';
import {CardModule} from 'primeng/card';
import { InventreePartNumberInputComponent } from './inventree-part-number-input/inventree-part-number-input.component';

import {InputTextModule} from 'primeng/inputtext';

@NgModule({
  declarations: [
    AppComponent,
    BarcodeScannerComponent,
    InventreeParameterSelectorComponent,
    InventreePartNumberInputComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    CardModule,
    InputTextModule,
    SelectButtonModule,
    DropdownModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
