from dataclasses import dataclass, field


@dataclass(frozen=True, order=True, kw_only=True)
class Package:
    full_name : str = field()
    short_name: str = field(compare=False)
    status    : str = field(compare=False)
