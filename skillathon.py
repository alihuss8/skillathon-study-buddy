from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'abc123xyz'  # Hardcoded for now; use a secure random string in production

# Your question data (unchanged, just collapsed for brevity)
questions = {
    "Feed Samples": [
        {"question": "Identify the feed", "answer": "Dry Molasses", "options": ["Dry Molasses", "Whole Kernel Corn", "Steam Rolled Oats", "Dried Whey", "Ground Corn", "Wheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cHiiTMVk6SMaMMl", "description": "A molasses-based feed supplement, high in sugar, used to improve palatability."},
        {"question": "Identify the feed", "answer": "Whole Kernel Corn", "options": ["Whole Kernel Corn", "Ground Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_eXxpBRqGn7o0sS1", "description": "Whole corn kernels, a high-energy feed rich in starch, used for livestock."},
        {"question": "Identify the feed", "answer": "Steam Rolled Oats", "options": ["Steam Rolled Oats", "Whole Grain Oats", "Oats", "Barley", "Wheat", "Milo", "Rye", "Buckwheat", "Ground Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_01j9P8F5huqF1TT", "description": "Oats processed with steam and rolling, improving digestibility and energy availability."},
        {"question": "Identify the feed", "answer": "Dried Whey", "options": ["Dried Whey", "Dry Molasses", "Whole Kernel Corn", "Steam Rolled Oats", "Fish Meal", "Corn Gluten Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3wpuaCxwz3aKg0l", "description": "Dried whey from dairy, rich in protein and lactose."},
        {"question": "Identify the feed", "answer": "Trace Mineralized Salt", "options": ["Trace Mineralized Salt", "Ground Limestone", "Salt", "Dicalcium Phosphate", "Urea", "Sugar Beet Pulp"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2ueNiloFZRw2gPX", "description": "Salt block with trace minerals for livestock health."},
        {"question": "Identify the feed", "answer": "Ground Limestone", "options": ["Ground Limestone", "Trace Mineralized Salt", "Salt", "Dicalcium Phosphate", "Urea", "Cottonseed Hulls"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0NxnMjYGYbltmXX", "description": "Finely ground limestone, a calcium source for bones."},
        {"question": "Identify the feed", "answer": "Sugar Beet Pulp", "options": ["Sugar Beet Pulp", "Hay Cubes", "Alfalfa Meal Pellets", "Cottonseed Hulls", "Wheat Bran", "Buckwheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_00tV6yZjGg6HOgR", "description": "Pulp from sugar beets, high in fiber."},
        {"question": "Identify the feed", "answer": "Steam Rolled Barley", "options": ["Steam Rolled Barley", "Whole Kernel Corn", "Ground Corn", "Dried Whey", "Barley", "Oats"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cMZbiFunGQ34WLb", "description": "Barley processed for enhanced digestibility."},
        {"question": "Identify the feed", "answer": "Hay Cubes", "options": ["Hay Cubes", "Sugar Beet Pulp", "Alfalfa Meal Pellets", "Cottonseed Hulls", "Wheat Middlings", "Rye"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0uEEvKKmWOy3IwJ", "description": "Compressed hay blocks, rich in fiber."},
        {"question": "Identify the feed", "answer": "Wheat Middlings", "options": ["Wheat Middlings", "Wheat", "Wheat Bran", "Barley", "Ground Corn", "Milo"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_78vaXSpzXPytmPr", "description": "Byproduct of flour milling, high in fiber."},
        {"question": "Identify the feed", "answer": "Salt", "options": ["Salt", "Trace Mineralized Salt", "Dicalcium Phosphate", "Ground Limestone", "Urea", "Fish Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cURXrsFjIqOVu3r", "description": "Pure sodium chloride for hydration."},
        {"question": "Identify the feed", "answer": "Fish Meal", "options": ["Fish Meal", "Dried Whey", "Cottonseed Meal", "Corn Gluten Meal", "Blood Meal", "Distiller’s Grain"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNlzyS7pL4dvff", "description": "Dried fish, a 60% protein supplement."},
        {"question": "Identify the feed", "answer": "Distiller’s Grain", "options": ["Distiller’s Grain", "Wheat Middlings", "Fish Meal", "Corn Gluten Meal", "Cottonseed Meal", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNrwz4J2IkFitv", "description": "Whiskey residue, energy and protein source."},
        {"question": "Identify the feed", "answer": "Dicalcium Phosphate", "options": ["Dicalcium Phosphate", "Trace Mineralized Salt", "Ground Limestone", "Salt", "Urea", "Sugar Beet Pulp"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_724XxWWXxecjVsh", "description": "Calcium and phosphorus for bones and functions."},
        {"question": "Identify the feed", "answer": "Corn Gluten Meal", "options": ["Corn Gluten Meal", "Distiller’s Grain", "Fish Meal", "Wheat Middlings", "Cottonseed Meal", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_09aFgNL7UBCu8yV", "description": "Corn residue with 43% protein."},
        {"question": "Identify the feed", "answer": "Alfalfa Meal Pellets", "options": ["Alfalfa Meal Pellets", "Hay Cubes", "Sugar Beet Pulp", "Cottonseed Hulls", "Wheat Bran", "Rye"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2nlYF2zaMrUHOq9", "description": "Ground, dried alfalfa, good protein source."},
        {"question": "Identify the feed", "answer": "Urea", "options": ["Urea", "Dicalcium Phosphate", "Trace Mineralized Salt", "Salt", "Ground Limestone", "Fish Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9mKWzWzZ6QAmcM5", "description": "Nitrogen source for ruminants, toxic to horses."},
        {"question": "Identify the feed", "answer": "Wheat", "options": ["Wheat", "Wheat Middlings", "Wheat Bran", "Barley", "Oats", "Milo", "Rye", "Buckwheat", "Ground Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9G2LtnngnVfm8AJ", "description": "Wheats are generally high in protein, averaging 13-15%, as with many other cereal grains, wheat is primarily a source of energy in the form of carbohydrates."},
        {"question": "Identify the feed", "answer": "Milo", "options": ["Milo", "Barley", "Wheat", "Oats", "Rye", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3yeuMnFw1PhbuV7", "description": "Worldwide, sorghum is a food grain for humans. In the United States, sorghum is used primarily as a feed grain for livestock."},
        {"question": "Identify the feed", "answer": "Cottonseed Hulls", "options": ["Cottonseed Hulls", "Hay Cubes", "Alfalfa Meal Pellets", "Sugar Beet Pulp", "Wheat Bran", "Buckwheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bNin7O2GLgObQeF", "description": "High-fiber, fat, and protein for dairy."},
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Barley", "Oats", "Milo", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_daRDa8qLjvsrZnn", "description": "Minor Crop in U.S., growing plants may be harvested as haylage."},
        {"question": "Identify the feed", "answer": "Ground Corn", "options": ["Ground Corn", "Whole Kernel Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_ehNO2twWd5dowbb", "description": "Corn is the most commonly used energy source fed to animals."},
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Corn Gluten Meal", "Fish Meal", "Distiller’s Grain", "Blood Meal", "Wheat Middlings"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_8esYlVAgpexIlyB", "description": "Protein source (36-48%), toxic to hogs/chickens."},
        {"question": "Identify the feed", "answer": "Wheat Bran", "options": ["Wheat Bran", "Wheat Middlings", "Wheat", "Barley", "Oats", "Milo"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bIOenYbo9Q5ceVL", "description": "Outer grain layer, rich in fiber and omegas."},
        {"question": "Identify the feed", "answer": "Buckwheat", "options": ["Buckwheat", "Wheat", "Barley", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_41JMXdWaByeoA97", "description": "Buckwheat is primarily a human food crop, used in similar fashion to cereal grains such as wheat or oats."},
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Wheat", "Buckwheat", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bee4PEKLZhfTJul", "description": "Barley is ranked third among feed grains cultivated in the U.S."},
        {"question": "Identify the feed", "answer": "Blood Meal", "options": ["Blood Meal", "Fish Meal", "Cottonseed Meal", "Dried Whey", "Corn Gluten Meal", "Distiller’s Grain"], "image": "https://m.media-amazon.com/images/I/41lGr+Gc9tL._SY445_SX342_.jpg", "description": "Dried blood, high in protein (80-85%)."}
    ]
}

@app.before_request
def before_request():
    if 'quiz_state' not in session:
        session['quiz_state'] = {
            'current_quiz': [],
            'score': 0,
            'question_index': 0,
            'selected_category': '',
            'answers': []
        }

def get_quiz_state():
    return session['quiz_state']

@app.route('/')
def home():
    return render_template('home.html', categories=questions.keys())

@app.route('/start', methods=['POST'])
def start_quiz():
    quiz_state = get_quiz_state()
    quiz_state['current_quiz'] = []
    quiz_state['score'] = 0
    quiz_state['question_index'] = 0
    quiz_state['selected_category'] = request.form['category']
    quiz_state['answers'] = []
    
    category_questions = questions[quiz_state['selected_category']]
    quiz_state['current_quiz'] = random.sample(category_questions, len(category_questions))  # All 26 questions
    
    # Randomize options for each question
    for q in quiz_state['current_quiz']:
        q['shuffled_options'] = random.sample(q['options'], len(q['options']))  # Shuffle options
    
    session['quiz_state'] = quiz_state
    session.modified = True  # Force session save
    
    first_q = quiz_state['current_quiz'][0]
    return render_template('quiz.html', 
                          question=first_q["question"],
                          options=first_q["shuffled_options"],  # Use shuffled options
                          image=first_q["image"],
                          description=first_q["description"],
                          score=quiz_state['score'],
                          question_num=quiz_state['question_index'] + 1,
                          total=len(quiz_state['current_quiz']))

@app.route('/answer', methods=['POST'])
def answer():
    quiz_state = get_quiz_state()
    
    if quiz_state['question_index'] >= len(quiz_state['current_quiz']):
        return redirect(url_for('results'))

    current_q = quiz_state['current_quiz'][quiz_state['question_index']]
    user_answer = request.form.get('answer', '')  # Default to empty if missing
    correct_answer = current_q["answer"]
    
    # Log for debugging
    print(f"Q{quiz_state['question_index']+1}/{len(quiz_state['current_quiz'])}: Image={current_q['image']}, User='{user_answer}', Correct='{correct_answer}', Options={current_q['shuffled_options']}")
    
    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
    quiz_state['answers'].append({
        'question': current_q["question"],
        'image': current_q["image"],
        'description': current_q["description"],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct
    })

    if is_correct:
        quiz_state['score'] += 1
        feedback = "Correct!"
        feedback_color = "green"
    else:
        feedback = f"Incorrect. The correct answer is '{correct_answer}'."
        feedback_color = "red"

    quiz_state['question_index'] += 1
    session['quiz_state'] = quiz_state
    session.modified = True  # Force session save
    
    if quiz_state['question_index'] < len(quiz_state['current_quiz']):
        next_q = quiz_state['current_quiz'][quiz_state['question_index']]
        print(f"Next: Q{quiz_state['question_index']+1}, Image={next_q['image']}")
        return render_template('quiz.html',
                              question=next_q["question"],
                              options=next_q["shuffled_options"],
                              image=next_q["image"],
                              description=next_q["description"],
                              score=quiz_state['score'],
                              question_num=quiz_state['question_index'] + 1,
                              total=len(quiz_state['current_quiz']),
                              feedback=feedback,
                              feedback_color=feedback_color)
    else:
        print(f"Quiz complete: Score={quiz_state['score']}/{len(quiz_state['current_quiz'])}")
        return redirect(url_for('results'))

@app.route('/results')
def results():
    quiz_state = get_quiz_state()
    return render_template('result.html', 
                          score=quiz_state['score'], 
                          total=len(quiz_state['current_quiz']),
                          answers=quiz_state['answers'])

@app.route('/restart')
def restart():
    session.pop('quiz_state', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
