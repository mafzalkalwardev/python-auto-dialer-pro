<div align="center">

# 📞 Python Auto Dialer Pro

**PyQt desktop auto dialer with Excel contacts and PyAutoGUI automation.**

Excel import · Hotkeys · CSV logs · Resume support

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

</div>

---

## 🐍 Contribution graph

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mafzalkalwardev/python-auto-dialer-pro/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/mafzalkalwardev/python-auto-dialer-pro/output/snake.svg" />
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/mafzalkalwardev/python-auto-dialer-pro/output/snake.svg" />
</picture>

---

\# Python Auto Dialer Pro

A Python GUI-based auto dialer system built with Tkinter and PyAutoGUI for automating outbound calls using Excel contact lists.

The application supports automatic dialing, call logging, resume functionality, keyboard shortcuts, progress tracking, and desktop automation workflows.

\## Screenshots

## Features

\- GUI-based auto dialer

\- Excel contact loading

\- Automated outbound calling

\- Call logging system

\- Resume unfinished calls

\- Keyboard shortcuts

\- Progress tracking

\- Call timer

\- Multi-threading support

\- Desktop automation using PyAutoGUI

\## Tech Stack

\- Python

\- Tkinter

\- Pandas

\- PyAutoGUI

\- Pynput

\- CSV Logging

\## Project Structure

```text

python-auto-dialer-pro/

│

├── auto\_dialer.py

├── call\_logs.csv

├── README.md

└── .gitignore

```

\## Installation

Install required packages:

```bash

pip install pandas pyautogui pynput openpyxl

```

\## How to Run

```bash

python auto\_dialer.py

```

\## Features Overview

\### Excel Contact Loading

Loads phone numbers automatically from Excel spreadsheets.

\### Auto Dialing

Automates:

\- number input

\- call button clicking

\- call ending

\### Resume System

Skips already completed calls using log history.

\### Keyboard Shortcuts

| Key | Action |

|----|----|

| SPACE | Pause/Resume |

| X | End current call and move next |

\### Logging System

All calls are stored inside:

```text

call\_logs.csv

```

\## Use Cases

\- Call center automation

\- Lead calling

\- CRM workflows

\- Sales outreach

\- Dispatch operations

\## Security Note

Do not upload private contact lists publicly.

\## Author

Muhammad Afzal Kalwar

GitHub:

@mafzalkalwardev
