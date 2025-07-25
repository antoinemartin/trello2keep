"""trello2keep: Extract Trello list items and create Google Keep notes.

This module provides functionality to extract items from specified lists in a
Trello board and create organized Google Keep notes. It's designed to help
manage shopping lists and other tasks by transferring items from Trello
boards to Google Keep for easier mobile access.

The module supports:
- Trello API integration for extracting list items
- Google Keep API integration with service account authentication
- Domain-wide delegation for Google Workspace environments
- Flexible configuration via command-line options

Example usage:
    python -m trello2keep.main Lidl Carrefour "Whole Foods"

Author: Antoine Martin (antoine.martin@octave.biz)
"""

import json
import pathlib
from typing import Any

import click
from google.oauth2 import service_account
from googleapiclient.discovery import build

from .trello import TrelloClient

# Scopes required for Google Keep
SCOPES = ["https://www.googleapis.com/auth/keep"]
DEFAULT_CREDENTIALS_PATH = pathlib.Path("credentials.json")
DEFAULT_IMPERSONATED_USER_EMAIL = "antoine@openance.com"


def get_keep_service(
    credentials_path: pathlib.Path = DEFAULT_CREDENTIALS_PATH,
    impersonated_user_email: str = DEFAULT_IMPERSONATED_USER_EMAIL,
):
    """Authenticate and return the Google Keep service.

    This function creates a Google Keep service client using service account
    credentials with domain-wide delegation to impersonate a specific user.

    Args:
        credentials_path: Path to the Google service account credentials JSON file.
            The file should contain private key information for a service account
            that has been granted domain-wide delegation.
        impersonated_user_email: Email address of the user to impersonate when
            accessing Google Keep. The service account must have domain-wide
            delegation permissions for this user's domain.

    Returns:
        A Google Keep service client object that can be used to interact with
        the Google Keep API.

    Raises:
        google.auth.exceptions.DefaultCredentialsError: If the credentials file
            is invalid or cannot be loaded.
        googleapiclient.errors.HttpError: If the API client cannot be built.
    """
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES, subject=impersonated_user_email
    )

    return build("keep", "v1", credentials=creds)


def extract_list_items(
    trello_board_id: str, lists: list[str], credentials_path: pathlib.Path = DEFAULT_CREDENTIALS_PATH
) -> dict[str, list[str]] | None:
    """Extract list items from a Trello board.

    This function connects to the Trello API using credentials from a JSON file,
    fetches data from a specified board, and extracts card names from the
    specified lists.

    Args:
        trello_board_id: The unique identifier for the Trello board to extract
            items from. This can be found in the board's URL.
        lists: A list of Trello list names to extract cards from. The names
            are case-insensitive and will be matched against existing list names
            on the board.
        credentials_path: Path to the credentials JSON file containing Trello
            API credentials. The file should have a 'trello' key with 'api_key'
            and 'token' subkeys.

    Returns:
        A dictionary mapping list names (lowercase) to lists of card names from
        those lists. Returns None if there's an error (missing credentials file,
        invalid credentials structure, or invalid board data).

    Example:
        >>> extract_list_items("abc123", ["Shopping", "Todo"])
        {"shopping": ["Milk", "Bread"], "todo": ["Call dentist"]}
    """

    # Read the JSON file credentials_path
    if not credentials_path.exists():
        click.echo(f"Error: Credentials file {credentials_path} does not exist.")
        return None

    with open(credentials_path, "r", encoding="utf-8") as f:
        credentials_data = json.load(f)

    # get the API key, token, and board ID from the credentials file
    if "trello" not in credentials_data:
        click.echo("Error: Trello credentials not found in the credentials file.")
        return None
    trello = credentials_data["trello"]
    api_key = trello.get("api_key")
    token = trello.get("token")

    client = TrelloClient(api_key, token)
    data = client.get_board_data(trello_board_id)

    lists = [name.lower() for name in lists]

    if "cards" not in data:
        click.echo("Error: Invalid JSON file.")
        return None

    list_items: dict[str, list[str]] = {name: [] for name in lists}

    list_id_to_name = {it["id"]: it["name"].lower() for it in data["lists"] if it["name"].lower() in lists}
    list_ids = list(list_id_to_name.keys())

    for card in data["cards"]:
        if card["idList"] in list_ids:
            list_name = list_id_to_name.get(card["idList"])
            if list_name and list_name in lists:
                card_name = card["name"]
                list_items[list_name].append(card_name)
    return list_items


