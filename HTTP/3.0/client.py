import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

async def main():
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False

    async with connect("localhost", 8003, configuration=configuration) as protocol:
        stream_id = protocol._quic.get_next_available_stream_id()
        request = (
            "GET / HTTP/3\r\n"
            "Host: localhost\r\n"
            "\r\n"
        ).encode()
        protocol._quic.send_stream_data(stream_id, request, end_stream=True)

        event = await protocol.wait_for_event()
        if isinstance(event, StreamDataReceived):
            print("Response received:")
            print(event.data.decode())

if __name__ == "__main__":
    asyncio.run(main())
