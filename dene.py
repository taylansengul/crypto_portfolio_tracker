from rich.console import Console
from rich.table import Table
from rich.text import Text

# Create a table
table = Table()

# Add columns to the table
table.add_column("Column 1")
table.add_column("Column 2")

# Add rows with cells and style
row = table.add_row(Text("Styled Value 1", style="bold red"), Text("Styled Value 2", style="italic green"))

# Create a console
console = Console()

# Print the table
console.print(table)