def create_google_keep_note(
    service, note_title: str, list_items: dict[str, list[str]], text_only: bool = False
) -> dict[str, Any]:
    """Create a Google Keep note with organized list items.

    This function takes extracted Trello list items and creates a formatted
    Google Keep note. Each list becomes a section in the note with its name
    in uppercase, followed by the items from that list.

    Args:
        service: An authenticated Google Keep service client object, typically
            obtained from get_keep_service().
        note_title: The title to give the created Google Keep note.
        list_items: A dictionary mapping list names to lists of item names.
            Each key represents a list/section name, and each value is a list
            of items for that section.

    Returns:
        The created note object returned by the Google Keep API.

    Raises:
        googleapiclient.errors.HttpError: If the note creation fails due to
            API errors or insufficient permissions.

    Note:
        The function creates a text note rather than a checklist note to make
        reordering items easier in Google Keep. A commented implementation
        for checkbox-style notes is available in the source code.
    """

    # Generate the note content
    if text_only:
        note_lines = []
        for list_name in list_items.keys():
            section_items = list_items.get(list_name, [])
            if section_items:
                note_lines.append(f"{list_name.upper()}")
                for item in section_items:
                    note_lines.append(f"{item}")
                note_lines.append("")  # empty line
        body = {
            "title": note_title,
            "body": {"text": {"text": "\n".join(note_lines)}},
        }
    else:
        items = []
        for list_name in list_items.keys():
            items.append(
                {
                    "text": {"text": f"{list_name.upper()}"},
                    "checked": False,
                    "childListItems": [{"text": {"text": item}, "checked": False} for item in list_items[list_name]],
                }
            )

        # Create the note body
        body = {
            "title": note_title,
            "body": {"list": {"listItems": items}},
        }

    result = service.notes().create(body=body).execute()
    return result


@click.command()
@click.option(
    "--credentials",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=DEFAULT_CREDENTIALS_PATH,
    show_default=True,
    help="Path to credentials file.",
)
@click.option(
    "--title",
    type=str,
    help="Title of the Google Keep note. Name of the Trello board will be used if not specified.",
)
@click.option(
    "--impersonated-user-email",
    type=str,
    default=DEFAULT_IMPERSONATED_USER_EMAIL,
    show_default=True,
    help="Email address of the user to impersonate.",
)
@click.option(
    "--text/--no-text",
    default=False,
    help="Create a text note instead of a checklist note. Default is False (checklist note).",
    show_default=False,
)
@click.argument(
    "trello_board",
    type=str,
)
@click.argument("list_items", nargs=-1)
def main(
    credentials: pathlib.Path,
    title: str,
    impersonated_user_email: str,
    text: bool,
    trello_board: str,
    list_items: list[str],
):
    """Extract items from Trello lists and create a Google Keep note.

    This command extracts items from specified Trello lists and creates
    a formatted Google Keep note. Specify list names as arguments.

    Example: trello2keep Kanban Ongoing Validating
    """
    if not title:
        title = trello_board
    _execute_main(trello_board, title, impersonated_user_email, text, list_items, credentials)


def _execute_main(
    trello_board: str,
    title: str,
    impersonated_user_email: str,
    text: bool,
    list_items: list[str],
    credentials: pathlib.Path,
):
    """Execute the main application logic.

    This is the main entry point for the application logic. It orchestrates the
    process of extracting items from specified Trello lists and creating
    a formatted Google Keep note with those items.

    Args:
        trello_board: The Trello board  name.
        title: The title for the created Google Keep note.
        impersonated_user_email: Email address of the user to impersonate
            when creating the Google Keep note.
        text: If True, create a text note instead of a checklist note.
        list_items: A tuple of list names to extract from the Trello board.
        credentials: Path to the credentials JSON file containing both
            Trello API credentials and Google service account credentials.

    The function will:
    1. Extract items from the specified Trello lists
    2. Print the extracted items as JSON to stdout
    3. Create a Google Keep note with the extracted items
    4. Print the created note's ID

    Raises:
        AssertionError: If the item extraction from Trello fails.
        Various API errors: If Google Keep note creation fails.
    """
    items = extract_list_items(trello_board, list_items, credentials_path=credentials)
    if items is None:
        raise click.ClickException("Failed to extract items from Trello. Please check your credentials and board ID.")
    keep_service = get_keep_service(credentials_path=credentials, impersonated_user_email=impersonated_user_email)
    note = create_google_keep_note(keep_service, title, items, text)
    click.secho(f'Google Keep note created: "{note.get("title")}" ({note.get("name")})', fg="green")


if __name__ == "__main__":
    main()
