# My Experience With Axle’s Grid Event Service

I recently signed up for Axle Energy’s grid services beta programme, choosing the **Events-Only mode**. Since I already manage my inverter and battery myself through Home Assistant using a local Modbus connection, I didn’t need Axle’s full-control option. What I did want was the ability to take part in paid grid-support events in a way that didn’t interfere with my existing automations.

---

## What is a Grid Event

Events are short periods when the grid needs extra support. During these periods, when the electricity grid is under strain, any power supplied to the grid is valuable — hence the high rate of **£1 per kWh**.

Here’s a full breakdown of my first event, how it performed, and what people can expect.

---

## My Home Energy Setup

- **5 kW inverter** (Fox Ess H1-5.0-E-G2)  
- **20.72 kWh battery** (2 × Fox Ess EP11)  
- **17 × 420 W solar panels** (9 north-facing, 8 south-facing)  
- **Battery minimum charge:** 10%  
- **Installed:** March 2025  

Plenty of headroom for export events, even in winter.

---

## Notification of the First Event

Axle sent a message the day before:

> We’ll be exporting from your battery tomorrow 2025-12-04 from 16:30 to 17:30…  
> We’ll pay you £1/kWh… You don’t need to do anything — we’ll handle this automatically and reset your settings afterwards.

Clear, simple, and no action required.

---

## What Happened During the Event

Nothing changed during the day. Then exactly at **16:30**, a scheduled event appeared automatically in my Fox app.

My inverter immediately began exporting at the full **5 kW** limit. During the event:

- **Export rate from inverter:** 5 kW  
- **House load:** around 0.75 kW  
- **Net export to grid:** around 4.25 kW  
- **Total energy exported during event:** 4.25 kWh  

Everything operated smoothly and exactly as described.

---

## After the Event

At 17:30, discharge stopped automatically and the inverter reverted to its previous configuration. The Axle-created schedule also disappeared.

After the event, the battery had:

- Started around 15.5 kWh (about 77%)  
- Exported 4.25 kWh  
- Ending the event at roughly 10.8 kWh  

Through the evening, the house continued running from the battery ***until around 9:15 pm, when it reached the 10% minimum capacity***.

- Average consumption per hour between 9:15 pm and midnight: ~1 kWh total  
***Once the battery hit its 10% limit (around 2 kWh), the remaining evening and night-time load came from the grid. Had there been no grid event, the battery would have comfortably supplied the home until midnight when the low-cost overnight rate begins.***

---

## Earnings Breakdown

Axle pays **£1/kWh** exported during an event. So, for 4.25 kWh:

- £4.25 from Axle  

Plus my normal export tariff:

- **E.ON Next:** £0.165/kWh → ~£0.70 extra  

**Total earned:** £4.95  

***Because the battery reached 10% earlier than it would have without the grid event, we paid for extra imported electricity between 9:15 pm and midnight. That’s 2.45 hours × 1 kWh = 2.45 kWh at £0.265 per kWh, totalling £0.65. Subtracting this from the earnings leaves a net profit of £4.30 for the one-hour export event.***

**Cost to recharge:**  
My off-peak rate is £0.067/kWh:  

***4.25 kWh × £0.067 ≈ £0.29 to refill the portion of the battery used during the export event.***

Even after accounting for battery wear, the return is excellent and provides a return on the capital spent on the inverter and battery setup that I had not anticipated.

**Guaranteed minimum:**  
Axle also guarantees at least £10 per month in payouts ***until the end of March 2026***, even in months with few grid events.

---

## Control Options: Event Mode vs Full Control

Axle offers two modes:

### Full Control

For users who prefer automation instead of DIY tinkering:

- Axle automatically schedules pre-charging before grid events  
- Ensures the battery has enough stored energy to maximise earnings  
- Handles all inverter settings for you  

### Events-Only (my choice)

For home automation enthusiasts:

- You keep full control of your battery day-to-day  
- Axle only controls the inverter during the event window  
- Axle provides an API endpoint with event start/end times, which Home Assistant users can integrate into their automations for:  
  - Pre-charging  
  - Adjusting behaviour during the event  
  - Logging and statistics  

Axle works independently of your electricity supplier and tariff.

---

## Overall Impression

My first Axle event was:

- Seamless  
- Fully automatic  
- Financially worthwhile  
- Non-intrusive  
- Quickly settled  

For me, it’s an ideal balance: an effortless extra income stream that slots neatly into my existing Home Assistant setup.  

***One area still unclear is how frequent grid events are. We have requested from Axle some insight into the last two or three months of events to get a better feel for the typical frequency.***

---

## How to Join Axle and Take Part in Paid Export Events

The sign-up process is straightforward:

1. **Create your account**  
   Use this link to receive £25 credit instantly:  
   [https://vpp.axle.energy/landing?ref=R-JQDOUROD](https://vpp.axle.energy/landing?ref=R-JQDOUROD)  

   *(I also receive £25, which helps me maintain the Home Assistant Axle integration.)*

2. **Upload a recent electricity bill**  
   This allows Axle to retrieve your MPAN and meter details.

3. **Provide inverter login information**  
   So Axle can control charging and exporting during events.

4. **Add your tariff details**  
   This lets them optimise your participation effectively.

After that, you’re ready for your first grid event.




