from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        if 'upload' in request.form:
            pass  #call function to handle folder upload
        elif 'results' in request.form:
            return redirect(url_for("results"))

    html = render_template('home.html')
    return html

@app.route("/results",methods=['GET','POST'])
def results():

    html = render_template('results.html')
    return html

if __name__ == "__main__":
    app.run(port=8000, debug=True)