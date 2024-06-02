from src import adb_utils
from src.device_manager import DeviceManager
from src.gui.tkinter.window_main import WindowMain
from src.logging import logging_utils
from src.package_manager import PackageManager


def main() -> None:
    logging_utils.load_config()

    adb_utils.start_server()

    # Initialize managers
    device_manager = DeviceManager()
    package_manager = PackageManager(device_manager)

    # Initialize window and run main loop
    WindowMain(device_manager, package_manager).mainloop()


if __name__ == "__main__":
    main()
