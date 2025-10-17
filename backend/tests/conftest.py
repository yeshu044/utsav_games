"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, Event, Game, EventLevel, OTPVerification
from app.core.security import create_access_token
from datetime import datetime, timedelta
import base64

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database session"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    user = User(
        name="Test User",
        phone_number="+919876543210",
        email="test@example.com",
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user):
    """Create JWT token for test user"""
    token = create_access_token(data={"sub": str(test_user.user_id)})
    return token


@pytest.fixture
def auth_headers(test_user_token):
    """Create authorization headers"""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def test_game(db):
    """Create a test game"""
    import json
    game = Game(
        game_name="Test Game",
        game_type="TEST_GAME",
        description="A test game",
        component_name="TestGameComponent",
        default_config_schema=json.dumps({"setting": "value"}),
        is_active=True
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@pytest.fixture
def test_event(db):
    """Create a test event"""
    import json
    event = Event(
        event_name="Test Event",
        event_date=datetime.now() + timedelta(days=7),
        organizer_name="Test Organizer",
        organizer_contact="+919999999999",
        baby_name_encrypted=base64.b64encode("TestBaby".encode()).decode(),
        qr_code_token="test_token_123",
        total_levels=5,
        is_active=True,
        description="Test event description",
        theme_config=json.dumps({"color": "blue"})
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@pytest.fixture
def test_level(db, test_event, test_game):
    """Create a test level"""
    import json
    level = EventLevel(
        event_id=test_event.event_id,
        game_id=test_game.game_id,
        level_number=1,
        level_config=json.dumps({"difficulty": "easy"}),
        passing_criteria=json.dumps({"type": "completion"}),
        max_retries=-1,
        is_final_level=False,
        is_enabled=True
    )
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


@pytest.fixture
def multiple_users(db):
    """Create multiple test users"""
    users = []
    for i in range(5):
        user = User(
            name=f"User {i+1}",
            phone_number=f"+9187654321{i}",
            is_verified=True
        )
        db.add(user)
        users.append(user)
    db.commit()
    for user in users:
        db.refresh(user)
    return users
