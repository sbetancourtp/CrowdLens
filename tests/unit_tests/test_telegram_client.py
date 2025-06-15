import pytest
from unittest.mock import patch, MagicMock

from messaging.telegram_client import capture_entry_message
from tests.tests_data.mocked_data import EntryMockedData as Emd
from telegram.ext import ConversationHandler


@pytest.mark.asyncio
async def test_capture_entry_message_text(monkeypatch):
    mock_update = Emd.TELEGRAM_ENTRY_ONE
    mock_context = MagicMock()

    with patch("messaging.telegram_client.write_entry_to_db") as write_entry_to_db_mock:
        result = await capture_entry_message(mock_update, mock_context)

        assert result == ConversationHandler.END

        write_entry_to_db_mock.assert_called_once()
        entry_obj = write_entry_to_db_mock.call_args[0][0]

        assert isinstance(entry_obj.text, str)
        assert entry_obj.text == Emd.TEXT_ONE
        assert len(entry_obj.entry_id) == 36
        assert entry_obj.media_type == "text"
        assert entry_obj.user_id == Emd.USER_ID_ONE


@pytest.mark.asyncio
async def test_capture_entry_message_with_minimal_data(monkeypatch):
    mock_update = Emd.TELEGRAM_ENTRY_TWO
    mock_context = MagicMock()

    with patch("messaging.telegram_client.write_entry_to_db") as write_entry_to_db_mock:
        result = await capture_entry_message(mock_update, mock_context)

        assert result == ConversationHandler.END

        write_entry_to_db_mock.assert_called_once()
        entry_obj = write_entry_to_db_mock.call_args[0][0]

        assert isinstance(entry_obj.text, str)
        assert entry_obj.text == Emd.TEXT_ONE
        assert len(entry_obj.entry_id) == 36
        assert entry_obj.media_type == "text"
        assert entry_obj.user_id == Emd.USER_ID_ONE
