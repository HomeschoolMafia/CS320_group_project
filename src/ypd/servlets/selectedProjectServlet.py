from flask import Flask
from flask_classy import FlaskView


class SelectedProjectView(FlaskView):
    def get(self):
        return render_template('ProjectList.html')
        
        # get project by id, display to projectlist html
   