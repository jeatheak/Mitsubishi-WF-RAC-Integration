"""Guards against the #219 regression: a WfRacEntity subclass that leaves one
of the two hooks to the base class. WfRacEntity._apply_state() calls
_update_state() on every coordinator update and _mark_state_unknown() whenever
that read fails; the base implementations raise NotImplementedError, so a
missing override turns every poll - or every unreadable frame - into a
traceback.
"""

import pytest

from custom_components.mitsubishi_wf_rac import (
    binary_sensor,  # noqa: F401
    button,  # noqa: F401
    climate,  # noqa: F401
    number,  # noqa: F401
    select,  # noqa: F401
    sensor,  # noqa: F401
    update,  # noqa: F401
)
from custom_components.mitsubishi_wf_rac.entity import WfRacEntity


@pytest.mark.parametrize("hook", ["_update_state", "_mark_state_unknown"])
def test_every_entity_subclass_overrides(hook):
    # Importing the platform modules above is what populates this - each of
    # their entity classes subclasses WfRacEntity directly.
    subclasses = WfRacEntity.__subclasses__()
    assert subclasses

    # Compared against the base implementation rather than asked for with
    # hasattr(): the base class defines both hooks, so hasattr() is true for
    # every subclass whether it overrides them or not.
    missing = [
        cls.__name__
        for cls in subclasses
        if getattr(cls, hook) is getattr(WfRacEntity, hook)
    ]
    assert not missing, f"missing {hook}(): {missing}"
