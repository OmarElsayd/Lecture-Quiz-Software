import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateClassComponent } from './instructor/create-class/create-class.component';
import { CreateQuizComponent } from './instructor/create-quiz/create-quiz.component';
import { StartQuizComponent } from './instructor/create-quiz/start-quiz/start-quiz.component';
import { InstructorComponent } from './instructor/instructor.component';
import { ViewQuizComponent } from './instructor/view-quiz/view-quiz.component';
import { ViewStudentsComponent } from './instructor/view-students/view-students.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { StudentsComponent } from './students/students.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'student_dash', component: StudentsComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'instructor_dash', component: InstructorComponent },
  { path: 'create_quiz', component: CreateQuizComponent },
  { path: 'start_quiz', component: StartQuizComponent},
  { path: 'view_students', component: ViewStudentsComponent},
  { path: 'create_class', component: CreateClassComponent},
  { path: 'view_quizzies', component: ViewQuizComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
