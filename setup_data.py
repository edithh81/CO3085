import os
import json

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# Check if menu.json exists
if not os.path.exists("data/menu.json"):
    print("menu.json not found. Please create it first.")
else:
    print("Data setup complete!")
