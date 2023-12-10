import { TestBed } from '@angular/core/testing';

import { ToastHandlerService } from './toast-handler.service';

describe('ToastHandlerService', () => {
  let service: ToastHandlerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ToastHandlerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
