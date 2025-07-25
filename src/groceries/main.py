import json
import csv
import click


@click.command()
@click.argument("json_file", type=click.Path(exists=True))
@click.argument("lists", nargs=-1)
def old(json_file, lists):
    """
    Export cards from the given lists from a Trello JSON export to a CSV file.

    JSON_FILE: Trello export file.
    LISTS: Names of lists to export (e.g. Lidl Carrefour)
    """
    # Read JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check for actions in the file
    if "actions" not in data:
        click.echo("Error: JSON file does not contain actions.")
        return

    # Get list names and associated cards
    cards = []
    for action in data["actions"]:
        if action["type"] == "createCard" and "list" in action["data"]:
            list_name = action["data"]["list"]["name"]
            if list_name.lower() in [l.lower() for l in lists]:
                card_name = action["data"]["card"]["name"]
                cards.append({"list": list_name, "item": card_name})

    if not cards:
        click.echo("No cards found in the specified lists.")
        return

    # Output file name
    csv_file = "courses_export.csv"

    # Write to CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["list", "item"])
        writer.writeheader()
        writer.writerows(cards)

    click.echo(f"{len(cards)} items exported to {csv_file}.")


@click.command()
@click.argument("json_file", type=click.Path(exists=True))
@click.argument("lists", nargs=-1)
def main(json_file, lists):
    """
    Generate a Google Keep note with checkboxes from a Trello JSON export.
    Order of lists: Lidl first, then Carrefour.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lists = [name.lower() for name in lists]

    if "cards" not in data:
        click.echo("Error: Invalid JSON file.")
        return

    list_items = {name: [] for name in lists}

    list_id_to_name = {
        it["id"]: it["name"].lower()
        for it in data["lists"]
        if it["name"].lower() in lists and not it["closed"]
    }
    list_ids = list(list_id_to_name.keys())

    for card in data["cards"]:
        if card["idList"] in list_ids and not card["closed"]:
            list_name = list_id_to_name.get(card["idList"])
            if list_name and list_name in lists:
                card_name = card["name"]
                list_items[list_name].append(card_name)

    # Generate the note content
    note_lines = []
    for list_name in lists:
        items = list_items.get(list_name, [])
        if items:
            note_lines.append(f"{list_name.upper()}")
            for item in items:
                note_lines.append(f"{item}")
            note_lines.append("")  # empty line

    note_text = "\n".join(note_lines)

    # Write to a text file
    with open("courses_keep_note.txt", "w", encoding="utf-8") as f:
        f.write(note_text)

    click.echo("Google Keep note generated in 'courses_keep_note.txt'.")


if __name__ == "__main__":
    main()
