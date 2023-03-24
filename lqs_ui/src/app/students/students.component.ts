import { Component, OnInit } from '@angular/core';
import { QuizData } from './quizData';
import { StudentServicesService } from './student-services.service';
import { AuthServiceService } from '../api_services/auth-service.service';
import { Subscription, timer } from 'rxjs';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.scss']
})
export class StudentsComponent implements OnInit{
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  quizCode! : string;
  quizData!: QuizData;
  errorMessage: string | null = null;
  answers: { [index: number]: string } = {};
  quizStarted: boolean = false;
  isHideQuizCodePart: boolean = false;
  startQuizTime!: Date;
  remainingTime!: number;
  timerSubscription!: Subscription;


  constructor(private studentService: StudentServicesService, private quizService: AuthServiceService) { }

  join_quiz(){
    console.log(this.quizCode);
  }

  ngOnInit() {
    console.log('Student component loaded');
    this.quizService.quizWebSocket.subscribe(
      (message) => {
        console.log(message);
        if (message.event === 'start_quiz') {
          console.log('Quiz started');
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
        if (data){
          this.isHideQuizCodePart = true;
          this.quizService.addStudentToLobby();
          this.quizService.lobbyWebSocket.subscribe();
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
    // Submit the quiz
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
