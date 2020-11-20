# biosec_employee_management
Dependencies

1.Virtualenv

2. python3

3.Django3.x
4.django-restframework
5.crispy_forms
6.mysqlclient

installation
ensure that all dependencies are installed, clone project from : https://github.com/nugwuegbu/biosec_employee_management.git

The project has been developed on a virtual environment on the root of the project"venv"
launch the project by activating the venv while in the project directory.

relpace the database information with your own credentials in settings.py on the root directory
run migration and also createsuper with the commands below:

1 python3 manager.py migrate
2.python3 manager.py createsuperuser

Launch the project with the command below:
python3 manager.py runserver

when the app is launched , you will be required to login with the Super user created in previous step

I have also attached Postman collections to test the API endpoints

