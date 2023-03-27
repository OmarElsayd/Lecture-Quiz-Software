import { Component } from '@angular/core';
import { AuthServiceService } from '../api_services/auth-service.service';
import { ToastHandlerService } from '../toastHandle/toast-handler.service'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';

  name!: string;
  email!: string;
  confirm_email!: string;
  password!: string;
  confirm_password!: string;
  class_code!: string;

  data: any;
  constructor(private authService: AuthServiceService, private ToastHandlerService:ToastHandlerService) {}

  RegisterProsses() {
    if (this.name == undefined || this.name == ''){
      alert('Name is required');
      return;
    }
    if (this.email == undefined || this.email == ''){
      alert('Email is required');
      return;
    }
    if (this.confirm_email == undefined || this.confirm_email == ''){
      alert('Confirm Email is required');
      return;
    }

    if (this.password == undefined || this.password == ''){
      alert('Password is required');
      return;
    }

    if (this.password != this.confirm_password){
      alert('Passwords do not match');
      return;
    }

    if (this.class_code == undefined || this.class_code == ''){
      alert('Class Code is required');
      return;
    }
    if (this.email != this.confirm_email){
      alert('Emails do not match');
      return;
    }
    if (this.password != this.confirm_password){
      alert('Passwords do not match');
      return;
    }
    this.authService.register({name: this.name, email: this.email, password: this.password, course_code: this.class_code}).subscribe((data: any) => {
      this.data = data;
      if (this.data.error){
        alert(this.data.error);
      }
      if (this.data.status){
        this.ToastHandlerService.handleToast(this.data);
        window.location.href = '';
      }
    });
  }
}
