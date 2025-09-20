Store modules you want NovaSystem to use inside this directory.

Nova should load these modules into its infrastructure automatically when it starts.

It doesn't, but it should. That's on the todo list.

## CrewAI PocketBase helper

The `crewai/pocketbase_test.py` helper now expects credentials to be provided
via environment variables before execution:

```bash
export POCKETBASE_ADMIN_EMAIL="admin@example.com"
export POCKETBASE_ADMIN_PASSWORD="super-secret-password"
python pocketbase_test.py < input.json
```

Optionally, set `POCKETBASE_URL` to point to a non-local PocketBase instance.
The script will raise an explicit error if any required credential variable is
missing.