# USALB Radio 24 — Architecture

## Core components

1. **Radio server**
   - Runs the 24/7 audio automation and streaming service.
   - Hosts playlists, schedules, metadata and the public stream.

2. **Live broadcast client**
   - A desktop application can send microphone/live-show audio to the radio server.
   - Live mode should be able to override the automated playlist and return to automation afterward.

3. **Web player**
   - Public-facing player for listeners.
   - Displays station name, playback state and current metadata.

4. **Management**
   - Station configuration and operational documentation live in this repository.
   - Secrets must remain in environment variables and must never be committed.

## Initial deployment direction

The first implementation will keep the radio backend separate from the public web interface. This makes it possible to change the streaming backend later without rebuilding the listener-facing player.

## Future modules

- Now-playing metadata
- Schedule management
- Podcast/show pages
- Live/DJ mode
- Admin authentication
- Health monitoring
- Backup/restore
