from flask import Response 
from app import app
from .layers import super_graph

@app.route('/api')
def index():
    def generate():
        for s in super_graph.stream(
            {
                "messages": [
                    ("user", "Research AI agents and write a brief report about them.")
                ],
            },
            {"recursion_limit": 150},
        ):
            yield f"data:{s}\n\n" 

    return Response(generate(), mimetype='text/event-stream')