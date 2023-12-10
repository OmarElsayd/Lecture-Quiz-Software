import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import { ToastHandlerService } from 'src/app/toastHandle/toast-handler.service';
import { AuthServiceService } from '../../api_services/auth-service.service'


@Component({
  selector: 'app-get-start-quiz',
  templateUrl: './get-start-quiz.component.html',
  styleUrls: ['./get-start-quiz.component.scss']
})
export class GetStartQuizComponent {
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';

  constructor (private AuthServiceService: AuthServiceService, private ToastMessage: ToastHandlerService){

  }

  onSubmitQuizCode(form: NgForm) {
    if (form.valid) {
      if (localStorage.getItem('quiz_code')){
        localStorage.removeItem('quiz_code');
      }
      localStorage.setItem('quiz_code', form.value.quizCode);

      this.AuthServiceService.get_quiz_id(form.value.quizCode).subscribe((data)=> {
        try{
          if (data){
            if (localStorage.getItem("quiz_id")){
              localStorage.removeItem('quiz_id');
            }
            localStorage.setItem('quiz_id', data.id);
            this.ToastMessage.showToast("success", "Getting Quiz!", "Getting your quiz ready for your!");
            setTimeout(()=>{
              window.location.href = '/start_quiz';
            }, 2000)
          }
        }catch (error){
          this.ToastMessage.showToast("warning", "Not Found!", "Quiz was not found or Quiz code is invalid");
      }
      })
      


    }
  }
}
