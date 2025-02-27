from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

questions = {
    "Breed ID (Photos)": [
        {"question": "Identify the breed", "answer": "Holstein", "options": ["Holstein", "Jersey", "Guernsey", "Ayrshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Cow_female_black_white.jpg"},
        {"question": "Identify the breed", "answer": "Hereford", "options": ["Hereford", "Shorthorn", "Charolais", "Simmental"], "image": "https://images.unsplash.com/photo-1583511655857-d19b37e8c751"},
        {"question": "Identify the breed", "answer": "Angus", "options": ["Angus", "Brangus", "Galloway", "Limousin"], "image": "https://images.unsplash.com/photo-1583511666372-62fc62497358"},
        {"question": "Identify the breed", "answer": "Jersey", "options": ["Jersey", "Holstein", "Guernsey", "Brown Swiss"], "image": "https://images.unsplash.com/photo-1583511666445-775f1f2116f5"},
        {"question": "Identify the breed", "answer": "Guernsey", "options": ["Guernsey", "Jersey", "Ayrshire", "Holstein"], "image": "https://images.unsplash.com/photo-1583511655906-8133a8a4a5cf"},
        {"question": "Identify the breed", "answer": "Ayrshire", "options": ["Ayrshire", "Guernsey", "Jersey", "Shorthorn"], "image": "https://images.unsplash.com/photo-1583512603806-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Brown Swiss", "options": ["Brown Swiss", "Jersey", "Holstein", "Simmental"], "image": "https://images.unsplash.com/photo-1583512603826-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Shorthorn", "options": ["Shorthorn", "Hereford", "Angus", "Charolais"], "image": "https://images.unsplash.com/photo-1583512603846-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Charolais", "options": ["Charolais", "Simmental", "Limousin", "Hereford"], "image": "https://images.unsplash.com/photo-1583512603866-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Simmental", "options": ["Simmental", "Charolais", "Angus", "Brangus"], "image": "https://images.unsplash.com/photo-1583512603886-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Limousin", "options": ["Limousin", "Charolais", "Angus", "Texas Longhorn"], "image": "https://images.unsplash.com/photo-1583512603906-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Texas Longhorn", "options": ["Texas Longhorn", "Corriente", "Watusi", "Ankole"], "image": "https://images.unsplash.com/photo-1583512603926-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Brangus", "options": ["Brangus", "Angus", "Brahman", "Santa Gertrudis"], "image": "https://images.unsplash.com/photo-1583512603946-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Brahman", "options": ["Brahman", "Brangus", "Santa Gertrudis", "Nellore"], "image": "https://images.unsplash.com/photo-1583512603966-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Santa Gertrudis", "options": ["Santa Gertrudis", "Brahman", "Brangus", "Shorthorn"], "image": "https://images.unsplash.com/photo-1583512603986-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Dexter", "options": ["Dexter", "Jersey", "Milking Shorthorn", "Red Poll"], "image": "https://images.unsplash.com/photo-1583512604006-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Milking Shorthorn", "options": ["Milking Shorthorn", "Shorthorn", "Ayrshire", "Holstein"], "image": "https://images.unsplash.com/photo-1583512604026-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Red Poll", "options": ["Red Poll", "Dexter", "Shorthorn", "Angus"], "image": "https://images.unsplash.com/photo-1583512604046-7d806615ddbc"},
        # Sheep
        {"question": "Identify the breed", "answer": "Merino", "options": ["Merino", "Rambouillet", "Columbia", "Corriedale"], "image": "https://images.unsplash.com/photo-1583512604066-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Suffolk", "options": ["Suffolk", "Hampshire", "Dorset", "Southdown"], "image": "https://images.unsplash.com/photo-1583512604086-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Suffolk", "Dorset", "Cheviot"], "image": "https://images.unsplash.com/photo-1583512604106-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Dorset", "options": ["Dorset", "Suffolk", "Hampshire", "Southdown"], "image": "https://images.unsplash.com/photo-1583512604126-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Southdown", "options": ["Southdown", "Dorset", "Suffolk", "Cheviot"], "image": "https://images.unsplash.com/photo-1583512604146-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Rambouillet", "options": ["Rambouillet", "Merino", "Columbia", "Targhee"], "image": "https://images.unsplash.com/photo-1583512604166-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Columbia", "options": ["Columbia", "Rambouillet", "Merino", "Corriedale"], "image": "https://images.unsplash.com/photo-1583512604186-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Corriedale", "options": ["Corriedale", "Columbia", "Merino", "Rambouillet"], "image": "https://images.unsplash.com/photo-1583512604206-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Cheviot", "options": ["Cheviot", "Southdown", "Dorset", "Suffolk"], "image": "https://images.unsplash.com/photo-1583512604226-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Targhee", "options": ["Targhee", "Rambouillet", "Columbia", "Merino"], "image": "https://images.unsplash.com/photo-1583512604246-7d806615ddbc"},
        # Swine
        {"question": "Identify the breed", "answer": "Duroc", "options": ["Duroc", "Hampshire", "Yorkshire", "Berkshire"], "image": "https://images.unsplash.com/photo-1583512604266-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Yorkshire", "options": ["Yorkshire", "Landrace", "Chester White", "Spotted"], "image": "https://images.unsplash.com/photo-1583512604286-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Hampshire", "options": ["Hampshire", "Duroc", "Berkshire", "Poland China"], "image": "https://images.unsplash.com/photo-1583512604306-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Berkshire", "options": ["Berkshire", "Hampshire", "Duroc", "Spotted"], "image": "https://images.unsplash.com/photo-1583512604326-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Landrace", "options": ["Landrace", "Yorkshire", "Chester White", "Duroc"], "image": "https://images.unsplash.com/photo-1583512604346-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Chester White", "options": ["Chester White", "Landrace", "Yorkshire", "Spotted"], "image": "https://images.unsplash.com/photo-1583512604366-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Spotted", "options": ["Spotted", "Berkshire", "Hampshire", "Duroc"], "image": "https://images.unsplash.com/photo-1583512604386-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Poland China", "options": ["Poland China", "Hampshire", "Berkshire", "Duroc"], "image": "https://images.unsplash.com/photo-1583512604406-7d806615ddbc"},
        # Goats
        {"question": "Identify the breed", "answer": "Nubian", "options": ["Nubian", "Boer", "Alpine", "LaMancha"], "image": "https://images.unsplash.com/photo-1583512604426-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Boer", "options": ["Boer", "Nubian", "Alpine", "Saanen"], "image": "https://images.unsplash.com/photo-1583512604446-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Alpine", "options": ["Alpine", "Nubian", "Boer", "Toggenburg"], "image": "https://images.unsplash.com/photo-1583512604466-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "LaMancha", "options": ["LaMancha", "Nubian", "Alpine", "Saanen"], "image": "https://images.unsplash.com/photo-1583512604486-7d806615ddbc"},
        {"question": "Identify the breed", "answer": "Saanen", "options": ["Saanen", "Alpine", "Nubian", "Toggenburg"], "image": "https://images.unsplash.com/photo-1583512604506-6cc1ca656a98"},
        {"question": "Identify the breed", "answer": "Toggenburg", "options": ["Toggenburg", "Saanen", "Alpine", "Boer"], "image": "https://images.unsplash.com/photo-1583512604526-7d806615ddbc"}
    ],
    "Meat Cuts (Photos)": [
        {"question": "Identify the species", "answer": "Beef", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://images.unsplash.com/photo-1583511655857-d19b37e8c751"},
        {"question": "Identify the primal cut", "answer": "Rib", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://images.unsplash.com/photo-1583511655857-d19b37e8c751"},
        # Add more...
    ],
    "Hay Analysis": [
        {"question": "Which hay has the highest protein (A: 12.5%, B: 17.8%, C: 14.2%)?", "answer": "B", "options": ["A", "B", "C"], "image": None},
        # Unchanged...
    ],
    "Wool Analysis (Photos)": [
        {"question": "Which wool sample is finest? (A: 19 microns, B: 24 microns, C: 22 microns)", "answer": "A", "options": ["A", "B", "C"], "image": "https://images.unsplash.com/photo-1583512604546-6cc1ca656a98"},
        # Add more...
    ],
    "Feed Samples (Photos)": [
        {"question": "Identify the feed", "answer": "Corn", "options": ["Corn", "Soybeans", "Oats", "Wheat"], "image": "https://images.unsplash.com/photo-1583512604566-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Oats", "options": ["Wheat", "Oats", "Milo", "Rye"], "image": "https://images.unsplash.com/photo-1583512604586-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Alfalfa", "options": ["Corn Gluten", "Alfalfa", "Cottonseed", "Beet Pulp"], "image": "https://images.unsplash.com/photo-1583512604606-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Soybean Meal", "options": ["Soybean Meal", "Wheat Midds", "Cottonseed Meal", "Distillers Grains"], "image": "https://images.unsplash.com/photo-1583512604626-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Milo", "options": ["Milo", "Barley", "Corn", "Oats"], "image": "https://images.unsplash.com/photo-1583512604646-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Salt Block", "options": ["Salt Block", "Mineral Mix", "Soybean Meal", "Alfalfa Pellets"], "image": "https://images.unsplash.com/photo-1583512604666-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Oats", "Corn", "Wheat"], "image": "https://images.unsplash.com/photo-1583512604686-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Soybean Meal", "Fish Meal", "Blood Meal"], "image": "https://images.unsplash.com/photo-1583512604706-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Alfalfa Pellets", "options": ["Alfalfa Pellets", "Timothy Pellets", "Beet Pulp", "Corn Gluten"], "image": "https://images.unsplash.com/photo-1583512604726-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Wheat", "options": ["Wheat", "Oats", "Milo", "Barley"], "image": "https://images.unsplash.com/photo-1583512604746-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Oats", "Milo"], "image": "https://images.unsplash.com/photo-1583512604766-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Timothy Hay", "options": ["Timothy Hay", "Alfalfa", "Corn Gluten", "Beet Pulp"], "image": "https://images.unsplash.com/photo-1583512604786-6cc1ca656a98"},
        {"question": "Identify the feed", "answer": "Beet Pulp", "options": ["Beet Pulp", "Alfalfa Pellets", "Cottonseed Meal", "Soybean Meal"], "image": "https://images.unsplash.com/photo-1583512604806-6cc1ca656a98"}
    ],
    "Equipment ID (Photos)": [
        {"question": "Identify the equipment", "answer": "Balling Gun", "options": ["Balling Gun", "Drench Gun", "Ear Tagger", "Hoof Trimmer"], "image": "https://images.unsplash.com/photo-1583512604826-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Ear Tagger", "options": ["Ear Tagger", "Syringe", "Castration Knife", "Dehorner"], "image": "https://images.unsplash.com/photo-1583512604846-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Drench Gun", "options": ["Drench Gun", "Balling Gun", "Needle", "Sheep Shears"], "image": "https://images.unsplash.com/photo-1583512604866-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Hoof Trimmer", "options": ["Hoof Trimmer", "Sheep Shears", "Castration Knife", "Branding Iron"], "image": "https://images.unsplash.com/photo-1583512604886-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Syringe", "options": ["Syringe", "Ear Tagger", "Drench Gun", "Thermometer"], "image": "https://images.unsplash.com/photo-1583512604906-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Dehorner", "options": ["Dehorner", "Hoof Trimmer", "Balling Gun", "Elastrator"], "image": "https://images.unsplash.com/photo-1583512604926-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Sheep Shears", "options": ["Sheep Shears", "Hoof Trimmer", "Castration Knife", "Ear Notcher"], "image": "https://images.unsplash.com/photo-1583512604946-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Castration Knife", "options": ["Castration Knife", "Dehorner", "Syringe", "Branding Iron"], "image": "https://images.unsplash.com/photo-1583512604966-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Ear Notcher", "options": ["Ear Notcher", "Syringe", "Drench Gun", "Hoof Trimmer"], "image": "https://images.unsplash.com/photo-1583512604986-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Thermometer", "options": ["Thermometer", "Syringe", "Ear Tagger", "Balling Gun"], "image": "https://images.unsplash.com/photo-1583512605006-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Branding Iron", "options": ["Branding Iron", "Castration Knife", "Sheep Shears", "Dehorner"], "image": "https://images.unsplash.com/photo-1583512605026-6cc1ca656a98"},
        {"question": "Identify the equipment", "answer": "Elastrator", "options": ["Elastrator", "Dehorner", "Syringe", "Ear Notcher"], "image": "https://images.unsplash.com/photo-1583512605046-6cc1ca656a98"}
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
    current_quiz = random.sample(category_questions, k=5 if len(category_questions) >= 5 else len(category_questions))
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
        feedback = "Correct!"
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
