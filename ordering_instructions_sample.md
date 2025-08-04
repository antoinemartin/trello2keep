# Sample Ordering Instructions

This is a sample instructions file that demonstrates how to specify input and
output formats for grocery list organization using trello2keep.

## Purpose

This file serves as a template for creating custom ordering instructions that
can be used to organize list items, for instance in a specific order (e.g., by
store layout, category, or shopping route for a grocery items list).

## Input Format

The input consists of grocery items extracted from Trello lists in JSON format.
The structure contains a list of shopping lists, each with a name and items.

### JSON Structure

The input follows this JSON schema:

```json
{
    "lists": [
        {
            "name": "list_name",
            "items": ["item1", "item2", "item3"]
        }
    ]
}
```

### Example Input

```json
{
    "lists": [
        {
            "name": "whole_foods",
            "items": [
                "organic spinach",
                "grass-fed ground beef",
                "sourdough bread",
                "free-range eggs",
                "almond milk",
                "wild salmon fillet",
                "organic tomatoes",
                "aged cheddar cheese",
                "coconut oil",
                "greek yogurt",
                "avocados 3",
                "quinoa pasta",
                "olive oil extra virgin",
                "organic bananas"
            ]
        },
        {
            "name": "costco",
            "items": [
                "paper towels bulk pack",
                "dishwasher detergent",
                "frozen berries 2kg"
            ]
        }
    ]
}
```

## Output Format

The output should be a reorganized JSON structure following a specific order
that makes shopping more efficient, grouped by store sections or categories.

### Organization Principles

1. **Store Layout Order**: Arrange items according to typical grocery store
   layout
2. **Category Grouping**: Group similar items together within each store
3. **Shopping Route**: Order items to minimize backtracking in the store

### Example Output (Store Layout Order)

```json
{
    "lists": [
        {
            "name": "whole_foods",
            "items": [
                "organic spinach",
                "organic tomatoes",
                "organic bananas",
                "avocados 3",
                "almond milk",
                "greek yogurt",
                "aged cheddar cheese",
                "free-range eggs",
                "grass-fed ground beef",
                "wild salmon fillet",
                "coconut oil",
                "olive oil extra virgin",
                "quinoa pasta",
                "sourdough bread"
            ]
        },
        {
            "name": "costco",
            "items": [
                "frozen berries 2kg",
                "dishwasher detergent",
                "paper towels bulk pack"
            ]
        }
    ]
}
```

## Customization Instructions

To create your own ordering instructions:

1. **Analyze Your Store**: Map out the layout of your regular grocery store
2. **Define Categories**: Create logical groupings (Produce, Dairy, Meat, etc.)
3. **Establish Order**: Determine the most efficient shopping route
4. **Create Rules**: Define how items should be categorized and ordered

### Store Layout Template

```
1. Produce (fruits, vegetables)
2. Dairy (milk, cheese, yogurt)
3. Meat & Seafood
4. Frozen Foods
5. Pantry/Dry Goods (rice, pasta, canned goods)
6. Condiments & Oils
7. Bakery
8. Household Items
```

## Implementation Notes

-   The JSON structure must be preserved in both input and output
-   Items not matching any category should be placed at the end of their
    respective list
-   Case-insensitive matching should be used for item names
-   Consider common variations of item names (e.g., "greek yogurt" → Dairy
    section)
-   Maintain original item names and quantities while organizing by category
-   Each store list should be organized according to that specific store's
    layout

## Example Use Case

**Scenario**: Shopping at multiple stores with different layouts

**Input Process**:

1. Extract items from Trello lists: "Whole Foods Shopping", "Costco Bulk Items"
2. Apply AI filtering with ordering instructions to reorganize items by store
   layout
3. Create Google Keep note with organized sections for each store

**Result**: A shopping list organized by store layout for each location,
reducing shopping time and ensuring optimal routes through different stores.

---

_This is a sample template. Create your own `ordering_instructions.md` file with
store-specific or personal preferences for optimal grocery shopping
organization._
