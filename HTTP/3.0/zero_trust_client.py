import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
import jwt

SECRET_KEY = "supersecretkey"
TOKEN = jwt.encode({"user": "client1"}, SECRET_KEY, algorithm="HS256")

async def main():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False

    async with connect("localhost", 8003, configuration=config) as protocol:
        stream_id = protocol._quic.get_next_available_stream_id()
        request = (
            f"GET / HTTP/3\r\nAuthorization: Bearer {TOKEN}\r\n\r\n"
        ).encode()
        protocol._quic.send_stream_data(stream_id, request, end_stream=True)

        event = await protocol.wait_for_event()
        print("Response:", event.data.decode())

if __name__ == "__main__":
    asyncio.run(main())
