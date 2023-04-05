import { Component, OnInit } from '@angular/core';
import { QuizData } from './quizData';
import { StudentServicesService } from './student-services.service';
import { AuthServiceService } from '../api_services/auth-service.service';
import { Subscription, timer } from 'rxjs';
import { ToastHandlerService } from '../toastHandle/toast-handler.service'
import { ToastConfig } from '../toastHandle/toast-config';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.scss']
})
export class StudentsComponent implements OnInit {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  quizCode!: string;
  quizData!: QuizData;
  errorMessage: string | null = null;
  answers: { [index: number]: { answer: string, correct_answer: string, question_id: number} } = {};
  quizStarted: boolean = false;
  isHideQuizCodePart: boolean = false;
  quizCompleted: boolean = false;
  quizDataInfo: boolean = false;
  startQuizTime!: Date;
  remainingTime!: number;
  timerSubscription!: Subscription;
  userInfo = {user_id: localStorage.getItem('user_id')}

  constructor(private studentService: StudentServicesService,
     private quizService: AuthServiceService,
     private ToastHandlerService:ToastHandlerService
     ) { }

  join_quiz() {
    console.log(this.quizCode);
  }

  ngOnInit() {
    console.log('Student component loaded');
    this.quizService.quizWebSocket.subscribe(
      (message) => {
        console.log(message);
        if (message.event === 'start_quiz') {
          this.ToastHandlerService.showToast(ToastConfig.S200.severity, ToastConfig.S200.summary, 'Quiz Started');
          this.quizStarted = true;
          this.startTimer(this.quizData.quiz_header.quiz_duration);
        }
      },
      (error) => console.error(error)
    );
  }
  

  get_quiz() {
    this.studentService.getQuiz(this.quizCode).subscribe(
      (data: QuizData) => {
        console.log(data);
        this.quizData = data;
        this.errorMessage = null;
        if (this.quizData.questions.length === 0) {
          this.errorMessage = 'No questions found';
        }
        if (data) {
          let quizId = localStorage.getItem('quiz_id');
          if (quizId){
            localStorage.removeItem('quiz_id');
          }
          localStorage.setItem('quiz_id', data.quiz_header.quiz_id);
          this.isHideQuizCodePart = true;
          this.quizService.addStudentToLobby();
          this.quizService.lobbyWebSocket.subscribe();
          this.quizDataInfo = true;
  
          // Initialize answers object for each question
          for (let question of this.quizData.questions) {
            this.answers[question.question_id] = {
              answer: '',
              correct_answer: question.correct_answer,
              question_id: question.question_id,
            };
          }
        }
      },
      (error) => {
        console.error(error);
        this.errorMessage = error;
      }
    );
  }

  submitQuiz(event: Event | null) {
    if (event) {
      event.preventDefault();
    }
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
    
    const answerList: any[] = Object.values(this.answers).map(answer => ({
      ...answer,
      quiz_id: localStorage.getItem('quiz_id'),
    }));
  
    console.log("Answer List:", answerList);
    this.quizService.submitQuiz(answerList, this.userInfo).subscribe(
      (data) => {
        this.ToastHandlerService.handleToast(data);
        this.quizCompleted = true;
        this.quizStarted = false;
        this.quizDataInfo = false;
      }
    );
  }

  getFormattedTime() {
    const minutes = Math.floor(this.remainingTime / 60);
    const seconds = this.remainingTime % 60;
    return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
  }

  startTimer(duration: number) {
    this.remainingTime = duration * 60; // Convert minutes to seconds
    const time = timer(1000, 1000);
    this.timerSubscription = time.subscribe(() => {
      this.remainingTime -= 1;
      if (this.remainingTime <= 0) {
        this.submitQuiz(null);
      }
    });
  }
}
