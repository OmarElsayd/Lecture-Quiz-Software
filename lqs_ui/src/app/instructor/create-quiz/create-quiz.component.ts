import { Component, OnInit } from '@angular/core';
import { CdkDrag, CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { AuthServiceService } from 'src/app/api_services/auth-service.service';
import { delay } from 'rxjs';



interface Choice {
  text: string;
  isCorrect: boolean;
}

interface Question {
  type: string;
  question: string;
  choices?: Choice[];
  answer?: string;
  answerBoolean?: boolean;
}

interface QuizData {
  quiz_header: {
    number_of_questions: number;
    quiz_duration: number;
    class_code: string;
    lecture_name: string;
    lecture_date: string;
  },
  questions: {
    index: number;
    question_type: string;
    question: string;
    correct_answer: string;
    option1?: string;
    option2?: string;
    option3?: string;
    option4?: string;
  }[];
}

@Component({
  selector: 'app-create-quiz',
  templateUrl: './create-quiz.component.html',
  styleUrls: ['./create-quiz.component.scss']
})
export class CreateQuizComponent implements OnInit{
  title = 'lqs_ui';
  date = new Date().toLocaleDateString();
  time = new Date().toLocaleTimeString();
  version = '1.0.0';
  current_question: any;
  done: Question[] = [];
  quizDuration!: number;
  lectureName!: string;
  lectureDate = new Date().toLocaleDateString();
  courseNames!: string[];
  selectedCourse!: string;
  quiz: any;


  

  newQuestion: Question = {
    type: '',
    question: '',
    answer: '',
    answerBoolean: false, 
    choices: []
  };

  newChoice: Choice = {
    text: '',
    isCorrect: false
  };
  

  constructor(private authService: AuthServiceService) {}

  ngOnInit() {
    this.authService.getCourses().subscribe((data: string[]) => {
      this.courseNames = data;
    });
  }

  onAnswerBooleanChange() {
    console.log(this.newQuestion); // log the updated object
  }

  questionTypes = ['Multiple Choice', 'True or False', 'Short Answer'];

  addQuestion() {
    const question: Question = { ...this.newQuestion };
    this.done.push(question);
    this.newQuestion.question = '';
    this.newQuestion.type = '';
    this.newQuestion.answerBoolean = false;
    this.newQuestion.answer;
    this.newQuestion.choices = [];
  }

  addChoice() {
    if (this.newQuestion) {
      this.newQuestion.choices = this.newQuestion.choices || [];
      this.newQuestion.choices.push({ ...this.newChoice });
      this.newChoice.text = '';
      this.newChoice.isCorrect = false;
    }
  }

  removeChoice(index: number) {
    if (this.newQuestion) {
      this.newQuestion.choices?.splice(index, 1);
    }
  }

  removeQuestion(question: Question) {
    const index = this.done.indexOf(question);
    if (index >= 0) {
      this.done.splice(index, 1);
    }
  }

  drop(event: CdkDragDrop<Question[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex);
    }
  }
  
  admin_console() {
    window.location.href = '/admin_console';
  }

  submitQuiz(){
    console.log(this.done);
    if (this.done.length < 1) {
      alert('Please add at least one question');
      return;
    }
    const questions = this.done.map(q => {
      let question: any = {
        question_type: q.type
      }
      if (q.type === 'Multiple Choice') {
        question.correct_answer = q.choices?.find(c => c.isCorrect)?.text;
        if (q.choices) {
          question.option1 = q.choices[0]?.text;
          question.option2 = q.choices[1]?.text;
          question.option3 = q.choices[2]?.text;
          question.option4 = q.choices[3]?.text;
        }
      } else if (q.type === 'True or False') {
        question.correct_answer = q.answerBoolean ? 'True' : 'False';
      } else if (q.type === 'Short Answer') {
        question.correct_answer = q.answer;
      }
      question.question = q.question;
      return question;
    });
  
    const quizData: QuizData = {
      quiz_header: {
        number_of_questions: questions.length,
        quiz_duration: this.quizDuration,
        class_code: this.selectedCourse,
        lecture_name: this.lectureName,
        lecture_date: this.lectureDate,
      },
      questions
    };

    this.authService.create_quiz(quizData).subscribe(
      (data) => {       
        if (localStorage.getItem("quiz_code")) {
          localStorage.removeItem("quiz_code");
        }
        if (localStorage.getItem("quiz_id")) {
          localStorage.removeItem("quiz_id");
        }
        localStorage.setItem("quiz_code", data.quiz_code);
        localStorage.setItem("quiz_id", data.quiz_id);
  
        // Move the if statement inside the subscribe block
        if (data.status === true) {
          window.location.href = '/start_quiz';
        } else {
          alert("Something went wrong. Please try again.");
        }
      },
      (error) => {
        console.error(error);
        alert("Something went wrong. Please try again.");
      }
    );
  }

}  