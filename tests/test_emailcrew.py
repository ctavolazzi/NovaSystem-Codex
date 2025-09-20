import base64
import os
import sys
import types
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict

import pytest

if "crewai" not in sys.modules:
    crewai_module = types.ModuleType("crewai")

    class _CrewStub:
        def __init__(self, *args, **kwargs):
            pass

    crewai_module.Agent = _CrewStub
    crewai_module.Crew = _CrewStub
    crewai_module.Task = _CrewStub

    class _ProcessStub:
        sequential = "sequential"

    crewai_module.Process = _ProcessStub
    sys.modules["crewai"] = crewai_module

if "crewai_tools" not in sys.modules:
    crewai_tools_module = types.ModuleType("crewai_tools")

    class BaseTool:  # type: ignore[override]
        name: str = ""
        description: str = ""

        def __init__(self, *args, **kwargs):
            pass

        def _run(self, *args, **kwargs):
            raise NotImplementedError

    crewai_tools_module.BaseTool = BaseTool
    sys.modules["crewai_tools"] = crewai_tools_module

if "langchain_community.llms" not in sys.modules:
    langchain_module = types.ModuleType("langchain_community")
    llms_module = types.ModuleType("langchain_community.llms")

    class Ollama:  # type: ignore[override]
        def __init__(self, *args, **kwargs):
            self._last_prompt: str | None = None

        def invoke(self, prompt: str):
            self._last_prompt = prompt
            return "stub-response"

    llms_module.Ollama = Ollama
    langchain_module.llms = llms_module
    sys.modules["langchain_community"] = langchain_module
    sys.modules["langchain_community.llms"] = llms_module

if "googleapiclient.discovery" not in sys.modules:
    googleapiclient_module = types.ModuleType("googleapiclient")
    discovery_module = types.ModuleType("googleapiclient.discovery")

    def build(*args, **kwargs):  # noqa: D401 - stub that should not be invoked in tests
        raise RuntimeError("googleapiclient.discovery.build should be patched in tests")

    discovery_module.build = build
    errors_module = types.ModuleType("googleapiclient.errors")

    class HttpError(Exception):
        pass

    errors_module.HttpError = HttpError
    googleapiclient_module.discovery = discovery_module
    googleapiclient_module.errors = errors_module
    sys.modules["googleapiclient"] = googleapiclient_module
    sys.modules["googleapiclient.discovery"] = discovery_module
    sys.modules["googleapiclient.errors"] = errors_module

if "google_auth_oauthlib.flow" not in sys.modules:
    flow_module = types.ModuleType("google_auth_oauthlib.flow")

    class InstalledAppFlow:  # type: ignore[override]
        @staticmethod
        def from_client_secrets_file(*args, **kwargs):
            return InstalledAppFlow()

        def run_local_server(self, port: int = 0):
            class _Creds:
                valid = True
                expired = False
                refresh_token = None

                def refresh(self, request):  # pragma: no cover - not used in tests
                    pass

            return _Creds()

    flow_module.InstalledAppFlow = InstalledAppFlow
    google_auth_oauthlib_module = types.ModuleType("google_auth_oauthlib")
    google_auth_oauthlib_module.flow = flow_module
    sys.modules["google_auth_oauthlib"] = google_auth_oauthlib_module
    sys.modules["google_auth_oauthlib.flow"] = flow_module

if "google.auth.transport.requests" not in sys.modules:
    requests_module = types.ModuleType("google.auth.transport.requests")

    class Request:  # type: ignore[override]
        pass

    requests_module.Request = Request
    transport_module = types.ModuleType("google.auth.transport")
    transport_module.requests = requests_module
    google_auth_module = types.ModuleType("google.auth")
    google_auth_module.transport = transport_module
    sys.modules["google.auth"] = google_auth_module
    sys.modules["google.auth.transport"] = transport_module
    sys.modules["google.auth.transport.requests"] = requests_module

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("SERPER_API_KEY", "test-serper")
os.environ.setdefault("OPENAI_API_KEY", "test-openai")
os.environ.setdefault("MODEL", "stub-model")

from waitaminute.dev.modules.Ollama import EmailCrew


class FakeExecutable:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def execute(self) -> Dict[str, Any]:
        return self._data


