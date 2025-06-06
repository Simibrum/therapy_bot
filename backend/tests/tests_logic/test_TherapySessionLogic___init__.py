# Generated by CodiumAI

import pytest
from logic.therapy_session_logic import (
    TherapistDoesNotExistError,
    TherapySessionDoesNotExistError,
    TherapySessionLogic,
    UserIdMismatchError,
)


class Test__Init__:
    #  Initialise a new therapy session with user_id and therapist_id
    def test_init_with_user_id_and_therapist_id(self, user_instance, therapist_instance):
        session = TherapySessionLogic(user_id=user_instance.id, therapist_id=therapist_instance.id)
        assert session.user_id == user_instance.id
        assert session.therapist_id == therapist_instance.id

    #  Initialise a new therapy session with user_id only
    def test_init_with_user_id_only_and_no_therapist(self, user_instance):
        with pytest.raises(TherapistDoesNotExistError):
            TherapySessionLogic(user_id=user_instance.id)

    def test_init_with_user_id_only_and_therapist(self, user_instance, therapist_instance):
        """Test initialising a new therapy session with user_id only and therapist."""
        session = TherapySessionLogic(user_id=user_instance.id)
        assert session.user_id == user_instance.id
        assert session.therapist_id == therapist_instance.id

    #  Initialise a pre-existing therapy session with pre_existing_session_id
    def test_init_with_pre_existing_session_id(self, user_instance, therapist_instance, therapy_session_instance):
        session = TherapySessionLogic(pre_existing_session_id=therapy_session_instance.id)
        assert session.therapy_session_id == 1

    #  Initialise a new therapy session without user_id or pre_existing_session_id
    def test_init_without_user_id_or_pre_existing_session_id(self):
        with pytest.raises(ValueError):
            TherapySessionLogic()

    #  Initialise a pre-existing therapy session with non-existent pre_existing_session_id
    def test_init_with_non_existent_pre_existing_session_id(self, therapy_session_instance):
        with pytest.raises(TherapySessionDoesNotExistError):
            TherapySessionLogic(pre_existing_session_id=999)

    #  Initialise a pre-existing therapy session with pre_existing_session_id and non-matching user_id
    def test_init_with_non_matching_user_id(self, therapy_session_instance):
        with pytest.raises(UserIdMismatchError):
            TherapySessionLogic(user_id=999, pre_existing_session_id=therapy_session_instance.id)
