import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived
import jwt

SECRET_KEY = "supersecretkey"

class ZeroTrustServer(QuicConnectionProtocol):
    def stream_data_received(self, stream_id: int, data: bytes, fin: bool):
        if fin:
            try:
                headers, payload = data.decode().split("\r\n\r\n", 1)
                token = headers.split("Authorization: Bearer ")[-1]
                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                response = (
                    "HTTP/3 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, Authorized Client!"
                ).encode()
            except Exception as e:
                response = (
                    "HTTP/3 401 Unauthorized\r\nContent-Type: text/plain\r\n\r\nUnauthorized!"
                ).encode()
            self._quic.send_stream_data(stream_id, response, end_stream=True)

async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    print("Zero Trust HTTP/3 server running...")
    await serve("0.0.0.0", 8003, configuration=config, create_protocol=ZeroTrustServer)

if __name__ == "__main__":
    asyncio.run(main())
