import json
import csv
import click


@click.command()
@click.argument("json_file", type=click.Path(exists=True))
@click.argument("lists", nargs=-1)
def main(json_file, lists):
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


if __name__ == "__main__":
    main()
