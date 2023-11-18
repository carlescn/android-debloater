from src.adb_utils import AdbUtils
from src.device_manager import DeviceManager
from src.gui.tkinter.main_window import MainWindow
from src.logging.logging_utils import LoggingUtils
from src.package_manager import PackageManager


class MainAppTkInter:
    def __init__(self):
        self.device_manager = DeviceManager()
        self.package_manager = PackageManager()

        self.main_window = MainWindow(self)
        self.update_devices_list()

        self.main_window.mainloop()

    def clear_packages_list(self) -> None:
        self.package_manager.clear_packages()
        self.main_window.clear_packages_list()

    def update_packages_list(self) -> None:
        self.package_manager.update_packages()
        packages = self.package_manager.get_packages()

        rows = [(p.short_name, p.full_name, p.status) for p in packages]

        self.main_window.update_packages_list(rows)

    def update_active_device(self, *args) -> None:
        device = self.main_window.get_active_device()
        self.device_manager.set_active_device(device)
        self.package_manager.set_device(device)
        self.main_window.clear_packages_list()

    def update_devices_list(self) -> None:
        self.device_manager.update_devices()
        serials = list(self.device_manager.get_devices_serials())
        self.main_window.update_devices_list(serials)
        self.update_active_device()


if __name__ == "__main__":
    LoggingUtils().load_config()

    AdbUtils().start_server()

    MainAppTkInter()
