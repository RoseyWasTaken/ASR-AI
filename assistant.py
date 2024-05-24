import queue
import sys
import json
import sounddevice as sd
import requests
import threading
from vosk import Model, KaldiRecognizer
from gui import displayFace, shared_data, change_event  # Assuming displayFace is imported from a module named gui

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

q = queue.Queue()

text =""

device_info = sd.query_devices(1, "input")
samplerate = int(device_info["default_samplerate"])
model = Model(model_path="vosk-model-small-en-us-0.15")

def inferVoice(rec):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            inferrence = json.loads(rec.Result())
            text = inferrence.get("text")
            if text:
                return text

def modelRequest(message):
    url = "http://localhost:11434/api/generate"
    body = {
        "model": "llama3",
        "prompt": str(message + " Be very brief. In one sentence."),
        "stream": False  # responds once the entire response is ready
    }
    x = requests.post(url, json=body)
    response = json.loads(x.text)
    return response.get("response")

try:
    print("hi!")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=1,  # adjust device if needed
                           dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, samplerate)
        # Start the displayFace function in a separate thread with the "sleeping" state
        background_thread = threading.Thread(target=displayFace)  
        background_thread.start()

        # sleeping face = 0
        # speaking face = 1
        # thinking face = 2

        while True:
            wakeWord = inferVoice(rec)
            print(wakeWord)
            if wakeWord == "hey robot":
                shared_data["face"] = 2
                change_event.set()

                print(wakeWord)
                print("Wake word detected.")
                
                heard = inferVoice(rec)
                print("I heard: " + str(heard))
                
                response = modelRequest(heard)
                shared_data["face"] = 1
                shared_data["text"] = response
                change_event.set()
                print(response)

            else:
                shared_data["face"] = 0
                change_event.set()
                print("Sleeping")

except KeyboardInterrupt:
    print("\nDone")
    exit(0)
