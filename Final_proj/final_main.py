import requests
import random
import json
import final_class
import csv
from flask import Flask, render_template, request
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#random.seed(17) # for reproducible random numbers

##################################
# Common MACRO definition
##################################
USE_API = 0 # 1 for API, 0 for local
LOCAL_ML= 1 # 1 for local html, 0 print new
LOCAL_GPU=1 # same as above
YEAR_OF_INTEREST = range(2011,2021) # Search for 2011 to 2020 data


##################################
# Functions
##################################
def init_article():
    '''
        Return a dictionary that contain all the articles
    '''
    all_article_dict = {}
    # Get data from the IEEE API
    if(USE_API):
        # querytext: Enables Free-text search of all metadata
        # publication_year: Describe which year of content
        base_url    = "http://ieeexploreapi.ieee.org/api/v1/search/articles?"
        query_text  = "querytext=machine+learning" 
        apikey      = "&apikey=kc6k3nmh83ncfah2bp2r37fh"
        for year in YEAR_OF_INTEREST:
            #target_url = "http://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=machine+learning&publication_year=2020&format=json&apikey=kc6k3nmh83ncfah2bp2r37fh"

            # Get Request
            publication_year = '&publication_year=' + str(year)
            target_url = base_url + query_text + publication_year + apikey
            response = requests.get(target_url)
            r_json = response.json()

            # Store into the global variable
            all_article_dict[year] = {}
            all_article_dict[year] = final_class.articles_per_year(r_json['articles'])

            # Store into a JSON file
            file_name = 'XPLORE_' + str(year) + '.json'
            json_file = open(file_name,'w')
            json.dump(r_json,json_file)

    # Load from local JSON files
    else:
        for year in YEAR_OF_INTEREST:
            file_name = 'XPLORE_' + str(year) + '.json'
            with open(file_name,'r') as file:
                r_json = json.load(file)
                all_article_dict[year] = {}
                all_article_dict[year] = final_class.articles_per_year(r_json)
    
    return all_article_dict

def all_art_record(all_art_dict):
    record_list = []
    for year in YEAR_OF_INTEREST:
        record_list.append(all_art_dict[year].total_record())
    return record_list


