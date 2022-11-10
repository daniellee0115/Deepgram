from flask import Flask, jsonify, request
import librosa

app = Flask(__name__)

audio_files = {}
audio_duration = {}
audio_names = {'names': []}

@app.route('/post', methods=['POST'])
def upload_audio():
    file = request.files['upload']
    name = file.filename
    binary = file.read()
    with open('buf.wav', 'bw') as buf:
        buf.write(binary)
    duration = librosa.get_duration(filename='buf.wav')
    audio_files[name] = {'file': str(binary)}
    audio_duration[name] = {'duration': duration}
    audio_names['names'].append(name)
    return '', 200

@app.route('/download')
def download_contents():
    return jsonify(audio_files[request.args['name']])

@app.route('/list')
def list():
    result = audio_names['names']
    if len(request.args) > 0:
        if 'maxduration' in request.args and 'minduration' in request.args:
            maxduration = float(request.args['maxduration'])
            minduration = float(request.args['minduration'])
            result = [i for i in audio_duration if minduration <= float(audio_duration[i]['duration']) <= maxduration]
        elif 'maxduration' in request.args:
            maxduration = float(request.args['maxduration'])
            result = [i for i in audio_duration if float(audio_duration[i]['duration']) <= maxduration]
        else:
            minduration = float(request.args['minduration'])
            result = [i for i in audio_duration if minduration <= float(audio_duration[i]['duration'])]
    return jsonify({"Audio files": result})

@app.route('/info')
def info():
    return jsonify(audio_duration[request.args['name']])

if __name__ == '__main__':
    app.run()