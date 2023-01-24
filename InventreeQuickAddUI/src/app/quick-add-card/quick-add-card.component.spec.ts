import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuickAddCardComponent } from './quick-add-card.component';

describe('QuickAddCardComponent', () => {
  let component: QuickAddCardComponent;
  let fixture: ComponentFixture<QuickAddCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QuickAddCardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuickAddCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
