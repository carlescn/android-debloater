from src import adb_utils
from src.device_manager import DeviceManager
from src.gui.tkinter.main_window import MainWindow
from src.logging import logging_utils
from src.package_manager import PackageManager


if __name__ == "__main__":
    logging_utils.load_config()

    adb_utils.start_server()

    # Initialize managers
    DeviceManager()
    PackageManager()

    # Initialize window and run main loop
    MainWindow().mainloop()
