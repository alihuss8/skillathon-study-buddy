from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Expanded question bank from provided resources
questions = {
    "Breed ID (Photos)": [
        # Cattle (ANLS p. 11-12, Breed ID p. 2-5)
        {"question": "Identify the breed", "answer": "Holstein", "options": ["Holstein", "Jersey", "Guernsey", "Ayrshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Holstein_cow.jpg"},
        {"question": "Identify the breed", "answer": "Hereford", "options": ["Hereford", "Shorthorn", "Charolais", "Simmental"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Hereford_bull_large.jpg"},
        {"question": "Identify the breed", "answer": "Angus", "options": ["Angus", "Brangus", "Galloway", "Limousin"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Angus_cow_%28bred%29_standing_in_farm_yard.jpg"},
        {"question": "Identify the breed", "answer": "Jersey", "options": ["Jersey", "Holstein", "Guernsey", "Brown Swiss"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Jersey_cow_in_Jersey.jpg"},
        {"question": "Identify the breed", "answer": "Guernsey", "options": ["Guernsey", "Jersey", "Ayrshire", "Holstein"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Guernsey_cow_-_Ohio.jpg"},
        {"question": "Identify the breed", "answer": "Ayrshire", "options": ["Ayrshire", "Guernsey", "Jersey", "Shorthorn"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Ayrshire_cow.jpg"},
        {"question": "Identify the breed", "answer": "Brown Swiss", "options": ["Brown Swiss", "Jersey", "Holstein", "Simmental"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Brown_Swiss_cow.jpg"},
        {"question": "Identify the breed", "answer": "Shorthorn", "options": ["Shorthorn", "Hereford", "Angus", "Charolais"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Shorthorn_cow.jpg"},
        {"question": "Identify the breed", "answer": "Charolais", "options": ["Charolais", "Simmental", "Limousin", "Hereford"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Charolais_bull.jpg"},
        {"question": "Identify the breed", "answer": "Simmental", "options": ["Simmental", "Charolais", "Angus", "Brangus"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Simmental_cow.jpg"},
        {"question": "Identify the breed", "answer": "Limousin", "options": ["Limousin", "Charolais", "Angus", "Texas Longhorn"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Limousin_bull.jpg"},
        {"question": "Identify the breed", "answer": "Texas Longhorn", "options": ["Texas Longhorn", "Corriente", "Watusi", "Ankole"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Texas_Longhorn_in_Liberal%2C_Kansas_%2827609245310%29.jpg"},
        {"question": "Identify the breed", "answer": "Brangus", "options": ["Brangus", "Angus", "Brahman", "Santa Gertrudis"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Brangus_cow.jpg"},
        {"question": "Identify the breed", "answer": "Brahman", "options": ["Brahman", "Brangus", "Santa Gertrudis", "Nellore"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Brahman_cow.jpg"},
        {"question": "Identify the breed", "answer": "Santa Gertrudis", "options": ["Santa Gertrudis", "Brahman", "Brangus", "Shorthorn"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Santa_Gertrudis_cow.jpg"},
        {"question": "Identify the breed", "answer": "Dexter", "options": ["Dexter", "Jersey", "Milking Shorthorn", "Red Poll"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Dexter_cow_2.jpg"},
        {"question": "Identify the breed", "answer": "Milking Shorthorn", "options": ["Milking Shorthorn", "Shorthorn", "Ayrshire", "Holstein"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Milking_Shorthorn_cow.jpg"},
        {"question": "Identify the breed", "answer": "Red Poll", "options": ["Red Poll", "Dexter", "Shorthorn", "Angus"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Red_Poll_cow.jpg"},
        # Sheep (ANLS p. 12, Breed ID p. 6-7)
        {"question": "Identify the breed", "answer": "Merino", "options": ["Merino", "Rambouillet", "Columbia", "Corriedale"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Merino_sheep_Dan_Needham.jpg"},
        {"question": "Identify the breed", "answer": "Suffolk", "options": ["Suffolk", "Hampshire", "Dorset", "Southdown"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Suffolk_sheep_02.jpg"},
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Suffolk", "Dorset", "Cheviot"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Hampshire_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Dorset", "options": ["Dorset", "Suffolk", "Hampshire", "Southdown"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Dorset_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Southdown", "options": ["Southdown", "Dorset", "Suffolk", "Cheviot"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Southdown_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Rambouillet", "options": ["Rambouillet", "Merino", "Columbia", "Targhee"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Rambouillet_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Columbia", "options": ["Columbia", "Rambouillet", "Merino", "Corriedale"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Columbia_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Corriedale", "options": ["Corriedale", "Columbia", "Merino", "Rambouillet"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Corriedale_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Cheviot", "options": ["Cheviot", "Southdown", "Dorset", "Suffolk"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Cheviot_sheep.jpg"},
        {"question": "Identify the breed", "answer": "Targhee", "options": ["Targhee", "Rambouillet", "Columbia", "Merino"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Targhee_sheep.jpg"},
        # Swine (ANLS p. 12, Breed ID p. 8-9)
        {"question": "Identify the breed", "answer": "Duroc", "options": ["Duroc", "Hampshire", "Yorkshire", "Berkshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Duroc_boar.jpg"},
        {"question": "Identify the breed", "answer": "Yorkshire", "options": ["Yorkshire", "Landrace", "Chester White", "Spotted"], "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Yorkshire_pig_-_geograph.org.uk_-_1504378.jpg"},
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Duroc", "Berkshire", "Poland China"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Hampshire_pig.jpg"},
        {"question": "Identify the breed", "answer": "Berkshire", "options": ["Berkshire", "Hampshire", "Duroc", "Spotted"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Berkshire_pig.jpg"},
        {"question": "Identify the breed", "answer": "Landrace", "options": ["Landrace", "Yorkshire", "Chester White", "Duroc"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Landrace_pig.jpg"},
        {"question": "Identify the breed", "answer": "Chester White", "options": ["Chester White", "Landrace", "Yorkshire", "Spotted"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Chester_White_pig.jpg"},
        {"question": "Identify the breed", "answer": "Spotted", "options": ["Spotted", "Berkshire", "Hampshire", "Duroc"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Spotted_pig.jpg"},
        {"question": "Identify the breed", "answer": "Poland China", "options": ["Poland China", "Hampshire", "Berkshire", "Duroc"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Poland_China_pig.jpg"},
        # Goats (ANLS p. 13, Breed ID p. 10-11)
        {"question": "Identify the breed", "answer": "Nubian", "options": ["Nubian", "Boer", "Alpine", "LaMancha"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Nubian_Goat.jpg"},
        {"question": "Identify the breed", "answer": "Boer", "options": ["Boer", "Nubian", "Alpine", "Saanen"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Boer_goat.jpg"},
        {"question": "Identify the breed", "answer": "Alpine", "options": ["Alpine", "Nubian", "Boer", "Toggenburg"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Alpine_goat.jpg"},
        {"question": "Identify the breed", "answer": "LaMancha", "options": ["LaMancha", "Nubian", "Alpine", "Saanen"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/LaMancha_goat.jpg"},
        {"question": "Identify the breed", "answer": "Saanen", "options": ["Saanen", "Alpine", "Nubian", "Toggenburg"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Saanen_goat.jpg"},
        {"question": "Identify the breed", "answer": "Toggenburg", "options": ["Toggenburg", "Saanen", "Alpine", "Boer"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Toggenburg_goat.jpg"}
    ],
    "Meat Cuts (Photos)": [
        # Beef (ANLS p. 17-18)
        {"question": "Identify the species", "answer": "Beef", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        {"question": "Identify the primal cut", "answer": "Rib", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "Ribeye", "options": ["Ribeye", "T-Bone", "Sirloin", "Brisket"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        {"question": "Identify the primal cut", "answer": "Chuck", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Chuck_roast.jpg"},
        {"question": "Identify the retail cut", "answer": "Chuck Roast", "options": ["Chuck Roast", "Ribeye", "Sirloin", "Brisket"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Chuck_roast.jpg"},
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/T-bone_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "T-Bone", "options": ["T-Bone", "Ribeye", "Sirloin", "Chuck Roast"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/T-bone_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "Sirloin", "options": ["Sirloin", "T-Bone", "Ribeye", "Brisket"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Sirloin_steak.jpg"},
        {"question": "Identify the primal cut", "answer": "Round", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Round_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "Round Steak", "options": ["Round Steak", "Sirloin", "T-Bone", "Brisket"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Round_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "Brisket", "options": ["Brisket", "Ribeye", "Sirloin", "Chuck Roast"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Beef_brisket.jpg"},
        # Pork (ANLS p. 18)
        {"question": "Identify the species", "answer": "Pork", "options": ["Beef", "Pork", "Lamb", "Chicken"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        {"question": "Identify the retail cut", "answer": "Pork Chop", "options": ["Pork Chop", "Bacon", "Ham Steak", "Ribs"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        {"question": "Identify the primal cut", "answer": "Shoulder", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Pork_shoulder_roast.jpg"},
        {"question": "Identify the retail cut", "answer": "Shoulder Roast", "options": ["Shoulder Roast", "Pork Chop", "Bacon", "Ribs"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Pork_shoulder_roast.jpg"},
        {"question": "Identify the primal cut", "answer": "Ham", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Ham_steak.jpg"},
        {"question": "Identify the retail cut", "answer": "Ham Steak", "options": ["Ham Steak", "Pork Chop", "Bacon", "Ribs"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Ham_steak.jpg"},
        {"question": "Identify the primal cut", "answer": "Belly", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Bacon.jpg"},
        {"question": "Identify the retail cut", "answer": "Bacon", "options": ["Bacon", "Pork Chop", "Ham Steak", "Ribs"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Bacon.jpg"},
        {"question": "Identify the retail cut", "answer": "Ribs", "options": ["Ribs", "Pork Chop", "Bacon", "Shoulder Roast"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Pork_ribs.jpg"},
        # Lamb (ANLS p. 19)
        {"question": "Identify the species", "answer": "Lamb", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        {"question": "Identify the primal cut", "answer": "Leg", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        {"question": "Identify the retail cut", "answer": "Leg of Lamb", "options": ["Lamb Chop", "Leg of Lamb", "Rack of Lamb", "Shank"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        {"question": "Identify the primal cut", "answer": "Loin", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Lamb_chop.jpg"},
        {"question": "Identify the retail cut", "answer": "Lamb Chop", "options": ["Lamb Chop", "Leg of Lamb", "Rack of Lamb", "Shank"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Lamb_chop.jpg"},
        {"question": "Identify the primal cut", "answer": "Rib", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Rack_of_lamb.jpg"},
        {"question": "Identify the retail cut", "answer": "Rack of Lamb", "options": ["Rack of Lamb", "Lamb Chop", "Leg of Lamb", "Shank"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Rack_of_lamb.jpg"},
        {"question": "Identify the primal cut", "answer": "Shoulder", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_shank.jpg"},
        {"question": "Identify the retail cut", "answer": "Shank", "options": ["Shank", "Lamb Chop", "Rack of Lamb", "Leg of Lamb"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_shank.jpg"}
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
        {"question": "Which wool sample is finest? (A: 19 microns, B: 24 microns, C: 22 microns)", "answer": "A", "options": ["A", "B", "C"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Merino_wool_closeup.jpg"},
        {"question": "Identify the wool breed", "answer": "Merino", "options": ["Merino", "Rambouillet", "Suffolk", "Columbia"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Merino_wool_closeup.jpg"},
        {"question": "Which wool sample has the longest staple? (A: 2.5 in, B: 4.5 in, C: 3.5 in)", "answer": "B", "options": ["A", "B", "C"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Wool_fiber.jpg"},
        {"question": "Which wool is coarsest? (A: 28 microns, B: 23 microns, C: 25 microns)", "answer": "A", "options": ["A", "B", "C"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Wool_sample.jpg"},
        {"question": "Identify the wool breed", "answer": "Suffolk", "options": ["Suffolk", "Dorset", "Merino", "Hampshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Suffolk_wool.jpg"}
    ],
    "Feed Samples (Photos)": [  # Purdue p. 7-9
        {"question": "Identify the feed", "answer": "Corn", "options": ["Corn", "Soybeans", "Oats", "Wheat"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Corn_kernels.jpg"},
        {"question": "Identify the feed", "answer": "Oats", "options": ["Wheat", "Oats", "Milo", "Rye"], "image": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Oats_closeup.jpg"},
        {"question": "Identify the feed", "answer": "Alfalfa", "options": ["Corn Gluten", "Alfalfa", "Cottonseed", "Beet Pulp"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Alfalfa_hay.jpg"},
        {"question": "Identify the feed", "answer": "Soybean Meal", "options": ["Soybean Meal", "Wheat Midds", "Cottonseed Meal", "Distillers Grains"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Soybean_meal.jpg"},
        {"question": "Identify the feed", "answer": "Milo", "options": ["Milo", "Barley", "Corn", "Oats"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Milo_grain.jpg"},
        {"question": "Identify the feed", "answer": "Salt Block", "options": ["Salt Block", "Mineral Mix", "Soybean Meal", "Alfalfa Pellets"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Salt_block.jpg"},
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Oats", "Corn", "Wheat"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Barley_grains.jpg"},
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Soybean Meal", "Fish Meal", "Blood Meal"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Cottonseed_meal.jpg"},
        {"question": "Identify the feed", "answer": "Alfalfa Pellets", "options": ["Alfalfa Pellets", "Timothy Pellets", "Beet Pulp", "Corn Gluten"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Alfalfa_pellets.jpg"},
        {"question": "Identify the feed", "answer": "Wheat", "options": ["Wheat", "Oats", "Milo", "Barley"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Wheat_grains.jpg"},
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Oats", "Milo"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Rye_grain.jpg"},
        {"question": "Identify the feed", "answer": "Timothy Hay", "options": ["Timothy Hay", "Alfalfa", "Corn Gluten", "Beet Pulp"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Timothy_hay.jpg"},
        {"question": "Identify the feed", "answer": "Beet Pulp", "options": ["Beet Pulp", "Alfalfa Pellets", "Cottonseed Meal", "Soybean Meal"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Beet_pulp.jpg"}
    ],
    "Equipment ID (Photos)": [  # Equipment ID p. 1-8
        {"question": "Identify the equipment", "answer": "Balling Gun", "options": ["Balling Gun", "Drench Gun", "Ear Tagger", "Hoof Trimmer"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Balling_gun.jpg"},
        {"question": "Identify the equipment", "answer": "Ear Tagger", "options": ["Ear Tagger", "Syringe", "Castration Knife", "Dehorner"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Ear_tagger.jpg"},
        {"question": "Identify the equipment", "answer": "Drench Gun", "options": ["Drench Gun", "Balling Gun", "Needle", "Sheep Shears"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Drench_gun.jpg"},
        {"question": "Identify the equipment", "answer": "Hoof Trimmer", "options": ["Hoof Trimmer", "Sheep Shears", "Castration Knife", "Branding Iron"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Hoof_trimmer.jpg"},
        {"question": "Identify the equipment", "answer": "Syringe", "options": ["Syringe", "Ear Tagger", "Drench Gun", "Thermometer"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Syringe.jpg"},
        {"question": "Identify the equipment", "answer": "Dehorner", "options": ["Dehorner", "Hoof Trimmer", "Balling Gun", "Elastrator"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Dehorner.jpg"},
        {"question": "Identify the equipment", "answer": "Sheep Shears", "options": ["Sheep Shears", "Hoof Trimmer", "Castration Knife", "Ear Notcher"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Sheep_shears.jpg"},
        {"question": "Identify the equipment", "answer": "Castration Knife", "options": ["Castration Knife", "Dehorner", "Syringe", "Branding Iron"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Castration_knife.jpg"},
        {"question": "Identify the equipment", "answer": "Ear Notcher", "options": ["Ear Notcher", "Syringe", "Drench Gun", "Hoof Trimmer"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Ear_notcher.jpg"},
        {"question": "Identify the equipment", "answer": "Thermometer", "options": ["Thermometer", "Syringe", "Ear Tagger", "Balling Gun"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Vet_thermometer.jpg"},
        {"question": "Identify the equipment", "answer": "Branding Iron", "options": ["Branding Iron", "Castration Knife", "Sheep Shears", "Dehorner"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Branding_iron.jpg"},
        {"question": "Identify the equipment", "answer": "Elastrator", "options": ["Elastrator", "Dehorner", "Syringe", "Ear Notcher"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Elastrator.jpg"}
    ]
}

# Store quiz state
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
    return render_template('quiz.html', question=current_quiz[0]["question"], options=current_quiz[0]["options"], score=score, total=len(current_quiz), image=current_quiz[0]["image"])

@app.route('/answer', methods=['POST'])
def answer():
    global score, question_index
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
        return render_template('quiz.html', question=current_quiz[question_index]["question"], options=current_quiz[question_index]["options"], score=score, total=len(current_quiz), feedback=feedback, feedback_color=feedback_color, image=current_quiz[question_index]["image"])
    else:
        return render_template('result.html', score=score, total=len(current_quiz))

@app.route('/restart')
def restart():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)