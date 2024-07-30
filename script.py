import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading
import signal
import sys

audio_files = {
    'KEY_A': 'File1.wav',
    'KEY_B': 'File2.wav',
    'KEY_Y': 'File3.wav',
}

device_paths = ['/dev/footswitch1', '/dev/footswitch2', '/dev/footswitch3']

devices = [InputDevice(path) for path in device_paths]

running = True
playback_lock = threading.Lock()
current_process = None

def play_audio(file_path):
    global current_process
    with playback_lock:
        if current_process:
            current_process.terminate()
            current_process.wait()
        current_process = subprocess.Popen(['aplay -D hw:1,0', file_path])

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
                        if key_code in audio_files:
                            print(f'Key {key_code} pressed on {device.path}, playing {audio_files[key_code]}')
                            play_audio(audio_files[key_code])
                            # Break the loop to handle the next input immediately
                            break
    finally:
        device.ungrab()

def signal_handler(sig, frame):
    global running
    print('Exiting gracefully...')
    running = False
    for device in devices:
        device.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f'Listening for key presses on {device_paths}...')

threads = []
for device in devices:
    thread = threading.Thread(target=monitor_device, args=(device,))
    threads.append(thread)
    thread.start()

# Keep the main thread alive
while running:
    signal.pause()

for device in devices:
    device.close()
