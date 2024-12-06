import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

class HTTP3Server(QuicConnectionProtocol):
    def stream_data_received(self, stream_id: int, data: bytes, fin: bool):
        if fin:
            response = (
                "HTTP/3 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 16\r\n"
                "\r\n"
                "Hello, HTTP/3!"
            ).encode()
            self._quic.send_stream_data(stream_id, response, end_stream=True)

async def main():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    print("HTTP/3 server running on port 8003...")
    await serve("0.0.0.0", 8003, configuration=configuration, create_protocol=HTTP3Server)

if __name__ == "__main__":
    asyncio.run(main())
