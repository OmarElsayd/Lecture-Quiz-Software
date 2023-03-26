import { Component } from '@angular/core';
import { InstructorService } from './instructor.service';


@Component({
  selector: 'app-instructor',
  templateUrl: './instructor.component.html',
  styleUrls: ['./instructor.component.scss']
})
export class InstructorComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';

  StudentsData: any;
  constructor() {}

  create_a_class(){
    window.location.href = '/create_class';
  }
  create_a_quiz(){
    window.location.href = '/create_quiz';
  }
  view_classes(){
    window.location.href = '/view_classes';
  }
  view_quizzes(){
    window.location.href = '/view_quizzies';
  }
  view_students(){
    window.location.href = '/view_students';  
  }
  admin_console(){
    window.location.href = '/admin_console';
  }
}


