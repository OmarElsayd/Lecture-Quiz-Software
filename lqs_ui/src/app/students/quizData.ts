export interface QuizData {
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