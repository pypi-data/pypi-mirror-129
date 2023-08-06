"""OT3 Hardware Controller Backend."""

from __future__ import annotations
import asyncio
from contextlib import contextmanager
import logging
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING, Sequence, Generator

from opentrons.config.types import RobotConfig
from opentrons.drivers.rpi_drivers.gpio_simulator import SimulatingGPIOCharDev
from opentrons.types import Mount

from .module_control import AttachedModulesControl
from .types import BoardRevision, Axis

if TYPE_CHECKING:
    from opentrons_shared_data.pipette.dev_types import PipetteName
    from .dev_types import (
        AttachedInstruments,
        InstrumentHardwareConfigs,
    )
    from opentrons.drivers.rpi_drivers.dev_types import GPIODriverLike

log = logging.getLogger(__name__)


AxisValueMap = Dict[str, float]


class OT3Controller:
    """OT3 Hardware Controller Backend."""

    @classmethod
    async def build(cls, config: RobotConfig) -> OT3Controller:
        """Create the OT3Controller instance.

        Args:
            config: Robot configuration

        Returns:
            Instance.
        """
        return cls(config)

    def __init__(self, config: RobotConfig) -> None:
        """Construct.

        Args:
            config: Robot configuration
        """
        self._configuration = config
        self._gpio_dev = SimulatingGPIOCharDev("simulated")
        self._module_controls: Optional[AttachedModulesControl] = None

    @property
    def gpio_chardev(self) -> GPIODriverLike:
        """Get the GPIO device."""
        return self._gpio_dev

    @property
    def board_revision(self) -> BoardRevision:
        """Get the board revision"""
        return BoardRevision.UNKNOWN

    @property
    def module_controls(self) -> AttachedModulesControl:
        """Get the module controls."""
        if self._module_controls is None:
            raise AttributeError("Module controls not found.")
        return self._module_controls

    @module_controls.setter
    def module_controls(self, module_controls: AttachedModulesControl) -> None:
        """Set the module controls"""
        self._module_controls = module_controls

    def is_homed(self, axes: Sequence[str]) -> bool:
        return True

    async def update_position(self) -> AxisValueMap:
        """Get the current position."""
        return {}

    async def move(
        self,
        target_position: AxisValueMap,
        home_flagged_axes: bool = True,
        speed: Optional[float] = None,
        axis_max_speeds: Optional[AxisValueMap] = None,
    ) -> None:
        """Move to a position.

        Args:
            target_position: Map of axis to position.
            home_flagged_axes: Whether to home afterwords.
            speed: Optional speed
            axis_max_speeds: Optional map of axis to speed.

        Returns:
            None
        """
        return None

    async def home(self, axes: Optional[List[str]] = None) -> AxisValueMap:
        """Home axes.

        Args:
            axes: Optional list of axes.

        Returns:
            Homed position.
        """
        return {}

    async def fast_home(self, axes: Sequence[str], margin: float) -> AxisValueMap:
        """Fast home axes.

        Args:
            axes: List of axes to home.
            margin: Margin

        Returns:
            New position.
        """
        return {}

    async def get_attached_instruments(
        self, expected: Dict[Mount, PipetteName]
    ) -> AttachedInstruments:
        """Get attached instruments.

        Args:
            expected: Which mounts are expected.

        Returns:
            A map of mount to pipette name.
        """
        return {}

    def set_active_current(self, axis_currents: Dict[Axis, float]) -> None:
        """Set the active current.

        Args:
            axis_currents: Axes' currents

        Returns:
            None
        """
        return None

    @contextmanager
    def save_current(self) -> Generator[None, None, None]:
        """Save the current."""
        yield

    async def watch(self, loop: asyncio.AbstractEventLoop) -> None:
        """Watch hardware events."""
        return None

    @property
    def axis_bounds(self) -> Dict[Axis, Tuple[float, float]]:
        """Get the axis bounds."""
        return {}

    @property
    def fw_version(self) -> Optional[str]:
        """Get the firmware version."""
        return None

    async def update_firmware(
        self, filename: str, loop: asyncio.AbstractEventLoop, modeset: bool
    ) -> str:
        """Update the firmware."""
        return "Done"

    def engaged_axes(self) -> Dict[str, bool]:
        """Get engaged axes."""
        return {}

    async def disengage_axes(self, axes: List[str]) -> None:
        """Disengage axes."""
        return None

    def set_lights(self, button: Optional[bool], rails: Optional[bool]) -> None:
        """Set the light states."""
        return None

    def get_lights(self) -> Dict[str, bool]:
        """Get the light state."""
        return {}

    def pause(self) -> None:
        """Pause the controller activity."""
        return None

    def resume(self) -> None:
        """Resume the controller activity."""
        return None

    async def halt(self) -> None:
        """Halt the motors."""
        return None

    async def hard_halt(self) -> None:
        """Halt the motors."""
        return None

    async def probe(self, axis: str, distance: float) -> AxisValueMap:
        """Probe."""
        return {}

    def clean_up(self) -> None:
        """Clean up."""
        return None

    async def configure_mount(
        self, mount: Mount, config: InstrumentHardwareConfigs
    ) -> None:
        """Configure a mount."""
        return None
