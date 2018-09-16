from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField
from sheets_api import get_tdc_info
import json
from os import path

####################################################################
# Tier List Stuff
####################################################################
def get_tier_list():
    """Get and Format the tier_list"""
    # Fetch TDC info
    header_list,tier_list = get_tdc_info()
    tier_dict = list()

    # Adjust Header Comment Keys
    for i in range(7,11):
        header_list[0][i]+='_comment'

    # Remove Header information
    tier_list = tier_list[2:]
    # Remove Apost
    tier_list = [[st.replace("'","") for st in row] for row in tier_list]
    # Remove all escape characters
    tier_list = [[st.replace("\n","") for st in row] for row in tier_list]
    tier_list = [[st.replace("\"","") for st in row] for row in tier_list]
    

    for row in tier_list:
        tier_dict.append(dict(zip(header_list[0],row)))

    return tier_dict

tier_info = get_tier_list()


####################################################################
# FLask Stuff
####################################################################
# Create the Flask Application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'FDFSGTRJNYDT5463GFDSW32FFVDFFMNHFMUUFFF4577'

class SearchForm(FlaskForm):
    card = StringField('Card', id='searchTextbox', render_kw={"placeholder":"Card Name", "class":"form-control"})

@app.route("/")
def draft_tierlist():
    form = SearchForm()
    return render_template('index.html',form=form, tier_info=tier_info)

if __name__ == '__main__':
    app.run(debug=True)