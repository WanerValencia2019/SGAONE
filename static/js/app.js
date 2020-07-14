const search = document.getElementById('search')
const course = document.getElementById('course')
const assignment = document.getElementById('assignment')

//EVENTOS
search.addEventListener('click', (e) => {
    const co = course.value

    const as = assignment.value
    console.log(as)

    //console.log(co, as)
    //console.log("ENVIANDO PETICIÓN")
    getData(co, as)
})

course.addEventListener('change', (e) => {
    const { value } = course
    //console.log(value)
    getAssignments(value)
})

//PETICIONES
const getAssignments = async(course) => {
    const url = `/sga/teacher/gradedAssigment/assignment/?course=${course}`
    const response = await fetch(url, {
        method: 'get',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    const data = await response.json()
    console.log(data)
    renderAssignments(data)
}


document.addEventListener('load', getAssignments(course.value))

const getData = async(course, assignment) => {
    const url = `/sga/teacher/gradedAssigment/?course=${course}&assignment=${assignment}`
    const response = await fetch(url, {
        method: 'get',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    const data = await response.json()

    renderData(data)
}

const renderAssignments = (data) => {
    data.length == 0 ? assignment.innerHTML = `<option value="">No hay exámenes para este curso</option>` : assignment.innerHTML = ""


    for (const a of data) {
        console.log(a.fields.title)
        assignment.innerHTML += `<option value="${a.fields.title}">${a.fields.title}</option>`
    }
}

const renderData = (data) => {
    const body = document.getElementById('body-qualification')
    console.log(data)
    data.length == 0 ? body.innerHTML = `<span class="text-info">No hay calificaciones para este curso</span>` : body.innerHTML = ""
    for (const qualification of data) {
        body.innerHTML += `
            <tr>
            <td>${qualification.id}</td>
            <td>${qualification.first_name}</td>
            <td>${qualification.last_name}</td>
            <td>${qualification.course}</td>
            <td>${qualification.assignment}</td>
            <td>${qualification.graded}</td>
            </tr>
        `
    }
}