class FakeMessagesResource:
    def __init__(self, message_response: Dict[str, Any]):
        self._message_response = message_response
        self.last_modify_body: Dict[str, Any] | None = None

    def list(self, userId: str, q: str, maxResults: int) -> FakeExecutable:  # noqa: N803 - mimics Google API signature
        assert userId == "me"
        assert maxResults == 1
        return FakeExecutable({"messages": [{"id": self._message_response["id"]}]})

    def get(self, userId: str, id: str, format: str) -> FakeExecutable:  # noqa: N803 - mimics Google API signature
        assert userId == "me"
        assert id == self._message_response["id"]
        assert format == "full"
        return FakeExecutable(self._message_response)

    def modify(self, userId: str, id: str, body: Dict[str, Any]) -> FakeExecutable:  # noqa: N803 - mimics Google API signature
        assert userId == "me"
        assert id == self._message_response["id"]
        self.last_modify_body = body
        return FakeExecutable({})


class FakeUsersResource:
    def __init__(self, messages_resource: FakeMessagesResource):
        self._messages_resource = messages_resource

    def messages(self) -> FakeMessagesResource:
        return self._messages_resource


class FakeService:
    def __init__(self, message_response: Dict[str, Any]):
        self.messages_resource = FakeMessagesResource(message_response)
        self.users_resource = FakeUsersResource(self.messages_resource)

    def users(self) -> FakeUsersResource:
        return self.users_resource


class FakeLLM:
    def __init__(self, response: str):
        self._response = response

    def invoke(self, prompt: str) -> str:
        return self._response


@contextmanager
def patched_local_llm(fake_llm: FakeLLM):
    original_llm = EmailCrew.local_llm
    EmailCrew.local_llm = fake_llm
    try:
        yield
    finally:
        EmailCrew.local_llm = original_llm


def build_fake_message(body_text: str) -> Dict[str, Any]:
    encoded_body = base64.urlsafe_b64encode(body_text.encode("utf-8")).decode("utf-8")
    payload = {
        "headers": [
            {"name": "Subject", "value": "Test Subject"},
            {"name": "From", "value": "sender@example.com"},
        ],
        "parts": [
            {"mimeType": "text/plain", "body": {"data": encoded_body}},
        ],
    }
    return {
        "id": "test-id",
        "payload": payload,
        "snippet": "Short snippet",
    }


def test_fetch_latest_unread_email_marks_unread_label_removed():
    message = build_fake_message("Hello World")
    fake_service = FakeService(message)

    result = EmailCrew.fetch_latest_unread_email(fake_service)

    assert result is not None
    assert result["id"] == message["id"]
    assert result["text"] == "Hello World"
    assert fake_service.messages_resource.last_modify_body == {"removeLabelIds": ["UNREAD"]}


def test_fetch_tool_returns_latest_email(monkeypatch: pytest.MonkeyPatch):
    message = build_fake_message("Tool Body")
    fake_service = FakeService(message)
    monkeypatch.setattr(EmailCrew, "get_gmail_service", lambda: fake_service)

    tool = EmailCrew.FetchLatestEmailTool()
    result = tool._run()

    assert result["subject"] == "Test Subject"
    assert result["text"] == "Tool Body"
    assert fake_service.messages_resource.last_modify_body == {"removeLabelIds": ["UNREAD"]}


def test_llm_tool_serializes_non_string_response():
    tool = EmailCrew.LLMRecommendationTool()
    with patched_local_llm(FakeLLM("Do something")):
        result = tool._run({"text": "content"})
    assert result == "Do something"


def test_smoke_email_workflow(monkeypatch: pytest.MonkeyPatch):
    message = build_fake_message("Workflow Body")
    fake_service = FakeService(message)
    monkeypatch.setattr(EmailCrew, "get_gmail_service", lambda: fake_service)

    fetch_tool = EmailCrew.FetchLatestEmailTool()
    recommend_tool = EmailCrew.LLMRecommendationTool()

    with patched_local_llm(FakeLLM("All set")):
        email_data = fetch_tool._run()
        recommendation = recommend_tool._run(email_data)

    assert email_data["text"] == "Workflow Body"
    assert recommendation == "All set"
    assert fake_service.messages_resource.last_modify_body == {"removeLabelIds": ["UNREAD"]}
