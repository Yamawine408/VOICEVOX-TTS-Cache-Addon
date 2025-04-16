# Voicevox TTS Cache Addon for Home Assistant

This addon provides a caching layer for Voicevox TTS synthesis.
It's useful when running Home Assistant on slower systems like NAS.

## Features

- Caches audio files by text hash
- Avoids redundant calls to Voicevox engine
- Exposes `/api/tts?text=...` HTTP endpoint

## Setup

1. Deploy this addon to Home Assistant
2. Ensure Voicevox engine is accessible (e.g., `http://voicevox-engine:50021`)
3. Use the API from Home Assistant with media_player:

```yaml
service: media_player.play_media
data:
  entity_id: media_player.living_room_speaker
  media_content_id: "http://homeassistant.local:8125/api/tts?text=こんにちは"
  media_content_type: "music"
