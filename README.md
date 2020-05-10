# project_proposer
Group Project for CS320

# Install
Run the command:
```
python3 -m pip install path_to_project
```

# Set your environment variables
In order to send emails properly, you must set the following environment variables:
 ```YPD_EMAIL_USERNAME```, and ```YPD_MAIL_PASSWORD```

# Initialize the databases
The command to initialize the databases from csvs is ```init_db```

# Run the program
Run the command:
```ypd_server```
When you do, the main function of the script at project_proposer/scripts/prototype_server.py runs.
If everything is working correctly, after running that commmand, you should be able to open a browser
and type
```
localhost:5000
```
This should display the login page. From there, you can navigate to every page of the website
