import csv
import random

# Generate fake review comments
fake_comments = [
    "Horrendous service.",
    "Complete rip-off.",
    "Unacceptable experience.",
    "Disgusting food quality.",
    "Unprofessional staff.",
    "Total waste of money.",
    "Absolutely terrible.",
    "Don't waste your time here.",
    "Appalling taste.",
    "Subpar ingredients.",
    "Never coming back again.",
    "Worst restaurant ever.",
    "Ruined my evening.",
    "Stay clear of this place.",
    "Disastrous service.",
    "Overpriced and underwhelming.",
    "Regrettable experience.",
    "Absolutely appalling.",
    "Avoid at all costs.",
    "Unsatisfactory service.",
    "Disappointing from start to finish.",
    "Truly dreadful.",
    "Nothing redeeming about this place.",
    "Extremely disappointed.",
    "Not fit for human consumption.",
    "Deplorable service.",
    "Couldn't be worse.",
    "Utterly dreadful.",
    "Avoid like the plague.",
    "Shameful performance."
]

# Generate genuine review comments
genuine_comments = [
    "Outstanding service!",
    "Mouthwatering cuisine.",
    "Exceptional experience.",
    "Warm and welcoming staff.",
    "A must-visit spot.",
    "Unbeatable quality.",
    "Impressive flavors.",
    "Consistently excellent.",
    "Can't wait to return.",
    "Incredible atmosphere.",
    "Highly satisfying.",
    "Well worth the visit.",
    "Charming ambiance.",
    "Absolutely delightful.",
    "Exemplary service.",
    "Culinary delight.",
    "A gem of a place.",
    "Perfection on a plate.",
    "Truly enjoyable.",
    "Exceeds expectations.",
    "A class above the rest.",
    "Impeccable service.",
    "Unforgettable experience.",
    "Always a pleasure.",
    "Incredible value for money.",
    "A real treat.",
    "Phenomenal flavors.",
    "Unparalleled hospitality.",
    "Absolutely divine.",
    "A wonderful find."
]

# List of app names
app_names = ["KFC", "PizzaHut", "Dominos", "McDonalds", "Starbucks", "Subway", "BurgerKing"]

# Generate 500 fake and 500 genuine reviews for each app
records = []
for app in app_names:
    for i in range(500):
        if i < 250:
            label = 0  # Fake review
            comment = random.choice(fake_comments)
        else:
            label = 1  # Genuine review
            comment = random.choice(genuine_comments)
        rating = random.randint(1, 5)  # Random rating between 1 and 5
        records.append((app, rating, comment, label))

# Write records to CSV file
with open('reviews.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['app', 'rating', 'comment', 'label'])
    writer.writerows(records)

print("CSV file with 10000 records generated successfully.")
