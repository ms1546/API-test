from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, jsonify

app = Quart(__name__)

@app.route('/')
async def hello():
    return jsonify(message="Hello, HTTP/2!")

if __name__ == '__main__':
    config = Config()
    config.bind = ["0.0.0.0:8001"]
    config.certfile = ".ssl/cert.pem"
    config.keyfile = ".ssl/key.pem"
    print("HTTP/2 server running on port 8001 with SSL...")
    import asyncio
    asyncio.run(serve(app, config))
