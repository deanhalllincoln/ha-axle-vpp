# My Experience With Axle’s Grid Event Service

I recently signed up for Axle Energy’s grid services beta programme, choosing the **Events-Only mode**. Since I already manage my inverter and battery myself through Home Assistant using a local Modbus connection, I didn’t need Axle’s full-control option. What I did want was the ability to take part in paid grid-support events in a way that didn’t interfere with my existing automations.

---

## What is a Grid Event

Events are short periods when the electricity grid needs extra support. During these periods, when the grid is under strain, any power exported to it is valuable, which is why Axle pays **£1 per kWh**.

Here’s a full breakdown of my first event, how it performed, and what people can expect.

---

## My Home Energy Setup

- **5 kW inverter** (Fox Ess H1-5.0-E-G2)  
- **20.72 kWh battery** (2 × Fox Ess EP11)  
- **17 × 420 W solar panels** (9 north-facing, 8 south-facing)  
- **Battery minimum charge:** 10%  
- **Installed:** March 2025  

---

## Notification of the First Event

Axle sent a day-ahead notification:

> We’ll be exporting from your battery tomorrow 2025-12-04 from 16:30 to 17:30…  
> We’ll pay you £1/kWh… You don’t need to do anything — we’ll handle this automatically and reset your settings afterwards.

Clear, simple, and no action required.

---

## What Happened During the Event

Nothing changed during the day. Then at **16:30** a scheduled discharge event appeared automatically in the Fox app.

During the one-hour window:

- **Export rate from inverter:** 5 kW  
- **House load:** ~0.75 kW  
- **Net export:** ~4.25 kW  
- **Total energy exported:** 4.25 kWh  

Everything worked exactly as expected.

---

## After the Event

At 17:30, export stopped and the inverter returned to its previous setup. The Axle-created schedule removed itself automatically.

Battery state:

- Starting level: ~15.5 kWh (77%)  
- Exported: 4.25 kWh  
- Ended event at ~10.8 kWh  

The house then ran on the battery until **9:15 pm**, when it reached the **10%** minimum. From that point until midnight (when the cheap rate starts), we drew energy from the grid.

---

## Earnings Breakdown

### Standard Axle Rate (Normal £1 per kWh)

Axle pays **£1/kWh** exported:

- **Axle payment:** £4.25  

Plus my standard export tariff:

- **E.ON Next:** £0.165/kWh → ~£0.70  

**Total earned:** £4.95  

Battery depletion meant the house imported extra energy from 9:15 pm to midnight:

- 2.45 hours × 1 kWh ≈ 2.45 kWh  
- At £0.265/kWh = **£0.65 cost**  

**Net profit from event:** **£4.30**

**Recharge cost:**  
4.25 kWh × £0.067 ≈ **£0.29**

Still an excellent return for a one-hour event.

---

## Bonus Payment for the First Event

Axle boosted the payout for this inaugural event to **£2 per kWh**.

### Earnings at £2/kWh bonus rate:

- **Axle bonus rate:** 4.25 kWh × £2 = **£8.50**  
- **Plus E.ON SEG:** ~£0.70  
- **Total:** **£9.20**  

Minus the evening grid import (£0.65):

- **Net profit at bonus rate:** **£8.55**  

### Speed of Payment

The credit for this event was added to my Axle account **within 48 hours**, and I can withdraw funds at **any time**.

---

## Guaranteed Minimum Payment

Axle guarantees **a minimum of £10/month** until **March 2026**, even if very few events occur.

---

## Control Options: Event Mode vs Full Control

### Full Control

For users who want a hands-off experience:

- Automatic pre-charging  
- Battery always prepared for maximum event export  
- Axle manages inverter behaviour end to end  

### Events-Only

My preferred mode:

- I maintain full control of daily operation  
- Axle only takes control during the event window  
- They provide an API endpoint with event start/end times, useful for:  
  - Pre-charge logic  
  - Managing discharge during events  
  - Logging and automations in Home Assistant  

Axle works independently of any energy supplier or tariff.

---

## Overall Impression

My first Axle event was:

- Seamless  
- Fully automated  
- Financially worthwhile  
- Non-intrusive  
- Quickly paid out  

An effortless way to make extra income from a battery system that would otherwise sit idle during peak-price stress events.

We’ve asked Axle for a list of recent past events to understand typical frequency, and I’m looking forward to seeing that data.

---

## How to Join Axle and Take Part in Paid Export Events

1. **Create your account**  
   Use this link to receive **£25 credit instantly**:  
   https://vpp.axle.energy/landing?ref=R-JQDOUROD

   *(I also receive £25, which helps fund development of the Home Assistant Axle integration.)*

2. **Upload a recent electricity bill**  
   This allows Axle to validate your MPAN.

3. **Provide inverter login details**  
   Needed so they can control export during event windows.

4. **Add your tariff information**  
   Used to optimise participation.

After that, you’re ready for your first grid event.


