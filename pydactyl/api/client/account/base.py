from pydactyl.api import base


class Account(base.PterodactylAPI):
    """Class for interacting with the Pterodactyl Client API."""

    def get_account(self):
        """List details of the account belonging to the client API key."""
        endpoint = 'client/account'
        response = self._api_request(endpoint=endpoint)
        return response

    def get_2fa_setup_code(self):
        """TODO"""
        pass

    def enable_2fa(self):
        """TODO"""
        pass

    def disable_2fa(self):
        """TODO"""
        pass

    def update_email(self):
        """TODO"""
        pass

    def update_password(self):
        """TODO"""
        pass

    def api_key_list(self):
        """List client's API keys."""
        endpoint = 'client/account/api-keys'
        response = self._api_request(endpoint=endpoint)
        return base.parse_response(response, detail=False)

    def api_key_create(self, description: str, allowed_ips: list):
        """Create a client API key.

        Args:
            description(str): Note for the API key
            allowed_ips(iter): List of allowed IPs
        """
        endpoint = 'client/account/api-keys'
        data = {'description': description, 'allowed_ips': allowed_ips}
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def api_key_delete(self, identifier):
        """Delete a client API key.

        Args:
            identifier(str): API key identifier
        """
        endpoint = 'client/account/api-keys/{}'.format(identifier)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
