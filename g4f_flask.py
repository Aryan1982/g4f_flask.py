from flask import Flask, request, jsonify, Response, stream_with_context
import g4f
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

g4f.debug.logging = True 
g4f.check_version = False  

def generate_stream(response, jailbreak):
    for message in response:
        yield f"data: {message}\n\n"
    if jailbreak:
        yield "event: jailbreak\ndata: {}\n\n"

@app.route('/chat', methods=['GET','POST'])
def chat():
    try:
         data = request.args.get('payload')
         payload = json.loads(data)
         user_message = payload['message']

         response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            stream=True,
         )
        # for message in response:
        #     print(message, flush=True, end='')
         return Response(
            stream_with_context(generate_stream(response, True)),
            mimetype='text/event-stream'
         )

    except Exception as e:
        return Response(
            stream_with_context(generate_stream([str(e)], True)),
            mimetype='text/event-stream'
        )
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
