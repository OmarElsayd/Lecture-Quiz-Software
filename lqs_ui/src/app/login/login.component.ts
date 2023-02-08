import { Component, Input } from '@angular/core';
import { AuthServiceService } from '../api_services/auth-service.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  email!: string;
  password!: string;

  data: any;
  constructor(private authService: AuthServiceService) {}

  LoginProsses() {
    if (this.email == undefined || this.email == ''){
      alert('Email is required');
      return;
    } 
    if (this.password == undefined || this.password == ''){
      alert('Password is required');
      return;
    }
    this.authService.login({email: this.email, password: this.password}).subscribe((data: any) => {
      this.data = data;
      if (this.data.error){
        alert(this.data.error);
      }
      if (this.data.status){
        alert(this.data.message);
        if (this.data.role == 'STUDENT'){
          window.location.href = '/student_dash';
        }
        else if (this.data.role == 'INSTRUCTOR'){
          window.location.href = '/instructor_dash';
        }
        else if (this.data.role == 'TA'){
          window.location.href = '/ta_dash';
        }
      }
    }
  );
  }



  Register(){
    window.location.href = '/register';
  }
}
