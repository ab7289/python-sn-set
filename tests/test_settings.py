from sn_set.settings import Settings


class TestSettings:
    def test_oauth_settings(self, mock_oauth_env_vars):
        test_settings = Settings()

        assert test_settings.get_user() == "abc123"
        assert test_settings.get_password() == "super-secret"
        assert test_settings.get_use_oauth()
        assert test_settings.get_client_id() == "client_id"
        assert test_settings.get_client_secret() == "super-secure"
        assert test_settings.get_grant_type() == "password"
