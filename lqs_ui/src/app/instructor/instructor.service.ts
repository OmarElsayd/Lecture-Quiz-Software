import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';
import { baseUrl } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class InstructorService {

  constructor(private http: HttpClient) { }

  get_all_students():Observable<any>{
    return this.http.get(`${baseUrl}/instructor/getAllStudents`)
    .pipe(
      map(data => data),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    alert(error.error.detail);
    return throwError(
      'Something bad happened; please try again later.');
  };
}
