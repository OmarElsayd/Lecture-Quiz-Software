import { Component, OnInit, ViewChild } from '@angular/core';
import { InstructorService } from '../instructor.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { ToastHandlerService } from '../../toastHandle/toast-handler.service'
import { ToastConfig } from 'src/app/toastHandle/toast-config';

interface Student {
  email: string;
  name: string;
}

@Component({
  selector: 'app-view-students',
  templateUrl: './view-students.component.html',
  styleUrls: ['./view-students.component.scss']
})
export class ViewStudentsComponent implements OnInit {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  students: Student[] = [];
  displayedColumns: string[] = ['name', 'email', 'delete'];
  dataSource = new MatTableDataSource<any>();
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private Service: InstructorService, private ToastHandlerService: ToastHandlerService) {}

  ngOnInit(): void {
    this.getStudents();
  }

  getStudents(): void {
    this.Service.get_all_students().subscribe((data: any) => {
      this.students = data;
      this.dataSource.data = data;
      this.dataSource.sort = this.sort;
    });
    if (this.students){
      console.log(this.students);
    }
  }

  deleteStudent(student: any) {
    console.log(student);
    this.Service.deleteStudent(student).subscribe(
      () => {
        // Refresh the student list after deleting
        this.getStudents();
        this.ToastHandlerService.showToast(ToastConfig.S200.severity, ToastConfig.S200.summary, "Success");

      },
      (error) => {
        console.error(error);
      }
    );
  }

  
}