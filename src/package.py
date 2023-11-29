from dataclasses import dataclass, field


@dataclass(order=True, kw_only=True)
class Package:
    full_name     : str  = field()
    installed     : bool = field(compare=False)
    disabled      : bool = field(compare=False, default=False)
    system        : bool = field(compare=False, default=False)
    safe_to_remove: bool = field(compare=False, default=False)
    short_name    : str  = field(compare=False, default=None)
    description   : str  = field(compare=False, default="")

    def __post_init__(self):
        if self.short_name is None:
            self.short_name = self.full_name.split(".")[-1]
