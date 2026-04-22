# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Core Persona
- **Objective**: Strictly direct, objective, and factual. No conversational filler.
- **No Sugarcoating**: State answers immediately. Do not soften bad news.
- **Directness**: Prioritize conciseness. Start yes/no questions with "Yes" or "No".
- **No Sycophancy**: Correct misconceptions directly. Do not compliment questions.
- **Tone**: Professional, clinical, efficient.

# Project Overview
Hybrid hardware/software industrial lighting controller based on ESP32-S3-MINI-1-N8 (dual-core Xtensa LX7, 8 MB flash). Receives DMX-512 (RS-485) and Art-Net/sACN (WiFi), drives WS2812B addressable LEDs and 3× RGB PWM outputs. 24V DC input only.

# Documentation Build

```bash
cd documentation/Latex
pdflatex -shell-escape -interaction=nonstopmode main.tex
```

Output: `documentation/Latex/main.pdf` (Design Reference Manual). For LaTeX editing rules, see `documentation/Latex/CLAUDE.md`.

# Firmware Style (Google C++ Style Guide)

## Naming Conventions
| Construct | Convention | Example |
|-----------|------------|---------|
| Classes/structs | `PascalCase` | `LightingConfig` |
| Functions | `ModuleName_ObjectVerb` | `EventManager_EventPost` |
| Variables | `snake_case` | `dmx_address` |
| Constants | `kCamelCase` | `kMaxChannels` |
| Macros | `UPPER_SNAKE_CASE` | `DMX_FRAME_SIZE` |

`ModuleName_ObjectVerb` is an intentional **deviation** from Google Style — use it consistently.

## Code Rules
- Headers: `#pragma once`. Include order: system → Arduino/ESP-IDF → project.
- Fixed-width types only (`uint8_t`, `uint32_t`). No plain `int` for hardware registers.
- No exceptions, no RTTI — `dynamic_cast` and `try/catch` are disabled on the target.
- Prefer stack allocation. No `new`/`delete` in ISRs or tight loops.
- ISRs: `IRAM_ATTR` required. No heap, no blocking calls, no `Serial` prints.
- No `delay()`. Use FreeRTOS tasks, timers, or state machines.
- Centralize GPIO pin assignments and tunable parameters in `config.h`.

# Firmware Architecture

The full specification lives in `documentation/Latex/sections/software_architecture.tex`. Summary:

## Dual-Core Task Partitioning (FreeRTOS)
| Core | Tasks | Constraint |
|------|-------|------------|
| **Core 0** | WiFi stack, Art-Net UDP parser, DMX-512 UART receiver, LED RMT output | No blocking calls; deterministic latency required |
| **Core 1** | Event Manager, Timer Manager, Rotary encoder, Menu engine, OLED display, NVS storage | Tolerates scheduler jitter |

WiFi **must** run on Core 0 — this is an ESP-IDF hard constraint.

## Key Modules

**Event Manager** (Core 1): Ring-buffer FIFO. Sources: rotary encoder ISR, button debounce, Timer Manager. Decouples ISR event generation from menu FSM processing.

**Timer Manager** (Core 1): Static array of timer entries polled each loop against `millis()`. On expiry, pushes an `event_id_t` into the Event Manager ring buffer. Supports periodic (animation cycles) and one-shot (display standby) modes.

**Menu Engine** (Core 1): Tree-based, data-driven UI. Zero dynamic allocation — all nodes in flash as `const` arrays. Node types: `SUBMENU`, `ACTION`, `EDIT_UINT16`, `BACK`. Nodes hold direct pointers to global variables for in-place editing.

**NVS Flash Storage** (Core 1): Persists `lighting_config_t`. Uses CRC validation; falls back to factory defaults on CRC failure. Save triggered by rotary button double-click.

**Shared Config**: `lighting_config_t` struct (mode, DMX address, Art-Net universe) shared between cores via `portMUX_TYPE` spinlock. Both cores hold the lock only for the duration of a struct copy — minimize critical section length.

## LED Output (SYS-009 — Hard Real-Time)
WS2812B timing is deterministic. The RMT peripheral on Core 0 generates the bitstream. UI/network activity on Core 1 must never introduce jitter into LED frame output.

## Protocol Input
Art-Net and sACN both write to a shared double-buffered universe store. Firmware arbitrates which source (DMX-512 or network) controls the output. sACN (ANSI E1.31) is optional (SYS-014).
