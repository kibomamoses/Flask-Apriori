
import os
from apriori import run_apriori, format_results
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import datetime

application = Flask(__name__)

application.config["UPLOAD_FOLDER"] = "static/"

#home page where user gives the dataset as input 
@application.route('/')
def upload_file():
    return render_template('index.html')

#Result page.
@application.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        s = request.form['support']
        support =int(s)
        filename = secure_filename(f.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))

        f.save(os.path.join(basedir, application.config['UPLOAD_FOLDER'], filename))
        file = open(application.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        
      
        #from upload file convert to array to pass to python file.
        inFile = []
    for line in content.split('\n'):
        line = line.strip().rstrip(",")  # Remove trailing comma
        record = frozenset(list(map(str.strip, line.split(",")[1:]))) 
        inFile.append(record)
    
    if inFile is not None:  
        start = datetime.datetime.now()
        items = run_apriori(inFile, support)
        #print(items)
        
        #calculating the algorithm execution time
        end = datetime.datetime.now()
        program_run_time = str((end - start))  

        res= format_results(items)
        total_item = len(items)  
        

    return render_template('content.html', res=res ,items =items ,s=s,total_item = total_item ,filename =filename , content= content, program_run_time =program_run_time) 

if __name__ == '__main__':
    application.run()