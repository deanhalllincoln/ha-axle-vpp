# ha-axle-vpp
Home Assistant HACS install for Axle VPP Api


Axle VPP Integration for Home Assistant

A custom Home Assistant integration for pulling Axle Virtual Power Plant (VPP) event data into individual, easy-to-use sensor entities.
This integration removes the need for manual REST sensors in configuration.yaml and provides a simpler, cleaner, HACS-friendly installation.

✨ Features

Fetches current Axle VPP event info from the official Axle API

Provides distinct Home Assistant sensor entities:

start_time

end_time

import_export

updated_at

Uses Home Assistant’s Config Flow (UI setup)

Supports HACS for simple installation and automatic updates

No YAML configuration required

📦 Installation (HACS)
Step 1: Add the repository to HACS

Open Home Assistant

Go to HACS → Integrations

Select the three-dot menu (⋮) → Custom repositories

Add:

https://github.com/deanhalllincoln/ha-axle-vpp


Category: Integration

Step 2: Install the integration

Return to HACS → Integrations

Search for Axle VPP

Click Install

Step 3: Configure

Go to Settings → Devices & Services

Click Add Integration

Search for Axle VPP

Enter your API token

Save

Your sensors will now appear under the "Axle VPP" device.

🔑 Getting Your Axle API Token

Axle provides your API token once your account is active.
To obtain one:

Log in to your Axle account:
https://vpp.axle.energy

Go to Account → Integrations / API

Copy the API token provided

Paste into the Axle VPP integration in Home Assistant

📝 How to Sign Up with Axle

Axle VPP is a UK-based flexibility service that rewards households for participating in demand-response events.
Signing up is straightforward:

Visit the sign-up page:
https://vpp.axle.energy/landing?ref=R-JQDOUROD

Create an account

Complete the onboarding steps

Wait for approval and activation of your Axle dashboard

Your API token will appear once you’re fully enrolled

💷 Bonus Credit

If you register using the link above, Axle will add £25 credit to your account, and they also add £25 to mine.
This helps support ongoing development and maintenance of this integration.

Participation via the referral link is optional, but very much appreciated.

📁 Directory Structure

For reference, the custom component uses the following layout:

custom_components/axle_vpp/
  ├── __init__.py
  ├── manifest.json
  ├── const.py
  ├── coordinator.py
  ├── sensor.py
  ├── config_flow.py
  └── strings.json

🛠 How It Works

The integration uses Home Assistant’s DataUpdateCoordinator to poll Axle's API every 600 seconds.

JSON from the Axle event endpoint is parsed.

Each attribute becomes its own Home Assistant sensor entity.

Entities update automatically and appear together under an Axle VPP device.

🚀 Roadmap

Optional sensors for additional Axle endpoints when released

Configurable scan interval

Error codes and event history

Optional notifications

💬 Support

If you discover issues, feel free to open a GitHub issue.
Feature requests and contributions are always welcome.

And if this integration helps you, using the referral link for your Axle signup really does assist with future development.
