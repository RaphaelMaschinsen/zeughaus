import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading

# Path to audio files
audio_files = {
    'KEY_A': 'File1.mp3',
    'KEY_B': 'File2.mp3',
    'KEY_Y': 'File3.mp3',  # Assuming this was intended to be File3.mp3
}

# Path to the input devices (footswitches)
device_paths = ['/dev/footswitch1', '/dev/footswitch2', '/dev/footswitch3']

# Initialize the input devices
devices = [InputDevice(path) for path in device_paths]

def play_audio(file_path):
    # Stop any currently playing audio
    subprocess.run(['pkill', 'mpg123'])
    # Play the new audio file
    subprocess.run(['mpg123', file_path])

def listen_device(device):
    print(f'Start listening on {device.path}')
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                key_code = key_event.keycode
                if key_code in audio_files:
                    print(f'Key {key_code} pressed on {device.path}, playing {audio_files[key_code]}')
                    play_audio(audio_files[key_code])

# Create and start a thread for each device
threads = []
for device in devices:
    thread = threading.Thread(target=listen_device, args=(device,))
    thread.daemon = True
    thread.start()
    threads.append(thread)

# Keep the main thread running to allow the listening threads to operate
print(f'Listening for key presses on {device_paths}...')
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping...")
