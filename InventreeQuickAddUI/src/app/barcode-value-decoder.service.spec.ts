import { TestBed } from '@angular/core/testing';

import { BarcodeValueDecoderService } from './barcode-value-decoder.service';

describe('BarcodeValueDecoderService', () => {
  let service: BarcodeValueDecoderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BarcodeValueDecoderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
