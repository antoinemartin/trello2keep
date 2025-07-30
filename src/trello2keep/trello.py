"""
Trello API Client Module

This module provides a simple client for interacting with the Trello API.
It allows fetching board data including lists and cards, and exporting
that data to JSON files.

Example:
    Basic usage of the TrelloClient:

    >>> client = TrelloClient(api_key="your_key", token="your_token")
    >>> board_data = client.get_board_data("board_id")
    >>> client.export_to_json("board_id", "output.json")
"""

import json
from typing import Any

import requests


class TrelloClient:
    """
    A client for interacting with the Trello API.

    This class provides methods to fetch board data from Trello and export
    it to JSON files. It handles authentication using API key and token.

    Attributes:
        api_key (str): The Trello API key for authentication
        token (str): The Trello token for authentication
        base_url (str): The base URL for Trello API endpoints

    Example:
        >>> client = TrelloClient("your_api_key", "your_token")
        >>> data = client.get_board_data("board_id")
    """

    api_key: str
    token: str
    base_url: str

    def __init__(self, api_key: str, token: str):
        """
        Initialize the TrelloClient with authentication credentials.

        Args:
            api_key (str): Your Trello API key. Can be obtained from
                          https://trello.com/app-key
            token (str): Your Trello token. Generated when authorizing
                        your application
        """
        self.api_key = api_key
        self.token = token
        self.base_url = 'https://api.trello.com/1'

    def get_board_id_by_name(self, board_name: str) -> str:
        """
        Find a board ID by its name.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            str: The ID of the board.

        Raises:
            ValueError: If no board with the given name is found.
            requests.HTTPError: If the API request fails
        """
        url = f'{self.base_url}/members/me/boards'
        params = {'key': self.api_key, 'token': self.token, 'fields': 'name'}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        boards = response.json()

        for board in boards:
            if board['name'] == board_name:
                return board['id']

        raise ValueError(f"Board with name '{board_name}' not found.")

    def get_board_data(self, board_name: str) -> dict[str, Any]:
        """
        Fetch comprehensive board data including lists and cards.

        Retrieves board information from the Trello API including all open
        lists and cards. The response includes card names, descriptions,
        and their associated list IDs.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            Dict[str, Any]: A dictionary containing the complete board data
                           including lists, cards, and metadata.

        Raises:
            requests.HTTPError: If the API request fails (invalid credentials,
                               board not found, etc.)
            requests.RequestException: For network-related errors
            ValueError: If the board name is not found.

        Example:
            >>> client = TrelloClient("api_key", "token")
            >>> board_data = client.get_board_data("Courses")
            >>> print(board_data['name'])  # Board name
            >>> print(len(board_data['lists']))  # Number of lists
        """
        board_id = self.get_board_id_by_name(board_name)
        url = f'{self.base_url}/boards/{board_id}'
        params = {
            'key': self.api_key,
            'token': self.token,
            'lists': 'open',
            'cards': 'open',
            'card_fields': 'name,idList,desc',
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def export_to_json(self, board_name: str, filename: str = 'courses.json') -> str:
        """
        Export board data to a JSON file in Trello export format.

        Fetches the complete board data and saves it to a JSON file with
        proper formatting and UTF-8 encoding to preserve special characters.

        Args:
            board_name (str): The name of the Trello board to export
            filename (str, optional): The output filename. Defaults to "courses.json"

        Returns:
            str: The filename of the created JSON file

        Raises:
            requests.HTTPError: If the API request fails
            IOError: If there's an error writing to the file
            PermissionError: If there are insufficient permissions to write the file
            ValueError: If the board name is not found.

        Example:
            >>> client = TrelloClient("api_key", "token")
            >>> output_file = client.export_to_json("Courses", "my_board.json")
            >>> print(f"Board exported to {output_file}")
        """
        board_data = self.get_board_data(board_name)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(board_data, f, indent=2, ensure_ascii=False)

        return filename


# Usage example
if __name__ == '__main__':
    """
    Example usage of the TrelloClient.

    This section demonstrates how to use the TrelloClient to export
    a Trello board to JSON. Make sure to replace the credentials
    and board name with your own values.

    Note:
        - Get your API key from: https://trello.com/app-key
        - Generate a token by following the instructions on the API key page
        - Board name is the name of the board you see in Trello
    """
    # Set your credentials (preferably from environment variables)
    import os

    API_KEY = os.getenv('TRELLO_API_KEY', 'your_api_key_here')
    TOKEN = os.getenv('TRELLO_TOKEN', 'your_token_here')
    BOARD_NAME = os.getenv('TRELLO_BOARD_NAME', 'Courses')

    client = TrelloClient(API_KEY, TOKEN)
    client.export_to_json(BOARD_NAME)
    print('Board data exported to courses.json')
