from models.entry_models import EntryRepo
from datetime import datetime, timezone
from uuid import uuid4
from types import SimpleNamespace


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
    TEXT_ONE = "Test Entry 📄📆"
    RAW_MESSAGE_ONE = {
        "message_id": MESSAGE_ID_ONE,
        "from": {"id": USER_ID_ONE, "username": USERNAME_ONE},
        "chat": {"id": CHAT_ID_ONE},
        "date": TIMESTAMP_ONE.isoformat(),
        "text": TEXT_ONE
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

    # Flags
    SAVE_FLAG_TRUE = True
    SAVE_FLAG_FALSE = False

    # Deck association
    DECK_ID_NONE = None
    DECK_ID_SAMPLE = str(uuid4())

    @staticmethod
    def to_dict_zero():
        return {
            "message_id": EntryMockedData.MESSAGE_ID_ONE,
            "from": {"id": EntryMockedData.USER_ID_ONE, "username": EntryMockedData.USERNAME_ONE},
            "chat": {"id": EntryMockedData.CHAT_ID_ONE},
            "date": EntryMockedData.TIMESTAMP_ONE,
            "voice": {"file_id": EntryMockedData.MEDIA_FILE_ID_ONE}
        }

    # Entries

    REPO_ENTRY_ONE = EntryRepo(
        entry_id=ENTRY_ID_ONE,
        message_id=MESSAGE_ID_ONE,
        user_id=USER_ID_ONE,
        username=USERNAME_ONE,
        chat_id=CHAT_ID_ONE,
        timestamp=TIMESTAMP_ONE,
        text=TEXT_ONE,
        raw_message=RAW_MESSAGE_ONE,
        media_type=MEDIA_TYPE_ONE,
        media_file_id=MEDIA_FILE_ID_ONE,
        deck_id=DECK_ID_NONE,
        save_flag=SAVE_FLAG_FALSE
    )

    TELEGRAM_ENTRY_ONE = SimpleNamespace(
        message=SimpleNamespace(
            message_id=MESSAGE_ID_ONE,
            from_user=SimpleNamespace(
                id=USER_ID_ONE,
                username=USERNAME_ONE
            ),
            chat=SimpleNamespace(
                id=CHAT_ID_ONE
            ),
            date=TIMESTAMP_ONE,
            text=TEXT_ONE,
            to_dict=to_dict_zero.__func__
        )
    )

    # REPO_ENTRY_TWO = EntryRepo(
    #     entry_id=ENTRY_ID_TWO,
    #     message_id=MESSAGE_ID_TWO,
    #     user_id=USER_ID_TWO,
    #     username=USERNAME_TWO,
    #     chat_id=CHAT_ID_TWO,
    #     timestamp=TIMESTAMP_TWO,
    #     text=TEXT_TWO,
    #     raw_message=RAW_MESSAGE_TWO,
    #     media_type=MEDIA_TYPE_TWO,
    #     media_file_id=MEDIA_FILE_ID_TWO,
    #     deck_id=DECK_ID_NONE,
    #     save_flag=SAVE_FLAG_FALSE
    # )


