from flask import Flask, render_template, request, jsonify
from dijkstra import classrooms, distances, coordinates, teachers, dijkstra
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', rooms=classrooms, teachers=teachers.keys())

@app.route('/get_path', methods=['POST'])
def get_path():
    data = request.get_json()
    
    start = data.get('start')
    end = data.get('end')
    start_type = data.get('start_type', 'room')  
    end_type = data.get('end_type', 'room')      
    
    if start_type == 'teacher':
        if start in teachers:
            start = teachers[start]
        else:
            return jsonify({'error': f'No room found for teacher: {start}'})
    
    if end_type == 'teacher':
        if end in teachers:
            end = teachers[end]
        else:
            return jsonify({'error': f'No room found for teacher: {end}'})
    
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