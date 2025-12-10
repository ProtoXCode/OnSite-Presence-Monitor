# TODO / Roadmap for OnSite Presence Monitor

## 🧠 Planned Features

- ✅ Mock ERP client for demo use
- 🛠 Monitor G5 client – WIP
  - [X] Connect to live API
  - [X] Authenticate via config
  - [X] Filter based on location data
- [ ] Auto-launch fullscreen kiosk mode (per-device optional config)
- [ ] Offline fallback display
- [ ] Reverse proxy with Nginx/Traefik for HTTPS

## 🐞 Known Gaps

- Monitor ERP client will error if config is missing or malformed
- No retry/backoff logic if ERP is temporarily unavailable
- Image fallback only tested locally — may fail on serverless hosts

## 🧪 Test Coverage Ideas

- Kiosk rendering on various screen resolutions

---

_This list is not exhaustive — PRs welcome!_
