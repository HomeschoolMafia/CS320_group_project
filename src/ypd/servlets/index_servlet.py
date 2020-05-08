from flask import current_app, render_template, request
from flask_classy import FlaskView
from flask_login import current_user, login_required
from sqlalchemy import Enum

from ..model.catalog import Catalog
from ..model.project import Provided, GradeAttributes
from ..model.user import User
from .tests import Tests


class IndexView(FlaskView):
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        search_text = request.args.get('search_text', default='')
        search_archived = request.args.get('archived', default=False)
        search_grade = GradeAttributes(int(request.args.get('year', default=GradeAttributes.Senior.value)))
        
        if request.args.get('electrical') == '1':
            search_electrical = True
        else:
            search_electrical = None
        if request.args.get('mechanical') == '1':
            search_mechanical = True
        else:
            search_mechanical = None
        if request.args.get('computer') == '1':
            search_computer = True
        else:
            search_computer = None
        if request.args.get('computersci') == '1':
            search_computersci = True
        else:
            search_computersci = None
        if request.args.get('electrical')==None and request.args.get('mechanical')==None and request.args.get('computer')==None and request.args.get('compuersci')==None:
            search_electrical=None
            search_mechanical=None
            search_computer=None
            search_computersci=None


        search_projSize = int(request.args.get('projSize', default=1))
        search_projType = int(request.args.get('projType', default=1))
        print(search_projSize)
        catalog = Catalog(search_projType, search_archived, search_text, search_grade=search_grade, max_ProjSize=search_projSize, electrical=search_electrical, mechanical=search_mechanical, 
                    computer=search_computer, computersci=search_computersci)
        catalog.apply()
        return render_template('index.html', catalog=catalog, user=current_user, GradeAttributes=GradeAttributes)
    
    @login_required
    def get_favorites(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_favorites_catalog()
        return render_template('index.html', catalog=catalog, user=current_user)

