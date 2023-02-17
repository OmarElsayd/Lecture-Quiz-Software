import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InstructorComponent } from './instructor/instructor.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { StudentsComponent } from './students/students.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'student_dash', component: StudentsComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'instructor_dash', component: InstructorComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
