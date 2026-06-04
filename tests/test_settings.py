from sn_set.settings import Settings


class TestSettings:
    def test_oauth_client_credentials_settings(self, mock_oauth_client_credentials_env):
        test_settings = Settings()

        assert test_settings.get_user() == "abc123"
        assert test_settings.get_password() is None
        assert test_settings.get_use_oauth()
        assert test_settings.get_client_id() == "client_id"
        assert test_settings.get_client_secret() == "super-secure"
        assert test_settings.get_grant_type() == "client_credentials"

    def test_oauth_password_settings(self, mock_oauth_password_env):
        test_settings = Settings()

        assert test_settings.get_user() == "abc123"
        assert test_settings.get_password() == "super-secret"
        assert test_settings.get_use_oauth()
        assert test_settings.get_client_id() == "client_id"
        assert test_settings.get_client_secret() == "super-secure"
        assert test_settings.get_grant_type() == "password"

    def test_basic_settings(self, mock_env_vars):
        test_settings = Settings()

        assert test_settings.get_user() == "user"
        assert test_settings.get_password() == "password"
        assert not test_settings.get_use_oauth()
        assert test_settings.get_client_id() is None
        assert test_settings.get_client_secret() is None
        assert test_settings.get_grant_type() is None
