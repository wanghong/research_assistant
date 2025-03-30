from flask import Response, request
import json
from app import app
from .layers import super_graph

@app.route('/api')
def index():
    question = request.args.get('question')

    def generate():
        #try:
            for s in super_graph.stream(
                {
                    "messages": [
                        ("user", question)
                    ],
                },
                {"recursion_limit": 150},
                stream_mode="messages"
            ):
                print(s)
                content = s[0].content#.replace('\n', '\\n').replace('\r', '\\r')
                data = json.dumps({"content": content})
                yield f"data:{data}\n\n"
        # except Exception as e:
        #     # 记录异常信息
        #     print(f"Error in streaming: {e}")
        #     # 可以选择发送错误信息给客户端
        #     yield f"data:Error occurred: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream')