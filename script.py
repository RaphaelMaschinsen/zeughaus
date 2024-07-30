import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading
import signal
import sys

# Define the audio file to be played
audio_file = 'File1.wav'

# Path to the input device (footswitch)
device_path = '/dev/footswitch'

# Initialize the input device
device = InputDevice(device_path)

running = True
playback_lock = threading.Lock()
current_process = None

def play_audio(file_path):
    global current_process
    with playback_lock:
        if current_process:
            current_process.terminate()
            current_process.wait()
        current_process = subprocess.Popen(['aplay', file_path])

def monitor_device(device):
    print(f'Start monitoring {device.path}')
    device.grab()  # Grab the device to get exclusive access
    try:
        while running:
            for event in device.read_loop():
                if not running:
                    break
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        key_code = key_event.keycode
                        print(f'Key {key_code} pressed on {device.path}, playing {audio_file}')
                        play_audio(audio_file)
                        # Break the loop to handle the next input immediately
                        break
    finally:
        device.ungrab()

def signal_handler(sig, frame):
    global running
    print('Exiting gracefully...')
    running = False
    device.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f'Listening for key presses on {device_path}...')

thread = threading.Thread(target=monitor_device, args=(device,))
thread.start()

# Keep the main thread alive
while running:
    signal.pause()

device.close()
