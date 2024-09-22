# Instrucciones generales

### Ejecución inicial:

1. Crear migraciones:
    ```bash
    python manage.py makemigrations
    ```

2. Correr migraciones:
    ```bash
    python manage.py migrate
    ```
3. Correr el script inicial para generar datos de prueba y super admin:
    ```bash
    python manage.py generar_datos_prueba
    ```

5. Ejecutar el proyecto:
    ```bash
    python manage.py runserver
    ```

6. Abrir backoffice(opcional):
    ```bash
    /admin
    ```

---

### Pasos para levantar después de algún cambio en algún modelo:

1. Crear migraciones:
    ```bash
    python manage.py makemigrations
    ```

2. Correr migraciones:
    ```bash
    python manage.py migrate
    ```

3. Ejecutar el proyecto:
    ```bash
    python manage.py runserver
    ```

### Resetear base de datos:
1. Borrar las migraciones (SALVO __ INIT __.py)
2. Borrar el archivo db.sqlite3
3. Remover la DB del gestor que se esté utilizando
4. Correr las migraciones y el script nuevamente:
```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py generar_datos_prueba
    python manage.py runserver
```

### Usuarios para pruebas:

##### Superadmin
User: *admin*
Pass: *admin*

##### Recepcionista
User: *recepcion*
Pass: *recepcion*

##### Médicos
User: *medico0.kinesiologia*
Pass: *medico*

User: *medico0.salud_mental*
Pass: *medico*

User: *medico0.clinica*
Pass: *medico*


### Consideraciones:
- Cuando se crea un médico se le crean automaticamente los turnos para los siguientes 30 días en el espacio de 8 a 17hrs. 
- Cuando se crea un médico se le crea un user con la pass "medico" y el user nombre.apellido