# USALB Radio 24 — Radio Server

The station backend is designed around AzuraCast, which provides:

- 24/7 automated radio playback
- Playlists and scheduling
- Live DJ/broadcast input
- Icecast streaming
- Now-playing metadata
- Web administration

## Deployment

Run this stack on a dedicated Linux VPS/server with Docker installed.

Before exposing it to the public internet:

1. Point a domain/subdomain to the server.
2. Configure HTTPS.
3. Create the USALB Radio 24 station in the AzuraCast administration interface.
4. Upload music that you have the necessary rights to broadcast.
5. Configure playlists and schedules.
6. Configure the live DJ source.
7. Put the resulting public stream URL into web/app.js.

## Important

Do not commit passwords, API keys, or stream credentials. Keep those in the server's environment/configuration.
