from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db import Base
from app.models.ticket import Ticket
from app.llm.llm_service import resolve_ticket
from app.llm import client  # this is where we'll stub `call_llm`

# Step 1: Create in-memory SQLite DB
engine = create_engine("sqlite:///:memory:", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Step 2: Create all tables
Base.metadata.create_all(engine)

# Step 3: Insert a dummy ticket
dummy_ticket = Ticket(
    title="Cannot connect to VPN",
    description="The VPN client shows 'Connection failed' when I try to log in.",
    user_id=1
)
session.add(dummy_ticket)
session.commit()

# Step 4: Monkey-patch call_llm
def fake_llm(prompt: str):
    print("Mock LLM called with prompt:")
    print(prompt[:300])  # truncate
    return {
        "summary": "User cannot connect to VPN.",
        "diagnosis": ["VPN server might be down", "User credentials invalid"],
        "solutions": ["Check VPN server status", "Reset VPN credentials"],
        "confidence": 0.91
    }

client.call_llm = fake_llm  # override the real one

# Step 5: Call resolve_ticket()
result = resolve_ticket(ticket_id=dummy_ticket.id, db=session)

# Step 6: Print the result
print("LLM Result:")
print(result)
