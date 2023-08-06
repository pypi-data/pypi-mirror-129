# RHVoice TTS plugin for Mycroft

## Installation
Install RVHVoice for your system (see [compiling instructions](https://github.com/RHVoice/RHVoice/blob/master/doc/en/index.md#compiling-instructions)):
```bash
sudo apt-get install scons libspeechd-dev
git clone --recurse-submodules https://github.com/RHVoice/RHVoice.git ~/RHVoice
cd ~/RHVoice
scons
sudo scons install
sudo ldconfig
```

Install plugin via pip:
```bash
mycroft-pip install mycroft-plugin-rhvoice
```

## Configuration
Edit `mycroft.conf` (`mycroft-config edit user`):

Basic config:
```json
{
  "tts": {
    "module": "rhvoice"
  }
}
```

Extended config (with default values):
```json
{
  "tts": {
    "module": "rhvoice",
    "rhvoice": {
      "voice": "aleksandr-hq",
      "rate": 24000
    }
  }
}
```

- `voice`: see [rhvoice.org](https://rhvoice.org/languages/)
- `rate`: 24000, 16000, 8000, etc
