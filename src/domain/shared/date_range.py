from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start must be before end.")

    def contains(self, dt: datetime) -> bool:
        return self.start <= dt <= self.end

    def overlaps(self, other: "DateRange") -> bool:
        return self.start <= other.end and other.start <= self.end

    @property
    def duration(self):
        return self.end - self.start
