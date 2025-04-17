import os
import json
import asyncio
import tempfile
import soundfile as sf
from aiohttp import web
from dotenv import load_dotenv
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaBlackhole
import openai
from openai import OpenAI
from langsmith import traceable

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

from langsmith import utils
print(utils.tracing_is_enabled())

pcs = set()


client = OpenAI()


@traceable
def generate_completion(message):
    # Define the conversation context
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    # Create the chat completion
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
    return completion.choices[0].message.content


class AudioProcessorTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()

        # Convert to numpy array
        audio_data = frame.to_ndarray()
        sample_rate = 48000  # WebRTC standard

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            sf.write(tmpfile.name, audio_data, samplerate=sample_rate)
            print(f"[DEBUG] Saved audio to: {tmpfile.name}")

            try:
                with open(tmpfile.name, "rb") as audio_file:
                    transcript = openai.Audio.transcribe("whisper-1", audio_file)
                    text = transcript["text"]
                    print(f"[TRANSCRIBED] {text}")

                    reply = generate_completion(text)
                    print(f"[GPT REPLY] {reply}")
            except Exception as e:
                print(f"[ERROR] {e}")

        return frame

async def index(request):
    with open("index.html", "r", encoding="utf-8") as f:
        return web.Response(content_type="text/html", text=f.read())

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("track")
    def on_track(track):
        print(f"Track received: {track.kind}")
        if track.kind == "audio":
            local_audio = AudioProcessorTrack(track)
        elif track.kind == "video":
            blackhole = MediaBlackhole()
            blackhole.addTrack(track)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),
    )

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)

app = web.Application()
app.on_shutdown.append(on_shutdown)
app.router.add_get("/", index)
app.router.add_post("/offer", offer)

# Change port if 8080 is taken
web.run_app(app, port=8081)
