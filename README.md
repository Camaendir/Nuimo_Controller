# Nuimo Controller

### Setup
- **1**: Follow the installation steps for your Bluetooth device on [Nuimo's Github](https://github.com/getsenic/nuimo-linux-python)
- **2**: Install the python requirements

    `python3 -m pip install -r requirements.txt`
- **3**: Create and configure the env.py

    This step depends on what type of controller you use. If you use a Spotipy-Controller you need to add your credentials in there (see env_example.py). For an MQTT connection add your MQTT host and port. If you use Phillips Hue add your Hue-Bridge IP in there.

### Available Controller

- **Spotipy-Controller**: control your Music!
- **Lighting-Controller**: control your Lighting with state,brightness,color and animations (through MQTT)