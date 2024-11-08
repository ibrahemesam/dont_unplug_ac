
import sys

if sys.platform == 'win32':
    from .win32 import (
        is_charger_plugged,
        set_on_ac_adapter_state_change,
    )
elif sys.platform == 'linux':
    from .linux import (
        is_charger_plugged,
        set_on_ac_adapter_state_change,
    )
else:
    raise Exception(f"Unsupported Platform: {sys.platform}")

__all__ = ('is_charger_plugged', 'set_on_ac_adapter_state_change')