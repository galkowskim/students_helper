# Students helper - app designed to help students, includes ToDoList and Translator

### Author: [@galkowskim](https://github.com/galkowskim)

## Introduction
This is a Django application that provides a ToDoList and a Translator. The application is built using the `Poetry` package manager, and the necessary files (`poetry.lock` and `pyproject.toml`) are included in the repository. In order for the application to work properly, two environment variables must be set: `EMAIL_USER` and `EMAIL_PASS`, in order for email sending to work properly (currently the entire project is configured for `Gmail`). Additionally, `requirements.txt` has been added for those not using `Poetry`.

## Installation
To install the application, follow these steps:

- Clone the repository: `git clone https://github.com/galkowskim/students_helper`
- Install the dependencies: `poetry install` or `pip install -r requirements.txt`
- Migrate the database: `python manage.py migrate`


## Usage
To run the application, use the following command:

`python manage.py runserver`

The application will be available at **http://localhost:8000/**.

## Contributing
If you would like to contribute to the application, please follow these guidelines:
- Fork the repository
- Create a new branch for your feature
- Make your changes
- Submit a pull request for review
