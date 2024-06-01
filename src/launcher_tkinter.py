from src import adb_utils
from src.device_manager import DeviceManager
from src.gui.tkinter.window_main import WindowMain
from src.logging import logging_utils
from src.package_manager import PackageManager


def main() -> None:
    logging_utils.load_config()

    adb_utils.start_server()

    # Initialize managers
    DeviceManager()
    PackageManager()

    # Initialize window and run main loop
    WindowMain().mainloop()


if __name__ == "__main__":
    main()
