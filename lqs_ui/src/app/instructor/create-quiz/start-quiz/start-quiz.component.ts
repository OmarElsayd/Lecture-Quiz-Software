import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';
import { AuthServiceService } from 'src/app/api_services/auth-service.service';
import { ToastConfig } from 'src/app/toastHandle/toast-config';
import { ToastHandlerService } from '../../../toastHandle/toast-handler.service'

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
  audioSrc: string | ArrayBuffer | null = null;

  @ViewChild('audioPlayer') audioPlayer!: ElementRef;

  constructor(private quizService: AuthServiceService, private ToastHandlerService: ToastHandlerService) { }

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
    this.ToastHandlerService.showToast(ToastConfig.S200.severity, ToastConfig.S200.summary, "Starting Quiz");
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.audioSrc = reader.result;
          setTimeout(() => {
            this.audioPlayer.nativeElement.load();
          }, 0);
        };
        reader.readAsDataURL(file);
      }
    }
  }

}
