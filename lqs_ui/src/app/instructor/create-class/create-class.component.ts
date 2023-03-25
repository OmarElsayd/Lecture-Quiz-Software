import { Component } from '@angular/core';
import { AuthServiceService } from 'src/app/api_services/auth-service.service';

@Component({
  selector: 'app-create-class',
  templateUrl: './create-class.component.html',
  styleUrls: ['./create-class.component.scss']
})
export class CreateClassComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  instructorId = localStorage.getItem("user_id") as string;
  courseCode : string = "";
  courseName : string = "";

  constructor(private apiServices: AuthServiceService) { }

  submitCreateClass() {
    this.apiServices.create_class({course_code: this.courseCode, class_name: this.courseName, instructor_id: this.instructorId}).subscribe(
      (data) => {
        console.log(data);
      },
      (error) => console.error(error)
    );
  }

}