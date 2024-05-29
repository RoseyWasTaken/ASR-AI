import queue, sys, json, requests
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from gui import display_face

q = queue.Queue()

mic = 3

device_info = sd.query_devices(mic, "input")
samplerate = int(device_info["default_samplerate"])
model = Model(model_path="vosk-model-small-en-us-0.15")

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def voice_inference(rec):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            inferrence = json.loads(rec.Result())
            text = inferrence.get("text")
            if text:
                return text

def modelRequest(message):
    url = "http://100.102.228.152:11434/api/generate"
    body = {
        "model": "llama3",
        "prompt": str(message + " Be very brief. In one sentence."),
        "stream": False  # responds once the entire response is ready
    }
    x = requests.post(url, json=body)
    response = json.loads(x.text)
    return response.get("response")

try:
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=mic,  # adjust device if needed
                           dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, samplerate)

        display_face("sleeping")
        while True:
            wakeWord = voice_inference(rec)
            print(wakeWord)
            if wakeWord == "hey robot":
                display_face("thinking")
                print(wakeWord)
                print("Wake word detected.")
                
                heard = voice_inference(rec)
                print("I heard: " + str(heard))
                
                response = modelRequest(heard)
                display_face("speaking", text=response)
                print(response)
            else:
               print("Sleeping")
               display_face("sleeping")
except KeyboardInterrupt:
    print("\nDone")
    exit(0)
