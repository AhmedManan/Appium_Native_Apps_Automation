"""
Appium Configuration - Android Dialer App
"""

APPIUM_SERVER_URL = "http://localhost:4723"

ANDROID_CAPABILITIES = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "acb2cc1e",       # device name (adb devices)
    # "platformVersion": "11.0",           # Android version
    "appPackage": "com.android.dialer",  # Stock Android dialer
    "appActivity": ".app.DialtactsActivity",
    "noReset": True,
    "fullReset": False,
    "newCommandTimeout": 60,
    "autoGrantPermissions": True,
    "skipUnlock": True,
    "uiautomator2ServerLaunchTimeout": 60000,
}

# Timeouts (seconds)
EXPLICIT_WAIT   = 15
IMPLICIT_WAIT   = 10
PAGE_LOAD_WAIT  = 20
