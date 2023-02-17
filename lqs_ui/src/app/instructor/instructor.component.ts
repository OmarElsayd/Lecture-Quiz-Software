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
  constructor(private Service: InstructorService) {}

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
    window.location.href = '/view_quizzes';
  }
  view_students(){
    this.Service.get_all_students().subscribe((data: any) => {
      this.StudentsData = data;
      if (this.StudentsData.error){
        alert(this.StudentsData.error);
      }
  }
  );
    // window.location.href = '/view_students';
    if (this.StudentsData){
      console.log(this.StudentsData);
    }
  }
  admin_console(){
    window.location.href = '/admin_console';
  }
  view_reports(){ 
    window.location.href = '/view_reports';
  }
}


