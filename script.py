import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess

# Path to audio files
audio_files = {
    'KEY_A': 'File1.wav',
    'KEY_B': 'File2.wav',
    'KEY_Y': 'File3.wav',
}

# Path to the input devices (footswitches)
device_paths = ['/dev/footswitch1', '/dev/footswitch2', '/dev/footswitch3']

# Initialize the input devices
devices = [InputDevice(path) for path in device_paths]

def play_audio(file_path):
    # Stop any currently playing audio
    subprocess.run(['pkill', 'aplay'])
    # Play the new audio file
    subprocess.run(['aplay', file_path])

print(f'Listening for key presses on {device_paths}...')

for device in devices:
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                key_code = key_event.keycode
                if key_code in audio_files:
                    print(f'Key {key_code} pressed, playing {audio_files[key_code]}')
                    play_audio(audio_files[key_code])
