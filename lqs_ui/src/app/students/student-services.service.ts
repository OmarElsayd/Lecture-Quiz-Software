import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { baseUrl } from 'src/environments/environment';
import { catchError, Observable, throwError } from 'rxjs';
import { QuizData } from './quizData';

@Injectable({
  providedIn: 'root'
})
export class StudentServicesService {

  constructor(private http: HttpClient) { }

  private handleError(error: HttpErrorResponse) {
    alert(error.error.detail);
    return throwError(
      'Something bad happened; please try again later.');
  }
  
  getQuiz(quizCode: string): Observable<QuizData> {
    return this.http.get<QuizData>(`${baseUrl}/students/get_quiz?quiz_code=${quizCode}`).pipe(
      catchError((error) => this.handleError(error))
    );
  }
}
