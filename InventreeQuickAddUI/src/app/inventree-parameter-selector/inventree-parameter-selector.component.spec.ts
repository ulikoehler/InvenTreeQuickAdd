import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InventreeParameterSelectorComponent } from './inventree-parameter-selector.component';

describe('InventreeParameterSelectorComponent', () => {
  let component: InventreeParameterSelectorComponent;
  let fixture: ComponentFixture<InventreeParameterSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InventreeParameterSelectorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InventreeParameterSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
