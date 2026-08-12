# NC-Edit7 branding assets

All files are generated from `LOGO-base.png` on a white canvas without stretching.

## Web, Docker, and Azure

- `web/favicon-16.png`, `favicon-32.png`, `favicon-48.png`: browser icons
- `web/apple-touch-icon.png`: iOS home-screen icon
- `web/pwa-192.png`, `pwa-512.png`: installable web app icons
- `web/pwa-maskable-512.png`: Android maskable icon with extra safe-area padding
- `site.webmanifest`: web app metadata used by both Docker and Azure deployments

## VS Code extension

Use `vscode/icon.png` as the extension manifest icon:

```json
{
  "icon": "public/branding/vscode/icon.png"
}
```

The extension package must include this file. The VS Code Marketplace expects a square PNG of at least 128x128 pixels.

## Microsoft Store / Windows app

The `windows-store` directory contains common MSIX/AppxManifest assets:

- `StoreLogo.png`: 50x50
- `Square44x44Logo.png`: 44x44
- `Square71x71Logo.png`: 71x71
- `Square150x150Logo.png`: 150x150
- `Square310x310Logo.png`: 310x310
- `Wide310x150Logo.png`: 310x150
- `SplashScreen.png`: 620x300
- `StoreDisplayLogo.png`: 300x300 Partner Center listing image
- `app.ico`: Windows/Electron icon with 16, 24, 32, 48, 64, 128, and 256 pixel frames

Point the eventual MSIX/AppxManifest or Electron builder configuration at these files. Store submission artwork requirements can vary by listing type, so Partner Center may request additional screenshots or promotional images separately.
