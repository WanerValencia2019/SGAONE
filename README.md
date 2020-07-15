# SGAONE
Sistema de gestión y evaluación académica de escuelas

## Screenshot
1.  **Docente**
      - ![Inicio](/SGA-ONE%20DOCENTE/home.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/course.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/course11B.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/student.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/assignment.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/assignmentCreate.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/addQuestion.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/detailAssignment.PNG)
      - ![Inicio](/SGA-ONE%20DOCENTE/graded.PNG)

### Instalación

1. **Paso 1 - Creación del entorno virtual**
      - `python -m venv env`
      
2. **Paso 2 - Instalación de dependencias**
      - `pip install -r requirements.txt`
      
3. **Paso 3 - Migración inicial**
      - `python manage.py migrate`
      
4. **Paso - Migrar modelos**
      - `python manage.py makemigrations`
      - `python manage.py migrate`
      
