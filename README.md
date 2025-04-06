# 🍿 Jellyfin Media Stack

[![Docker Compose](https://img.shields.io/badge/Docker--Compose-Ready-blue?logo=docker)](https://docs.docker.com/compose/)
[![MIT License](https://img.shields.io/github/license/Kakise/jellyfin-media-stack.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Kakise/jellyfin-media-stack.svg?style=social)](https://github.com/Kakise/jellyfin-media-stack/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Kakise/jellyfin-media-stack)](https://github.com/Kakise/jellyfin-media-stack)

A powerful, almost plug-and-play media stack built around [Jellyfin](https://jellyfin.org), powered by Docker Compose.  
Inspired by and expanded from the awesome work on [Rick45/quick-arr-Stack](https://github.com/Rick45/quick-arr-Stack).  

---

## 🧩 Included Services

| Category     | Tool           | Description                          |
|--------------|----------------|--------------------------------------|
| 📥 Downloaders | **DMB**, **Decypharr**, **Deluge** | Smart torrent + RealDebrid automation |
| 📚 Indexers   | **Prowlarr**, **Sonarr**, **Radarr** | Manage TV/movies, HD and 4K |
| 🎬 Media Server | **Jellyfin**        | Local/remote streaming media server |
| 📬 Requests   | **Jellyseerr**     | Easy media request interface |
| 🧼 Housekeeping | **Watchtower**     | Automatic container updates |
| 🖥 UI Dashboard | **Homepage**        | Clean web UI with widgets |
| 💬 IRC Client | **TheLounge**       | Web-based IRC for chatting |

---

## ⚡ Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kakise/jellyfin-media-stack.git
   cd jellyfin-media-stack
   ```

2. **Configure Environment Variables**
   Create and edit a `.env` file:
   ```bash
   cp .env.example .env
   nano .env
   ```

   Example `.env`:
   ```env
   ROOT=/path/to/root
   HDDSTORAGE=/mnt/your/drive
   PUID=1000
   PGID=1000
   TZ=Your/Timezone
   HOSTNAME=localhost

   # API Keys
   RD_API_KEY=your_rd_key
   PROWLARR_API_KEY=your_prowlarr_key
   SONARR_API_KEY=your_sonarr_key
   SONARR_4K_API_KEY=your_sonarr_4k_key
   RADARR_API_KEY=your_radarr_key
   RADARR_4K_API_KEY=your_radarr_4k_key
   JELLYFIN_API_KEY=your_jellyfin_key
   JELLYSEERR_API_KEY=your_jellyseerr_key
   ```

3. **Launch the Stack**
   ```bash
   docker compose up -d
   ```

4. **Access Services**

   | Service      | URL                          |
   |--------------|------------------------------|
   | Jellyfin     | http://HOSTNAME:8096         |
   | Sonarr       | http://HOSTNAME:8989         |
   | Sonarr 4K    | http://HOSTNAME:8888         |
   | Radarr       | http://HOSTNAME:7878         |
   | Radarr 4K    | http://HOSTNAME:7979         |
   | Prowlarr     | http://HOSTNAME:9696         |
   | Decypharr    | http://HOSTNAME:8000         |
   | DMB Frontend | http://HOSTNAME:3005         |
   | pgAdmin      | http://HOSTNAME:5050         |
   | Jellyseerr   | http://HOSTNAME:5055         |
   | Homepage     | http://HOSTNAME:1903         |
   | TheLounge    | http://HOSTNAME:9000         |

---

## 🗂 Directory Structure

```
MediaCenter/
├── config/
│   ├── jellyfin/
│   ├── DMB/
│   ├── decypharr/
│   ├── sonarr/
│   ├── radarr/
│   └── ...
├── downloads/
├── media/
└── other/
```

---

## ✨ Features

- 🔁 **Auto-updating containers** via Watchtower
- 🎨 **Themed Jellyfin** with Theme Park (Rose Pine Moon)
- 🧠 **Split 4K & HD libraries** using multiple Sonarr/Radarr instances
- 📦 **Volume persistence** for all configurations
- 🔐 **Ready for reverse proxy & SSL**
- 🔌 **RealDebrid + Zurg mount support** via DMB
- 📊 **Homepage dashboard** with widgets for all services

---

## 🧠 Tips

- Use with NGINX Proxy Manager or Traefik for domain + HTTPS
- Schedule backups of config directories
- Consider using SSD storage for Jellyfin transcode temp
- Tweak your indexers in Prowlarr for best results
- Add homepage bookmarks or widgets via config

---

## 🙏 Credits

- [Rick45/quick-arr-Stack](https://github.com/Rick45/quick-arr-Stack) for their work on an easy to use arr stack
- [LinuxServer.io](https://www.linuxserver.io/) for many container images
- [Jellyfin](https://jellyfin.org) — open-source media server
- [Theme.park](https://github.com/GilbN/theme.park) — beautiful UI themes
- [Zurg](https://github.com/debridmediamanager/zurg-testing) for RealDebrid mount magic
- All the incredible maintainers of the open-source tools used here 🙌

---

## 📜 License

MIT © [Kakise](https://github.com/Kakise)

---

Enjoy your self-hosted media experience! 🎉
