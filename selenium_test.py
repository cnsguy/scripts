from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")

profile = FirefoxProfile("profile.default")
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)

profile.set_preference('browser.safebrowsing.enabled', False)
profile.set_preference('browser.safebrowsing.downloads.enabled', False)
profile.set_preference('browser.safebrowsing.malware.enabled', False)

profile.set_preference('datareporting.healthreport.service.enabled', False)
profile.set_preference('datareporting.healthreport.uploadEnabled', False)
profile.set_preference('datareporting.policy.dataSubmissionEnabled', False)

profile.set_preference('toolkit.telemetry.unified', False)
profile.set_preference('toolkit.telemetry.enabled', False)

profile.set_preference('media.eme.enabled', False)
profile.set_preference('browser.pocket.enabled', False)
profile.set_preference('extensions.pocket.enabled', False)
profile.set_preference('media.peerconnection.enabled', False)
profile.set_preference('media.peerconnection.ice.default_address_only', True)
profile.set_preference('geo.enabled', False)
profile.set_preference('privacy.resistFingerprinting', True)

driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path="C:\\Projects\\geckodriver.exe")
driver.maximize_window()
driver.get('https://www.google.com')
source = driver.page_source
print(source)
driver.save_screenshot("screenshot.png")
driver.quit()