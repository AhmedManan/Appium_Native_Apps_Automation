# 📱 Android Dialer App — Appium Automation (Python + Pytest + POM)

Native Android Dialer App এর UI automation framework।  
**Stack:** Python · Appium 2.x · pytest · Page Object Model

---

## 🗂️ প্রজেক্ট স্ট্রাকচার

```
dialer_app/
├── config/
│   └── config.py              # Appium capabilities ও timeout settings
├── pages/
│   ├── base_page.py           # সব page এর parent — common methods
│   ├── dialer_page.py         # Keypad screen — নম্বর ডায়াল করা
│   ├── call_log_page.py       # Recent/Missed calls তালিকা
│   └── contacts_page.py       # Contact দেখা, যোগ করা, খোঁজা
├── tests/
│   ├── conftest.py            # pytest fixtures (driver setup/teardown)
│   ├── test_dialer.py         # Keypad সম্পর্কিত tests (TC-001–008)
│   ├── test_call_log.py       # Call log সম্পর্কিত tests (TC-101–106)
│   └── test_contacts.py       # Contacts সম্পর্কিত tests (TC-201–206)
├── utils/
│   └── driver_factory.py      # Appium driver তৈরি ও destroy করে
├── reports/                   # Screenshots ও HTML report এখানে যায়
├── pytest.ini                 # pytest configuration
└── requirements.txt           # Python dependencies
```

---

## ✅ Test Cases

| ID       | Module     | বিবরণ                                     |
|----------|------------|------------------------------------------|
| TC-001   | Dialer     | Dial pad সফলভাবে খোলে                    |
| TC-002   | Dialer     | Keypad এ phone number enter হয়           |
| TC-003   | Dialer     | Delete button শেষ digit মুছে             |
| TC-004   | Dialer     | Long-press delete সব clear করে           |
| TC-005   | Dialer     | বিভিন্ন নম্বর ও USSD code (parametrized) |
| TC-006   | Dialer     | Call button নম্বর দেওয়ার পর visible      |
| TC-007   | Dialer     | Star (*) ও Hash (#) key কাজ করে          |
| TC-008   | Dialer     | শুরুতে input ফাঁকা থাকে                  |
| TC-101   | Call Log   | Recents tab navigate                      |
| TC-102   | Call Log   | Entries বা empty state দেখায়             |
| TC-103   | Call Log   | Count positive (call থাকলে)               |
| TC-104   | Call Log   | Missed calls filter                       |
| TC-105   | Call Log   | ALL ↔ MISSED tab switch                   |
| TC-106   | Call Log   | First entry tap                           |
| TC-201   | Contacts   | Contacts tab navigate                     |
| TC-202   | Contacts   | নতুন contact যোগ                          |
| TC-203   | Contacts   | বিদ্যমান contact সার্চ                   |
| TC-204   | Contacts   | না থাকা contact সার্চ → empty             |
| TC-205   | Contacts   | Contact যোগে count বাড়ে                  |
| TC-206   | Contacts   | বিভিন্ন নামে contact যোগ (parametrized) |

---

## ⚙️ সেটআপ (Setup)

### 1. প্রয়োজনীয় সফ্টওয়্যার

```bash
# Node.js ও Appium ইনস্টল
npm install -g appium
appium driver install uiautomator2

# Python dependencies
pip install -r requirements.txt
```

### 2. ডিভাইস সংযোগ

```bash
# Emulator চালু করুন অথবা Real Device USB দিয়ে লাগান
adb devices        # device ID দেখুন
```

### 3. Config আপডেট করুন

`config/config.py` খুলে আপনার device অনুযায়ী পরিবর্তন করুন:

```python
ANDROID_CAPABILITIES = {
    "deviceName":      "emulator-5554",  # ← আপনার device ID
    "platformVersion": "11.0",           # ← আপনার Android version
    ...
}
```

---

## ▶️ Tests চালানো

```bash
# Appium server চালু করুন (আলাদা terminal)
appium

# সব tests
pytest

# শুধু dialer tests
pytest tests/test_dialer.py -v

# শুধু call log tests
pytest tests/test_call_log.py -v

# শুধু contacts tests
pytest tests/test_contacts.py -v

# নির্দিষ্ট test
pytest tests/test_dialer.py::TestDialer::test_enter_phone_number_on_keypad -v

# HTML report সহ
pytest --html=reports/report.html --self-contained-html
```

---

## 🔍 Locator Inspector

Appium Inspector ব্যবহার করে locator খুঁজুন:

```
Appium Server URL:  http://127.0.0.1:4723
App Package:        com.android.dialer
App Activity:       .app.DialtactsActivity
```

> ⚠️ **Note:** Samsung/OnePlus/Xiaomi custom ROM এ package name ভিন্ন হতে পারে।  
> `adb shell dumpsys window | grep mCurrentFocus` দিয়ে বর্তমান package/activity দেখুন।

---

## 🏗️ Page Object Model (POM) ব্যাখ্যা

```
Test (test_dialer.py)
    │
    ▼
Page Object (dialer_page.py)   ← locator + action encapsulated
    │
    ▼
Base Page (base_page.py)       ← common find/click/wait methods
    │
    ▼
Appium Driver (driver_factory.py) ← WebDriver instance
```

- **Test file** শুধু **কী** test করবে তা বলে
- **Page Object** শুধু **কীভাবে** interact করবে তা জানে
- Locator change হলে শুধু Page Object বদলাতে হয়
