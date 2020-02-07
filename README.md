# project_proposer
Group Project for CS320

Alright y'all, sit down and buckle up because I'm about to tell you everything you need to know

# Resources
Some usefule resources for our project:

Python docs: https://docs.python.org/3/
    This website has all of the language specifications and stdlib information you need to know

The Hitchhikers Guide to Python: https://docs.python-guide.org/
    This website has a wealth of tutorials, pythonic programming, and other resources to
    help learn the language features.

SQLAlchemy documentation: https://www.sqlalchemy.org/
    For all your database needs

Flask documentation: https://flask.palletsprojects.com/en/1.1.x/
    Flask will handle the RESTful API stuff for us. It's analagous to JSP

HTML templating: 
https://jinja.palletsprojects.com/en/2.11.x/templates/
https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/ 
    Flask provides a Jinja2 templating environment set up for delivering HTML files. These are the
    Specifications for Jinja2 and the flask environment respectively

# Install instructions
I, personally, prefer to do all my python development from the command line, and use
VsCode as my editor. So these instructions apply to that. Hopefully you can translate them
to PyCharmese. 

Also, all of these commands are done in bash. They definitly run on a linux machine. They should run
in git bash or cygwin if you're using windows.
Alex, if you're developing on apple, I'm sorry. I have no fucking idea what to do, so you're on your own

Note: All of the instructions from now on assume CS320_group_project is your cwd. If it isn't, just
``` 
cd path_to_CS320_group_project
```

It's good practice to use a virtual environment, although it's not strictly necessary


All of the runtime dependencies are documented in setup.py. If you use pip to install the project,
all of those dependancies will be installed for you. 
To use pip to install:
    Install python and pip
    ```
    python3 -m pip install -e .
    ```

All of the packages listed in DEV_REQUIRES are useful programs to run on your code.
    pytest runs unit tests
    rope allows refactoring
    pylint notifies you of errors
    autopep8 cleans up your code and makes it readable

You'll have to pip install each of these individually
```
python3 -m pip install pytest rope pylint autopep8
```

# Solr install instruction
Download a binary solr 8.x release from https://lucene.apache.org/solr/downloads.html
Unzip the file
Add *your-solr_directory*/bin to your PATH environment variable
In the command line, run ```configure_solr```
Note: If this is the first time you have run configure_solr, you may see a few lines that look like
```ERROR: Failed to delete core```
This is normal

Once you've run ```conifgure_solr```, you won't have to run it again unless you modify
the collection or test_collection fields in config.ini, or modify sample_index.xml,
test_index.xml, or solr_schema.json

# Run the program
setup.py has an 'ENTRY_POINTS' variable that defines python scripts that can be run. The one
I've included is:
```python
'prototype_server=project_proposer.scripts.prototype_server:main'
```
The way this works is, the name before the '=' runs the script after the '='.
In the command line, you can type
```
prototype_server
```
When you do, the main function of the script at project_proposer/scripts/prototype_server.py runs.
Please note that because this is a stupid prototype script, your cwd has to be CS320_group_project,
or the program will fail.

If everything is working correctly, after running that commmand, you should be able to open a browser
and type
```
localhost:5000
```
This should display a webpage that says 'Hello, world!'

# Other things you should know
Note:
 I am the owner of the git repository, so I will be enforcing these rules

Version control: 
    I'm pushing this to the master branch for right now. But in the future, we should follow
    this model: https://nvie.com/posts/a-successful-git-branching-model/
    Essentially, this means we create our own branches to make our changes, and then merge
    into develop. Develop tracks our current 'incomplete' product. We only push to master
    when we have a working product for the demo

Docstrings:
    Because python is a statically typed language, we need to write sphinx style docstrings
    on every method a la add.py.
    Seriously. Document arguments, types, and return values.

Pytest:
    Pytest handles all of the unit testing very quickly
    (I assume PyCharm already has a tool for this)
    To run pytest,
    ```
        pytest
    ```
    AS long as your tests match the template given in test_sum.py, pytest will find all of the
    tests, run them, and print out a summary of the results

Autopep8:
    Autopep8 is a tool that improves the readability of your code by making little tweaks.
    Honestly, you don't have to use it. But it'll make things easier on everyone if you do.

    You should run it on every *.py file you modify.
    To run:
    ```
    autopep8 -i -v path_to_file
    ```
