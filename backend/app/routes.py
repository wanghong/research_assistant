from flask import Response, request
import json
from langchain_core.messages import ToolMessage
from app import app
from .layers import super_graph

@app.route('/api')
def index():
    question = request.args.get('question')

    def generate():
        try:
            for s in super_graph.stream(
                {
                    "messages": [
                        ("user", question)
                    ],
                },
                {"recursion_limit": 150},
                stream_mode="messages"
            ):
                if isinstance(s[0], ToolMessage):
                    continue
                if (s[1] and s[1]['langgraph_node'] == "supervisor"):
                    continue
                content = s[0].content
                data = json.dumps({"content": content})
                yield f"data:{data}\n\n"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            print(f"Error in streaming: {e}")
            error_message = {"content": f"Sorry, an error occurred while processing your request: {str(e)}"}
            yield f"data:{json.dumps(error_message)}\n\n"
            yield f"data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')