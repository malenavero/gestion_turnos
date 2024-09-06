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

3. Crear superusuario:
    ```bash
    python manage.py createsuperuser
    ```
    - **User**: admin
    - **Email**: Dejar en blanco
    - **Pass**: admin
    - Cuando te pregunte si querés usar una contraseña insegura, responde `sí`.

4. Correr el script inicial:
    ```bash
    python manage.py generar_datos_prueba
    ```

5. Ejecutar el proyecto:
    ```bash
    python manage.py runserver
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
