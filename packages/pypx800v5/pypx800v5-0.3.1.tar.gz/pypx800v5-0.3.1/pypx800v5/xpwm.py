"""IPX800V5 X-PWM."""
from .const import DEFAULT_TRANSITION, EXT_XPWM, TYPE_ANA, TYPE_IO
from .extension import Extension
from .ipx800 import IPX800

VALUE_ON = 100
VALUE_OFF = 0


class XPWM(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_XPWM, ext_number, output_number)
        self.ana_state_id = ipx.get_output_id(
            EXT_XPWM, ext_number, TYPE_ANA, output_number
        )
        self.ana_command_id = ipx.get_command_id(
            EXT_XPWM, ext_number, TYPE_ANA, output_number
        )

    @property
    async def status(self) -> bool:
        """Return the current X-PWM status."""
        return await self._ipx.get_ana(self.ana_state_id) > 0

    @property
    async def level(self) -> int:
        """Return the current X-PWM level."""
        return await self._ipx.get_ana(self.ana_state_id)

    async def on(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM."""
        await self._ipx.update_ana(self.ana_command_id, VALUE_ON)

    async def off(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-PWM."""
        await self._ipx.update_ana(self.ana_command_id, VALUE_OFF)

    async def toggle(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-PWM."""
        if self.status:
            await self._ipx.update_ana(self.ana_command_id, VALUE_OFF)
        else:
            await self._ipx.update_ana(self.ana_command_id, VALUE_ON)

    async def set_level(self, level: int, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM on a specific level."""
        await self._ipx.update_ana(self.ana_command_id, level)
