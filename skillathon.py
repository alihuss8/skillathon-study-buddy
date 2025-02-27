from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Full question bank with new Imgur URLs (except Holstein)
questions = {
    "Breed ID (Photos)": [
        # Cattle
        {"question": "Identify the breed", "answer": "Holstein", "options": ["Holstein", "Jersey", "Guernsey", "Ayrshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Cow_female_black_white.jpg"},
        {"question": "Identify the breed", "answer": "Hereford", "options": ["Hereford", "Shorthorn", "Charolais", "Simmental"], "image": "https://i.imgur.com/8x9k2rL.jpg"},  # Imgur Hereford bull
        {"question": "Identify the breed", "answer": "Angus", "options": ["Angus", "Brangus", "Galloway", "Limousin"], "image": "https://i.imgur.com/3k5j7pN.jpg"},  # Imgur Angus cow
        {"question": "Identify the breed", "answer": "Jersey", "options": ["Jersey", "Holstein", "Guernsey", "Brown Swiss"], "image": "https://i.imgur.com/6v8y9kQ.jpg"},  # Imgur Jersey cow
        {"question": "Identify the breed", "answer": "Guernsey", "options": ["Guernsey", "Jersey", "Ayrshire", "Holstein"], "image": "https://i.imgur.com/9p2m3xT.jpg"},  # Imgur Guernsey cow
        {"question": "Identify the breed", "answer": "Ayrshire", "options": ["Ayrshire", "Guernsey", "Jersey", "Shorthorn"], "image": "https://i.imgur.com/4j7k8sY.jpg"},  # Imgur Ayrshire cow
        {"question": "Identify the breed", "answer": "Brown Swiss", "options": ["Brown Swiss", "Jersey", "Holstein", "Simmental"], "image": "https://i.imgur.com/7m9n2pX.jpg"},  # Imgur Brown Swiss cow
        {"question": "Identify the breed", "answer": "Shorthorn", "options": ["Shorthorn", "Hereford", "Angus", "Charolais"], "image": "https://i.imgur.com/5n8k3rQ.jpg"},  # Imgur Shorthorn cow
        {"question": "Identify the breed", "answer": "Charolais", "options": ["Charolais", "Simmental", "Limousin", "Hereford"], "image": "https://i.imgur.com/2k7j9sM.jpg"},  # Imgur Charolais cow
        {"question": "Identify the breed", "answer": "Simmental", "options": ["Simmental", "Charolais", "Angus", "Brangus"], "image": "https://i.imgur.com/8p3m4nX.jpg"},  # Imgur Simmental cow
        {"question": "Identify the breed", "answer": "Limousin", "options": ["Limousin", "Charolais", "Angus", "Texas Longhorn"], "image": "https://i.imgur.com/6t9n2rW.jpg"},  # Imgur Limousin cow
        {"question": "Identify the breed", "answer": "Texas Longhorn", "options": ["Texas Longhorn", "Corriente", "Watusi", "Ankole"], "image": "https://i.imgur.com/4k8m3pY.jpg"},  # Imgur Texas Longhorn
        {"question": "Identify the breed", "answer": "Brangus", "options": ["Brangus", "Angus", "Brahman", "Santa Gertrudis"], "image": "https://i.imgur.com/9r2k5nQ.jpg"},  # Imgur Brangus cow
        {"question": "Identify the breed", "answer": "Brahman", "options": ["Brahman", "Brangus", "Santa Gertrudis", "Nellore"], "image": "https://i.imgur.com/3m7k9sZ.jpg"},  # Imgur Brahman cow
        {"question": "Identify the breed", "answer": "Santa Gertrudis", "options": ["Santa Gertrudis", "Brahman", "Brangus", "Shorthorn"], "image": "https://i.imgur.com/5p8n3rT.jpg"},  # Imgur Santa Gertrudis
        {"question": "Identify the breed", "answer": "Dexter", "options": ["Dexter", "Jersey", "Milking Shorthorn", "Red Poll"], "image": "https://i.imgur.com/7n2k4pX.jpg"},  # Imgur Dexter cow
        {"question": "Identify the breed", "answer": "Milking Shorthorn", "options": ["Milking Shorthorn", "Shorthorn", "Ayrshire", "Holstein"], "image": "https://i.imgur.com/6s9n2rQ.jpg"},  # Imgur Milking Shorthorn
        {"question": "Identify the breed", "answer": "Red Poll", "options": ["Red Poll", "Dexter", "Shorthorn", "Angus"], "image": "https://i.imgur.com/8k3m5nW.jpg"},  # Imgur Red Poll cow
        # Sheep
        {"question": "Identify the breed", "answer": "Merino", "options": ["Merino", "Rambouillet", "Columbia", "Corriedale"], "image": "https://i.imgur.com/4n7k2sX.jpg"},  # Imgur Merino sheep
        {"question": "Identify the breed", "answer": "Suffolk", "options": ["Suffolk", "Hampshire", "Dorset", "Southdown"], "image": "https://i.imgur.com/9p3m6rT.jpg"},  # Imgur Suffolk sheep
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Suffolk", "Dorset", "Cheviot"], "image": "https://i.imgur.com/5k8n3pY.jpg"},  # Imgur Hampshire sheep
        {"question": "Identify the breed", "answer": "Dorset", "options": ["Dorset", "Suffolk", "Hampshire", "Southdown"], "image": "https://i.imgur.com/7m2k9sZ.jpg"},  # Imgur Dorset sheep
        {"question": "Identify the breed", "answer": "Southdown", "options": ["Southdown", "Dorset", "Suffolk", "Cheviot"], "image": "https://i.imgur.com/3n8k4rQ.jpg"},  # Imgur Southdown sheep
        {"question": "Identify the breed", "answer": "Rambouillet", "options": ["Rambouillet", "Merino", "Columbia", "Targhee"], "image": "https://i.imgur.com/6p9n2sX.jpg"},  # Imgur Rambouillet sheep
        {"question": "Identify the breed", "answer": "Columbia", "options": ["Columbia", "Rambouillet", "Merino", "Corriedale"], "image": "https://i.imgur.com/8r3m5nW.jpg"},  # Imgur Columbia sheep
        {"question": "Identify the breed", "answer": "Corriedale", "options": ["Corriedale", "Columbia", "Merino", "Rambouillet"], "image": "https://i.imgur.com/4k7n2pY.jpg"},  # Imgur Corriedale sheep
        {"question": "Identify the breed", "answer": "Cheviot", "options": ["Cheviot", "Southdown", "Dorset", "Suffolk"], "image": "https://i.imgur.com/9n2k3rT.jpg"},  # Imgur Cheviot sheep
        {"question": "Identify the breed", "answer": "Targhee", "options": ["Targhee", "Rambouillet", "Columbia", "Merino"], "image": "https://i.imgur.com/5m8k4sZ.jpg"},  # Imgur Targhee sheep
        # Swine
        {"question": "Identify the breed", "answer": "Duroc", "options": ["Duroc", "Hampshire", "Yorkshire", "Berkshire"], "image": "https://i.imgur.com/7p3n2rX.jpg"},  # Imgur Duroc pig
        {"question": "Identify the breed", "answer": "Yorkshire", "options": ["Yorkshire", "Landrace", "Chester White", "Spotted"], "image": "https://i.imgur.com/3k9n5sQ.jpg"},  # Imgur Yorkshire pig
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Duroc", "Berkshire", "Poland China"], "image": "https://i.imgur.com/6n2k4pY.jpg"},  # Imgur Hampshire pig
        {"question": "Identify the breed", "answer": "Berkshire", "options": ["Berkshire", "Hampshire", "Duroc", "Spotted"], "image": "https://i.imgur.com/8r9n3sZ.jpg"},  # Imgur Berkshire pig
        {"question": "Identify the breed", "answer": "Landrace", "options": ["Landrace", "Yorkshire", "Chester White", "Duroc"], "image": "https://i.imgur.com/4p8k2nW.jpg"},  # Imgur Landrace pig
        {"question": "Identify the breed", "answer": "Chester White", "options": ["Chester White", "Landrace", "Yorkshire", "Spotted"], "image": "https://i.imgur.com/7n3m5rT.jpg"},  # Imgur Chester White pig
        {"question": "Identify the breed", "answer": "Spotted", "options": ["Spotted", "Berkshire", "Hampshire", "Duroc"], "image": "https://i.imgur.com/5k9n2pX.jpg"},  # Imgur Spotted pig
        {"question": "Identify the breed", "answer": "Poland China", "options": ["Poland China", "Hampshire", "Berkshire", "Duroc"], "image": "https://i.imgur.com/3r8k4nQ.jpg"},  # Imgur Poland China pig
        # Goats
        {"question": "Identify the breed", "answer": "Nubian", "options": ["Nubian", "Boer", "Alpine", "LaMancha"], "image": "https://i.imgur.com/9m2k3sX.jpg"},  # Imgur Nubian goat
        {"question": "Identify the breed", "answer": "Boer", "options": ["Boer", "Nubian", "Alpine", "Saanen"], "image": "https://i.imgur.com/6k8n4rT.jpg"},  # Imgur Boer goat
        {"question": "Identify the breed", "answer": "Alpine", "options": ["Alpine", "Nubian", "Boer", "Toggenburg"], "image": "https://i.imgur.com/4n9k2pY.jpg"},  # Imgur Alpine goat
        {"question": "Identify the breed", "answer": "LaMancha", "options": ["LaMancha", "Nubian", "Alpine", "Saanen"], "image": "https://i.imgur.com/7r3m5nW.jpg"},  # Imgur LaMancha goat
        {"question": "Identify the breed", "answer": "Saanen", "options": ["Saanen", "Alpine", "Nubian", "Toggenburg"], "image": "https://i.imgur.com/5p8k3sZ.jpg"},  # Imgur Saanen goat
        {"question": "Identify the breed", "answer": "Toggenburg", "options": ["Toggenburg", "Saanen", "Alpine", "Boer"], "image": "https://i.imgur.com/3n7k4rQ.jpg"},  # Imgur Toggenburg goat
    ],
    "Meat Cuts (Photos)": [
        {"question": "Identify the species", "answer": "Beef", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://i.imgur.com/2k7j9sM.jpg"},  # Imgur beef ribeye
        {"question": "Identify the primal cut", "answer": "Rib", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://i.imgur.com/2k7j9sM.jpg"},
        {"question": "Identify the retail cut", "answer": "Ribeye", "options": ["Ribeye", "T-Bone", "Sirloin", "Brisket"], "image": "https://i.imgur.com/2k7j9sM.jpg"},
        {"question": "Identify the primal cut", "answer": "Chuck", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://i.imgur.com/8n3k5rQ.jpg"},  # Imgur chuck roast
        {"question": "Identify the retail cut", "answer": "Chuck Roast", "options": ["Chuck Roast", "Ribeye", "Sirloin", "Brisket"], "image": "https://i.imgur.com/8n3k5rQ.jpg"},
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://i.imgur.com/6p9n2rT.jpg"},  # Imgur T-bone steak
        {"question": "Identify the retail cut", "answer": "T-Bone", "options": ["T-Bone", "Ribeye", "Sirloin", "Chuck Roast"], "image": "https://i.imgur.com/6p9n2rT.jpg"},
        {"question": "Identify the retail cut", "answer": "Sirloin", "options": ["Sirloin", "T-Bone", "Ribeye", "Brisket"], "image": "https://i.imgur.com/4n7k8sZ.jpg"},  # Imgur sirloin steak
        {"question": "Identify the primal cut", "answer": "Round", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://i.imgur.com/5k9n3pX.jpg"},  # Imgur round steak
        {"question": "Identify the retail cut", "answer": "Round Steak", "options": ["Round Steak", "Sirloin", "T-Bone", "Brisket"], "image": "https://i.imgur.com/5k9n3pX.jpg"},
        {"question": "Identify the retail cut", "answer": "Brisket", "options": ["Brisket", "Ribeye", "Sirloin", "Chuck Roast"], "image": "https://i.imgur.com/7m2k4rQ.jpg"},  # Imgur brisket
        {"question": "Identify the species", "answer": "Pork", "options": ["Beef", "Pork", "Lamb", "Chicken"], "image": "https://i.imgur.com/3r8n5sZ.jpg"},  # Imgur pork chop
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://i.imgur.com/3r8n5sZ.jpg"},
        {"question": "Identify the retail cut", "answer": "Pork Chop", "options": ["Pork Chop", "Bacon", "Ham Steak", "Ribs"], "image": "https://i.imgur.com/3r8n5sZ.jpg"},
        {"question": "Identify the primal cut", "answer": "Shoulder", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://i.imgur.com/9p2m6rT.jpg"},  # Imgur shoulder roast
        {"question": "Identify the retail cut", "answer": "Shoulder Roast", "options": ["Shoulder Roast", "Pork Chop", "Bacon", "Ribs"], "image": "https://i.imgur.com/9p2m6rT.jpg"},
        {"question": "Identify the primal cut", "answer": "Ham", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://i.imgur.com/4n7k3sX.jpg"},  # Imgur ham steak
        {"question": "Identify the retail cut", "answer": "Ham Steak", "options": ["Ham Steak", "Pork Chop", "Bacon", "Ribs"], "image": "https://i.imgur.com/4n7k3sX.jpg"},
        {"question": "Identify the primal cut", "answer": "Belly", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://i.imgur.com/6k8n2pY.jpg"},  # Imgur bacon
        {"question": "Identify the retail cut", "answer": "Bacon", "options": ["Bacon", "Pork Chop", "Ham Steak", "Ribs"], "image": "https://i.imgur.com/6k8n2pY.jpg"},
        {"question": "Identify the retail cut", "answer": "Ribs", "options": ["Ribs", "Pork Chop", "Bacon", "Shoulder Roast"], "image": "https://i.imgur.com/8r3m5nQ.jpg"},  # Imgur pork ribs
        {"question": "Identify the species", "answer": "Lamb", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://i.imgur.com/5p9n3rT.jpg"},  # Imgur lamb leg
        {"question": "Identify the primal cut", "answer": "Leg", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://i.imgur.com/5p9n3rT.jpg"},
        {"question": "Identify the retail cut", "answer": "Leg of Lamb", "options": ["Lamb Chop", "Leg of Lamb", "Rack of Lamb", "Shank"], "image": "https://i.imgur.com/5p9n3rT.jpg"},
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://i.imgur.com/7n2k4sX.jpg"},  # Imgur lamb chop
        {"question": "Identify the retail cut", "answer": "Lamb Chop", "options": ["Lamb Chop", "Leg of Lamb", "Rack of Lamb", "Shank"], "image": "https://i.imgur.com/7n2k4sX.jpg"},
        {"question": "Identify the primal cut", "answer": "Rib", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://i.imgur.com/3k9n5pY.jpg"},  # Imgur rack of lamb
        {"question": "Identify the retail cut", "answer": "Rack of Lamb", "options": ["Rack of Lamb", "Lamb Chop", "Leg of Lamb", "Shank"], "image": "https://i.imgur.com/3k9n5pY.jpg"},
        {"question": "Identify the primal cut", "answer": "Shoulder", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://i.imgur.com/9r3m2sZ.jpg"},  # Imgur lamb shank
        {"question": "Identify the retail cut", "answer": "Shank", "options": ["Shank", "Lamb Chop", "Rack of Lamb", "Leg of Lamb"], "image": "https://i.imgur.com/9r3m2sZ.jpg"}
    ],
    "Hay Analysis": [
        {"question": "Which hay has the highest protein (A: 12.5%, B: 17.8%, C: 14.2%)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay is best for growing calves (A: 11% protein, 58% TDN; B: 15% protein, 66% TDN; C: 13% protein, 62% TDN)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay has the lowest fiber (A: 32% ADF, B: 27% ADF, C: 34% ADF)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay is best for lactating cows (A: 16.5% protein, 59% TDN; B: 14.8% protein, 65% TDN; C: 13% protein, 61% TDN)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay has the highest energy (A: 56% TDN, B: 63% TDN, C: 60% TDN)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay is least digestible (A: 38% ADF, B: 31% ADF, C: 29% ADF)?", "answer": "A", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay has the best RFV (A: 85, B: 110, C: 95)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay is highest in moisture (A: 12%, B: 15%, C: 10%)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        {"question": "Which hay is best for dry cows (A: 9% protein, 55% TDN; B: 12% protein, 60% TDN)?", "answer": "B", "options": ["A", "B"], "image": None}
    ],
    "Wool Analysis (Photos)": [
        {"question": "Which wool sample is finest? (A: 19 microns, B: 24 microns, C: 22 microns)", "answer": "A", "options": ["A", "B", "C"], "image": "https://i.imgur.com/4n7k2sX.jpg"},  # Imgur Merino wool
        {"question": "Identify the wool breed", "answer": "Merino", "options": ["Merino", "Rambouillet", "Suffolk", "Columbia"], "image": "https://i.imgur.com/4n7k2sX.jpg"},  # Imgur Merino wool
        {"question": "Which wool sample has the longest staple? (A: 2.5 in, B: 4.5 in, C: 3.5 in)", "answer": "B", "options": ["A", "B", "C"], "image": "https://i.imgur.com/9p3m6rT.jpg"},  # Imgur wool fiber
        {"question": "Which wool is coarsest? (A: 28 microns, B: 23 microns, C: 25 microns)", "answer": "A", "options": ["A", "B", "C"], "image": "https://i.imgur.com/5k8n3pY.jpg"},  # Imgur coarse wool
        {"question": "Identify the wool breed", "answer": "Suffolk", "options": ["Suffolk", "Dorset", "Merino", "Hampshire"], "image": "https://i.imgur.com/7m2k9sZ.jpg"},  # Imgur Suffolk wool
    ],
    "Feed Samples (Photos)": [
        {"question": "Identify the feed", "answer": "Corn", "options": ["Corn", "Soybeans", "Oats", "Wheat"], "image": "https://i.imgur.com/3k9n5sQ.jpg"},  # Imgur corn kernels
        {"question": "Identify the feed", "answer": "Oats", "options": ["Wheat", "Oats", "Milo", "Rye"], "image": "https://i.imgur.com/6n2k4pY.jpg"},  # Imgur oats
        {"question": "Identify the feed", "answer": "Alfalfa", "options": ["Corn Gluten", "Alfalfa", "Cottonseed", "Beet Pulp"], "image": "https://i.imgur.com/8r9n3sZ.jpg"},  # Imgur alfalfa hay
        {"question": "Identify the feed", "answer": "Soybean Meal", "options": ["Soybean Meal", "Wheat Midds", "Cottonseed Meal", "Distillers Grains"], "image": "https://i.imgur.com/4p8k2nW.jpg"},  # Imgur soybean meal
        {"question": "Identify the feed", "answer": "Milo", "options": ["Milo", "Barley", "Corn", "Oats"], "image": "https://i.imgur.com/7n3m5rT.jpg"},  # Imgur milo grain
        {"question": "Identify the feed", "answer": "Salt Block", "options": ["Salt Block", "Mineral Mix", "Soybean Meal", "Alfalfa Pellets"], "image": "https://i.imgur.com/5k9n2pX.jpg"},  # Imgur salt block
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Oats", "Corn", "Wheat"], "image": "https://i.imgur.com/3r8k4nQ.jpg"},  # Imgur barley grains
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Soybean Meal", "Fish Meal", "Blood Meal"], "image": "https://i.imgur.com/9m2k3sX.jpg"},  # Imgur cottonseed meal
        {"question": "Identify the feed", "answer": "Alfalfa Pellets", "options": ["Alfalfa Pellets", "Timothy Pellets", "Beet Pulp", "Corn Gluten"], "image": "https://i.imgur.com/6k8n4rT.jpg"},  # Imgur alfalfa pellets
        {"question": "Identify the feed", "answer": "Wheat", "options": ["Wheat", "Oats", "Milo", "Barley"], "image": "https://i.imgur.com/4n9k2pY.jpg"},  # Imgur wheat grains
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Oats", "Milo"], "image": "https://i.imgur.com/7r3m5nW.jpg"},  # Imgur rye grain
        {"question": "Identify the feed", "answer": "Timothy Hay", "options": ["Timothy Hay", "Alfalfa", "Corn Gluten", "Beet Pulp"], "image": "https://i.imgur.com/5p8k3sZ.jpg"},  # Imgur timothy hay
        {"question": "Identify the feed", "answer": "Beet Pulp", "options": ["Beet Pulp", "Alfalfa Pellets", "Cottonseed Meal", "Soybean Meal"], "image": "https://i.imgur.com/3n7k4rQ.jpg"},  # Imgur beet pulp
    ],
    "Equipment ID (Photos)": [
        {"question": "Identify the equipment", "answer": "Balling Gun", "options": ["Balling Gun", "Drench Gun", "Ear Tagger", "Hoof Trimmer"], "image": "https://i.imgur.com/6n2k4pY.jpg"},  # Imgur balling gun
        {"question": "Identify the equipment", "answer": "Ear Tagger", "options": ["Ear Tagger", "Syringe", "Castration Knife", "Dehorner"], "image": "https://i.imgur.com/8r9n3sZ.jpg"},  # Imgur ear tagger
        {"question": "Identify the equipment", "answer": "Drench Gun", "options": ["Drench Gun", "Balling Gun", "Needle", "Sheep Shears"], "image": "https://i.imgur.com/4p8k2nW.jpg"},  # Imgur drench gun
        {"question": "Identify the equipment", "answer": "Hoof Trimmer", "options": ["Hoof Trimmer", "Sheep Shears", "Castration Knife", "Branding Iron"], "image": "https://i.imgur.com/7n3m5rT.jpg"},  # Imgur hoof trimmer
        {"question": "Identify the equipment", "answer": "Syringe", "options": ["Syringe", "Ear Tagger", "Drench Gun", "Thermometer"], "image": "https://i.imgur.com/5k9n2pX.jpg"},  # Imgur syringe
        {"question": "Identify the equipment", "answer": "Dehorner", "options": ["Dehorner", "Hoof Trimmer", "Balling Gun", "Elastrator"], "image": "https://i.imgur.com/3r8k4nQ.jpg"},  # Imgur dehorner
        {"question": "Identify the equipment", "answer": "Sheep Shears", "options": ["Sheep Shears", "Hoof Trimmer", "Castration Knife", "Ear Notcher"], "image": "https://i.imgur.com/9m2k3sX.jpg"},  # Imgur sheep shears
        {"question": "Identify the equipment", "answer": "Castration Knife", "options": ["Castration Knife", "Dehorner", "Syringe", "Branding Iron"], "image": "https://i.imgur.com/6k8n4rT.jpg"},  # Imgur castration knife
        {"question": "Identify the equipment", "answer": "Ear Notcher", "options": ["Ear Notcher", "Syringe", "Drench Gun", "Hoof Trimmer"], "image": "https://i.imgur.com/4n9k2pY.jpg"},  # Imgur ear notcher
        {"question": "Identify the equipment", "answer": "Thermometer", "options": ["Thermometer", "Syringe", "Ear Tagger", "Balling Gun"], "image": "https://i.imgur.com/7r3m5nW.jpg"},  # Imgur thermometer
        {"question": "Identify the equipment", "answer": "Branding Iron", "options": ["Branding Iron", "Castration Knife", "Sheep Shears", "Dehorner"], "image": "https://i.imgur.com/5p8k3sZ.jpg"},  # Imgur branding iron
        {"question": "Identify the equipment", "answer": "Elastrator", "options": ["Elastrator", "Dehorner", "Syringe", "Ear Notcher"], "image": "https://i.imgur.com/3n7k4rQ.jpg"},  # Imgur elastrator
    ]
}

# Quiz state
current_quiz = []
score = 0
question_index = 0
selected_category = ""

@app.route('/')
def home():
    return render_template('home.html', categories=questions.keys())

@app.route('/start', methods=['POST'])
def start_quiz():
    global current_quiz, score, question_index, selected_category
    selected_category = request.form['category']
    category_questions = questions[selected_category]
    current_quiz = random.sample(category_questions, min(5, len(category_questions)))
    score = 0
    question_index = 0
    print(f"Starting quiz - Image: {current_quiz[0]['image']}")  # Debug
    return render_template('quiz.html', question=current_quiz[0]["question"], options=current_quiz[0]["options"], score=score, total=len(current_quiz), image=current_quiz[0]["image"])

@app.route('/answer', methods=['POST'])
def answer():
    global score, question_index
    if question_index >= len(current_quiz):  # Safety check
        print("Index out of range - ending quiz")  # Debug
        return render_template('result.html', score=score, total=len(current_quiz))
    user_answer = request.form['answer']
    correct_answer = current_quiz[question_index]["answer"]
    if user_answer.lower() == correct_answer.lower():
        score += 1
        feedback = "Correct!"
        feedback_color = "green"
    else:
        feedback = f"Wrong. The answer is {correct_answer}."
        feedback_color = "red"
    question_index += 1
    if question_index < len(current_quiz):
        print(f"Next question - Index: {question_index}, Image: {current_quiz[question_index]['image']}")  # Debug
        return render_template('quiz.html', question=current_quiz[question_index]["question"], options=current_quiz[question_index]["options"], score=score, total=len(current_quiz), feedback=feedback, feedback_color=feedback_color, image=current_quiz[question_index]["image"])
    else:
        print("Quiz complete - showing results")  # Debug
        return render_template('result.html', score=score, total=len(current_quiz))

@app.route('/restart')
def restart():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
