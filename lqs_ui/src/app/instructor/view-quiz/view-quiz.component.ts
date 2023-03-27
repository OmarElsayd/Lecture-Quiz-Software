import { Component } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { AuthServiceService } from 'src/app/api_services/auth-service.service';
import { ToastConfig } from 'src/app/toastHandle/toast-config';
import { ToastHandlerService } from '../../toastHandle/toast-handler.service'

interface Quiz {
  quiz_id: number;
  quiz_name: string;
  number_of_questions: number;
  quiz_duration: number;
  lecture_id: number;
  created_date: string;
}

@Component({
  selector: 'app-view-quiz',
  templateUrl: './view-quiz.component.html',
  styleUrls: ['./view-quiz.component.scss']
})
export class ViewQuizComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  displayedColumns: string[] = ['quiz_id', 'quiz_name', 'number_of_questions', 'quiz_duration', 'lecture_id', 'created_date', 'actions'];
  dataSource!: MatTableDataSource<Quiz>;
  isQuizData: boolean = false;

  quizzes: Quiz[] = [
    // Your quiz data here
  ];

  constructor (private lqsService: AuthServiceService, private ToastHandlerService: ToastHandlerService) {}

  ngOnInit() {
    this.lqsService.getAllQuizzes().subscribe((data) => {
      if (data){
        this.isQuizData = true;
        this.quizzes = data;
        console.log(this.quizzes);
        this.dataSource = new MatTableDataSource(this.quizzes); // Move this line here
      }
    });
  }

  downloadQuiz(quiz: Quiz) {
    if (quiz.quiz_id) {
      this.lqsService.downloadQuizReport(quiz.quiz_id).subscribe(
        (data) => {
          const blob = new Blob([data], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `quiz-report-${quiz.quiz_id}-${quiz.quiz_name}-${quiz.created_date}.csv`;
          link.click();
          window.URL.revokeObjectURL(url);
          this.ToastHandlerService.showToast(ToastConfig.S200.severity, ToastConfig.S200.summary, "Downloading!");
        },
        (error) => {
          console.error('Failed to download quiz report', error);
        }
      );
    }
  }
  

  deleteQuiz(quiz: Quiz) {
    // Delete quiz implementation
  }

  editQuiz(quiz: Quiz) {
    // Edit quiz implementation
  }
}

