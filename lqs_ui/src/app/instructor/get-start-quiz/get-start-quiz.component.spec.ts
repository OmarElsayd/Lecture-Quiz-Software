import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetStartQuizComponent } from './get-start-quiz.component';

describe('GetStartQuizComponent', () => {
  let component: GetStartQuizComponent;
  let fixture: ComponentFixture<GetStartQuizComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GetStartQuizComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GetStartQuizComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
