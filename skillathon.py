from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

questions = {
    "Breed ID (Photos)": [
        {"question": "Identify the breed", "answer": "Holstein", "options": ["Holstein", "Jersey", "Guernsey", "Ayrshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Cow_female_black_white.jpg"},
    ],
    "Grains and Seeds": [
        {"question": "Identify the feed", "answer": "Whole Kernel Corn", "options": ["Whole Kernel Corn", "Ground Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_eXxpBRqGn7o0sS1", "description": "Whole corn kernels, a high-energy feed rich in starch, used for livestock."},
        {"question": "Identify the feed", "answer": "Steam Rolled Oats", "options": ["Steam Rolled Oats", "Whole Grain Oats", "Oats", "Barley", "Wheat", "Milo", "Rye", "Buckwheat", "Ground Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_01j9P8F5huqF1TT", "description": "Oats processed with steam and rolling, improving digestibility and energy availability."},
        {"question": "Identify the feed", "answer": "Wheat (Whole Grain)", "options": ["Wheat", "Wheat Middlings", "Wheat Bran", "Barley", "Oats", "Milo", "Rye", "Buckwheat", "Ground Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9G2LtnngnVfm8AJ", "description": "Wheats are generally high in protein, averaging 13-15%, as with many other cereal grains, wheat is primarily a source of energy in the form of carbohydrates. The glutenous nature of wheat makes it an excellent pelleting aid, for this reason, it is used in pelleted feeds."},
        {"question": "Identify the feed", "answer": "Milo (Whole Grain Sorghum)", "options": ["Milo", "Barley", "Wheat", "Oats", "Rye", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3yeuMnFw1PhbuV7", "description": "Worldwide, sorghum is a food grain for humans. In the United States, sorghum is used primarily as a feed grain for livestock. Feed value of grain sorghum is similar to corn. The grain has more protein and fat than corn, but is lower in vitamin A. Pasturing cattle or sheep on sorghum stubble, after the grain has been harvested, is a common practice. Basically, it can be interchanged with corn, as a corn substitute."},
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Barley", "Oats", "Milo", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_daRDa8qLjvsrZnn", "description": "Minor Crop in U.S., growing plants may be harvested as haylage. Grain may be fed as source of protein and energy."},
        {"question": "Identify the feed", "answer": "Ground Corn", "options": ["Ground Corn", "Whole Kernel Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_ehNO2twWd5dowbb", "description": "Corn is the most commonly used energy source fed to animals. Grain is ground to increase nutrient digestibility."},
        {"question": "Identify the feed", "answer": "Buckwheat", "options": ["Buckwheat", "Wheat", "Barley", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_41JMXdWaByeoA97", "description": "Buckwheat is primarily a human food crop, used in similar fashion to cereal grains such as wheat or oats. Buckwheat seeds are dehulled and the remaining seed material, call a groat, is ground into flour. The flour is often mixed with flour from other cereal grains to make breads, breakfast cereals or other multi-grain products. The protein content of dehulled buckwheat is about 12%, with only 2% fat. Buckwheat has roughly the feed value of oats when fed to livestock."},
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Wheat", "Buckwheat", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bee4PEKLZhfTJul", "description": "Barley is ranked third among feed grains cultivated in the U.S. In the U.S. barley is used as the major cereal component in beef and dairy diets throughout much of the Great Lakes region, the northern plains and mountain states, the northwest coast and Alaska. Compared to most other grains barley has more protein and important vitamins and minerals. By-products generated during the brewing and distilling processes offer high quality and are widely used as feed ingredients. The barley plant can be made into whole-plant or head-chop ensilage."},
        # Placeholders: Soybean Seeds, Cracked Corn
    ],
    "Hays and Forages": [
        {"question": "Identify the feed", "answer": "Hay Cubes", "options": ["Hay Cubes", "Alfalfa Meal Pellets", "Sugar Beet Pulp", "Cottonseed Hulls"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0uEEvKKmWOy3IwJ", "description": "Compressed hay blocks, convenient for feeding and storage, rich in fiber."},
        {"question": "Identify the feed", "answer": "Sugar Beet Pulp", "options": ["Sugar Beet Pulp", "Hay Cubes", "Alfalfa Meal Pellets", "Cottonseed Hulls"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_00tV6yZjGg6HOgR", "description": "Pulp from sugar beets after sugar extraction, high in fiber and digestible energy."},
        {"question": "Identify the feed", "answer": "Alfalfa Meal Pellets", "options": ["Alfalfa Meal Pellets", "Hay Cubes", "Sugar Beet Pulp", "Cottonseed Hulls"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2nlYF2zaMrUHOq9", "description": "This is a portion of the alfalfa plant, free from other plant crops, weed and mold, which has been finely ground and thermally dried. Alfalfa meal is a very good source of protein."},
        {"question": "Identify the feed", "answer": "Cottonseed Hulls", "options": ["Cottonseed Hulls", "Hay Cubes", "Alfalfa Meal Pellets", "Sugar Beet Pulp"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bNin7O2GLgObQeF", "description": "Unique feed for dairy cattle - combines fat for high energy with high protein (21-27%) and very high fiber levels."},
        # Placeholders: Alfalfa Hay, Timothy Hay, Orchardgrass Hay, Brome Hay, Bermuda Hay, Lespedeza Hay, Corn Silage
    ],
    "Byproducts and Meals": [
        {"question": "Identify the feed", "answer": "Dry Molasses", "options": ["Dry Molasses", "Dried Whey", "Fish Meal", "Distiller’s Grain", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cHiiTMVk6SMaMMl", "description": "A molasses-based feed supplement, high in sugar, used to improve palatability and energy content."},
        {"question": "Identify the feed", "answer": "Dried Whey", "options": ["Dried Whey", "Dry Molasses", "Fish Meal", "Distiller’s Grain", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3wpuaCxwz3aKg0l", "description": "Dried whey from dairy processing, rich in protein and lactose, used as a supplement."},
        {"question": "Identify the feed", "answer": "Wheat Middlings", "options": ["Wheat Middlings", "Dry Molasses", "Dried Whey", "Fish Meal", "Distiller’s Grain", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_78vaXSpzXPytmPr", "description": "Byproduct of flour milling, high in fiber and protein, used as a feed ingredient."},
        {"question": "Identify the feed", "answer": "Fish Meal", "options": ["Fish Meal", "Dry Molasses", "Dried Whey", "Distiller’s Grain", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNlzyS7pL4dvff", "description": "Dried, ground fish or cuttings, a high-protein (60%) supplement for livestock diets."},
        {"question": "Identify the feed", "answer": "Distiller’s Grain", "options": ["Distiller’s Grain", "Dry Molasses", "Dried Whey", "Fish Meal", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNrwz4J2IkFitv", "description": "Residue left after distilling whiskey from grains. Excellent source of energy and protein, especially bypass protein for ruminants."},
        {"question": "Identify the feed", "answer": "Corn Gluten Meal", "options": ["Corn Gluten Meal", "Dry Molasses", "Dried Whey", "Fish Meal", "Distiller’s Grain", "Cottonseed Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_09aFgNL7UBCu8yV", "description": "Dried residue of corn after removal of corn syrup and oil. Contains 43% protein."},
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Dry Molasses", "Dried Whey", "Fish Meal", "Distiller’s Grain", "Corn Gluten Meal", "Wheat Middlings", "Wheat Bran"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_8esYlVAgpexIlyB", "description": "Second ranked protein source for ruminants behind soybean meal. Can present problems when fed to hogs and chickens because of a substance called gossypol, which can be toxic. Contains 36 – 48% protein."},
        {"question": "Identify the feed", "answer": "Wheat Bran", "options": ["Wheat Bran", "Dry Molasses", "Dried Whey", "Fish Meal", "Distiller’s Grain", "Corn Gluten Meal", "Cottonseed Meal", "Wheat Middlings"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bIOenYbo9Q5ceVL", "description": "Bran is the hard outer layer of grain. Along with germ, it is an integral part of whole grains and is often produced as a by-product of milling in the production of refined grains. When bran is removed from grains, the latter lose a portion of their nutritional value. Bran is particularly rich in dietary fiber and omegas and contains significant quantities of starch, protein, vitamins and dietary minerals; Bran is widely used as a major component in animal foods for cattle, horses, goats, rabbits and many others."},
        # Placeholders: Corn Gluten Feed, Brewers’ Grains
    ],
    "Minerals and Supplements": [
        {"question": "Identify the feed", "answer": "Trace Mineralized Salt", "options": ["Trace Mineralized Salt", "Salt", "Dicalcium Phosphate", "Ground Limestone", "Urea", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2ueNiloFZRw2gPX", "description": "Salt block with added trace minerals (e.g., zinc, copper) to support livestock health."},
        {"question": "Identify the feed", "answer": "Ground Limestone (Calcium Carbonate)", "options": ["Ground Limestone", "Trace Mineralized Salt", "Dicalcium Phosphate", "Salt", "Urea", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0NxnMjYGYbltmXX", "description": "Finely ground limestone, a calcium source to balance diets and support bone health."},
        {"question": "Identify the feed", "answer": "Salt (Sodium Chloride)", "options": ["Salt", "Trace Mineralized Salt", "Dicalcium Phosphate", "Ground Limestone", "Urea", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cURXrsFjIqOVu3r", "description": "Pure sodium chloride, essential for livestock hydration and electrolyte balance."},
        {"question": "Identify the feed", "answer": "Dicalcium Phosphate (DiCal)", "options": ["Dicalcium Phosphate", "Trace Mineralized Salt", "Ground Limestone", "Salt", "Urea", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_724XxWWXxecjVsh", "description": "Calcium and phosphorus are important minerals in an animal’s diet because they insure strong bones and teeth and help with other body functions such as blood clotting and muscle contraction. Typical animal diets like corn and soybean meal are low in calcium and phosphorus so this mineral is added to the feed."},
        {"question": "Identify the feed", "answer": "Urea", "options": ["Urea", "Trace Mineralized Salt", "Dicalcium Phosphate", "Ground Limestone", "Salt", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9mKWzWzZ6QAmcM5", "description": "Non-protein nitrogen source, used as protein supplement for ruminants. Is toxic to horses."},
        {"question": "Identify the feed", "answer": "Blood Meal", "options": ["Blood Meal", "Fish Meal", "Trace Mineralized Salt", "Dicalcium Phosphate", "Urea", "Salt"], "image": "https://m.media-amazon.com/images/I/41lGr+Gc9tL._SY445_SX342_.jpg", "description": "Dried blood product, high in protein (80-85%), used as a supplement for livestock."},
    ],
    "Missing Feeds (Placeholders)": [
        {"question": "Identify the feed", "answer": "Alfalfa Hay", "options": ["Alfalfa Hay", "Timothy Hay", "Orchardgrass Hay", "Brome Hay"], "image": "[YOUR_ALFALFA_HAY_URL]", "description": "Dried alfalfa, a legume hay rich in protein and minerals."},
        {"question": "Identify the feed", "answer": "Timothy Hay", "options": ["Timothy Hay", "Alfalfa Hay", "Orchardgrass Hay", "Brome Hay"], "image": "[YOUR_TIMOTHY_HAY_URL]", "description": "Dried timothy grass, a common forage high in fiber."},
        {"question": "Identify the feed", "answer": "Orchardgrass Hay", "options": ["Orchardgrass Hay", "Alfalfa Hay", "Timothy Hay", "Brome Hay"], "image": "[YOUR_ORCHARDGRASS_HAY_URL]", "description": "Dried orchardgrass, a cool-season hay with good palatability."},
        {"question": "Identify the feed", "answer": "Brome Hay", "options": ["Brome Hay", "Alfalfa Hay", "Timothy Hay", "Orchardgrass Hay"], "image": "[YOUR_BROME_HAY_URL]", "description": "Dried bromegrass, a nutritious forage for livestock."},
        {"question": "Identify the feed", "answer": "Bermuda Hay", "options": ["Bermuda Hay", "Alfalfa Hay", "Timothy Hay", "Brome Hay"], "image": "[YOUR_BERMUDA_HAY_URL]", "description": "Dried bermudagrass, a warm-season hay for grazing."},
        {"question": "Identify the feed", "answer": "Lespedeza Hay", "options": ["Lespedeza Hay", "Alfalfa Hay", "Timothy Hay", "Brome Hay"], "image": "[YOUR_LESPEDEZA_HAY_URL]", "description": "Dried lespedeza, a legume hay with moderate protein."},
        {"question": "Identify the feed", "answer": "Soybean Seeds", "options": ["Soybean Seeds", "Soybean Meal", "Cottonseed Meal", "Corn"], "image": "[YOUR_SOYBEAN_SEEDS_URL]", "description": "Whole soybean seeds, rich in protein and oil before processing."},
        {"question": "Identify the feed", "answer": "Soybean Meal", "options": ["Soybean Meal", "Soybean Seeds", "Cottonseed Meal", "Fish Meal"], "image": "[YOUR_SOYBEAN_MEAL_URL]", "description": "High-protein meal from processed soybeans, primary ruminant feed."},
        {"question": "Identify the feed", "answer": "Corn Gluten Feed", "options": ["Corn Gluten Feed", "Corn Gluten Meal", "Distiller’s Grain", "Wheat Middlings"], "image": "[YOUR_CORN_GLUTEN_FEED_URL]", "description": "Byproduct of corn wet milling, lower protein than corn gluten meal, used in feeds."},
        {"question": "Identify the feed", "answer": "Cracked Corn", "options": ["Cracked Corn", "Whole Kernel Corn", "Ground Corn", "Oats"], "image": "[YOUR_CRACKED_CORN_URL]", "description": "Corn kernels broken into pieces, improving digestibility over whole corn."},
        {"question": "Identify the feed", "answer": "Corn Silage", "options": ["Corn Silage", "Alfalfa Hay", "Timothy Hay", "Sugar Beet Pulp"], "image": "[YOUR_CORN_SILAGE_URL]", "description": "Fermented corn plant, high in energy, used as cattle forage."},
        {"question": "Identify the feed", "answer": "Brewers’ Grains", "options": ["Brewers’ Grains", "Distiller’s Grain", "Wheat Middlings", "Corn Gluten Feed"], "image": "[YOUR_BREWERS_GRAINS_URL]", "description": "Wet or dried grains from brewing, high in protein and fiber."},
    ]
}

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
    # Set quiz length to 15-20 questions
    quiz_length = random.randint(15, 20)
    # Repeat questions to meet length, then shuffle
    current_quiz = category_questions * (quiz_length // len(category_questions)) + random.sample(category_questions, quiz_length % len(category_questions))
    random.shuffle(current_quiz)  # Shuffle to avoid predictable repeats
    score = 0
    question_index = 0
    print(f"Starting quiz - Image: {current_quiz[0]['image']}, Total: {len(current_quiz)}")
    return render_template('quiz.html', question=current_quiz[0]["question"], options=current_quiz[0]["options"], score=score, total=len(current_quiz), image=current_quiz[0]["image"])

@app.route('/answer', methods=['POST'])
def answer():
    global score, question_index
    if question_index >= len(current_quiz):
        print(f"Index out of range - ending, Index: {question_index}, Total: {len(current_quiz)}")
        return render_template('result.html', score=score, total=len(current_quiz))
    user_answer = request.form['answer']
    correct_answer = current_quiz[question_index]["answer"]
    if user_answer.lower() == correct_answer.lower():
        score += 1
        feedback = f"Correct! Description: {current_quiz[question_index]['description']}"
        feedback_color = "green"
    else:
        feedback = f"Wrong. The answer is {correct_answer}."
        feedback_color = "red"
    question_index += 1
    if question_index < len(current_quiz):
        print(f"Next - Index: {question_index}, Image: {current_quiz[question_index]['image']}")
        return render_template('quiz.html', question=current_quiz[question_index]["question"], options=current_quiz[question_index]["options"], score=score, total=len(current_quiz), feedback=feedback, feedback_color=feedback_color, image=current_quiz[question_index]["image"])
    else:
        print(f"Complete - Score: {score}, Total: {len(current_quiz)}")
        return render_template('result.html', score=score, total=len(current_quiz))

@app.route('/restart')
def restart():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
