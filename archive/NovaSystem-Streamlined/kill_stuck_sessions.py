#!/usr/bin/env python3
"""
Script to kill stuck sessions in the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from novasystem.database import get_database, SystemSession
from sqlalchemy import update
from datetime import datetime

def kill_stuck_sessions():
    """Kill all sessions with 'running' status."""
    try:
        db = get_database()

        with db.get_session() as session:
            # Update all running sessions to killed
            result = session.execute(
                update(SystemSession)
                .where(SystemSession.status == 'running')
                .values(
                    status='killed',
                    completed_at=datetime.utcnow(),
                    error_message='Session killed by admin'
                )
            )

            session.commit()

            print(f"✅ Successfully killed {result.rowcount} stuck sessions")

            # Show remaining sessions
            remaining_sessions = session.query(SystemSession).all()
            print(f"\n📊 Current session status:")
            for session_obj in remaining_sessions:
                print(f"  - {session_obj.session_id}: {session_obj.status}")

    except Exception as e:
        print(f"❌ Error killing sessions: {e}")
        return False

    return True

if __name__ == "__main__":
    kill_stuck_sessions()
