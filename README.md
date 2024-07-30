# Zeughaus Audio Player (Loop Version)

This project plays an audio file on a loop on a Raspberry Pi. The system is set up as a service that starts on boot and continuously plays the specified audio file.

## Table of Contents

- [Setup](#setup)
  - [Installing Raspberry Pi OS](#installing-raspberry-pi-os)
  - [Configuring Keyboard Layout](#configuring-keyboard-layout)
  - [Updating the Raspberry Pi](#updating-the-raspberry-pi)
  - [Cloning the Repository and Switching Branches](#cloning-the-repository-and-switching-branches)
  - [Installing Required Packages](#installing-required-packages)
  - [Configuring ALSA for Audio Output](#configuring-alsa-for-audio-output)
  - [Creating and Enabling the Service](#creating-and-enabling-the-service)
- [Checking the Logs](#checking-the-logs)
- [Troubleshooting](#troubleshooting)

## Setup

### Installing Raspberry Pi OS

1. Download the Raspberry Pi Imager from the official Raspberry Pi website: [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Install and run the Raspberry Pi Imager.
3. Choose the Model you are using (at the time of writing this it is Raspberry Pi 2 Model B).
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

    git checkout zeughaus-loop
    git pull origin zeughaus-loop

### Installing Required Packages

You need to install Python and necessary libraries, as well as `alsa-utils` for sound management:

    sudo apt install python3 python3-virtualenv python3-pip alsa-utils

Next, create a virtual environment for your project:

    python3 -m virtualenv env

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

To stop the service:

    sudo systemctl stop zeughaus.service

To restart the service:

    sudo systemctl restart zeughaus.service

To check the status of the service:

    sudo systemctl status zeughaus.service

For any issues with audio output, ensure that ALSA is configured correctly and that the correct audio device is set.





