const userForm = document.querySelector('#userForm')

let questions = []

/* Adding an event listener to the `window` object that listens for the `DOMContentLoaded`
event, which is fired when the initial HTML document has been completely loaded and parsed. When
this event is triggered, the code sends a GET request to the `/api/questions` endpoint using the
`fetch` API, and then waits for the response to be returned as JSON data. Once the data is received,
it is stored in the `questions` array and passed as an argument to the `renderQuestion` function,
which renders the data on the frontend. */

window.addEventListener('DOMContentLoaded', async ()=>{
    const response = await fetch('/api/questions');
    const data = await response.json()
    questions = data
    renderQuestion(questions)
});

/* Adding an event listener to the `userForm` element that listens for the `submit` event.
When the form is submitted, the function is executed, which prevents the default form submission
behavior using `e.preventDefault()`. It then retrieves the values of the `question` and `model`
input fields from the form, and sends a POST request to the `/api/questions` endpoint using the
`fetch` API. The request includes the `question` and `model` values in the request body as a JSON
string. Once the response is received, it is converted to JSON format using `response.json()`, and
the `userForm` is reset to its initial state. */

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
 * The function renders a list of questions with their corresponding models and answers on a web page.
 * @param questions - an array of objects representing questions, where each object has the following
 * properties:
 */
function renderQuestion(questions){
    const questionList = document.querySelector('#questionList')
    questionList.innerHTML = ''

    questions.forEach(element => {
        const questionItem = document.createElement('li')
        questionItem.classList = 'list-group-item list-group-item-dark my-2'
        //<button>edit</button>

        questionItem.innerHTML = `
        <header class= "d-flex justify-content-between aling-items-center">
            <h3>${'pregunta: ' + element.question}</h3>
            <div> 
                <buttom class= 'bnt-delete btn btn-danger btn-sm'>delete</button>
            </div>
        </header>
        <p>${element.answer}</p>
        `

        questionList.append(questionItem)
    });
}        
