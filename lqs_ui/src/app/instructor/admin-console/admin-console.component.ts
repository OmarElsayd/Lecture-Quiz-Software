import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { baseUrl } from 'src/environments/environment';
import { ToastHandlerService } from 'src/app/toastHandle/toast-handler.service';

@Component({
  selector: 'app-admin-console',
  templateUrl: './admin-console.component.html',
  styleUrls: ['./admin-console.component.scss']
})
export class AdminConsoleComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';

  isStudentForm = false;
  isTAForm = false;
  studentForm: FormGroup;
  taForm: FormGroup;

  constructor(private fb: FormBuilder, private http: HttpClient, private toastMessage: ToastHandlerService) { 
    this.studentForm = this.fb.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
    this.taForm = this.fb.group({
      name: ['', [Validators.required]],      
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onStudentSubmit() {
    if (this.studentForm.valid) {
      this.http.put(`${baseUrl}/instructor/add_new_user`, {
        name: this.studentForm.get('name')?.value,
        email: this.studentForm.get('email')?.value,
        password: this.studentForm.get('password')?.value,
        role: 'STUDENT'
      }).subscribe(
        (response) => {
          this.toastMessage.handleToast(response);
        },
        (error) => {
          this.toastMessage.handleToast(error);
        }
      );
    }
  }
  
  
  onTaSubmit() {
    if (this.taForm.valid) {
      this.http.put(`${baseUrl}/instructor/add_new_use`, {
        name: this.taForm.get('name')?.value,
        email: this.taForm.get('email')?.value,
        password: this.taForm.get('password')?.value,
        role: 'TA'
      }).subscribe(
        (response) => {
          this.toastMessage.handleToast(response);
        },
        (error) => {
          this.toastMessage.handleToast(error);
        }
      );
    }
  }
}

  
