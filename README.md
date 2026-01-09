# Home Assistant HACS Integration for Axle VPP API

## Axle VPP Integration for Home Assistant

A custom Home Assistant integration for pulling Axle Virtual Power Plant (VPP) event data into **individual, easy-to-use sensor entities**.

This integration removes the need for manual REST sensors in `configuration.yaml` and provides a **clean, UI-based, HACS-friendly installation**, suitable for both advanced Home Assistant users and those who prefer not to edit YAML.

---

## ✨ Features

- Fetches current Axle VPP event data from the official Axle API
- Provides separate Home Assistant sensor entities (no attributes buried in a single sensor)
- Includes **human-friendly datetime sensors** using Home Assistant’s native timestamp handling
- Uses Home Assistant Config Flow (UI-based setup)
- Fully HACS-compatible with versioned releases
- Automatic polling using `DataUpdateCoordinator`
- No YAML configuration required

---

## 📊 Available Sensors

### Raw API Sensors

These reflect the data exactly as returned by the Axle API:

- `sensor.axle_start_time`
- `sensor.axle_end_time`
- `sensor.axle_import_export`
- `sensor.axle_updated_at`

### Friendly Datetime Sensors

These convert Axle’s UTC timestamps into **local UK time** and use Home Assistant’s `timestamp` device class for easy use in automations and dashboards:

- `sensor.axle_start_time_friendly`
- `sensor.axle_end_time_friendly`
- `sensor.axle_updated_at_friendly`

> **Note**  
> When no grid event is active or scheduled, `start_time` and `end_time` (and their friendly versions) will show as `unknown`.  
> `updated_at_friendly` updates on every API poll (default every 600 seconds).

---

## 📦 Installation (HACS)

### Step 1: Add the repository to HACS

1. Open **Home Assistant**
2. Go to **HACS → Integrations**
3. Open the three-dot menu (⋮) → **Custom repositories**
4. Add:
https://github.com/deanhalllincoln/ha-axle-vpp

yaml
Copy code
5. Category: **Integration**

---

### Step 2: Install the integration

1. Go back to **HACS → Integrations**
2. Search for **Axle VPP**
3. Click **Install**

---

### Step 3: Configure the integration

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Axle VPP**
4. Enter your **Axle API token**
5. Save

Your sensors will appear under a device called **Axle VPP**.

---

## 🔑 Getting Your Axle API Token

Once your Axle account is active:

1. Log in to your Axle dashboard:  
https://vpp.axle.energy
2. Navigate to **Account → Integrations / API**
3. Copy your API token
4. Paste it into the Axle VPP integration setup in Home Assistant

---

## 📝 How to Sign Up with Axle

Axle is a UK-based flexibility service that rewards households for supporting the electricity grid during periods of high demand.

### Sign-up process

1. Visit the Axle sign-up page:  
https://vpp.axle.energy/landing?ref=R-JQDOUROD
2. Create an account
3. Upload a recent electricity bill (for meter and MPAN details)
4. Provide inverter access details
5. Add your electricity tariff information
6. Wait for approval and activation

Once approved, your API token will become available.

---

## 💷 Bonus Credit

If you register using the link above:

- **You receive £25 credit**
- **I also receive £25**

This helps support ongoing development and maintenance of this Home Assistant integration.

Using the referral link is optional, but very much appreciated.

---

## 📁 Directory Structure

custom_components/axle_vpp/
├── init.py
├── manifest.json
├── const.py
├── coordinator.py
├── sensor.py
├── config_flow.py
└── strings.json

---

## 🛠 How It Works

- Uses Home Assistant’s `DataUpdateCoordinator` to poll Axle’s API every **600 seconds**
- Fetches event data from:
https://api.axle.energy/vpp/home-assistant/event

yaml
Copy code
- Parses the response into individual sensors
- Friendly datetime sensors convert UTC timestamps into local UK time
- All entities update automatically and are grouped under a single device

---

## 🚀 Roadmap

- Additional Axle endpoints as they become available
- Event history sensors
- Optional notifications for upcoming grid events
- Configurable polling interval
- Improved diagnostics and logging

---

## 💬 Support

If you encounter issues, please open a GitHub issue with logs and details.

Feature requests and contributions are welcome.

And if this integration helps you, using the Axle referral link genuinely supports future development.
