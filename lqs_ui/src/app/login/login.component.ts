import { Component, Input } from '@angular/core';
import { AuthServiceService } from '../api_services/auth-service.service';
import { ToastHandlerService } from '../toastHandle/toast-handler.service';


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
  constructor(private authService: AuthServiceService, private ToastHandlerService: ToastHandlerService) {}

  LoginProsses() {
    if (this.email == undefined || this.email == ''){
      this.ToastHandlerService.showToast("error", "Error", "Email is requied");
      return;
    } 
    if (this.password == undefined || this.password == ''){
      this.ToastHandlerService.showToast("error", "Error", "Password is required");
      return;
    }
    this.authService.login({email: this.email, password: this.password}).subscribe((data: any) => {
      this.data = data;
      if (this.data.error){
        this.ToastHandlerService.handleToast(this.data);
      }
      if (this.data.status) {
        this.ToastHandlerService.handleToast(this.data);
        setTimeout(() => {
          if (this.data.role == 'STUDENT') {
            if (localStorage.getItem('user_id')) {
              localStorage.getItem('user_id');
            }
            localStorage.setItem('user_id', data.user_id);
            window.location.href = '/student_dash';
          } else if (this.data.role == 'INSTRUCTOR') {
            if (localStorage.getItem('user_id')) {
              localStorage.getItem('user_id');
            }
            localStorage.setItem('user_id', data.user_id);
            window.location.href = '/instructor_dash';
          } else if (this.data.role == 'TA') {
            if (localStorage.getItem('user_id')) {
              localStorage.getItem('user_id');
            }
            localStorage.setItem('user_id', data.user_id);
            window.location.href = '/ta_dash';
          }
        }, 2000); // The delay is in milliseconds, so 2000ms equals 2 seconds
      }
    }
  );
  }



  Register(){
    window.location.href = '/register';
  }
}
