"""Helper script for updating PocketBase records used by CrewAI tools."""

from __future__ import annotations

import json
import os
import sys
from typing import Iterable

import pocketbase

POCKETBASE_URL = os.getenv("POCKETBASE_URL", "http://127.0.0.1:8090")


def _get_admin_credentials() -> tuple[str, str]:
    """Fetch PocketBase admin credentials from environment variables.

    Returns:
        A tuple containing the admin email and password.

    Raises:
        RuntimeError: If one or both required environment variables are missing.
    """

    email = os.getenv("POCKETBASE_ADMIN_EMAIL")
    password = os.getenv("POCKETBASE_ADMIN_PASSWORD")

    missing = [
        name
        for name, value in (
            ("POCKETBASE_ADMIN_EMAIL", email),
            ("POCKETBASE_ADMIN_PASSWORD", password),
        )
        if not value
    ]

    if missing:
        missing_vars = ", ".join(missing)
        raise RuntimeError(
            "Missing required PocketBase admin credential environment "
            f"variable(s): {missing_vars}. Set them before running this script."
        )

    return email, password


def update_pocketbase(messages: Iterable[dict]) -> None:
    """Update the PocketBase record with the supplied chat messages."""

    pb = pocketbase.PocketBase(POCKETBASE_URL)

    admin_email, admin_password = _get_admin_credentials()

    try:
        # Authenticate the admin account
        auth_data = pb.admins.auth_with_password(admin_email, admin_password)

        if auth_data:
            print("Admin authenticated successfully.")

            # Prepare the data to be sent to the crewai_runs collection
            data = {
                "json": json.dumps({"messages": list(messages)}),
                "description": "Updated messages from the AI chat",
            }

            try:
                # Update the record in the crewai_runs collection
                response = pb.collection("ai_chats").update("ic74gxca6sa97sp", data)

                if response:
                    print("Record updated successfully:")
                    print(f"ID: {response.id}")
                    print(f"JSON: {response.json}")
                    print(f"Description: {response.description}")
                else:
                    print("Failed to update record.")
            except Exception as exc:  # pylint: disable=broad-exception-caught
                print(f"Error updating record: {exc}")

            # Clear the auth store to log out the admin account
            pb.auth_store.clear()
        else:
            print("Failed to authenticate admin.")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for CLI execution."""

    input_data = sys.stdin.read()
    data = json.loads(input_data)
    messages = data["messages"]

    update_pocketbase(messages)


if __name__ == "__main__":
    main()
