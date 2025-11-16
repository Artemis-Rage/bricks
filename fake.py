"""FakeArtemisBase: A mock version of ArtemisBase for testing purposes."""

import functools
import inspect
import math
import sys
from unittest import mock

try:
    import rich
    import rich.table

    _RICH_INSTALLED = True

except ImportError:
    print(
        "Rich library not found. "
        "Please install it with 'pip install rich'"
        "Running without rich..."
    )
    _RICH_INSTALLED = False


patches = {"umath": math}

with mock.patch.dict(sys.modules, patches):
    import geometry


def log(method):
    @functools.wraps(method)
    def with_logging(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        all_state = self.__dict__
        state = dict()
        for key in all_state.keys():
            if not key.startswith("_"):
                state[key] = all_state[key]
        sig = inspect.signature(method)
        bound = sig.bind(self, *args, **kwargs)
        bound.apply_defaults()
        arg_dict = {k: v for k, v in bound.arguments.items() if k != "self"}
        entry = {
            "method": method.__name__,
            "params": arg_dict,
        } | state
        self._log.append(entry)
        return result

    return with_logging


class Base:
    """A fake Base that  mimics the ArtemisBase interface for testing.

    This class keeps track of its heading and position but does not perform any actual movements.
    It logs all actions extensively for debugging purposes.
    """

    @log
    def __init__(
        self,
        verbose: bool = False,
    ):
        self.x = 0
        self.y = 0
        self.heading = 0  # In degrees
        self._verbose = verbose
        self._log = []
        if self._verbose:
            print("Initialized Base with position (0, 0) and heading 0 degrees.")

    @log
    def reset_position(
        self,
        x: float = 0,
        y: float = 0,
    ):
        self.x = x
        self.y = y
        if self._verbose:
            print(f"Position reset to ({x}, {y}).")

    @log
    def turn_to(
        self,
        heading: float,
        then=None,
        wait: bool = True,
    ):
        """Turns the robot to face in the direction `heading`."""
        current_heading = self.heading
        turn = (heading - current_heading) % 360
        if turn > 180:
            turn = turn - 360
        self.heading = (self.heading + turn) % 360

        if self._verbose:
            print(
                f"Current heading: {current_heading}\n"
                f"Target heading: {heading}\n"
                f"Turning {turn} degrees.\n"
                f"New heading: {self.heading}."
            )

    @log
    def drive_to(
        self,
        x: float,
        y: float,
        then=None,
        wait: bool = True,
    ):
        """Drives from the current location to (x, y)."""
        heading, distance = geometry.compute_trajectory(self.x, self.y, x, y)
        if self._verbose:
            print(f"Driving from ({self.x}, {self.y}) to ({x}, {y}).")
            print(f"Computed heading: {heading} Distance: {distance}.")
        self.turn_to(heading)
        self.x = x
        self.y = y
        if self._verbose:
            print(f"Arrived at ({x}, {y}).")

    @property
    def log(self):
        return self._log

    def _format_log_rows(self):
        if not self._log:
            return [], []
        headers = list(self._log[0].keys())
        rows = []
        for entry in self._log:
            row = []
            for key in headers:
                value = entry[key]
                if key == "params":
                    value = ", ".join(f"{k}={v}" for k, v in value.items())
                row.append(str(value))
            rows.append(row)
        return headers, rows

    def _rich_table(self):
        if not _RICH_INSTALLED:
            print("Rich library not installed.")
            return
        headers, rows = self._format_log_rows()
        if not headers:
            print("No log entries.")
            return
        table = rich.table.Table(title="Action Log")
        for key in headers:
            table.add_column(key, justify="right", style="cyan", no_wrap=True)
        for row in rows:
            table.add_row(*row)
        rich.print(table)

    def _ascii_table(self):
        headers, rows = self._format_log_rows()
        if not headers:
            print("No log entries.")
            return
        col_widths = [
            max(len(str(item)) for item in col) for col in zip(*([headers] + rows))
        ]
        format_str = " | ".join(f"{{:<{w}}}" for w in col_widths)
        separator = "-+-".join("-" * w for w in col_widths)
        lines = [format_str.format(*headers), separator]
        for row in rows:
            lines.append(format_str.format(*row))
        print("\n".join(lines))

    def table(self):
        if _RICH_INSTALLED:
            self._rich_table()
        else:
            self._ascii_table()


def demo():
    base = Base()
    base.reset_position()
    base.turn_to(90)
    base.drive_to(100, 100)
    base.turn_to(180)
    base.table()


if __name__ == "__main__":
    demo()
