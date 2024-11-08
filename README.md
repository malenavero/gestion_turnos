# Instrucciones generales



### Crear nuevo ambiente
```bash
python -m venv <nombre-env>
```

### Activar el ambiente
```bash
source env/bin/activate (linux)
.\env\Scripts\activate (win)
```

### Desactivar el ambiente
```bash
deactivate
```

### Correr requirements.txt
```bash
pip install -r requirements.txt
```

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
Puede ejecutarse el siguiente comando:
```bash
    python reset_db.py
```
El script se encarga de ejecutar los siguientes pasos:
1. Borrar las migraciones (SALVO __ INIT __.py)
2. Borrar el archivo db.sqlite3
3. Correr las migraciones y el script nuevamente:
```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py generar_datos_prueba
```
*¡Importante!* No olvidar actualizar la DB en el gestor que se esté utilizando


### Usuarios para pruebas:

##### Superadmin
User: *admin.admin*
Pass: *admin*

##### Jefe Recepción
User: *miriam.bianchi*
Pass: *jefe-recepcion*

##### Recepcionista
User: *roberto.smith*
Pass: *recepcion*

##### Médico
User: *ricardo.espinosa*
Pass: *medico*


### Consideraciones:
- Cuando se crea un médico se le crean automaticamente los turnos para los siguientes 30 días en el espacio de 8 a 17hrs. 
- Cuando se crea un médico se le crea un user con la pass "medico" y el user nombre.apellido