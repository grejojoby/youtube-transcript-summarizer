from flask import Flask
from flask import request
import datetime
import json

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter,WebVTTFormatter, PrettyPrintFormatter

# from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer

# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
@app.route('/')
def index_page():
    return "Hello world"

@app.route('/api/summarize/<youtube_id>', methods=['POST'])
def youtubeAPI(youtube_id):
    # video_id = request.form['youtubeid']
    video_id = youtube_id
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = JSONFormatter()

    json_formatted = formatter.format_transcript(transcript)
    final_dictionary = json.loads(json_formatted)

    print(type(final_dictionary))
    res = [ sub['text'] for sub in final_dictionary ]
    transcriptRes = ' '.join(res)
    trimmedRes = ' '.join(transcriptRes.split()[:900])
    summary = summarizeTranscriptT5API(trimmedRes)
    if(summary):
        return {"transcript": trimmedRes, "summary": summary}, 200
    else:
        return {"transcript": trimmedRes, "summary": "Error"}, 400
    
def summarizeTranscriptT5API(transcriptData):
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + transcriptData, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    # just for debugging
    print(outputs)
    T5Result = tokenizer.decode(outputs[0])
    print(T5Result)
    return T5Result


# @app.route('/youtube', methods=['GET', 'POST'])
# def youtube():
#     if request.method == 'POST':
#         video_id = request.form['youtubeid']
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         formatter = JSONFormatter()

#         json_formatted = formatter.format_transcript(transcript)
#         final_dictionary = json.loads(json_formatted)

#         print(type(final_dictionary))
#         res = [ sub['text'] for sub in final_dictionary ]
#         transcriptRes = ' '.join(res)
#         trimmedRes = ' '.join(transcriptRes.split()[:900])
#         summary = summarizeTranscriptT5(trimmedRes)
#         return '''
#                  <!doctype html>
#                  <title>Transcript</title>
#                  <h1>Actual Data</h1>
#                  <div>''' + trimmedRes + '''</div>
#                  <br>
#                  <h1>Summary</h1>
#                  <div>''' + summary + '''</div>
#                  '''

    
#     elif request.method == 'GET':
#         # case when page is loaded on browser
        
#         return '''
#             <!doctype html>
#             <title>Enter Youtube ID</title>
#             <h1>Enter the youtube video id</h1>
#             <form method=POST enctype=multipart/form-data>
#               <input type=text name=youtubeid value=youtubeid>
#               <input type=submit value=Submit>
#             </form>
#             '''

# def summarizeTranscriptT5(transcriptData):
#     model = T5ForConditionalGeneration.from_pretrained("t5-base")
#     tokenizer = T5Tokenizer.from_pretrained("t5-base")
#     inputs = tokenizer.encode("summarize: " + transcriptData, return_tensors="pt", max_length=1024, truncation=True)
#     outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
#     # just for debugging
#     print(outputs)
#     T5Result = tokenizer.decode(outputs[0])
#     print(T5Result)
#     return T5Result


# def summarizeTranscript(transcriptData):
#     summarization = pipeline("summarization")
#     summary_text = summarization(transcriptData)[0]['summary_text']
#     print("Summary:", summary_text)
#     return summary_text
    
# server the app when this file is run
if __name__ == '__main__':
    app.run()