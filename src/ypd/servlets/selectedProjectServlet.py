from flask import Flask, render_template, request
from flask_classy import FlaskView
from ..model.project import Provided, Solicited

class SelectedProjectView(FlaskView):
    def get(self):
                
        # Get project by id
        isProvided =  request.args.get('isProvided', default=False, type = bool)
        id         =  request.args.get('id', default = ' ', type=int)
        
        if isProvided:
            s = Provided.get(id)
        else:
            s = Solicited.get(id)
            
        # Render HTML
        return render_template('ProjectList.html', project = s)
    