import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess

audio_files = {
    'KEY_A': 'File1.wav',
    'KEY_B': 'File2.wav',
    'KEY_Y': 'File3.wav',
}

device_paths = ['/dev/footswitch1', '/dev/footswitch2', '/dev/footswitch3']

devices = [InputDevice(path) for path in device_paths]

def play_audio(file_path):
    subprocess.run(['pkill', 'aplay'])
    subprocess.run(['aplay', file_path])

def monitor_device(device):
    print(f'Start monitoring {device.path}')
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                key_code = key_event.keycode
                if key_code in audio_files:
                    print(f'Key {key_code} pressed on {device.path}, playing {audio_files[key_code]}')
                    play_audio(audio_files[key_code])

print(f'Listening for key presses on {device_paths}...')

# Create a separate process for each device to handle events concurrently
import threading

threads = []
for device in devices:
    thread = threading.Thread(target=monitor_device, args=(device,))
    threads.append(thread)
    thread.start()

# Join all threads
for thread in threads:
    thread.join()
