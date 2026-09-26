"""Default CLI uses the human-approval workflow."""
import asyncio
from .hackathon import main

if __name__ == "__main__":
    asyncio.run(main())
