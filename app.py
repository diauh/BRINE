"""
app.py
------
The Flask web server for BRINE.

Routes:
    /             -> homepage + search form (GET and POST)
    /random-dive  -> returns one random document as JSON
"""

import random

from flask import Flask, jsonify, render_template, request

from search_engine import ALL_CATEGORIES, CATEGORIES, SearchEngine


app = Flask(__name__)

# Build the search engine once when the app starts
engine = SearchEngine()


# ----------------------------------------------------------------------
# Static content used by the homepage
# ----------------------------------------------------------------------
OCEAN_FACTS = [
    "More than 80% of the ocean has never been mapped, explored or even seen by humans.",
    "The ocean holds about 97% of all the water on Earth.",
    "The blue whale's heart can be as large as a small car.",
    "Sound travels about four times faster in water than it does in air.",
    "The deepest known point, Challenger Deep, lies almost 11,000 metres below the surface.",
    "Many deep-sea animals make their own light using a chemical reaction called bioluminescence.",
    "Coral reefs cover less than 1% of the seafloor but support about 25% of all marine species.",
    "The giant squid has the largest eye in the animal kingdom, up to 27 centimetres across.",
    "Around 70% of the oxygen we breathe is produced by marine plants and plankton.",
    "Pressure at the bottom of the Mariana Trench is over 1,000 times normal air pressure.",
]

CATEGORY_CARDS = [
    {
        "name": "Ocean Animals",
        "emoji": "🐋",
        "description": "Whales, sharks, dolphins and other animals of the open sea.",
    },
    {
        "name": "Deep Sea Life",
        "emoji": "🦑",
        "description": "Strange creatures that survive in the dark, cold deep ocean.",
    },
    {
        "name": "Ocean Habitats",
        "emoji": "🪸",
        "description": "Coral reefs, kelp forests, seagrass beds and vent ecosystems.",
    },
    {
        "name": "Ocean Depths",
        "emoji": "🌊",
        "description": "The layers of the ocean, from the sunlit surface down to the abyss.",
    },
    {
        "name": "Underwater Wonders",
        "emoji": "🔱",
        "description": "Trenches, seamounts and volcanoes hidden beneath the waves.",
    },
]


# ----------------------------------------------------------------------
# Homepage + search
# ----------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    query = ""
    selected_category = ALL_CATEGORIES
    results = []
    searched = False

    if request.method == "POST":
        query = (request.form.get("query") or "").strip()
        selected_category = (request.form.get("category") or ALL_CATEGORIES).strip()

        if selected_category not in CATEGORIES:
            selected_category = ALL_CATEGORIES

        results = engine.search(query, selected_category)
        searched = True

    return render_template(
        "index.html",
        query=query,
        selected_category=selected_category,
        results=results,
        searched=searched,
        categories=CATEGORIES,
        category_cards=CATEGORY_CARDS,
        fact=random.choice(OCEAN_FACTS),
    )


# ----------------------------------------------------------------------
# Random Dive feature
# ----------------------------------------------------------------------
@app.route("/random-dive")
def random_dive():
    document = engine.random_document()
    return jsonify(document)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)