"""H1.7 ticket state machine: transition matrix and capacity rule."""

import pytest
from app.domain.tickets import (
    RegistrationStatus,
    can_transition,
    counts_towards_capacity,
)

VALID = [
    (RegistrationStatus.reserved, RegistrationStatus.pending_payment),
    (RegistrationStatus.reserved, RegistrationStatus.cancelled),
    (RegistrationStatus.reserved, RegistrationStatus.expired),
    (RegistrationStatus.pending_payment, RegistrationStatus.paid),
    (RegistrationStatus.pending_payment, RegistrationStatus.cancelled),
    (RegistrationStatus.pending_payment, RegistrationStatus.expired),
    (RegistrationStatus.paid, RegistrationStatus.used),
    (RegistrationStatus.paid, RegistrationStatus.refunded),
    (RegistrationStatus.paid, RegistrationStatus.cancelled),
    (RegistrationStatus.free_granted, RegistrationStatus.used),
    (RegistrationStatus.free_granted, RegistrationStatus.cancelled),
]

INVALID = [
    (RegistrationStatus.used, RegistrationStatus.paid),
    (RegistrationStatus.cancelled, RegistrationStatus.reserved),
    (RegistrationStatus.refunded, RegistrationStatus.paid),
    (RegistrationStatus.expired, RegistrationStatus.pending_payment),
    (RegistrationStatus.reserved, RegistrationStatus.used),
]


@pytest.mark.parametrize(("current", "target"), VALID)
def test_valid_transition(current, target) -> None:
    """Documented transitions are allowed."""
    assert can_transition(current, target)


@pytest.mark.parametrize(("current", "target"), INVALID)
def test_invalid_transition(current, target) -> None:
    """Terminal and skipped states cannot be re-entered."""
    assert not can_transition(current, target)


def test_capacity_only_counts_paid_and_granted() -> None:
    """Reserved and pending-payment hold a slot but do not increment sold_count."""
    assert counts_towards_capacity(RegistrationStatus.paid)
    assert counts_towards_capacity(RegistrationStatus.free_granted)
    assert not counts_towards_capacity(RegistrationStatus.reserved)
    assert not counts_towards_capacity(RegistrationStatus.pending_payment)
    assert not counts_towards_capacity(RegistrationStatus.cancelled)
