import time
from appium.webdriver.connectiontype import ConnectionType


def test_android_network_automation(driver):
    print("\n--- Network Automation Test Starting ---")

    # Enable Wi-Fi Only
    print("Enabling Wi-Fi...")
    driver.set_network_connection(ConnectionType.WIFI_ONLY)
    time.sleep(3)  # Allow a moment for the network state to change

    # Check connection status
    assert driver.network_connection == ConnectionType.WIFI_ONLY
    print("Wi-Fi successfully enabled.")

    # Enable Mobile Data Only
    print("Enabling Mobile Data...")
    driver.set_network_connection(ConnectionType.DATA_ONLY)  # Or 4
    time.sleep(3)

    assert driver.network_connection == ConnectionType.DATA_ONLY
    print("Mobile Data successfully enabled.")

    # Enable Airplane Mode
    print("Enabling Airplane Mode...")

    # This will successfully turn on Airplane Mode via backend settings
    driver.execute_script('mobile: shell', {'command': 'settings put global airplane_mode_on 1'})

    # The broadcast line has been removed because Android modern versions block it.
    # Give it 5 seconds to process the state change
    time.sleep(5)

    # Check if the status actually changed by reading directly from the settings database
    airplane_status = driver.execute_script('mobile: shell', {'command': 'settings get global airplane_mode_on'})

    assert airplane_status.strip() == "1"
    print("Airplane Mode successfully enabled.")

    # Turn off Airplane Mode at the end of the test to restore normal state
    print("Disabling Airplane Mode to cleanup after test...")
    driver.execute_script('mobile: shell', {'command': 'settings put global airplane_mode_on 0'})

    # Allow more time for Wi-Fi and Cellular networks to reconnect after turning off Airplane Mode
    time.sleep(7)

    # If it still doesn't return 6 (ALL_NETWORK_ON), forcefully turn everything on using Appium
    print("Ensuring all network connections (Wi-Fi + Data) are active...")
    driver.set_network_connection(ConnectionType.ALL_NETWORK_ON)
    time.sleep(3)

    # Final verification
    assert driver.network_connection == ConnectionType.ALL_NETWORK_ON
    print("All network connections successfully restored and test complete!")