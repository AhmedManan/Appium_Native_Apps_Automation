# Appium Native Apps Automation Test (Android)

An advanced automation testing framework for Android Native Applications (e.g., Dialer, Settings, Camera, File Manager, Calendar, and more) using **Appium**, **Python**, and **Pytest**. 

This repository serves as a centralized hub for mastering and implementing robust end-to-end (E2E) automation scripts for built-in Android system applications using the **Page Object Model (POM)** design pattern.

---

## 🚀 Project Overview

Testing native system apps requires handling diverse UI components, dynamic resource IDs, device-specific permissions, and deep system interactions. This project aims to build a scalable, maintainable, and robust automation suite that covers critical functional scenarios across various default Android applications.

### 📱 Target Applications
* **Dialer / Contacts:** Call automation, contact creation, and history validation.
* **Settings:** Wi-Fi/Bluetooth toggles, display adjustments, and app permission management.
* **Camera:** Capturing photos/videos, toggling modes, and flash settings.
* **File Manager:** Directory navigation, file creation, moving, and deletion.
* **Calendar:** Event creation, reminders, and date/view transitions.
* *...and other core Android system applications.*

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.x
* **Automation Tool:** Appium Server & Appium Python Client
* **Test Framework:** Pytest
* **Design Pattern:** Page Object Model (POM)
* **Reporting:** Allure Reports (or Pytest-HTML)
* **CI/CD Ready:** GitHub Actions integration

---

## 📁 Repository Structure

```text
├── config/
│   └── capabilities.py     # Desired capabilities configurations
├── pages/
│   ├── base_page.py        # Common wrapper methods (click, scroll, explicit waits)
│   ├── dialer_page.py      # Page objects for Dialer App
│   └── settings_page.py    # Page objects for Settings App
├── tests/
│   ├── conftest.py         # Pytest fixtures for driver initialization/teardown
│   ├── test_dialer.py      # Test cases for Dialer App
│   └── test_settings.py    # Test cases for Settings App
├── utils/
│   └── logger.py           # Custom logging utilities
├── requirements.txt        # Python dependencies
└── README.md
