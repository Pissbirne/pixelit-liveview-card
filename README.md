# PixelIt Liveview Card

A custom Lovelace card for Home Assistant that **mirrors the live content of a [PixelIt](https://github.com/pixelit-project/PixelIt) matrix display** — the clock, bitmaps, text, everything you see on the physical display — as a mini pixel grid.

Unlike a naive direct-connection approach, this card reads the display content **through Home Assistant**, so it works everywhere: on the desktop, in the Companion App over **Nabu Casa (remote/https)**, and on any network.

## Features

- **Live pixel mirror** — Shows exactly what the PixelIt display is currently showing (rendered from the real LED pixels, ~250ms updates)
- **Works over Nabu Casa / remote** — Uses a HA sensor, not a direct device WebSocket, so it works in the Companion App and from outside your LAN
- **Theme-compatible** — Transparent background, adapts to any HA theme (including glass/Frosted Glass themes)
- **Connection status badge** — Shows "Verbunden" / "Getrennt" (connected/disconnected)
- **Visual editor** — Full configuration via UI, no YAML needed
- **Multi-language** — German, English (auto-detects HA language)

![PixelIt Liveview Card in the dashboard](images/screenshot-dashboard.png)

## Requirements

This card needs a small companion **integration** (`pixelit_liveview`) installed on Home Assistant. The integration connects to your PixelIt's WebSocket (port 81) and exposes the live content as a sensor. Without it the card has nothing to read.

> **Why an integration?** PixelIt sends its live pixels only over WebSocket (port 81). A browser can't reach that from a Companion App over Nabu Casa (mixed content + different network). Running the WebSocket on HA and exposing a sensor makes it work everywhere.

## Installation

### 1. Install the integration

The integration is **not yet in HACS**, so install it manually:

1. Create the folder `/config/custom_components/pixelit_liveview/`
2. Download these files into it (from the `custom_components/pixelit_liveview/` folder of this repo):
   - `__init__.py`
   - `const.py`
   - `coordinator.py`
   - `manifest.json`
3. Add to `configuration.yaml`:
   ```yaml
   pixelit_liveview:
     host: 192.168.178.8   # your PixelIt IP
     port: 81
     width: 32
     height: 8
   ```
4. Restart Home Assistant

> The integration uses `aiohttp` (bundled with HA) — no external Python packages needed.

### 2. Install the card

#### HACS (recommended)
1. Add this repo as a custom repository in HACS (type: **Dashboard**)
2. Install
3. Restart Home Assistant
4. Add card to your dashboard

#### Manual
1. Copy `pixelit-liveview-card.js` to your `www/custom/` directory
2. Add resource: `/local/custom/pixelit-liveview-card.js` (type: JavaScript Module)
3. Restart Home Assistant
4. Add card to your dashboard

## Configuration

### Visual Editor
Add a new card and search for **"PixelIt Liveview"**. Select the sensor (`sensor.pixelit_liveview`) and set the matrix size. Configure display options in the editor.

![PixelIt Liveview Card editor](images/screenshot-editor.png)

### YAML
```yaml
type: custom:pixelit-liveview-card
entity: sensor.pixelit_liveview
width: 32
height: 8
gap: 1
title: PixelIt
show_header: true
show_status: true
show_pixels: true
```

### Card Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | `sensor.pixelit_liveview` | Sensor exposing the liveview data (from the integration) |
| `width` | int | 32 | Matrix width in pixels |
| `height` | int | 8 | Matrix height in pixels |
| `gap` | int | 1 | Gap between pixels (px) |
| `title` | string | `PixelIt` | Card title |
| `show_header` | bool | true | Show card title |
| `show_status` | bool | true | Show connection status badge |
| `show_pixels` | bool | true | Show the pixel grid |

## How it works

1. The `pixelit_liveview` integration on HA opens a WebSocket to `ws://<pixelit-ip>:81`.
2. PixelIt streams its live pixels as `{"liveview":"<hex>"}` (~6 hex chars per pixel, row by row).
3. The integration parses the hex into `{r,g,b}` pixels and writes them to the `sensor.pixelit_liveview` attributes.
4. The card reads the sensor via HA and renders the pixels as a grid, stretching to fill the card width while keeping pixels square.

## License

MIT
