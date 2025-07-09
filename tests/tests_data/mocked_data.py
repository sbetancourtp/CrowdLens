from models.entry_models import EntryRepo
from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import MagicMock


class EntryMockedData:

    # Chat ids

    CHAT_ID_ONE = 1043412725
    CHAT_ID_TWO = 888777666

    # Entries body of info

    ENTRY_ID_ONE = 'aaaaaaaa-2222-cccc-4444-eeeeeeeeeeee'
    MESSAGE_ID_ONE = 55
    USER_ID_ONE = 1043412725
    USERNAME_ONE = "cmejia"
    TIMESTAMP_ONE = datetime(2025, 5, 29, 12, 19, 43, tzinfo=timezone.utc)
    TEXT_ONE_THREE_KWDS = "A pen, a mirror and a towel. 🖊️🪞"
    RAW_MESSAGE_ONE = {
        "message_id": MESSAGE_ID_ONE,
        "from": {"id": USER_ID_ONE, "username": USERNAME_ONE},
        "chat": {"id": CHAT_ID_ONE},
        "date": TIMESTAMP_ONE.isoformat(),
        "text": TEXT_ONE_THREE_KWDS
    }
    MEDIA_TYPE_ONE = "text"

    ENTRY_ID_TWO = '11111111-bbbb-3333-dddd-555555555555'
    MESSAGE_ID_TWO = 102
    USER_ID_TWO = 999888777
    USERNAME_TWO = "another_user"
    TIMESTAMP_TWO = datetime(2025, 5, 30, 15, 45, 10, tzinfo=timezone.utc)
    TEXT_TWO = "Hello world with media 🎧"
    RAW_MESSAGE_TWO = {
        "message_id": MESSAGE_ID_TWO,
        "from": {"id": USER_ID_TWO, "username": USERNAME_TWO},
        "chat": {"id": CHAT_ID_TWO},
        "date": TIMESTAMP_TWO.isoformat(),
        "text": TEXT_TWO
    }
    MEDIA_TYPE_TWO = "voice"

    # Media

    MEDIA_FILE_ID_ONE = None
    MEDIA_FILE_ID_TWO = "abc123mediafile"

    # Different text variations
    TEXT_WITH_FOUR_KEYWORDS = 'The ant walked in the street with a banana!'
    TEXT_WITH_FIVE_KEYWORDS = 'He did not drink the pill and his health is on decline, help him!'

    # Flags
    SAVE_FLAG_TRUE = True
    SAVE_FLAG_FALSE = False

    # Deck association
    DECK_ID_NONE = None
    DECK_ID_SAMPLE = str(uuid4())

    # Nulls

    TEXT_NONE = None
    MEDIA_TYPE_NONE = None

    @staticmethod
    def to_dict_one():
        return {
            "message_id": EntryMockedData.MESSAGE_ID_ONE,
            "from": {"id": EntryMockedData.USER_ID_ONE, "username": EntryMockedData.USERNAME_ONE},
            "chat": {"id": EntryMockedData.CHAT_ID_ONE},
            "date": EntryMockedData.TIMESTAMP_ONE,
            "voice": {"file_id": EntryMockedData.MEDIA_FILE_ID_ONE}
        }

    # Entries

    REPO_ENTRY_ONE_WITH_THREE_KWDS = EntryRepo(
        entry_id=ENTRY_ID_ONE,
        message_id=MESSAGE_ID_ONE,
        user_id=USER_ID_ONE,
        username=USERNAME_ONE,
        chat_id=CHAT_ID_ONE,
        timestamp=TIMESTAMP_ONE,
        text=TEXT_ONE_THREE_KWDS,
        raw_message=RAW_MESSAGE_ONE,
        media_type=MEDIA_TYPE_ONE,
        media_file_id=MEDIA_FILE_ID_ONE,
        deck_id=DECK_ID_NONE,
        save_flag=SAVE_FLAG_FALSE
    )

    REPO_ENTRY_ONE_WITH_FOUR_KWDS = EntryRepo(
        entry_id=ENTRY_ID_ONE,
        message_id=MESSAGE_ID_ONE,
        user_id=USER_ID_ONE,
        username=USERNAME_ONE,
        chat_id=CHAT_ID_ONE,
        timestamp=TIMESTAMP_ONE,
        text=TEXT_WITH_FOUR_KEYWORDS,
        raw_message=RAW_MESSAGE_ONE,
        media_type=MEDIA_TYPE_ONE,
        media_file_id=MEDIA_FILE_ID_ONE,
        deck_id=DECK_ID_NONE,
        save_flag=SAVE_FLAG_FALSE
    )

    # Mock ONE of telegram client entry object

    USER_ONE = MagicMock()
    USER_ONE.id = USER_ID_ONE
    USER_ONE.username = USERNAME_ONE

    MESSAGE_ONE = MagicMock()
    MESSAGE_ONE.message_id = MESSAGE_ID_ONE
    MESSAGE_ONE.from_user = USER_ONE
    MESSAGE_ONE.date = TIMESTAMP_ONE
    MESSAGE_ONE.text = TEXT_ONE_THREE_KWDS
    MESSAGE_ONE.photo = None
    MESSAGE_ONE.voice = None
    MESSAGE_ONE.to_dict = to_dict_one.__func__

    TELEGRAM_ENTRY_ONE = MagicMock()
    TELEGRAM_ENTRY_ONE.message = MESSAGE_ONE

    # Mock TWO of telegram client entry object

    USER_TWO = MagicMock()
    USER_TWO.id = USER_ID_ONE
    USER_TWO.username = None

    MESSAGE_TWO = MagicMock()
    MESSAGE_TWO.message_id = MESSAGE_ID_ONE
    MESSAGE_TWO.from_user = USER_TWO
    MESSAGE_TWO.date = TIMESTAMP_ONE
    MESSAGE_TWO.text = TEXT_ONE_THREE_KWDS
    MESSAGE_TWO.photo = None
    MESSAGE_TWO.voice = None
    MESSAGE_TWO.to_dict.return_value = None

    TELEGRAM_ENTRY_TWO = MagicMock()
    TELEGRAM_ENTRY_TWO.message = MESSAGE_TWO
