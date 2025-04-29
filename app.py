from flask import Flask, render_template, request, jsonify
from dijkstra import classrooms, distances, coordinates, dijkstra
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', rooms=classrooms)

@app.route('/get_path', methods=['POST'])
def get_path():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    
    if start not in classrooms or end not in classrooms:
        return jsonify({'error': 'Invalid room name'})
    
    try:
        distance, path = dijkstra(classrooms, distances, start, end)
        
        # Create path with coordinates
        path_coordinates = []
        for room in path:
            if room in coordinates:
                path_coordinates.append({
                    'name': room,
                    'coords': coordinates[room]
                })
        
        return jsonify({
            'distance': distance,
            'path': path,
            'path_coordinates': path_coordinates
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)