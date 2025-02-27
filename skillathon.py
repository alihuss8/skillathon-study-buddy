from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Question bank with cloud-hosted image URLs
questions = {
    "Breed ID (Photos)": {
        "Identify the breed (Holstein cow)": {"answer": "Holstein", "options": ["Holstein", "Jersey", "Guernsey", "Ayrshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Holstein_cow.jpg"},
        "Identify the breed (Hereford cattle)": {"answer": "Hereford", "options": ["Hereford", "Shorthorn", "Charolais", "Simmental"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Hereford_bull_large.jpg"},
        "Identify the breed (Angus cattle)": {"answer": "Angus", "options": ["Angus", "Brangus", "Galloway", "Limousin"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Angus_cow_%28bred%29_standing_in_farm_yard.jpg"},
        "Identify the breed (Merino sheep)": {"answer": "Merino", "options": ["Merino", "Rambouillet", "Columbia", "Corriedale"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Merino_sheep_Dan_Needham.jpg"},
        "Identify the breed (Duroc pig)": {"answer": "Duroc", "options": ["Duroc", "Hampshire", "Yorkshire", "Berkshire"], "image": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Duroc_boar.jpg"},
        "Identify the breed (Suffolk sheep)": {"answer": "Suffolk", "options": ["Suffolk", "Hampshire", "Dorset", "Southdown"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Suffolk_sheep_02.jpg"},
        "Identify the breed (Yorkshire pig)": {"answer": "Yorkshire", "options": ["Yorkshire", "Landrace", "Chester White", "Spotted"], "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Yorkshire_pig_-_geograph.org.uk_-_1504378.jpg"},
        "Identify the breed (Texas Longhorn)": {"answer": "Texas Longhorn", "options": ["Texas Longhorn", "Corriente", "Watusi", "Ankole"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Texas_Longhorn_in_Liberal%2C_Kansas_%2827609245310%29.jpg"},
        "Identify the breed (Nubian goat)": {"answer": "Nubian", "options": ["Nubian", "Boer", "Alpine", "LaMancha"], "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Nubian_Goat.jpg"},
        "Identify the breed (Dexter cattle)": {"answer": "Dexter", "options": ["Dexter", "Jersey", "Milking Shorthorn", "Red Poll"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Dexter_cow_2.jpg"}
    },
    "Meat Cuts (Photos)": {
        "In beef rib cut, identify the species": {"answer": "Beef", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        "In beef rib cut, identify the primal cut": {"answer": "Rib", "options": ["Chuck", "Rib", "Loin", "Round"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        "In beef rib cut, identify the retail cut": {"answer": "Ribeye", "options": ["Ribeye", "T-Bone", "Sirloin", "Brisket"], "image": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Ribeye_steak.jpg"},
        "In pork loin cut, identify the species": {"answer": "Pork", "options": ["Beef", "Pork", "Lamb", "Chicken"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        "In pork loin cut, identify the primal cut": {"answer": "Loin", "options": ["Shoulder", "Loin", "Ham", "Belly"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        "In pork loin cut, identify the retail cut": {"answer": "Pork Chop", "options": ["Pork Chop", "Bacon", "Ham Steak", "Ribs"], "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Pork_chops_with_apple_sauce.jpg"},
        "In lamb leg cut, identify the species": {"answer": "Lamb", "options": ["Beef", "Pork", "Lamb", "Goat"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        "In lamb leg cut, identify the primal cut": {"answer": "Leg", "options": ["Loin", "Rib", "Leg", "Shoulder"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        "In lamb leg cut, identify the retail cut": {"answer": "Leg of Lamb", "options": ["Lamb Chop", "Leg of Lamb", "Rack of Lamb", "Shank"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Lamb_leg_roast.jpg"},
        "In beef round cut, identify the retail cut": {"answer": "Round Steak", "options": ["Round Steak", "Sirloin", "Brisket", "Chuck Roast"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Round_steak.jpg"}
    },
    "Hay Analysis": {  # No images needed
        "Which hay has the highest protein (A: 12.5%, B: 17.8%, C: 14.2%)?": {"answer": "B", "options": ["A", "B", "C"], "image": None},
        "Which hay is best for growing calves (A: 11% protein, 58% TDN; B: 15% protein, 66% TDN)?": {"answer": "B", "options": ["A", "B"], "image": None}
    },
    "Wool Analysis (Photos)": {
        "In wool sample, which is finest? (A: 19 microns, B: 24 microns)": {"answer": "A", "options": ["A", "B"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Merino_wool_closeup.jpg"},
        "In wool sample, identify the breed": {"answer": "Merino", "options": ["Merino", "Rambouillet", "Suffolk", "Columbia"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Merino_wool_closeup.jpg"},
        "In wool sample, which has longest staple? (A: 2.5 in, B: 4.5 in)": {"answer": "B", "options": ["A", "B"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Wool_fiber.jpg"}
    },
    "Feed Samples (Photos)": {
        "Identify the feed (Corn)": {"answer": "Corn", "options": ["Corn", "Soybeans", "Oats", "Wheat"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Corn_kernels.jpg"},
        "Identify the feed (Oats)": {"answer": "Oats", "options": ["Wheat", "Oats", "Milo", "Rye"], "image": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Oats_closeup.jpg"},
        "Identify the feed (Alfalfa)": {"answer": "Alfalfa", "options": ["Corn Gluten", "Alfalfa", "Cottonseed", "Beet Pulp"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Alfalfa_hay.jpg"}
    },
    "Equipment ID (Photos)": {
        "Identify the equipment (Balling Gun)": {"answer": "Balling Gun", "options": ["Balling Gun", "Drench Gun", "Ear Tagger", "Hoof Trimmer"], "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Balling_gun.jpg"},
        "Identify the equipment (Ear Tagger)": {"answer": "Ear Tagger", "options": ["Ear Tagger", "Syringe", "Castration Knife", "Dehorner"], "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Ear_tagger.jpg"},
        "Identify the equipment (Drench Gun)": {"answer": "Drench Gun", "options": ["Drench Gun", "Balling Gun", "Needle", "Sheep Shears"], "image": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Drench_gun.jpg"}
    }
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
    category_questions = [(q, v["answer"], v["options"], v["image"]) for q, v in questions[selected_category].items()]
    current_quiz = random.sample(category_questions, min(5, len(category_questions)))  # Reduced to 5 for simplicity
    score = 0
    question_index = 0
    return render_template('quiz.html', question=current_quiz[0][0], options=current_quiz[0][2], score=score, total=len(current_quiz), image=current_quiz[0][3])

@app.route('/answer', methods=['POST'])
def answer():
    global score, question_index
    user_answer = request.form['answer']
    correct_answer = current_quiz[question_index][1]
    
    if user_answer.lower() == correct_answer.lower():
        score += 1
        feedback = "Correct!"
        feedback_color = "green"
    else:
        feedback = f"Wrong. The answer is {correct_answer}."
        feedback_color = "red"
    
    question_index += 1
    if question_index < len(current_quiz):
        return render_template('quiz.html', question=current_quiz[question_index][0], options=current_quiz[question_index][2], score=score, total=len(current_quiz), feedback=feedback, feedback_color=feedback_color, image=current_quiz[question_index][3])
    else:
        return render_template('result.html', score=score, total=len(current_quiz))

@app.route('/restart')
def restart():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)  # Changed for Heroku compatibility
