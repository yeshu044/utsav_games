"""
Seed data script for Utsav Games
Populates the database with sample games, events, levels, and test users.
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Event, Game, EventLevel, MediaAsset
from app.core.security import get_password_hash
import json

# Create tables
Base.metadata.create_all(bind=engine)

def clear_database(db: Session):
    """Clear all existing data (optional - use with caution!)"""
    print("⚠️  Clearing existing data...")
    db.query(MediaAsset).delete()
    db.query(EventLevel).delete()
    db.query(Event).delete()
    db.query(Game).delete()
    db.query(User).delete()
    db.commit()
    print("✅ Database cleared")


def seed_users(db: Session):
    """Create test users"""
    print("\n📱 Creating test users...")
    
    users_data = [
        {"name": "Priya Sharma", "phone": "+919876543210"},
        {"name": "Rahul Kumar", "phone": "+919876543211"},
        {"name": "Anjali Mehta", "phone": "+919876543212"},
        {"name": "Vikram Patel", "phone": "+919876543213"},
        {"name": "Neha Reddy", "phone": "+919876543214"},
        {"name": "Admin User", "phone": "+919999999999", "email": "admin@utsavgames.com"},
    ]
    
    created_users = []
    for user_data in users_data:
        user = User(
            name=user_data["name"],
            phone_number=user_data["phone"],
            email=user_data.get("email"),
            is_verified=True
        )
        db.add(user)
        created_users.append(user)
        print(f"  ✓ Created user: {user.name}")
    
    db.commit()
    print(f"✅ Created {len(created_users)} users")
    return created_users


def seed_games(db: Session):
    """Create game catalog"""
    print("\n🎮 Creating game catalog...")
    
    games_data = [
        {
            "game_name": "2048 Puzzle",
            "game_type": "2048_PUZZLE",
            "description": "Combine tiles to reach the target number",
            "component_name": "Game2048",
            "default_config_schema": json.dumps({
                "target_tile": {"type": "number", "default": 512, "options": [256, 512, 1024, 2048]},
                "grid_size": {"type": "number", "default": 4, "options": [4, 5]},
                "allow_undo": {"type": "boolean", "default": False}
            })
        },
        {
            "game_name": "Memory Match",
            "game_type": "MEMORY_MATCH",
            "description": "Find matching pairs of cards",
            "component_name": "MemoryMatchGame",
            "default_config_schema": json.dumps({
                "num_pairs": {"type": "number", "default": 8, "min": 4, "max": 15},
                "flip_delay_ms": {"type": "number", "default": 1000, "min": 500, "max": 2000},
                "show_timer": {"type": "boolean", "default": False}
            })
        },
        {
            "game_name": "Jigsaw Puzzle",
            "game_type": "JIGSAW_PUZZLE",
            "description": "Piece together the image",
            "component_name": "JigsawPuzzleGame",
            "default_config_schema": json.dumps({
                "num_pieces": {"type": "number", "default": 25, "options": [16, 25, 36, 49]},
                "show_reference": {"type": "boolean", "default": True},
                "piece_shape": {"type": "string", "default": "square", "options": ["square", "jigsaw"]}
            })
        },
        {
            "game_name": "Balloon Pop",
            "game_type": "BALLOON_POP",
            "description": "Pop balloons in sequence or by target",
            "component_name": "BalloonPopGame",
            "default_config_schema": json.dumps({
                "target_count": {"type": "number", "default": 20, "min": 10, "max": 50},
                "time_limit_seconds": {"type": "number", "default": 30, "min": 15, "max": 60},
                "sequence_type": {"type": "string", "default": "numbers", "options": ["numbers", "colors", "random"]}
            })
        },
        {
            "game_name": "Name Guessing",
            "game_type": "NAME_GUESS",
            "description": "Guess the baby's name from options",
            "component_name": "NameGuessingGame",
            "default_config_schema": json.dumps({
                "num_options": {"type": "number", "default": 5, "min": 3, "max": 8},
                "show_hints": {"type": "boolean", "default": False}
            })
        }
    ]
    
    created_games = []
    for game_data in games_data:
        game = Game(**game_data)
        db.add(game)
        created_games.append(game)
        print(f"  ✓ Created game: {game.game_name}")
    
    db.commit()
    print(f"✅ Created {len(created_games)} games")
    return created_games


def seed_events(db: Session):
    """Create sample events"""
    print("\n🎊 Creating sample events...")
    
    import base64
    
    # Event 1: Upcoming naming ceremony
    event1 = Event(
        event_name="Aarav's Naming Ceremony",
        event_date=datetime.now() + timedelta(days=15),
        organizer_name="Sharma Family",
        organizer_contact="+919876543210",
        baby_name_encrypted=base64.b64encode("Aarav".encode()).decode(),
        qr_code_token=Event.generate_qr_token(),
        total_levels=5,
        event_start_time=datetime.now() + timedelta(days=15, hours=-1),
        event_end_time=datetime.now() + timedelta(days=15, hours=6),
        description="Join us in celebrating baby Aarav's naming ceremony! Play games and win prizes.",
        theme_config=json.dumps({
            "primary_color": "#F4C430",
            "secondary_color": "#FF6F61",
            "background": "baby-theme"
        }),
        is_active=True
    )
    
    # Event 2: Past event for testing
    event2 = Event(
        event_name="Ananya's First Birthday",
        event_date=datetime.now() - timedelta(days=5),
        organizer_name="Patel Family",
        organizer_contact="+919876543211",
        baby_name_encrypted=base64.b64encode("Ananya".encode()).decode(),
        qr_code_token=Event.generate_qr_token(),
        total_levels=5,
        event_start_time=datetime.now() - timedelta(days=5, hours=2),
        event_end_time=datetime.now() - timedelta(days=5, hours=-4),
        description="Ananya turns ONE! Celebrate with fun games.",
        is_active=False  # Past event
    )
    
    # Event 3: Test event (active now)
    event3 = Event(
        event_name="Test Event - Active Now",
        event_date=datetime.now(),
        organizer_name="Test Organizer",
        organizer_contact="+919999999999",
        baby_name_encrypted=base64.b64encode("TestBaby".encode()).decode(),
        qr_code_token=Event.generate_qr_token(),
        total_levels=5,
        event_start_time=datetime.now() - timedelta(hours=1),
        event_end_time=datetime.now() + timedelta(hours=5),
        description="Test event for development and testing",
        is_active=True
    )
    
    db.add_all([event1, event2, event3])
    db.commit()
    
    print(f"  ✓ Created event: {event1.event_name} (QR: {event1.qr_code_token})")
    print(f"  ✓ Created event: {event2.event_name} (QR: {event2.qr_code_token})")
    print(f"  ✓ Created event: {event3.event_name} (QR: {event3.qr_code_token})")
    print(f"✅ Created 3 events")
    
    return [event1, event2, event3]


def seed_event_levels(db: Session, events, games):
    """Configure levels for events"""
    print("\n🎯 Configuring event levels...")
    
    # Configure levels for Event 1 (Aarav's Naming Ceremony)
    event1_levels = [
        {
            "event_id": events[0].event_id,
            "game_id": games[0].game_id,  # 2048
            "level_number": 1,
            "level_config": json.dumps({
                "target_tile": 512,
                "grid_size": 4,
                "allow_undo": False
            }),
            "passing_criteria": json.dumps({
                "type": "tile_reached",
                "value": 512
            }),
            "max_retries": -1,
            "is_final_level": False
        },
        {
            "event_id": events[0].event_id,
            "game_id": games[1].game_id,  # Memory Match
            "level_number": 2,
            "level_config": json.dumps({
                "num_pairs": 8,
                "flip_delay_ms": 800,
                "show_timer": False
            }),
            "passing_criteria": json.dumps({
                "type": "all_pairs_matched"
            }),
            "max_retries": -1,
            "is_final_level": False
        },
        {
            "event_id": events[0].event_id,
            "game_id": games[2].game_id,  # Jigsaw Puzzle
            "level_number": 3,
            "level_config": json.dumps({
                "num_pieces": 25,
                "show_reference": True,
                "piece_shape": "square"
            }),
            "passing_criteria": json.dumps({
                "type": "puzzle_complete"
            }),
            "max_retries": -1,
            "is_final_level": False
        },
        {
            "event_id": events[0].event_id,
            "game_id": games[3].game_id,  # Balloon Pop
            "level_number": 4,
            "level_config": json.dumps({
                "target_count": 20,
                "time_limit_seconds": 30,
                "sequence_type": "numbers"
            }),
            "passing_criteria": json.dumps({
                "type": "target_reached",
                "value": 20
            }),
            "max_retries": -1,
            "is_final_level": False
        },
        {
            "event_id": events[0].event_id,
            "game_id": games[4].game_id,  # Name Guessing
            "level_number": 5,
            "level_config": json.dumps({
                "name_options": ["Aarav", "Vivaan", "Aditya", "Arjun", "Reyansh"],
                "correct_name": "Aarav",
                "show_hints": False
            }),
            "passing_criteria": json.dumps({
                "type": "correct_selection"
            }),
            "max_retries": 1,  # Only one attempt for final level
            "is_final_level": True
        }
    ]
    
    # Configure levels for Event 3 (Test Event) - same as Event 1
    event3_levels = []
    for level_data in event1_levels:
        event3_level = level_data.copy()
        event3_level["event_id"] = events[2].event_id
        
        # Update name options for test event
        if level_data["level_number"] == 5:
            event3_level["level_config"] = json.dumps({
                "name_options": ["TestBaby", "Sample", "Demo", "Example"],
                "correct_name": "TestBaby",
                "show_hints": False
            })
        
        event3_levels.append(event3_level)
    
    all_levels = event1_levels + event3_levels
    
    created_levels = []
    for level_data in all_levels:
        level = EventLevel(**level_data)
        db.add(level)
        created_levels.append(level)
    
    db.commit()
    print(f"✅ Configured {len(created_levels)} levels across events")
    return created_levels


def seed_media_assets(db: Session, events, levels):
    """Add sample media assets (placeholder URLs)"""
    print("\n🖼️  Adding sample media assets...")
    
    # Find memory match levels
    memory_levels = [l for l in levels if l.level_number == 2]
    
    # Sample image URLs (you can replace with actual Cloudinary URLs)
    sample_images = [
        "https://via.placeholder.com/200x200/FFB6C1/000000?text=Baby",
        "https://via.placeholder.com/200x200/87CEEB/000000?text=Mom",
        "https://via.placeholder.com/200x200/98FB98/000000?text=Dad",
        "https://via.placeholder.com/200x200/DDA0DD/000000?text=Grandma",
        "https://via.placeholder.com/200x200/F0E68C/000000?text=Grandpa",
        "https://via.placeholder.com/200x200/FFD700/000000?text=Uncle",
        "https://via.placeholder.com/200x200/FF6347/000000?text=Aunt",
        "https://via.placeholder.com/200x200/40E0D0/000000?text=Sibling"
    ]
    
    created_assets = []
    for level in memory_levels:
        for idx, image_url in enumerate(sample_images):
            asset = MediaAsset(
                event_id=level.event_id,
                level_id=level.level_id,
                asset_type="MEMORY_CARD_IMAGE",
                file_url=image_url,
                thumbnail_url=image_url,
                display_order=idx,
                asset_metadata=json.dumps({"description": f"Memory card {idx + 1}"})
            )
            db.add(asset)
            created_assets.append(asset)
    
    # Add puzzle images
    puzzle_levels = [l for l in levels if l.level_number == 3]
    for level in puzzle_levels:
        asset = MediaAsset(
            event_id=level.event_id,
            level_id=level.level_id,
            asset_type="PUZZLE_IMAGE",
            file_url="https://via.placeholder.com/600x600/FFB6C1/000000?text=Ultrasound",
            thumbnail_url="https://via.placeholder.com/150x150/FFB6C1/000000?text=Ultrasound",
            display_order=0,
            asset_metadata=json.dumps({"description": "Baby ultrasound image"})
        )
        db.add(asset)
        created_assets.append(asset)
    
    db.commit()
    print(f"✅ Added {len(created_assets)} media assets")
    return created_assets


def print_summary(users, games, events):
    """Print a summary of seeded data"""
    print("\n" + "="*60)
    print("🎉 SEED DATA SUMMARY")
    print("="*60)
    
    print(f"\n👥 Users Created: {len(users)}")
    for user in users:
        print(f"   • {user.name} ({user.phone_number})")
    
    print(f"\n🎮 Games in Catalog: {len(games)}")
    for game in games:
        print(f"   • {game.game_name} ({game.game_type})")
    
    print(f"\n🎊 Events Created: {len(events)}")
    for event in events:
        status = "🟢 ACTIVE" if event.is_active else "🔴 INACTIVE"
        print(f"   • {event.event_name} - {status}")
        print(f"     QR Token: {event.qr_code_token}")
        print(f"     QR URL: http://localhost:8000/api/events/qr/{event.qr_code_token}")
    
    print("\n" + "="*60)
    print("✅ Database seeded successfully!")
    print("="*60)
    
    print("\n📝 QUICK START:")
    print("1. Start the server: uvicorn app.main:app --reload")
    print("2. Visit: http://localhost:8000/docs")
    print("3. Test with phone: +919876543210 (Priya Sharma)")
    print("4. Access event via QR token above")
    print("\n")


def main():
    """Main seed function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE")
    print("="*60)
    
    # Check if user wants to clear existing data
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        response = input("\n⚠️  Clear all existing data? (yes/no): ")
        if response.lower() == "yes":
            db = SessionLocal()
            clear_database(db)
            db.close()
        else:
            print("Aborted.")
            return
    
    # Create new session
    db = SessionLocal()
    
    try:
        # Seed data in order
        users = seed_users(db)
        games = seed_games(db)
        events = seed_events(db)
        levels = seed_event_levels(db, events, games)
        media = seed_media_assets(db, events, levels)
        
        # Print summary
        print_summary(users, games, events)
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
