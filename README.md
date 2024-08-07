# Zeughaus Footswitch Audio Player

This project uses USB footswitches to play different audio files on a Raspberry Pi. The system is set up as a service that starts on boot and listens for footswitch inputs to play corresponding audio files.

## Table of Contents

- [Setup](#setup)
  - [Important: USB Hub and Footswitch Connection](#important-usb-hub-and-footswitch-connection)
  - [Installing Raspberry Pi OS](#installing-raspberry-pi-os)
  - [Configuring Keyboard Layout](#configuring-keyboard-layout)
  - [Updating the Raspberry Pi](#updating-the-raspberry-pi)
  - [Cloning the Repository and Switching Branches](#cloning-the-repository-and-switching-branches)
  - [Installing Required Packages](#installing-required-packages)
  - [Downloading the large audio file from Google Drive](#downloading-the-large-audio-file-from-google-drive)
  - [Configuring ALSA for Audio Output](#configuring-alsa-for-audio-output)
  - [Creating and Deploying Udev Rules](#creating-and-deploying-udev-rules)
  - [Creating and Enabling the Service](#creating-and-enabling-the-service)
- [Checking the Logs](#checking-the-logs)
- [Troubleshooting](#troubleshooting)

## Setup

### Important: USB Hub and Footswitch Connection

1. Ensure the USB hub is plugged into the upper USB port on the Raspberry Pi.
2. Use the officially supported USB hub: 'usb3.0-SuperSpeed 4Ports Hub'.
3. Connect the footswitches to port 1, port 2, and port 3 of the USB hub.

### Installing Raspberry Pi OS

1. Download the Raspberry Pi Imager from the official Raspberry Pi website: [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Install and run the Raspberry Pi Imager.
3. Choose the Model you are using (at the time of writing this it is Raspberry Pi 2 Model B)
4. Select "Raspberry Pi OS (32-bit)" as the operating system.
5. In the Settings unselect everything except for 'Set Username and Password' and choose 'pi' as the username and as the password.
6. Choose your SD card and click "Continue" to start the installation process.
7. Once the process is complete, insert the SD card into your Raspberry Pi and power it on.

### Configuring Keyboard Layout

To change the keyboard layout, use the `raspi-config` tool:

    sudo raspi-config

Navigate to `Localisation Options` > `Keyboard` > `Keyboard Layout`, then follow the prompts to select your keyboard model and layout.

### Updating the Raspberry Pi

First, ensure your Raspberry Pi is up-to-date. Open a terminal and run:

    sudo apt update
    sudo apt upgrade -y

### Cloning the Repository and Switching Branches

Clone the GitHub repository to your Raspberry Pi:

    git clone https://github.com/RaphaelMaschinsen/zeughaus.git
    cd zeughaus

Switch to the appropriate branch for your project:

    git checkout zeughaus-switch

### Installing Required Packages

You need to install Python and necessary libraries, as well as `alsa-utils` for sound management:

    sudo apt install gedit python3 python3-virtualenv python3-pip alsa-utils

Next, create a virtual environment for your project (within the zeughaus folder):

    python3 -m virtualenv env

Then activate:

    source env/bin/activate

### Downloading the large audio file from Google Drive

You can download the Audio files from google drive with wget. An easy way to do this is to at first open the readme with getit like so:

    gedit README.md

And then copy these commands one by one and paste them into the terminal to download the audio files:

    wget --no-check-certificate "https://drive.google.com/file/d/1-IIKx6UeGYzfwNDlefj1MpjoddJfrZMt" -O File1.wav
    wget --no-check-certificate "https://drive.google.com/file/d/1Ipsh08Rka17ZytI56oulxZc1_CYr3Aie" -O File2.wav
    wget --no-check-certificate "https://drive.google.com/file/d/1uKsJsVJhhpd17EF4GcNRUIUOb97-OAJe" -O File3.wav

### Installing Python Libraries

Install the required Python libraries using pip with the activated virtual env:

    pip install evdev

### Configuring ALSA for Audio Output

To configure ALSA to use the audio jack, open the `alsa.conf` file:

    sudo nano /usr/share/alsa/alsa.conf

Find the following lines:

    defaults.ctl.card 0
    defaults.pcm.card 0

Change them to:

    defaults.ctl.card 1
    defaults.pcm.card 1

Save and exit the file.

### Creating and Deploying Udev Rules

Copy your `99-footswitch.rules` file to the correct directory to set up udev rules:

    sudo cp /home/pi/zeughaus/99-footswitch.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    sudo udevadm trigger

### Creating and Enabling the Service

Copy your service file to the systemd directory:

    sudo cp /home/pi/zeughaus/zeughaus.service /etc/systemd/system/

Reload the systemd daemon to recognize the new service:

    sudo systemctl daemon-reload

Enable the service to start on boot:

    sudo systemctl enable zeughaus.service

Start the service:

    sudo systemctl start zeughaus.service

## Checking the Logs

To see the logs for the service since the last boot and troubleshoot any issues, you can use the following command:

    sudo journalctl -u zeughaus.service -b

## Troubleshooting

If the footswitches are not recognized after a reboot, make sure the udev rules are correctly applied and check for any errors in the logs.

To stop the service:

    sudo systemctl stop zeughaus.service

To restart the service:

    sudo systemctl restart zeughaus.service

To check the status of the service:

    sudo systemctl status zeughaus.service

For any issues with audio output, ensure that ALSA is configured correctly and that the correct audio device is set.
