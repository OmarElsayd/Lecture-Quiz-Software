import { Component, OnInit } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';
import { AuthServiceService } from 'src/app/api_services/auth-service.service';

@Component({
  selector: 'app-start-quiz',
  templateUrl: './start-quiz.component.html',
  styleUrls: ['./start-quiz.component.scss']
})
export class StartQuizComponent implements OnInit {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  course_code! : string;
  // quizWebSocket!: WebSocketSubject<any>;
  studentInlobby: number = 0;

  constructor(private quizService: AuthServiceService) { }

  ngOnInit() {
    this.course_code = localStorage.getItem("quiz_code") as string;
    this.quizService.lobbyWebSocket.subscribe(
      (message) => {
        console.log(message);
        if (message.event === 'student_joined') {
          this.studentInlobby = this.studentInlobby + 1;
        }
      },
      (error) => console.error(error)
    );
  }

  start_quiz() {
    this.quizService.start_quiz();
    this.quizService.quizWebSocket.subscribe();
    console.log("start quiz");
  }

}
