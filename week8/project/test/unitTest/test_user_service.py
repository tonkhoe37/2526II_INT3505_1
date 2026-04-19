import pytest
from unittest.mock import patch
from services import user_service


# TEST GET USERS
def test_get_users():
    mock_users = [{"id": 1, "name": "Khoa"}]

    with patch("services.user_service.user_repository.get_all_users") as mock_repo:
        mock_repo.return_value = mock_users

        result = user_service.get_users()

        assert result == mock_users
        mock_repo.assert_called_once()


# TEST CREATE USER
def test_create_user():
    data = {"name": "Khoa", "email": "khoa@gmail.com", "password": "123"}

    with patch("services.user_service.user_repository.create_user") as mock_repo:
        mock_repo.return_value = {"id": 1, **data}

        result = user_service.create_user(data)

        assert result["name"] == "Khoa"
        assert result["email"] == "khoa@gmail.com"
        mock_repo.assert_called_once_with(data)


# TEST UPDATE USER
def test_update_user():
    data = {"name": "New Name", "email": "new@gmail.com", "password": "456"}

    with patch("services.user_service.user_repository.update_user") as mock_repo:
        mock_repo.return_value = True

        result = user_service.update_user(1, data)

        assert result is True
        mock_repo.assert_called_once_with(1, "New Name", "new@gmail.com", "456")


# TEST DELETE USER
def test_delete_user():
    with patch("services.user_service.user_repository.delete_user") as mock_repo:
        mock_repo.return_value = True

        result = user_service.delete_user(1)

        assert result is True
        mock_repo.assert_called_once_with(1)


# TEST FIND USER
def test_find_user():
    mock_user = {"id": 1, "name": "Khoa"}

    with patch("services.user_service.user_repository.find_user_by_id") as mock_repo:
        mock_repo.return_value = mock_user

        result = user_service.find_user(1)

        assert result == mock_user
        mock_repo.assert_called_once_with(1)


# TEST LOGIN SUCCESS
def test_login_success():
    mock_user = {"id": 1, "email": "khoa@gmail.com"}

    with patch("services.user_service.user_repository.login") as mock_repo:
        mock_repo.return_value = mock_user

        result = user_service.login("khoa@gmail.com", "123")

        assert result["email"] == "khoa@gmail.com"
        mock_repo.assert_called_once_with("khoa@gmail.com", "123")


# TEST LOGIN FAIL
def test_login_fail():
    with patch("services.user_service.user_repository.login") as mock_repo:
        mock_repo.return_value = None

        result = user_service.login("wrong@gmail.com", "123")

        assert result is None
