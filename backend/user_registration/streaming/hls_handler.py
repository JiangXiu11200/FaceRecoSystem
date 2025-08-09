# streaming/hls_handler.py
import os
import subprocess
import threading

from django.conf import settings


class HLSStreamHandler:
    def __init__(self, stream_id):
        self.stream_id = stream_id
        self.output_path = os.path.join(settings.HLS_OUTPUT_PATH, stream_id)
        self.process = None
        self.is_running = False

        # 確保輸出目錄存在
        os.makedirs(self.output_path, exist_ok=True)

    def start_stream(self):
        """
        開始將輸入源轉換為 HLS 串流
        """
        if self.is_running:
            return False

        output_playlist = os.path.join(self.output_path, "playlist.m3u8")

        # FIXME: 透過 settings 或設定頁面來帶入參數
        source_args = [
            "-f", "avfoundation",
            "-framerate", "30",
            "-video_size", "1280x720",
            "-i", "0:none",
        ]

        cmd = [
            "ffmpeg",
            *source_args,
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "23",
            "-f",
            "hls",
            "-hls_time",
            "4",
            "-hls_list_size",
            "10",
            "-hls_flags",
            "delete_segments+append_list",
            "-hls_segment_filename",
            os.path.join(self.output_path, "segment_%03d.ts"),  # 片段路徑
            output_playlist,
        ]

        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.is_running = True

        threading.Thread(target=self._monitor_output).start()

        return True

    def _monitor_output(self):
        while self.is_running:
            if self.process:
                output = self.process.stderr.readline()
                if output:
                    print(f"FFmpeg output: {output.decode('utf-8').strip()}")
                elif self.process.poll() is not None:
                    self.is_running = False
                    break

    def stop_stream(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.is_running = False
            return True
        return False

    def get_playlist_url(self):
        """Get the URL of the HLS playlist."""
        return f"/media/hls/{self.stream_id}/playlist.m3u8"
