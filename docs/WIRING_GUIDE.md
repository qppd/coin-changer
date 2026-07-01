# Coin Changer — Complete Wiring Guide

> **Project:** Coin Changer (Vendo Machine Bill/Coin Acceptor + Dispenser)
> **Document Version:** 1.0
> **Last Updated:** July 2026
> **Author:** sajed Mendoza

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Hardware List](#2-hardware-list)
3. [Electrical Safety Warnings](#3-electrical-safety-warnings)
4. [Power Distribution](#4-power-distribution)
5. [ESP32 #1 — Main Controller](#5-esp32-1--main-controller)
   - 5.1 [GPIO Allocation Table](#51-gpio-allocation-table)
   - 5.2 [16×2 I2C LCD](#52-16x2-i2c-lcd)
   - 5.3 [MPU6050 (Accelerometer/Gyroscope)](#53-mpu6050)
   - 5.4 [Shared I2C Bus Notes](#54-shared-i2c-bus-notes)
   - 5.5 [Tactile Buttons (×2)](#55-tactile-buttons-x2)
   - 5.6 [TB74 Bill Acceptor](#56-tb74-bill-acceptor)
   - 5.7 [Allan Coin Slot](#57-allan-coin-slot)
6. [ESP32 #2 — Dispenser Controller](#6-esp32-2--dispenser-controller)
   - 6.1 [GPIO Allocation Table](#61-gpio-allocation-table)
   - 6.2 [Buzzer](#62-buzzer)
   - 6.3 [Solid State Relay (SSR) + Allan Coin Hopper](#63-solid-state-relay-ssr--allan-coin-hopper)
7. [Power Supply Detail](#7-power-supply-detail)
8. [Complete Wiring Verification Checklist](#8-complete-wiring-verification-checklist)
9. [Common Troubleshooting](#9-common-troubleshooting)
10. [Future Expansion Notes](#10-future-expansion-notes)

---

## 1. Project Overview

This project uses **two ESP32 38-pin development boards** to control a coin-operated vending machine:

- **ESP32 #1 (Main Controller)** — Handles user interaction: LCD display, bill/coin acceptance, motion/impact sensing, and button input.
- **ESP32 #2 (Dispenser Controller)** — Controls the physical dispensing output: buzzer alerts, relay-controlled hopper payout.

The two ESP32 boards communicate over serial or GPIO handshake (determined by firmware implementation — not covered in this wiring guide).

### ASCII System Block Diagram

```
                    ┌──────────────────────────────────┐
                    │           220 VAC                 │
                    └────────────┬─────────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │     12V PSU (SMPS)       │
                    │   (Converts 220V → 12V)  │
                    └────────┬──────────┬──────┘
                             │          │
                    ┌────────▼───────────┐
                    │    LM2596S         │
                    │   (Set to 5.0V)    │
                    └────────┬───────────┘
                             │
                    ┌────────┴───────────┐
                    │   5V Rail ─────────┤
                    │ (shared by both    │
                    │  ESP32s + LCD)     │
                    └────────┬───────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
          ┌────▼────┐  ┌────▼──────┐      │
          │ ESP32   │  │ ESP32     │      │
          │ #1 Main │  │ #2 Disp.  │      │
          └────┬────┘  └────┬──────┘      │
               │            │             │
     ┌─────────┼────────┐  │    ┌────────┼────────┐
     │ LCD     │ MPU6050│  │    │ Buzzer │ SSR ───┤
     │ Buttons │Bill Acc│  │    │→Hopper │        │
     │Coin Slot│        │  │    │        │        │
     └─────────┴────────┘  │    └────────┴────────┘
```

---

## 2. Hardware List

| # | Component | Qty | Purpose | Connected To |
|---|-----------|:---:|---------|-------------|
| 1 | ESP32 38-pin Dev Board | 2 | Main + Dispenser controllers | Peripherals below |
| 2 | 16×2 I2C LCD (PCF8574) | 1 | Display user messages | ESP32 #1 (I2C) |
| 3 | MPU6050 (GY-521) | 1 | Vibration / tilt detection | ESP32 #1 (I2C) |
| 4 | Tactile Push Button | 2 | User input (menu/confirm) | ESP32 #1 (GPIO) |
| 5 | 1kΩ Resistor | 2 | Button pull-down current limit | Button → GND |
| 6 | TB74 Bill Acceptor | 1 | Accepts paper bills | ESP32 #1 + 12V PSU |
| 7 | Allan Coin Slot | 1 | Accepts coins | ESP32 #1 + 12V PSU |
| 8 | Active Buzzer (5V) | 1 | Audible alerts | ESP32 #2 (GPIO) |
| 9 | Solid State Relay (SSR) | 1 | Switches 220VAC to hopper | ESP32 #2 (control) + 220VAC |
| 10 | Allan Coin Hopper | 1 | Dispenses coins | SSR + 220VAC |
| 11 | 12V SMPS PSU | 1 | System power supply | 220VAC → 12V |
|| 12 | LM2596S Buck Converter | 1 | 12V → 5V for both ESP32s | PSU → Both ESP32 VIN (parallel) |
| — | Jumper wires, screw terminals, heat shrink | — | Interconnections | — |

---

## 3. ⚠️ Electrical Safety Warnings

**This project involves 220 VAC mains voltage. Improper wiring can cause electrocution, fire, or equipment damage.**

1. **DISCONNECT ALL POWER** before making or modifying any connections.
2. The **220 VAC circuit** (PSU input, SSR output to hopper) must be treated as **LETHAL** — do not touch bare wires while the system is plugged in.
3. Use appropriately rated wire (at least 1.0 mm² / 18 AWG for AC power, 0.5 mm² / 22 AWG for signal wires).
4. Secure all AC connections with screw terminals or wire nuts — **no loose splices**.
5. The 12V PSU and LM2596S modules must be mounted in a ventilated, dry enclosure.
6. Use a **fuse on the 220VAC line** (e.g., 5A fuse in series with the Line wire before the PSU).
7. Ensure the enclosure is earthed/grounded if metal.
8. Double-check all polarities before applying power — reversed polarity on LM2596S input can destroy the module.

> **I AM NOT A LICENSED ELECTRICIAN. CONSULT A QUALIFIED ELECTRICIAN IF YOU ARE UNSURE ABOUT MAINS WIRING.**

---

## 4. Power Distribution

### 4.1 Overview

```
220 VAC Mains
    │
    ├─── Line (L) ──► [Fuse 5A] ──► PSU L Terminal
    │                                  │
    └─── Neutral (N) ──────────────► PSU N Terminal
                                       │
                               PSU PE / Earth ═══► Chassis Ground
                                       │
                                  ┌────┴────┐
                                  │  12V DC │
                                  │  Output │
                                  └──┬──────┘
                                     │
                    ┌────────────────┼─────────────────┐
                    │                │                  │
           ┌────────▼───────────┐
           │    LM2596S          │
           │  (Set ▼ to 5.0V)   │
           └────────┬───────────┘
                    │
           ┌────────┴───────────┐
           │  5V Rail (shared)  │
           │  ───────────────── │
           │  ESP32 #1 VIN      │
           │  ESP32 #2 VIN      │
           │  LCD VCC           │
           └────────┬───────────┘
                    │
           ┌────────┴────────────┐
           │  12V Peripherals    │
           │  ──────────────     │
           │  TB74 (Red)         │
           │  Allan Coin Slot    │
           │  (+12V wire)        │
           └─────────────────────┘
```

### 4.2 LM2596S Buck Converter — Wiring (Single Module, Both ESP32s)

| LM2596S Terminal | Connection |
|:----------------:|------------|
| **IN+**          | PSU +12V Output |
| **IN−**          | PSU GND Output |
| **OUT+**         | ESP32 #1 **VIN** + ESP32 #2 **VIN** (wired in parallel) |
| **OUT−**         | ESP32 #1 **GND** + ESP32 #2 **GND** (wired in parallel) |

> Both ESP32s share the same 5V rail from one LM2596S. The LM2596S is rated for 3A — enough to power both boards (each ~200mA peak) plus the LCD (~50mA) with plenty of headroom.
>
> **Adjustment:** Before connecting to the ESP32s, power the LM2596S from the 12V PSU (no load on output) and adjust its trimmer potentiometer so the output measures **exactly 5.0V** between OUT+ and OUT−. Using a multimeter here is critical — too high a voltage can damage both ESP32s.

### 4.3 Power Connections Summary

| Component | Voltage Source | Notes |
|-----------|:-------------:|-------|
| ESP32 #1 VIN | LM2596S OUT | 5V regulated (shared rail) |
| ESP32 #2 VIN | LM2596S OUT | 5V regulated (same rail as #1) |
| LCD VCC | ESP32 #1 VIN | 5V (pulled from board VIN) |
| MPU6050 VCC | ESP32 #1 3.3V | 3.3V only! |
| TB74 Red Wire | PSU +12V | Direct from 12V PSU output |
| Allan Coin Slot +12V | PSU +12V | Direct from 12V PSU output |
| Buzzer Positive | ESP32 #2 GPIO5 | Driven by GPIO (5V tolerant via GPIO) |
| SSR Control + | (TBD — see §6.3) | |
| Hopper AC | SSR Output + 220VAC | Switched by SSR |

> **Important:** The ESP32 VIN pin accepts 5V input (the on-board voltage regulator drops it to 3.3V for the ESP32 core). Do NOT feed more than 5.5V into VIN.

---

## 5. ESP32 #1 — Main Controller

### 5.1 GPIO Allocation Table

| GPIO Pin | Connected To | Direction | Notes |
|:--------:|-------------|:---------:|-------|
| **VIN**  | LM2596S OUT+ | Power IN | 5V input (shared rail with ESP32 #2) |
| **3.3V** | MPU6050 VCC | 3.3V OUT | Powers MPU6050 (do not use 5V!) |
| **GND**  | LM2596S OUT− | Power GND | System ground (shared with ESP32 #2) |
| **GND**  | All peripheral GNDs | GND | Common ground plane |
| **GPIO22** | LCD SDA + MPU6050 SDA | I²C Data | Shared bus |
| **GPIO21** | LCD SCL + MPU6050 SCL | I²C Clock | Shared bus |
| **GPIO19** | Button 1 Signal | Input w/ pull-up | Active LOW (press = GND) |
| **GPIO18** | Button 2 Signal | Input w/ pull-up | Active LOW (press = GND) |
| **GPIO32** | TB74 — Green Wire | Input | Bill acceptor validation signal |
| **GPIO23** | TB74 — Blue Wire | Input | Bill acceptor pulse output / data |
| **GPIO26** | Coin Slot — Signal | Input | Coin pulse signal |
| **GPIO27** | Coin Slot — Set | Output | Coin slot configuration/set pin |

**Unused GPIOs on ESP32 #1:** GPIO2, GPIO4, GPIO5, GPIO12–17, GPIO25, GPIO33–36, GPIO39 — available for future expansion (but note GPIO12 is a strapping pin — use with caution).

---

### 5.2 16×2 I2C LCD

The LCD uses an **I²C adapter board (PCF8574)** which reduces the interface to just 4 wires.

| LCD Adapter Pin | ESP32 #1 Pin |
|:---------------:|:------------:|
| VCC             | **VIN** (5V) |
| GND             | **GND** |
| SDA             | **GPIO22** |
| SCL             | **GPIO21** |

**Default I²C Address:** `0x27` or `0x3F` (common for PCF8574-based LCD backpacks). Run an I²C scanner sketch on first boot to confirm.

---

### 5.3 MPU6050

The MPU6050 is a 6-axis accelerometer + gyroscope. It runs on **3.3V** only.

| MPU6050 Pin | ESP32 #1 Pin |
|:-----------:|:------------:|
| VCC         | **3.3V** |
| GND         | **GND** |
| SDA         | **GPIO22** |
| SCL         | **GPIO21** |

**Default I²C Address:** `0x68` (can be changed to `0x69` by bridging the AD0 pin to VCC).

**Additional pins on GY-521 module (not used in this build):**
- **AD0** — I²C address select (leave open for 0x68)
- **INT** — Interrupt output (unused, can connect to any free GPIO for motion-triggered interrupts)
- **XDA / XCL** — Auxiliary I²C bus (unused)

---

### 5.4 Shared I²C Bus Notes

Both the **LCD** and **MPU6050** share the same I²C bus (GPIO22 = SDA, GPIO21 = SCL).

| Detail | Value |
|--------|-------|
| Bus Type | I²C |
| SDA | GPIO22 |
| SCL | GPIO21 |
| LCD Address | `0x27` or `0x3F` |
| MPU6050 Address | `0x68` (or `0x69` if AD0 bridged) |
| Pull-up resistors | Built-in on most breakout boards + ESP32 internal |
| Bus voltage | 3.3V (ESP32 native) |

**Considerations:**
- The LCD operates at 5V but its I²C lines are pulled to 5V. The ESP32 GPIOs are **5V tolerant**, so this works without a level shifter. The MPU6050 runs at 3.3V and uses the same 3.3V I²C bus. Because the two devices sit at different voltage domains on the same bus, verify reliable communication — if glitches occur, add an I²C level shifter (e.g., BSS138) between the LCD's SDA/SCL and ESP32.
- Run an **I²C scanner** at startup to confirm both devices respond on their expected addresses.
- I²C bus maximum cable length should be kept under ~50 cm. Longer runs may require lower pull-up resistor values (e.g., 4.7kΩ).

**ASCII I²C Bus Diagram:**

```
┌─────────────────────────────────────────────────┐
│                 ESP32 #1                        │
│                                                 │
│  GPIO21 (SCL) ───┬─────────────────────────────┐│
│                  │                             ││
│  GPIO22 (SDA) ───┼─────────────────────────┐   ││
│                  │                         │   ││
└──────────────────┼─────────────────────────┼───┘│
                   │                         │    │
              ┌────▼─────┐            ┌──────▼──────┐
              │ 16×2 LCD │            │  MPU6050    │
              │(PCF8574) │            │  (GY-521)   │
              │5V I²C    │            │3.3V I²C     │
              └──────────┘            └─────────────┘
```

---

### 5.5 Tactile Buttons (×2)

Two push buttons for user input (e.g., menu navigation / selection).

#### Wiring

```
Button 1:
  ESP32 GPIO19 ─────► Tactile Switch Pin 1
  Tactile Switch Pin 2 ───► 1kΩ Resistor ───► GND

Button 2:
  ESP32 GPIO18 ─────► Tactile Switch Pin 1
  Tactile Switch Pin 2 ───► 1kΩ Resistor ───► GND
```

#### How It Works

| State | Circuit Path | GPIO Reads |
|-------|-------------|:----------:|
| **Button released** | Circuit open (no path to GND) | **HIGH** (requires internal pull-up enabled in firmware) |
| **Button pressed** | GPIO → button contacts → 1kΩ → GND | **LOW** |

- The **1kΩ resistor** is in series between the switch and GND. Its purpose is **current limiting** — when the button is pressed, it prevents a direct short from the GPIO pin to ground, limiting the current to ~3.3 mA.
- Because the button only connects the GPIO to GND when pressed, the GPIO is **floating when unpressed**. The firmware **must enable the ESP32 internal pull-up resistor** (`pinMode(pin, INPUT_PULLUP)`) for GPIO19 and GPIO18. Without this, the pins will read random noise when the button is not pressed.

> **Alternative (if internal pull-ups are unreliable):** Connect an external 10kΩ resistor from GPIO19/GPIO18 to 3.3V as an external pull-up.

#### Pin Summary

| Button | GPIO | Other Pin | Resistor | State When Pressed |
|:------:|:----:|:---------:|:--------:|:------------------:|
| Button 1 | GPIO19 | → 1kΩ → GND | Series current limit | LOW (active LOW) |
| Button 2 | GPIO18 | → 1kΩ → GND | Series current limit | LOW (active LOW) |

---

### 5.6 TB74 Bill Acceptor

The TB74 is a bill validator with a 6-wire harness. Wire colors and functions:

> **Note:** These assignments are based on documented TB74 pinouts. If the bill acceptor behaves unexpectedly, verify each wire's function with a multimeter before the 12V PSU is connected.

| Wire Color | Connection | Purpose |
|:----------:|:----------:|---------|
| **Red**    | PSU **+12V** | **Power +12V** — Powers the bill acceptor's internal electronics |
| **Orange** | PSU **GND** | **Power Ground** — Return path for the 12V supply |
| **Green**  | ESP32 **GPIO32** | **Validation / Busy** — Goes HIGH (or LOW, depending on unit configuration) when a bill is being validated. ESP32 reads this to know if the acceptor is busy or has accepted a bill. |
| **Yellow** | PSU **GND** | **Signal Ground** — Ground reference for the signal wires |
| **Blue**   | ESP32 **GPIO23** | **Pulse / Data Output** — Each accepted bill generates a pulse train. The ESP32 counts pulses to determine the bill value (e.g., 1 pulse = ₱20, 2 pulses = ₱50, etc.). |
| **Purple** | PSU **GND** | **Inhibit / Signal Ground** — Additional ground. In some configurations, this wire is an inhibit signal (when connected to GND, the acceptor is enabled). |

> **Note on Purple wire:** If your TB74 uses the purple wire as an **inhibit** function instead of a ground, wire it to ESP32 GPIO (not PSU GND) so firmware can enable/disable the acceptor. Verify with your specific TB74 datasheet.

#### ASCII Wiring

```
      TB74 Bill Acceptor               ESP32 #1 / PSU
  ┌─────────────────────┐
  │  Red    ────────────┼─────────────────► PSU +12V
  │  Orange ────────────┼─────────────────► PSU GND
  │  Green  ────────────┼─────────────────► GPIO32
  │  Yellow ────────────┼─────────────────► PSU GND
  │  Blue   ────────────┼─────────────────► GPIO23
  │  Purple ────────────┼─────────────────► PSU GND   (or GPIO if inhibit)
  └─────────────────────┘
```

---

### 5.7 Allan Coin Slot

The Allan Coin Slot accepts coins and signals the ESP32 when a coin is deposited. It also has a "Set" line for configuration.

| Wire / Terminal | Connection | Purpose |
|:---------------:|:----------:|---------|
| **Signal**      | ESP32 **GPIO26** | **Coin pulse output** — Each coin triggers a pulse on this line. The ESP32 counts pulses (and potentially measures pulse width) to identify coin type. |
| **Set**         | ESP32 **GPIO27** | **Configuration/Setting** — When pulsed or held high/low (depending on model), enters a configuration mode (e.g., assigning coin types to pulse counts). Not used during normal operation but required for initial setup. |
| **GND (×2)**    | PSU **GND** | **Ground** — Two ground wires for redundancy / separate return paths. Connect both to PSU GND. |
| **+12V**        | PSU **+12V** | **Power** — 12V DC input to the coin slot's internal circuitry. |

> **Note on coin pulse detection:** In firmware, attach an interrupt to GPIO26. Most coin slots generate a brief LOW pulse (50–200ms) when a coin is accepted. The number of pulses or the pulse duration distinguishes coin denominations. Configure this with the "Set" pin during initial calibration.

#### ASCII Wiring

```
   Allan Coin Slot                ESP32 #1 / PSU
  ┌────────────────────┐
  │  Signal ───────────┼─────────────────► GPIO26
  │  Set    ───────────┼─────────────────► GPIO27
  │  GND #1 ───────────┼─────────────────► PSU GND
  │  GND #2 ───────────┼─────────────────► PSU GND
  │  +12V   ───────────┼─────────────────► PSU +12V
  └────────────────────┘
```

---

## 6. ESP32 #2 — Dispenser Controller

### 6.1 GPIO Allocation Table

| GPIO Pin | Connected To | Direction | Notes |
|:--------:|-------------|:---------:|-------|
| **VIN**  | LM2596S OUT+ | Power IN | 5V input (shared rail with ESP32 #1) |
| **GND**  | LM2596S OUT− | Power GND | System ground (shared with ESP32 #1) |
| **GPIO5** | Buzzer (+) | Output | Active HIGH to sound buzzer |
| **TBD**   | SSR Control (+) | Output | **See §6.3 — TO BE VERIFIED** |
| **GND**   | SSR Control (−) | GND | SSR control ground (share ESP32 GND) |
| — | — | — | Remaining GPIOs free for expansion |

**Unused GPIOs on ESP32 #2** (available for expansion): GPIO2, GPIO4, GPIO12–19, GPIO21–23, GPIO25–27, GPIO32–39.

> **Note:** ESP32 #2 has most of its GPIOs free — it has a very simple role in this design. Reserve at least two GPIOs for serial or handshake communication with ESP32 #1 if not already handled.

---

### 6.2 Buzzer

A 5V active buzzer used for audible feedback (e.g., successful payment, error alert, dispensing complete).

| Buzzer Pin | ESP32 #2 Pin |
|:----------:|:------------:|
| **Positive** (+) | **GPIO5** |
| **Negative** (−) | **GND** |

> **Firmware:** Set GPIO5 as OUTPUT. `digitalWrite(GPIO5, HIGH)` = buzzer on, `LOW` = buzzer off. Use PWM or `tone()` for variable-frequency buzzers (if using a passive buzzer instead of active).
>
> **Resistor:** If the buzzer draws more than 12 mA (check datasheet), add a small NPN transistor (e.g., 2N2222) or a MOSFET as a driver between GPIO5 and the buzzer. Most 5V active buzzers are self-oscillating and can be driven directly from the ESP32 GPIO.

---

### 6.3 Solid State Relay (SSR) + Allan Coin Hopper

The **Allan Coin Hopper** is a 220VAC device that dispenses coins. A **Solid State Relay (SSR)** is used to safely switch the 220VAC line to the hopper using a low-voltage signal from ESP32 #2.

#### SSR — High Side (AC Load — Hopper)

```
        220 VAC Mains
             │
        ┌────┴──────┐
        │  SSR      │
        │           │
        │  ┌─────┐  │
Line ───┼─┤ OUT1├──┼─────► Hopper Wire 1
        │  └─────┘  │
        │           │
        │  ┌─────┐  │
        │  │ OUT2├──┼─────► NOT CONNECTED (or GND side)
        │  └─────┘  │
        └─────┬─────┘
              │
       Neutral ──────────────────► Hopper Wire 2 (direct)
```

**Explanation:**

| Connection | Detail |
|------------|--------|
| **SSR Output Terminal 1** | Connected to **one wire of the Allan Coin Hopper** |
| **SSR Output Terminal 2** | Connected to **220VAC Line** |
| **Hopper's other wire** | Connected **directly to 220VAC Neutral** |

The SSR switches **one side of the AC line** (the Line / phase). When the SSR is triggered by the ESP32, it completes the circuit through the hopper:

- SSR ON → Line flows through SSR → hopper → Neutral → **hopper runs**
- SSR OFF → circuit broken → **hopper stops**

> **⚠️ Mains voltage!** The hopper and SSR output terminals carry **lethal 220VAC** when the SSR is on. Ensure all AC connections are inside an insulated enclosure with proper strain relief.
>
> **Zero-crossing SSR:** Use a zero-crossing SSR (e.g., Fotek SSR-25DA or similar) to minimize electrical noise and relay wear when switching the inductive hopper motor.

#### SSR — Control Side (Low Voltage — ESP32 #2)

> **⚠️ TO BE VERIFIED — Control Wiring Unknown**
>
> The DC control input wiring of the SSR to ESP32 #2 has **not been confirmed**. Complete this section once the SSR model and its control specifications are known.

**Typical SSR Control Wiring (for reference — VERIFY WITH YOUR SSR DATASHEET):**

| SSR Control Terminal | Typical Connection | Notes |
|:--------------------:|:------------------|-------|
| **Control (+)**      | ESP32 **GPIO ??** (TBD) | Most SSRs require **3–32 VDC** on the control input. If the SSR control current is >15mA, use a transistor driver. |
| **Control (−)**      | **ESP32 GND** | Must share ground with the ESP32 for the control circuit to work. |
| **Series Resistor**  | GPIO → 220Ω–1kΩ to control (+) | Limits current into the SSR's internal LED (optocoupler). Check your SSR datasheet for the recommended resistor value. |

> **Action Required:** Identify your SSR model and its DC control voltage/current specifications. Then choose an appropriate GPIO on ESP32 #2 and update this document.

---

## 7. Power Supply Detail

### 7.1 Power Flow

```
220 VAC ──► 12V SMPS PSU ──┬──► LM2596S ──► 5V ──┬──► ESP32 #1 VIN
                           │                      │
                           │                      └──► ESP32 #2 VIN
                           │
                           ├──► TB74 (Red wire) ── 12V ──► Bill Acceptor
                           │
                           └──► Allan Coin Slot (+12V wire) ── 12V
```

### 7.2 Voltage Requirements by Component

| Component | Voltage | Current (approx.) | Source |
|-----------|:-------:|:-----------------:|--------|
| ESP32 (each) | 5.0V (VIN) | ~200mA peak | LM2596S buck (shared 5V rail) |
| LCD (I²C) | 5.0V | ~50mA (backlit) | ESP32 VIN rail |
| MPU6050 | 3.3V | ~5mA | ESP32 3.3V pin |
| TB74 Bill Acceptor | 12V | ~200mA | PSU direct |
| Allan Coin Slot | 12V | ~150mA | PSU direct |
| Buzzer | 5V | ~30mA | ESP32 GPIO5 |
| SSR Control | 3–32V DC | ~5–20mA | ESP32 GPIO (TBD) |
| Hopper (AC) | 220 VAC | ~500mA–2A | Switched via SSR |

### 7.3 Why Only One LM2596S Module?

A single LM2596S buck converter powers both ESP32 boards. Here's why:

1. **Enough current:** The LM2596S is rated at **3A max**. Both ESP32s peak at ~200mA each + LCD at ~50mA = **~450mA total**. That's well within the module's capability.
2. **Simpler wiring:** One module means fewer connections, fewer failure points, and less clutter in the enclosure.
3. **5V rail is shared:** Both ESP32s and the LCD share the same 5V rail — their VIN and GND pins are simply wired in parallel (VIN-to-VIN, GND-to-GND).
4. **Same ground plane:** Because both boards share GND, communication between them (serial/GPIO handshake) doesn't need level shifters or isolation.

> **Note:** The two LM2596S modules you see in the shopping list (qty 2 in `components.md`) are **spares**. You only need to wire in **one** — keep the other as backup in case the first one fails.

---

## 8. Complete Wiring Verification Checklist

Use this checklist before applying power.

### Pre-Power Checks ☐

- [ ] All connections are mechanically secure (screw terminals tightened, solder joints verified)
- [ ] **No exposed 220VAC wiring** outside the enclosure
- [ ] Fuse (5A) installed on 220VAC Line before PSU
- [ ] PSU earth/ground connected to chassis (if metal enclosure)
- [ ] LM2596S output adjusted to **5.0V** (measured with multimeter, no load)
- [ ] No stray wire strands touching adjacent pins or exposed conductors
- [ ] ESP32 boards correctly oriented (not reversed or offset in headers)

### ESP32 #1 (Main Controller) Checks ☐

- [ ] LM2596S OUT+ → ESP32 #1 VIN (also spliced to ESP32 #2 VIN)
- [ ] LM2596S OUT− → ESP32 #1 GND (also spliced to ESP32 #2 GND)
- [ ] LCD VCC → VIN, GND → GND, SDA → GPIO22, SCL → GPIO21
- [ ] MPU6050 VCC → 3.3V (NOT VIN!), GND → GND
- [ ] MPU6050 SDA → GPIO22, SCL → GPIO21
- [ ] Button 1: GPIO19 → button → 1kΩ → GND
- [ ] Button 2: GPIO18 → button → 1kΩ → GND
- [ ] Internal pull-up enabled in code for GPIO18, GPIO19
- [ ] TB74 Red → PSU +12V, Orange → PSU GND, Green → GPIO32
- [ ] TB74 Yellow → PSU GND, Blue → GPIO23, Purple → PSU GND
- [ ] Coin Slot Signal → GPIO26, Set → GPIO27
- [ ] Coin Slot GND ×2 → PSU GND, +12V → PSU +12V

### ESP32 #2 (Dispenser Controller) Checks ☐

- [ ] LM2596S OUT+ → ESP32 #2 VIN (shared 5V rail with ESP32 #1)
- [ ] LM2596S OUT− → ESP32 #2 GND (shared GND with ESP32 #1)
- [ ] Buzzer (+) → GPIO5, Buzzer (−) → GND
- [ ] SSR control wiring — **CONFIRM AND UPDATE HERE**
- [ ] SSR Output Terminal 1 → Hopper Wire 1
- [ ] SSR Output Terminal 2 → 220VAC Line
- [ ] Hopper Wire 2 → 220VAC Neutral

### Power-On Sequence ☐

- [ ] 1. Do NOT plug in 220VAC yet
- [ ] 2. Measure LM2596S output voltage at ESP32 #1 VIN pin — **expect +5.0V**
- [ ] 3. Measure LM2596S output voltage at ESP32 #2 VIN pin — **expect +5.0V** (same rail)
- [ ] 4. Plug in 220VAC
- [ ] 5. Measure PSU 12V output — **expect ~12V**
- [ ] 6. Check both ESP32 boards power on (onboard LED blinks / serial output shows)
- [ ] 7. Run I²C scanner — confirm LCD and MPU6050 respond
- [ ] 8. Test buttons — serial monitor shows correct pin state changes
- [ ] 9. Test buzzer — brief tone on startup
- [ ] 10. Test bill acceptor — serial shows pulse counts when a bill is inserted
- [ ] 11. Test coin slot — serial shows pulse when coin is dropped
- [ ] 12. Test hopper — SSR triggers and hopper dispenses coins

---

## 9. Common Troubleshooting

### 9.1 ESP32 Won't Power On

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No LED, no serial | No 5V at VIN | Measure LM2596S output; adjust trimmer to 5.0V |
| Board gets hot | VIN voltage > 5.5V | Immediately disconnect; re-adjust LM2596S |
| Boot loops | Insufficient current | Check LM2596S wiring — ensure both ESP32s share the same 5V rail |

### 9.2 I²C Issues (LCD / MPU6050)

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| LCD shows nothing | Wrong I²C address | Run I²C scanner; try both 0x27 and 0x3F |
| MPU6050 not detected | Wrong I²C address or voltage | Verify VCC is 3.3V; try address 0x69 |
| Intermittent readings | Long I²C wires / noise | Keep I²C wires under 50cm; add 4.7kΩ pull-ups |
| One device drops when other is active | Bus contention on shared SDA/SCL | Add I²C level shifter for 5V LCD |

### 9.3 Buttons Not Working

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Button always reads HIGH | Internal pull-up not enabled | Add `pinMode(pin, INPUT_PULLUP)` in setup() |
| Button always reads LOW | GPIO shorted to GND | Check wiring — no unintended contact between GPIO and GND |
| Intermittent readings | Button bounce | Add 50–100ms debounce delay in firmware |
| Resistor gets hot | Short instead of 1kΩ | Verify resistor value is 1kΩ (not lower!) |

### 9.4 TB74 Bill Acceptor Not Working

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No power (no LED on acceptor) | 12V not reaching Red wire | Check PSU output and Red wire connection |
| Bills rejected instantly | Signal ground not connected | Ensure Yellow wire is connected to PSU GND |
| No pulse on GPIO23 | Purple wired as inhibit but is GND | Move Purple to a GPIO and set HIGH to enable |
| Erratic pulses | Ground loop / shared GND issues | Ensure all ground wires connect to the same PSU GND point |

### 9.5 Coin Slot Not Detecting Coins

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No signal on GPIO26 | Coin not reaching sensor | Verify coin slot mechanism is not jammed |
| Signal constantly HIGH/LOW | Pin floating or GND missing | Wire both GND wires to PSU GND |
| Multiple coins = single pulse | Debounce too long in firmware | Reduce debounce time in interrupt handler |

### 9.6 SSR / Hopper Not Working

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Hopper doesn't run | SSR not triggered | Verify GPIO control wiring and firmware state |
| Hopper runs constantly | SSR failed ON (shorted) | **IMMEDIATELY UNPLUG** — replace SSR |
| SSR clicks but hopper doesn't run | Failed AC connection | Check SSR output to hopper and Neutral connection |
| Hopper hums but doesn't turn | Jammed or failed hopper motor | Mechanically inspect hopper |

---

## 10. Future Expansion Notes

The following additions are possible without major rewiring:

### Additional Sensors

| Component | Recommended ESP32 | GPIO Suggestion | Notes |
|-----------|:-----------------:|:---------------:|-------|
| Door/Tamper switch | ESP32 #1 | GPIO4 | Input with pull-up; triggers alarm if opened |
| Temperature sensor (DHT22) | ESP32 #1 | GPIO25 | 1-wire protocol; monitor PSU / enclosure temp |
| PIR motion sensor | ESP32 #1 | GPIO33 | Detects user presence to wake LCD |
| Weight sensor (HX711 + load cell) | ESP32 #2 | GPIO16, GPIO17 | Detect if hopper is empty / coin count |

### Additional Outputs

| Component | Recommended ESP32 | GPIO Suggestion | Notes |
|-----------|:-----------------:|:---------------:|-------|
| Second hopper / dispenser | ESP32 #2 | GPIO15 + second SSR | Additional payout mechanism |
| RGB LED strip | ESP32 #1 | GPIO25 | Visual status indicators (WS2812B) |
| Relay for machine lock | ESP32 #1 | GPIO33 | Electronic lock for service access |

### Communication

- **ESP32-to-ESP32:** The two boards can communicate via **UART** (serial: TX/RX crossover), **I²C** (if addresses don't conflict), or **GPIO handshake** lines. Choose based on firmware complexity.
  - UART: Connect ESP32 #1 TX to ESP32 #2 RX, and vice versa. Use `Serial2` on both.
  - GPIO handshake: Two GPIOs per direction (request + acknowledge) — simple but slow.

### System Monitoring

- Add a **current sensor (ACS712)** on the 12V PSU output to detect when the hopper is drawing current (SSR actually triggered).
- Add a **coin level sensor** (e.g., IR break beam) inside the coin hopper to detect "low coin" condition.

---

## Document Revision History

| Date | Version | Changes |
|------|:-------:|---------|
| Jul 2026 | 1.1 | Changed to single LM2596S powering both ESP32s (parallel 5V rail) |
| Jul 2026 | 1.0 | Initial wiring guide created |

---

*End of Document — Always verify wiring with a multimeter before applying power.*
