"""Ticket state machine and capacity rules (§4.2, §8.1 rule 7).

The state machine is pure: no database, HTTP, or clock dependency. The
registrations repo stores the status; services decide when a transition is
allowed.
"""

from __future__ import annotations

import enum


class RegistrationStatus(enum.StrEnum):
    """Lifecycle of a ticket registration."""

    reserved = "reserved"
    pending_payment = "pending_payment"
    paid = "paid"
    free_granted = "free_granted"
    used = "used"
    cancelled = "cancelled"
    refunded = "refunded"
    expired = "expired"


ALLOWED_TRANSITIONS: dict[RegistrationStatus, frozenset[RegistrationStatus]] = {
    RegistrationStatus.reserved: frozenset(
        {
            RegistrationStatus.pending_payment,
            RegistrationStatus.cancelled,
            RegistrationStatus.expired,
        }
    ),
    RegistrationStatus.pending_payment: frozenset(
        {RegistrationStatus.paid, RegistrationStatus.cancelled, RegistrationStatus.expired}
    ),
    RegistrationStatus.paid: frozenset(
        {RegistrationStatus.used, RegistrationStatus.refunded, RegistrationStatus.cancelled}
    ),
    RegistrationStatus.free_granted: frozenset(
        {RegistrationStatus.used, RegistrationStatus.cancelled}
    ),
    RegistrationStatus.used: frozenset(),
    RegistrationStatus.cancelled: frozenset(),
    RegistrationStatus.refunded: frozenset(),
    RegistrationStatus.expired: frozenset(),
}

CAPACITY_STATUSES: frozenset[RegistrationStatus] = frozenset(
    {RegistrationStatus.paid, RegistrationStatus.free_granted}
)


def can_transition(current: RegistrationStatus, target: RegistrationStatus) -> bool:
    """Return whether a status change is allowed.

    Args:
        current: Current registration status.
        target: Requested next status.

    Returns:
        True when the transition exists in the state machine.
    """
    return target in ALLOWED_TRANSITIONS[current]


def counts_towards_capacity(status: RegistrationStatus) -> bool:
    """Return whether a status consumes a ticket's sold_count.

    Reserved and pending-payment rows hold a slot but do not increment
    ``sold_count`` (§8.1 rule 7).
    """
    return status in CAPACITY_STATUSES
