"""H2.1/H2.2 service tests with an in-memory repository (no DB required)."""

from __future__ import annotations

import datetime
import uuid

import pytest
from app.core import security
from app.core.errors import ApiError
from app.repos.auth import User
from app.schemas.auth import ProfileUpdate
from app.services import auth as service


class FakeRefresh:
    """Mutable refresh-token row used by the repository double."""

    def __init__(self, user_id, expires_at, device_id) -> None:
        self.user_id = user_id
        self.expires_at = expires_at
        self.device_id = device_id
        self.revoked_at = None


class FakeUserRepo:
    """Minimal repository double: users, refresh tokens, commits."""

    def __init__(self) -> None:
        self.users: dict[str, User] = {}
        self.refresh: dict[str, FakeRefresh] = {}
        self.commits = 0

    async def get_by_email(self, email: str) -> User | None:
        return self.users.get(email.lower())

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return next((u for u in self.users.values() if u.id == user_id), None)

    async def create_user(self, *, email: str, password_hash: str, display_name: str) -> User:
        user = User(
            id=uuid.uuid4(),
            email=email.lower(),
            password_hash=password_hash,
            display_name=display_name,
            created_at=datetime.datetime.now(datetime.UTC),
            locale="tr",
            budget_currency="TRY",
        )
        self.users[user.email] = user
        return user

    async def update_profile(self, user: User, changes: dict[str, object]) -> User:
        for key, value in changes.items():
            setattr(user, key, value)
        return user

    async def add_refresh_token(self, *, user_id, token_hash, expires_at, device_id):
        self.refresh[token_hash] = FakeRefresh(user_id, expires_at, device_id)
        return self.refresh[token_hash]

    async def get_refresh_token(self, token_hash: str) -> FakeRefresh | None:
        return self.refresh.get(token_hash)

    async def revoke_refresh_token(self, record) -> None:
        record.revoked_at = datetime.datetime.now(datetime.UTC)

    async def commit(self) -> None:
        self.commits += 1


@pytest.mark.asyncio
async def test_register_hashes_password_and_returns_tokens() -> None:
    """Registration never stores plaintext and returns a usable token pair."""
    repo = FakeUserRepo()
    result = await service.register_user(
        repo,
        email="Ada@Example.com",
        password="correct-horse",
        display_name="Ada",
        device_id="test-device",
    )
    assert result.user.email == "ada@example.com"
    assert result.access_token
    assert result.refresh_token
    user = repo.users["ada@example.com"]
    assert user.password_hash != "correct-horse"
    assert security.verify_password("correct-horse", user.password_hash)
    assert repo.commits == 1


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email() -> None:
    """A second registration with the same e-mail is 409."""
    repo = FakeUserRepo()
    await service.register_user(
        repo, email="a@example.com", password="correct-horse", display_name="A", device_id=None
    )
    with pytest.raises(ApiError) as exc:
        await service.register_user(
            repo, email="A@Example.com", password="another-pass", display_name="A", device_id=None
        )
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_login_rejects_wrong_password() -> None:
    """Wrong credentials return 401, not a user enumeration detail."""
    repo = FakeUserRepo()
    await service.register_user(
        repo, email="a@example.com", password="correct-horse", display_name="A", device_id=None
    )
    with pytest.raises(ApiError) as exc:
        await service.login_user(
            repo, email="a@example.com", password="wrong-password", device_id=None
        )
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_refresh_rotates_and_revokes_old_token() -> None:
    """Refresh revokes the presented token and issues a new pair."""
    repo = FakeUserRepo()
    first = await service.register_user(
        repo, email="a@example.com", password="correct-horse", display_name="A", device_id=None
    )
    old_hash = security.hash_refresh_token(first.refresh_token)
    second = await service.refresh_tokens(repo, raw_refresh=first.refresh_token, device_id=None)
    assert second.refresh_token != first.refresh_token
    assert repo.refresh[old_hash].revoked_at is not None
    with pytest.raises(ApiError):
        await service.refresh_tokens(repo, raw_refresh=first.refresh_token, device_id=None)


@pytest.mark.asyncio
async def test_logout_is_idempotent() -> None:
    """Logout revokes once; a second call does not fail."""
    repo = FakeUserRepo()
    result = await service.register_user(
        repo, email="a@example.com", password="correct-horse", display_name="A", device_id=None
    )
    await service.logout_user(repo, raw_refresh=result.refresh_token)
    await service.logout_user(repo, raw_refresh=result.refresh_token)
    assert repo.refresh[security.hash_refresh_token(result.refresh_token)].revoked_at is not None


@pytest.mark.asyncio
async def test_profile_update_returns_complete_profile() -> None:
    """H2.2 profile fields survive the update round-trip."""
    repo = FakeUserRepo()
    await service.register_user(
        repo, email="a@example.com", password="correct-horse", display_name="A", device_id=None
    )
    user = repo.users["a@example.com"]
    updated = await service.update_profile(
        repo,
        user=user,
        payload=ProfileUpdate(
            bio="Kampüs müziği",
            city="Ankara",
            interests=["müzik", "tiyatro"],
            locale="tr",
            budget_minor=25000,
        ),
    )
    assert updated.bio == "Kampüs müziği"
    assert updated.city == "Ankara"
    assert updated.interests == ["müzik", "tiyatro"]
    assert updated.budget_minor == 25000


def test_access_token_round_trip_and_tamper() -> None:
    """Access tokens decode to the user id and reject tampering."""
    user_id = uuid.uuid4()
    token = security.create_access_token(user_id)
    assert security.decode_access_token(token) == user_id
    with pytest.raises(ApiError):
        security.decode_access_token(token + "x")
