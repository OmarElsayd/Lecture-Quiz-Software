import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RegisterComponent } from './register/register.component';

import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './login/login.component';
import { StudentsComponent } from './students/students.component';
import { InstructorComponent } from './instructor/instructor.component';
import { CreateQuizComponent } from './instructor/create-quiz/create-quiz.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {CalendarModule} from 'primeng/calendar';
import { StartQuizComponent } from './instructor/create-quiz/start-quiz/start-quiz.component';
import { MatRadioModule } from '@angular/material/radio';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { OrderByPipe } from './order-by.pipe';
import { ViewStudentsComponent } from './instructor/view-students/view-students.component';
import { CreateClassComponent } from './instructor/create-class/create-class.component';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { ViewQuizComponent } from './instructor/view-quiz/view-quiz.component';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    StudentsComponent,
    InstructorComponent,
    CreateQuizComponent,
    StartQuizComponent,
    OrderByPipe,
    ViewStudentsComponent,
    CreateClassComponent,
    ViewQuizComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    DragDropModule,
    CalendarModule,
    MatRadioModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FormsModule,
    MatTableModule,
    MatSortModule,
    ToastModule,
  ],
  exports: [],
  providers: [
    MessageService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
