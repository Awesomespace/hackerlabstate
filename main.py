from main.ota_updater import OTAUpdater

wifi_ssid = "ASS"
wifi_password = "eurosnoeren"

def download_and_install_update_if_available():
    ota = OTAUpdater("https://github.com/Awesomespace/hackerlabstate")
    ota.download_and_install_update_if_available(wifi_ssid, wifi_password)

def start():
    from main.hackerlabstate import HackerLabState
    hackerlabstate = HackerLabState()

def main():
    download_and_install_update_if_available()
    start()

main()
