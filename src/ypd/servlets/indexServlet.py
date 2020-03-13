from flask import Flask, render_template
from flask_classy import FlaskView

class IndexView(FlaskView):
    def get(self):
        catalog = [{'logo': '', 'link': '#', 'name': 'Test1', 'title': 'Test1 Project'}, 
                   {'logo': '', 'link': '#', 'name': 'Test2', 'title': 'Test2 Project'}, 
                   {'logo': '', 'link': '#', 'name': 'Test3', 'title': 'Test3 Project'}, 
                   {'logo': '', 'link': '#', 'name': 'Test4', 'title': 'Test4 Project'}, 
                   {'logo': '', 'link': '#', 'name': 'Test5', 'title': 'Test5 Project'}]
        return render_template('CS320-ProjectMainPage.html', catalog=catalog)
        