def init_gpu():
    '''
        Initialize the GPU data set
        Return a dict for GPU data
    '''
    gpu_dict = {}
    with open('gpus_v2.csv',newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        i = 0
        for row in spamreader:
            #print(row)
            if(i != 0) and (row[1] == 'Datacenter') and (int(row[3]) in YEAR_OF_INTEREST):
                gpu_dict[row[2]] = {}
                gpu_dict[row[2]]['year'] = int(row[3])
                gpu_dict[row[2]]['perf'] = float(row[9])
            i += 1
    return(final_class.gpu_dataset(gpu_dict))


def gpu_selection(brand,usage):
    gpu_list = []
    with open('gpus_v2.csv',newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #print(row)
            if(row[1] == usage) and (row[0] == brand) and (int(row[3]) in YEAR_OF_INTEREST):
                gpu_list.append(row[2])
    n = random.randint(0,len(gpu_list))
    return gpu_list[n]
        
def gpu_tree():
    
    gpu_root = final_class.Node('GPU')
    amd_node = final_class.Node('AMD')
    nv_node = final_class.Node('NVIDIA')
    gpu_root.left = amd_node
    gpu_root.right = nv_node
    gpu_dict = {}

    with open('gpus_v2.csv',newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        i = 0
        for row in spamreader:
            if(i != 0) and (row[1] == 'Datacenter') and (int(row[3]) in YEAR_OF_INTEREST):
                gpu_dict[row[2]] = {}
                gpu_dict[row[2]]['year'] = int(row[3])
                gpu_dict[row[2]]['perf'] = float(row[9])
            i += 1
    
    with open('gpu_tree.json','w') as json_file:
        json.dump(gpu_dict,json_file,indent=2, sort_keys=True)
    




##################################
# Flask Settings
##################################       
app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/article_records')
def show_records():
    return render_template('ArticleRecords.html')

@app.route('/GPU')
def show_GPU():
    return render_template('GPU.html')

@app.route('/VS')
def show_VS():
    return render_template('VS.html')

@app.route('/cite_year')
def show_year():
    return render_template('cite_year.html')

@app.route('/cite_year/2011')
def show_2011_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/5473234/',name="Nonconvex Online Support Vector Machines")

@app.route('/cite_year/2012')
def show_2012_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/6183517/',name="Generalized SMO Algorithm for SVM-Based Multitask Learning")

@app.route('/cite_year/2013')
def show_2013_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/6472238/',name="Representation Learning: A Review and New Perspectives")

@app.route('/cite_year/2014')
def show_2014_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/6756997/',name="Sparse Extreme Learning Machine for Classification")

@app.route('/cite_year/2015')
def show_2015_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/6847217/',name="Transfer Learning for Visual Categorization: A Survey")

@app.route('/cite_year/2016')
def show_2016_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/7347425/',name="Driver Distraction Detection Using Semi-Supervised Machine Learning")

@app.route('/cite_year/2017')
def show_2017_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/7943475/',name="How to steal a machine learning classifier with deep learning")

@app.route('/cite_year/2018')
def show_2018_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/8441123/',name="Comparison of Deep Learning and the Classical Machine Learning Algorithm for the Malware Detection")

@app.route('/cite_year/2019')
def show_2019_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/8862451/',name="A Quick Review of Machine Learning Algorithms")

@app.route('/cite_year/2020')
def show_2020_article():
    return render_template('text.html',link_for_article='https://ieeexplore.ieee.org/document/9091758/',name="Traffic Prediction for Intelligent Transportation System using Machine Learning")

@app.route('/GPU_recommend')
def GPU_recommend():
    return render_template('FlaskInputs2.html') # just the static HTML
    

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    user_name = request.form["name"]
    brand = request.form["brands"]
    usage = request.form["usage"]
    sel = gpu_selection(brand,usage)
    webpage="https://www.google.com/search?q=" + sel.replace(" ", "+")
    return render_template('response.html', 
        name=user_name, 
        brand=brand,
        usage=usage,
        select=sel,
        webpage=webpage)
    

##################################
# Plotly Settings
################################## 
def print_ML_html(all_article_dict):
    xval = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    yval = all_art_record(all_article_dict)
    data = go.Scatter(x=xval,y=yval)
    layout = go.Layout(title='Article for Machine Learning Count')
    fig = go.Figure(data=data, layout=layout)
    fig.write_html('ArticleRecords.html',auto_open=True)

def print_GPU_html(gpu_obj):
    xval = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    yval = gpu_obj.avg_perf_each_year()
    data = go.Scatter(x=xval,y=yval)
    layout = go.Layout(title='GPU average performance each year(counted as Millison Floting execution / second)')
    fig = go.Figure(data=data, layout=layout)
    fig.write_html('GPU.html',auto_open=True)

def print_sub_plot(gpu_obj, all_article_dict):
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Machine Learning Research Count","GPU perf" ))
    fig.add_trace(go.Scatter(x=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020], y=all_art_record(all_article_dict)),
              row=1, col=1)
    fig.add_trace(go.Scatter(x=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020], y=gpu_obj.avg_perf_each_year()),
                row=2, col=1)
    fig.update_layout(title_text="ML Research vs GPU avg perf(counted as Millison Floting execution / second)")
    fig.write_html('VS.html',auto_open=True)
    
##################################
# MAIN program
##################################
if __name__ == '__main__':
    all_article_dict = init_article()
    gpu_obj = init_gpu()
    gpu_tree()
    app.run(debug=True)
    if(LOCAL_ML == 0):
        print_ML_html(all_article_dict)
    if(LOCAL_GPU == 0):
        print_GPU_html(gpu_obj)

