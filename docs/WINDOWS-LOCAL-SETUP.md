# USALB Radio 24 — Windows 11 Local Setup

This project is designed to be tested on the owner's Windows 11 PC before moving the radio server to another computer.

## Goal

Run the radio backend locally at $0:

Windows 11 PC
→ Linux environment (WSL2)
→ Docker
→ AzuraCast
→ automated radio stream

The public listener website remains a separate part of the project.

## Important

The repository does **not** use the small `docker-compose.yml` file as the official AzuraCast installation method. AzuraCast's current documentation provides its own Docker installer script. Use that installation method rather than guessing or manually assembling the AzuraCast containers.

Official installation documentation:
https://www.azuracast.com/docs/getting-started/installation/docker/

## What we will install

1. Windows Subsystem for Linux 2 (WSL2)
2. A Linux distribution such as Ubuntu
3. Docker/Docker Compose support
4. AzuraCast
5. A USALB Radio 24 station inside AzuraCast

## After installation

We will configure:

- Station name: USALB Radio 24
- Time zone: Europe/Tirane
- Automated music playlists
- 24/7 schedule
- Stream mount point
- Now-playing metadata
- Live DJ/microphone input
- Website player connection

## Free-testing limitations

This local setup costs $0, but the Windows PC must stay powered on and connected to the internet for continuous broadcasting.

Making the stream publicly reachable from a home connection may also depend on the router and ISP. We will test this after the local station works.

## Do not commit

Never put these into GitHub:

- AzuraCast administrator passwords
- Stream/DJ passwords
- Router credentials
- API tokens
- Personal access tokens
- Private keys

Use local environment/configuration for secrets.

## Migration later

When the station is finished, the AzuraCast data can be migrated to the uncle's computer or another server. The public website can remain separate.
