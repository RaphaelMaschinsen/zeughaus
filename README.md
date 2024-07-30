# Raspberry Pi Project Setup Repository

This repository is intended to help set up Raspberry Pis for various projects. There are three specific branches you can switch to, each providing the setup instructions and files for different projects.

## Available Branches

1. **Zeughaus-Switch**: This branch contains the setup for the Zeughaus footswitch audio player project, which uses USB footswitches to play different audio files.
2. **Zeughaus-Switch-simple**: This branch provides a simplified version of the Zeughaus footswitch audio player project.
3. **Zeughaus-loop**: This branch contains the setup for a looping audio playback project.

## How to Switch Branches

To switch to a specific branch, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/zeughaus-switch.git
    cd zeughaus-switch
    ```

2. Check out the desired branch:

    ```sh
    git checkout branch-name
    ```

   Replace `branch-name` with one of the following:

   - `Zeughaus-Switch`
   - `Zeughaus-Switch-simple`
   - `Zeughaus-loop`

## Branch Descriptions

### Zeughaus-Switch

This branch contains the complete setup for the Zeughaus footswitch audio player project. It includes detailed instructions for configuring the Raspberry Pi, installing necessary libraries, and setting up the system as a service.

### Zeughaus-Switch-simple

This branch provides a simplified version of the Zeughaus footswitch audio player project. It may have fewer features or simplified configurations compared to the main Zeughaus-Switch branch.

### Zeughaus-loop

This branch contains the setup for a looping audio playback project. It is designed for continuous playback of audio files in a loop, suitable for installations that require uninterrupted audio.

## Getting Started

1. Switch to the desired branch as described above.
2. Follow the instructions in the `README.md` file within the selected branch to set up your Raspberry Pi for the project.

For any issues or questions, please refer to the `README.md` file in the respective branch for troubleshooting tips and contact information.
