import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


class ObservabilityHTTP3Server(QuicConnectionProtocol):
    def stream_data_received(self, stream_id: int, data: bytes, fin: bool):
        with tracer.start_as_current_span("handle_request"):
            if fin:
                with tracer.start_as_current_span("process_request"):
                    print(f"Received data: {data.decode()}")
                    response = (
                        "HTTP/3 200 OK\r\n"
                        "Content-Type: text/plain\r\n"
                        "Content-Length: 16\r\n"
                        "\r\n"
                        "Hello, Observability!"
                    ).encode()
                    self._quic.send_stream_data(stream_id, response, end_stream=True)


async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    print("HTTP/3 server with OpenTelemetry running on port 8003...")
    await serve(
        "0.0.0.0",
        8003,
        configuration=config,
        create_protocol=ObservabilityHTTP3Server,
    )


if __name__ == "__main__":
    asyncio.run(main())
