import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .hls_handler import HLSStreamHandler


class StreamConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_handler = None
        self.stream_id = None

    async def connect(self):
        self.stream_id = self.scope["url_route"]["kwargs"]["stream_id"]
        self.room_group_name = f"stream_{self.stream_id}"

        # Add the channel to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        self.stream_handler = HLSStreamHandler(self.stream_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Stop the stream if it's running
        if self.stream_handler:
            self.stream_handler.stop_stream()

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get("command")

        if command == "start_stream":
            # TODO: Can add OpenCV method
            if self.stream_handler.start_stream():
                playlist_url = self.stream_handler.get_playlist_url()
                await self.send(text_data=json.dumps({"type": "stream_started", "playlist_url": playlist_url}))

        elif command == "stop_stream":
            if self.stream_handler.stop_stream():
                await self.send(text_data=json.dumps({"type": "stream_stopped"}))

        elif command == "get_status":
            await self.send(
                text_data=json.dumps(
                    {"type": "status", "is_running": self.stream_handler.is_running if self.stream_handler else False}
                )
            )
