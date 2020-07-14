console.log("FUE CARGADO EL JS")
    //Cargando el modulo que permite poner un date time picker a los input con sus respectivo id


//Cargando las variables del form del modal

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const title = document.getElementById('title')
const save = document.getElementById('save-questions')
const answer = document.getElementById('answer')
const table = document.getElementById('table-assignment')
const countChoices = document.getElementById('count-choices')
const addQuestion = document.getElementById('add-question')
const containerChoices = document.getElementById('container-choices');
const dataQuestion = []
let assignment = []
const dataChoices = []
const dataAnswers = []

//obteniendo el assigment el cual fue seleccionado
table.addEventListener('click', (e) => {
    const { target } = e
    const name = target.getAttribute('name');
    console.log()
    if (name == "add") {
        const selectedID = target.parentElement.parentNode.firstElementChild.nextElementSibling;
        id = selectedID.getAttribute('name')
        assignment.push(id)
        console.log(assignment);
    }
})

//Evento para renderizar la cantidad de choices necesarias
countChoices.addEventListener('change', () => {
    renderChoices(countChoices.value)
})

//Agregar una nueva question
addQuestion.addEventListener('click', async() => {
    console.log('click')
    await getData();
    clearInputs();
})

//detectar el cambio del contenedor de los input de las opciones de respuesta
containerChoices.addEventListener('change', (e) => {

    answer.innerHTML += `
        <option value='${e.target.value}'>${e.target.value}</option>
    `
})

//creando la question y los items en nuestra bd
save.addEventListener('click', async() => {
    await getData()
        //console.log("Guardando datos");
        //console.log(assignment)
        //console.log(dataQuestion);
        //console.log(dataAnswers);
        //console.log(dataChoices);
        //await createChoices();
    await createAssignment();
    clearInputs();
})


//renderizando los input choices en el html
const renderChoices = (count) => {
    containerChoices.innerHTML = ""
    for (let w = 0; w < count; w++) {
        containerChoices.innerHTML += `
            <div class='form-group'>
            <input type="text" placeholder='item #${w+1}' name= '${w+1}' class='form-control'  />
            </div>
        `
    }
}

//obteniendo la data de los formularios
const getData = () => {

    const choices = document.querySelectorAll('#container-choices input')
    const answer_correct = answer.value
    const items = {}
    console.log(choices)
    choices.forEach((ch) => {
        items[ch.value] = ch.value.trimEnd()
    })
    dataQuestion.push(title.value)
    dataChoices.push(items)
    dataAnswers.push(answer_correct)

    console.log(dataAnswers)
}

//limpiando inputs para una nueva question
const clearInputs = () => {
    const choices = document.querySelectorAll('#container-choices input')
    choices.forEach((ch) => {
        ch.value = ""
    })
    answer.innerHTML = ""
    title.value = ""
        //assignment = []
}

document.addEventListener('load', renderChoices(countChoices.value))

const createAssignment = async() => {

    console.log(assignment);
    const url = '/sga/teacher/choices'
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            title: dataQuestion,
            choices: dataChoices,
            answers: dataAnswers,
            id: assignment[0]
        }),
    })
    const data = await res.json()
    console.log(data)
}