const userForm = document.querySelector('#userForm')

let questions = []

/* This code is adding an event listener to the `window` object that listens for the `DOMContentLoaded`
event, which is fired when the initial HTML document has been completely loaded and parsed. When
this event is triggered, the code sends a GET request to the `/api/questions` endpoint to retrieve a
list of questions from the server. Once the response is received, the data is extracted from the
response using the `json()` method, and the resulting array of questions is stored in the
`questions` variable. Finally, the `renderQuestion()` function is called with the `questions` array
as an argument to display the list of questions on the web page. */
window.addEventListener('DOMContentLoaded', async ()=>{
    const response = await fetch('/api/questions');
    const data = await response.json()
    questions = data
    renderQuestion(questions)
});

/* This code is adding an event listener to the `userForm` element that listens for the `submit` event.
When the form is submitted, the function is triggered and it prevents the default form submission
behavior using `e.preventDefault()`. It then retrieves the values of the `question` and `model`
input fields from the form, and sends a POST request to the `/api/questions` endpoint with the
question and model data in the request body. Once the response is received, the data is extracted
from the response using the `json()` method, and the resulting question object is added to the
beginning of the `questions` array using the `unshift()` method. Finally, the `renderQuestion()`
function is called with the updated `questions` array as an argument to display the new question on
the web page, and the form is reset using `userForm.reset()`. */
userForm.addEventListener('submit', async e => {
    e.preventDefault()

    const question = userForm['question'].value
    const model = userForm['model'].value

    const response = await fetch('/api/questions',{
        method : 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
            question,
            model
        })
    })
    const data = await response.json()

    questions.unshift(data)

    renderQuestion(questions)

    userForm.reset();
})



/**
 * The function renders a list of questions with a delete button for each question and handles the
 * deletion of a question when the delete button is clicked.
 * @param questions - an array of objects representing questions, where each object has the properties
 * "id", "question", and "answer".
 */
function renderQuestion(questions){
    const questionList = document.querySelector('#questionList');
    questionList.innerHTML = '';

    questions.forEach((question) => {
        const questionItem = document.createElement('li')
        questionItem.classList = 'list-group-item list-group-item-dark my-2';

        questionItem.innerHTML = `
        <header class= "d-flex justify-content-between aling-items-center">
            <h3>${'pregunta: ' + question.question}</h3>
            <div> 
                <buttom data-id="${question.id}" class= 'bnt-delete btn btn-danger btn-sm'>delete</button>
            </div>
        </header>
        <p>${question.answer}</p>
        `;

        // Handle delete button
        const btnDelete = questionItem.querySelector('.bnt-delete');

        btnDelete.addEventListener('click', async ()=>{
            const response = await fetch(`/api/questions/${question.id}`, {
                method: 'DELETE',
            });

            const data = await response.json();

            questions = questions.filter((question) => question.id !== data.id);

            renderQuestion(questions);

        });

        questionList.appendChild(questionItem);

    });
}        
