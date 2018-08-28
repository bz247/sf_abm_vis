from flask import Flask, render_template, request, jsonify
import igraph 
import random 
import warnings 
import json 
import ast 
import numpy as np 

app = Flask(__name__)

global g
g = igraph.Graph.Read_Pickle('SF.pkl')
g.es['weight'] = g.es['sec_length']

def OD2routes(g):
    #g = igraph.Graph.Read_Pickle('SF.pkl')
    random.seed(10)
    OD_sample = random.sample(range(g.vcount()), 50)
    OD_pairs = [(OD_sample[i*2], OD_sample[i*2+1]) for i in range(25)]
    paths = []
    origins = []
    destinations = []
    for p in range(25):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message="Couldn't reach some vertices at structural_properties")
            vpath = g.get_shortest_paths(OD_pairs[p][0], OD_pairs[p][1], weights='weight', output='vpath')
        if len(vpath[0])==0:
            #print('no route found')
            continue
        else:
            coordinates = [[g.vs[vert]['n_x'], g.vs[vert]['n_y']] for vert in vpath[0]]
            paths.append({'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': coordinates}})
            origins.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [g.vs[vpath[0][0]]['n_x'], g.vs[vpath[0][0]]['n_y']]}})
            destinations.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [g.vs[vpath[0][-1]]['n_x'], g.vs[vpath[0][-1]]['n_y']]}})

    return {'paths': {'type': 'FeatureCollection', 'features': paths},
        'origins': {'type': 'FeatureCollection', 'features': origins},
        'destinations': {'type': 'FeatureCollection', 'features': destinations},
        }

@app.route('/', methods=['GET', 'POST'])
def app_home():
    return render_template("index.html", variable_here = 100)

@app.route("/getData", methods=['GET'])
def getData():

    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')

    var1 = int(entry2Value) + int(entry1Value)
    var2 = 10
    var3 = 15

    return jsonify({ 'var1': var1, 'var2': var2, 'var3': var3 })

@app.route("/get_point", methods=['GET'])
def get_point():
    return jsonify({'lon': -71.97722138410576, 'lat': -13.517379300798098})

@app.route('/get_route', methods=['GET'])
def get_route():
    initial_route_res = OD2routes(g)
    return jsonify(initial_route_res)

@app.route('/get_closure', methods=['GET', 'POST'])
def get_closure():

    try:
        [click_lon, click_lat] = ast.literal_eval(request.data.decode('utf-8'))
    except ValueError:
        print('Unable to parse JSON data from request.')
        return "Error 400"
    
    g.vs['closed'] = 0
    g.vs.select(n_x_lt=click_lon+0.001, n_x_gt=(click_lon-0.001), n_y_lt=(click_lat+0.001), n_y_gt=(click_lat-0.001))['closed'] = 1
    g.es['weight'] = g.es['sec_length']
    g.es.select(_source_in = g.vs.select(closed_eq=1), _target_in = g.vs.select(closed_eq=1))['weight'] = 1000000
    
    updated_route_res = OD2routes(g)
    return jsonify(updated_route_res)


app.run(debug=True)
