# RLC v4 — RGB Lighting Controller

Hybrid hardware/software industrial lighting controller based on the ESP32-S3-MINI-1-N8 (dual-core Xtensa LX7, 8 MB flash).

## Goal

Design a self-contained lighting controller that accepts industry-standard control protocols and drives both addressable and analog LED outputs from a single 24 V DC supply.

## Features

- **Protocol inputs**: DMX-512 (RS-485) and Art-Net / sACN (Wi-Fi)
- **Outputs**: WS2812B addressable LEDs (via RMT) and 3× RGB PWM channels
- **UI**: Rotary encoder + OLED display with a tree-based menu
- **Storage**: NVS flash persistence with CRC validation and factory-default fallback
- **Power**: 24 V DC input only

## Repository Layout

```
PCB/          KiCad schematic and PCB layout files
documentation/
  Latex/      Design Reference Manual (LaTeX source → main.pdf)
```

## Building the Documentation

```bash
cd documentation/Latex
pdflatex -shell-escape -interaction=nonstopmode main.tex
```

Output: `documentation/Latex/main.pdf`
