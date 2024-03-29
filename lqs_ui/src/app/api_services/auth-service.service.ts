import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable, Subject, throwError } from 'rxjs';
import { WebSocketSubject } from 'rxjs/webSocket';
import { baseUrl, wsBaseUrl } from 'src/environments/environment';
import { ToastHandlerService } from '../toastHandle/toast-handler.service';

@Injectable({
  providedIn: 'root'
})
export class AuthServiceService {
  quizWebSocket!: WebSocketSubject<any>;
  lobbyWebSocket!: WebSocketSubject<any>;

  constructor(private http: HttpClient, private ToastService: ToastHandlerService) {
    this.connectToQuizWebSocket();
  }

  login(data: any):Observable<any>{
    return this.http.post(`${baseUrl}/login`, data)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }
  create_quiz(data: any):Observable<any>{
    return this.http.put(`${baseUrl}/instructor/create_quiz`, data)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }

  register(data: any):Observable<any>{
    return this.http.post(`${baseUrl}/register`, data)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }
  
  getCourses():Observable<any>{
    return this.http.get(`${baseUrl}/instructor/all_courses`)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }

  create_class(data: any){
    return this.http.post(`${baseUrl}/instructor/NewClass`, data)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }


  handleError(error: HttpErrorResponse) {
    return throwError(
      'Something bad happened; please try again later.');
  };

  
  connectToQuizWebSocket() {
    this.quizWebSocket = new WebSocketSubject(`ws://${wsBaseUrl}/instructor/start_quiz_ws`);
    this.lobbyWebSocket = new WebSocketSubject(`ws://${wsBaseUrl}/students/lobby_wait_ws`);
  }

  start_quiz() {
    this.quizWebSocket.next('start');
    console.log(this.quizWebSocket);
  }

  get_quiz_id(quiz_code: any): Observable<any>{
     return this.http.get(`${baseUrl}/instructor/get_quiz_id?quiz_code=${quiz_code}`).pipe(
       map(data=>data)
     );
  }

  addStudentToLobby() {
    this.lobbyWebSocket.next('add_one');
    console.log(this.lobbyWebSocket);
  }

  submitQuiz(quiz_answer_body: any, user_info: any):Observable<any> {
    let data = { quiz_answer_body, user_info };
    console.log(data);
    return this.http.put(`${baseUrl}/students/submit_quiz`, data)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }

  getAllQuizzes():Observable<any>{
    return this.http.get(`${baseUrl}/instructor/all_quizes`)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    )
  }

  downloadQuizReport(quiz_id: any): Observable<Blob> {
    return this.http.get(`${baseUrl}/instructor/download_quiz/${quiz_id}`, { responseType: 'blob' }).pipe(
      catchError(this.handleError)
    );
  }
  

}
