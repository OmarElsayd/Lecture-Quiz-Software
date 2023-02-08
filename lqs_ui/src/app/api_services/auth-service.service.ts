import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable, throwError } from 'rxjs';
import { baseUrl } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthServiceService {
  constructor(private http: HttpClient) { }

  login(data: any):Observable<any>{
    return this.http.post(`${baseUrl}/login`, data)
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
