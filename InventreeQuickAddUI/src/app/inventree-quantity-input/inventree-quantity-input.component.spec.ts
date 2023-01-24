import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InventreeQuantityInputComponent } from './inventree-quantity-input.component';

describe('InventreeQuantityInputComponent', () => {
  let component: InventreeQuantityInputComponent;
  let fixture: ComponentFixture<InventreeQuantityInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InventreeQuantityInputComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InventreeQuantityInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
