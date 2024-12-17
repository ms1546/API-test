from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.webtransport import WebTransportProtocol

class WebTransportServer(WebTransportProtocol):
    async def http_request(self, stream_id, headers, body):
        if headers[":path"] == "/webtransport":
            await self.accept()
        else:
            self._quic.send_stream_data(
                stream_id,
                b"HTTP/3 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found",
                end_stream=True,
            )

async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    await serve("0.0.0.0", 8003, configuration=config, create_protocol=WebTransportServer)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
