# Coin Changer — Components & Lazada Shopping List

> **Project:** Coin Changer (Vendo Machine Bill/Coin Acceptor + Dispenser)
> **Last Updated:** July 2026
> **Author:** sajed Mendoza
> **All links verified working as of:** July 2026

---

## Shopping List

| # | Component | Qty | Unit Price | Subtotal | ⭐ Rating | Lazada Link |
|---|-----------|:---:|:----------:|:--------:|:---------:|-------------|
| 1 | **ESP32 38-pin Dev Board** (Type C, CP2102) | 2 | ₱385 | **₱770** | ⭐4.9 (142) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4449712984-s25235315582.html) |
| 2 | **16×2 I2C LCD Module** (PCF8574 backpack) | 1 | ₱57 | **₱57** | ⭐4.95 (100) | [Buy Here](https://www.lazada.com.ph/products/pdp-i3308136855-s17624526933.html) |
| 3 | **MPU6050 GY-521** (6-axis gyro + accelerometer) | 1 | ₱118 | **₱118** | ⭐5.0 (13) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4888126305-s28447887072.html) |
| 4 | **TOP TB74 Bill Acceptor** (bill validator) | 1 | ₱3,000 | **₱3,000** | ⭐5.0 (8) | [Buy Here](https://www.lazada.com.ph/products/pdp-i5309596401-s31663475796.html) |
| 5 | **ALLAN Universal Coin Slot 1238/1238A** | 1 | ₱550 | **₱550** | ⭐4.92 (811) | [Buy Here](https://www.lazada.com.ph/products/pdp-i1713218179-s7401620412.html) |
| 6 | **ALLAN Coin Hopper** (for dispensing) | 1 | ₱1,300 | **₱1,300** | ⭐4.66 (83) | [Buy Here](https://www.lazada.com.ph/products/pdp-i535822240-s24290004550.html) |
| 7 | **LM2596S Buck Converter** (12V → 5V) | 1 | ₱35 | **₱35** | ⭐4.87 (47) | [Buy Here](https://www.lazada.com.ph/products/pdp-i3761886653-s19926607155.html) |
| 8 | **12V 5A SMPS PSU** (ALLAN centralized) | 1 | ₱195 | **₱195** | ⭐4.92 (100) | [Buy Here](https://www.lazada.com.ph/products/pdp-i2298938223-s10430420525.html) |
| 9 | **Active Buzzer 5V** (2pcs, PowerMav) | 1 | ₱32 | **₱32** | ⭐5.0 (13) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4262918143-s23830169369.html) |
| 10 | **SSR-25DA Solid State Relay** (25A, 3-32VDC control) | 1 | ₱200 | **₱200** | ⭐4.96 (93) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4409263181-s24806163371.html) |
| 11 | **Tactile Push Buttons 12×12×7.3mm** (20pcs) | 1 | ₱103 | **₱103** | ⭐5.0 (10) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4606620692-s26454280448.html) |
| 12 | **1kΩ Resistor** (20pcs, PowerMav, 1/4W) | 1 | ₱24 | **₱24** | ⭐4.91 (263) | [Buy Here](https://www.lazada.com.ph/products/pdp-i268787131-s382101641.html) |
| 13 | **Jumper Wires Dupont** (40pin M-M + M-F + F-F) | 1 | ₱25 | **₱25** | ⭐5.0 (352) | [Buy Here](https://www.lazada.com.ph/products/pdp-i4888130155-s28447850086.html) |
| 14 | **Breadboard 830 points** (MB-102, Makerlab) | 1 | ₱29 | **₱29** | ⭐4.94 (1.9K) | [Buy Here](https://www.lazada.com.ph/products/pdp-i8845741-s10900196504.html) |

---

## Estimated Total

| Item | Amount |
|------|:------:|
| **Components Subtotal** | **₱6,438** |
| Most items free shipping | ± ₱0 |
| **Estimated Grand Total** | **~₱5,900** |

---

## Alternative / Backup Options

| Component | Option | Price | ⭐ | Link |
|-----------|--------|:-----:|:-:|------|
| **TB74** (cheaper, pulse protocol) | TOP TB74 Pulse | ₱1,950 | ⭐4.9 (41) | [View on Lazada](https://www.lazada.com.ph/catalog/?q=Bill+Acceptor+Top+TB74+Pulse+protocol) |
| **SSR-25DA** (local, faster shipping) | Parañaque store | ₱188 | — | [View on Lazada](https://www.lazada.com.ph/catalog/?q=SSR+25DA+solid+state+relay+module+single+phase) |
| **Resistor Kit** (assorted values) | Circuitrocks Kit | ₱75 | ⭐4.91 (32) | [View on Lazada](https://www.lazada.com.ph/products/pdp-i268787131-s382101641.html) |
| **LM2596S** (extra spare) | Second unit as backup | ₱35 | ⭐4.87 (47) | Same link as above |
| **ALLAN Bill Acceptor** (full setup) | Allan brand | ₱3,500 | ⭐5.0 (6) | [View on Lazada](https://www.lazada.com.ph/products/pdp-i2298938223-s10430420525.html) |

---

## Store Directory

| Store | Location | Items to Buy |
|-------|----------|-------------|
| **Makerlab** | Bulacan | ESP32 (×2), Breadboard |
| **PowerMav Electronics** | Bulacan | Buzzer, Resistors, LM2596S |
| **ALLAN Official** | Manila | Coin Slot, Coin Hopper, 12V PSU |
| **TOP Bill Acceptor** | Manila | TB74 Bill Acceptor |
| **—** | Valenzuela | MPU6050, Jumper Wires |
| **—** | Parañaque | SSR (alt), Resistor Kit (alt) |

---

## Wiring Reference (Quick GPIO Lookup)

### ESP32 #1 — Main Controller

| GPIO Pin | Component | Function |
|:--------:|-----------|----------|
| VIN | LM2596S OUT+ (shared with ESP32 #2) | 5V Power In |
| 3.3V | MPU6050 VCC | 3.3V Out (MPU6050 only) |
| GND | LM2596S OUT− (shared with ESP32 #2) | System ground |
| GPIO22 | LCD SDA + MPU6050 SDA | I²C Data (shared bus) |
| GPIO21 | LCD SCL + MPU6050 SCL | I²C Clock (shared bus) |
| GPIO19 | Button 1 Signal | Active LOW (INPUT_PULLUP) |
| GPIO18 | Button 2 Signal | Active LOW (INPUT_PULLUP) |
| GPIO32 | TB74 — Green Wire | Bill validation signal |
| GPIO23 | TB74 — Blue Wire | Bill pulse/data |
| GPIO26 | Coin Slot — Signal | Coin pulse input |
| GPIO27 | Coin Slot — Set | Coin slot config |

### ESP32 #2 — Dispenser Controller

| GPIO Pin | Component | Function |
|:--------:|-----------|----------|
| VIN | LM2596S OUT+ (shared with ESP32 #1) | 5V Power In |
| GND | LM2596S OUT− (shared with ESP32 #1) | System ground |
| GPIO5 | Buzzer (+) | Active HIGH = beep |
| TBD | SSR Control (+) | Hopper switch (verify SSR specs) |
| GND | SSR Control (−) | Control ground |

---

> **See [WIRING_GUIDE.md](./WIRING_GUIDE.md) for the full detailed wiring instructions and safety warnings.**
