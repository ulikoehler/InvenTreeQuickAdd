import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InventreePartNumberInputComponent } from './inventree-part-number-input.component';

describe('InventreePartNumberInputComponent', () => {
  let component: InventreePartNumberInputComponent;
  let fixture: ComponentFixture<InventreePartNumberInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InventreePartNumberInputComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InventreePartNumberInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
