# My Django Project

This is a sample Django project created to demonstrate how to set up and use Django.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Creating an App](#creating-an-app)
- [Database Migrations](#database-migrations)
- [Running the Development Server](#running-the-development-server)
- [Creating Super User](#Creating-Super-User)   

## Requirements

- Python 3.6 or higher
- Django

## Installation



1. **Create a virtual environment**:

    ```sh
    python -m venv myenv
    ```

2. **Activate the virtual environment**:

    ```sh
    myenv\Scripts\activate
    ```

3. **Install the required packages**:

    ```sh
    pip install django
    ```

## Running the Project

1. **Create Django Project**:   

    ```sh 
    django-admin startproject  startapp  
    ```



1. **Navigate to the project directory**:

    ```sh
    cd myproject
    ```

2. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

3. **Open your web browser** and go to `http://127.0.0.1:8000/` to see the project running.

## Creating an App

1. **Create a new app**:

    ```sh
    python manage.py startapp myapp
    ```

2. **Add your app to the project's settings**:

    Edit `myproject/settings.py` and add `'myapp'` to the `INSTALLED_APPS` list.

## Database Migrations

1. **Create migrations for your app's models**:

    ```sh
    python manage.py makemigrations myapp
    ```

2. **Apply the migrations**:

    ```sh
    python manage.py migrate
    ```

## Running the Development Server

1. **Ensure your virtual environment is activated**:

    ```sh
    myenv\Scripts\activate
    ```

2. **Run the server**:

    ```sh
    python manage.py runserver
    ```

3. **Open your web browser** and go to `http://127.0.0.1:8000/`.

## Deactivating the Virtual Environment

To deactivate the virtual environment, simply run:

```sh
deactivate

```

## Admin control access    


1.  **Creating Super-User** 
```sh 
python manage.py createsuperuser
```    
2. **Register the model in myapp/admin.py**   

```sh  
admin.site.register(ExampleModel)
``` 

3. **Access the admin interface using the below URL**   
```sh  
http://127.0.0.1:8000/admin/
```   


## Setup mysql docker container    


1. **Pull Latest Image**   

```sh 
docker pull mysql:latest
```  

2. **Create Docker container for mysql**   

```sh   
docker run -d --name mysql-container -p 3306:3306 -e MYSQL_ROOT_PASSWORD="root" mysql:latest
```   

3. **Get into CMD interface for mysql**   

```sh 
mysql  -p
```   






