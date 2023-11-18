from dataclasses import dataclass, field


@dataclass(frozen=True, order=True, kw_only=True)
class Device:
    serial      : str = field()
    model       : str = field(compare=False)
    device      : str = field(compare=False)
    status      : str = field(compare=False)
    usb         : str = field(compare=False)
    product     : str = field(compare=False)
    transport_id: str = field(compare=False)
