from flask import Flask
from flask import render_template
from flask import request
import datetime
import json

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter,WebVTTFormatter, PrettyPrintFormatter




# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
@app.route('/')
def index_page():


    return "Hello world"


@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'POST':
        video_id = request.form['youtubeid']
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = JSONFormatter()

        json_formatted = formatter.format_transcript(transcript)
        final_dictionary = json.loads(json_formatted)

        print(type(final_dictionary))
        res = [ sub['text'] for sub in final_dictionary ]
        return '''
            <!doctype html>
            <title>Transcript</title>
            <h1>Enter the youtube video id</h1>
            <div>''' + ' '.join(res) + '''</div>
            '''
    
    elif request.method == 'GET':
        # case when page is loaded on browser
        
        return '''
            <!doctype html>
            <title>Enter Youtube ID</title>
            <h1>Enter the youtube video id</h1>
            <form method=POST enctype=multipart/form-data>
              <input type=text name=youtubeid value=youtubeid>
              <input type=submit value=Submit>
            </form>
            '''

# server the app when this file is run
if __name__ == '__main__':
    app.run()