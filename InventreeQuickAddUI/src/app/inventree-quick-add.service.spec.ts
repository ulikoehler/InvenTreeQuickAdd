import { TestBed } from '@angular/core/testing';

import { InventreeQuickAddService } from './inventree-quick-add.service';

describe('InventreeQuickAddService', () => {
  let service: InventreeQuickAddService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InventreeQuickAddService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
