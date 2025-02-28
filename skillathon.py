from flask import Flask, render_template, request, redirect, url_for, session
import random
import logging
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'abc123xyz'

# Global dictionary to store quiz results per user
quiz_results = {}  # Format: {"user_id": [{"image": "...", "description": "...", "is_correct": True}, ...]}

questions = {
    "Feed Samples": [
        {"question": "Identify the feed", "answer": "Dry Molasses", "options": ["Dry Molasses", "Whole Kernel Corn", "Steam Rolled Oats", "Dried Whey", "Ground Corn", "Wheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cHiiTMVk6SMaMMl", "description": "A molasses-based feed supplement, high in sugar (up to 50% carbohydrates), used to improve palatability and provide quick energy. Often mixed with other feeds as a binder in pelleted rations or to entice livestock to eat less palatable ingredients."},
        {"question": "Identify the feed", "answer": "Whole Kernel Corn", "options": ["Whole Kernel Corn", "Ground Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_eXxpBRqGn7o0sS1", "description": "Whole corn kernels, a high-energy feed rich in starch (70-75%), widely used as a staple carbohydrate source for livestock like cattle, swine, and poultry. Fed whole, it requires more chewing, aiding rumen fermentation in cattle."},
        {"question": "Identify the feed", "answer": "Steam Rolled Oats", "options": ["Steam Rolled Oats", "Whole Grain Oats", "Oats", "Barley", "Wheat", "Milo", "Rye", "Buckwheat", "Ground Corn", "Steam Rolled Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_01j9P8F5huqF1TT", "description": "Oats processed by steaming and rolling to break the hull, improving digestibility and energy availability. High in fiber (10-12%) and moderate in protein (11-13%), it’s a preferred feed for horses and young livestock due to its palatability and gentle digestion."},
        {"question": "Identify the feed", "answer": "Dried Whey", "options": ["Dried Whey", "Dry Molasses", "Whole Kernel Corn", "Steam Rolled Oats", "Fish Meal", "Corn Gluten Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3wpuaCxwz3aKg0l", "description": "A byproduct of cheese-making, dried whey is rich in protein (10-12%) and lactose (70%), providing a highly palatable, energy-dense supplement. Commonly fed to young animals like calves and piglets to support growth and gut health."},
        {"question": "Identify the feed", "answer": "Trace Mineralized Salt", "options": ["Trace Mineralized Salt", "Ground Limestone", "Salt", "Dicalcium Phosphate", "Urea", "Sugar Beet Pulp"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2ueNiloFZRw2gPX", "description": "Salt fortified with trace minerals (e.g., zinc, copper, iodine, manganese), essential for livestock health. It supports growth, reproduction, and immune function, typically provided as a block or loose mix for free-choice consumption."},
        {"question": "Identify the feed", "answer": "Ground Limestone", "options": ["Ground Limestone", "Trace Mineralized Salt", "Salt", "Dicalcium Phosphate", "Urea", "Cottonseed Hulls"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0NxnMjYGYbltmXX", "description": "Finely ground limestone, delivering 38-40% calcium, used to strengthen bones in growing animals and improve eggshell quality in poultry. A key mineral supplement in balanced livestock rations."},
        {"question": "Identify the feed", "answer": "Sugar Beet Pulp", "options": ["Sugar Beet Pulp", "Hay Cubes", "Alfalfa Meal Pellets", "Cottonseed Hulls", "Wheat Bran", "Buckwheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_00tV6yZjGg6HOgR", "description": "A byproduct of sugar beet processing, high in digestible fiber (18-20%), offering energy and promoting rumen health in cattle. Often fed to dairy cows to boost milk production and maintain digestive balance."},
        {"question": "Identify the feed", "answer": "Steam Rolled Barley", "options": ["Steam Rolled Barley", "Whole Kernel Corn", "Ground Corn", "Dried Whey", "Barley", "Oats", "Steam Rolled Oats"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cMZbiFunGQ34WLb", "description": "Barley processed by steaming and rolling to enhance digestibility, providing high energy and moderate protein (10-12%). Widely used in beef and dairy cattle diets, especially in regions like the Great Lakes and northern plains."},
        {"question": "Identify the feed", "answer": "Hay Cubes", "options": ["Hay Cubes", "Sugar Beet Pulp", "Alfalfa Meal Pellets", "Cottonseed Hulls", "Wheat Middlings", "Rye"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_0uEEvKKmWOy3IwJ", "description": "Compressed blocks of dried hay, typically alfalfa or grass, rich in fiber (25-30%). Convenient for feeding horses and cattle, ensuring consistent nutrition and reducing waste compared to loose hay."},
        {"question": "Identify the feed", "answer": "Wheat Middlings", "options": ["Wheat Middlings", "Wheat", "Wheat Bran", "Barley", "Ground Corn", "Milo"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_78vaXSpzXPytmPr", "description": "A byproduct of wheat flour milling, containing the bran, germ, and some endosperm, with moderate protein (16-18%) and high fiber. Used as an economical energy and protein source in livestock feeds."},
        {"question": "Identify the feed", "answer": "Salt", "options": ["Salt", "Trace Mineralized Salt", "Dicalcium Phosphate", "Ground Limestone", "Urea", "Fish Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_cURXrsFjIqOVu3r", "description": "Pure sodium chloride, critical for maintaining hydration, nerve function, and muscle activity in livestock. Provided as a block or loose form for free-choice intake, often a base for mineral mixes."},
        {"question": "Identify the feed", "answer": "Fish Meal", "options": ["Fish Meal", "Dried Whey", "Cottonseed Meal", "Corn Gluten Meal", "Blood Meal", "Distiller’s Grain"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNlzyS7pL4dvff", "description": "Dried and ground fish, offering 60-70% protein, rich in essential amino acids (e.g., lysine) and omega-3 fatty acids. A premium supplement for poultry, swine, and aquaculture diets."},
        {"question": "Identify the feed", "answer": "Distiller’s Grain", "options": ["Distiller’s Grain", "Wheat Middlings", "Fish Meal", "Corn Gluten Meal", "Cottonseed Meal", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bCNrwz4J2IkFitv", "description": "A byproduct of ethanol production from corn, high in protein (25-30%) and fiber, used as an energy and protein source. Commonly fed to cattle, enhancing rumen fermentation."},
        {"question": "Identify the feed", "answer": "Dicalcium Phosphate", "options": ["Dicalcium Phosphate", "Trace Mineralized Salt", "Ground Limestone", "Salt", "Urea", "Sugar Beet Pulp"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_724XxWWXxecjVsh", "description": "A mineral supplement providing calcium (22-24%) and phosphorus (18-20%), vital for bone development and metabolic functions in livestock like poultry and swine."},
        {"question": "Identify the feed", "answer": "Corn Gluten Meal", "options": ["Corn Gluten Meal", "Distiller’s Grain", "Fish Meal", "Wheat Middlings", "Cottonseed Meal", "Blood Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_09aFgNL7UBCu8yV", "description": "A byproduct of corn wet-milling, containing 40-60% protein, used as a high-protein feed for poultry and cattle. Rich in xanthophylls, it enhances egg yolk and skin pigmentation."},
        {"question": "Identify the feed", "answer": "Alfalfa Meal Pellets", "options": ["Alfalfa Meal Pellets", "Hay Cubes", "Sugar Beet Pulp", "Cottonseed Hulls", "Wheat Bran", "Rye"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_2nlYF2zaMrUHOq9", "description": "Ground and pelleted alfalfa, high in protein (15-20%) and fiber (25%), a nutritious forage feed for cattle, horses, and rabbits, providing vitamins like A and K."},
        {"question": "Identify the feed", "answer": "Urea", "options": ["Urea", "Dicalcium Phosphate", "Trace Mineralized Salt", "Salt", "Ground Limestone", "Fish Meal"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9mKWzWzZ6QAmcM5", "description": "A synthetic nitrogen source (46% nitrogen), converted to protein by rumen microbes in cattle. Toxic to monogastrics like horses and swine if overfed."},
        {"question": "Identify the feed", "answer": "Wheat", "options": ["Wheat", "Wheat Middlings", "Wheat Bran", "Barley", "Oats", "Milo", "Rye", "Buckwheat", "Ground Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_9G2LtnngnVfm8AJ", "description": "Whole wheat grain, high in protein (13-15%) and carbohydrates (>70%), used as an energy source in livestock diets. Its gluten content makes it an excellent pelleting aid."},
        {"question": "Identify the feed", "answer": "Milo", "options": ["Milo", "Barley", "Wheat", "Oats", "Rye", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_3yeuMnFw1PhbuV7", "description": "Grain sorghum, similar to corn in feed value, with higher protein (11-13%) and fat but lower vitamin A. Used as an energy source for livestock, especially in the U.S. Southwest."},
        {"question": "Identify the feed", "answer": "Cottonseed Hulls", "options": ["Cottonseed Hulls", "Hay Cubes", "Alfalfa Meal Pellets", "Sugar Beet Pulp", "Wheat Bran", "Buckwheat"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bNin7O2GLgObQeF", "description": "The outer hulls of cottonseeds, high in fiber (40-50%) and low in protein, used as a roughage source for dairy cattle to maintain rumen function and milk fat content."},
        {"question": "Identify the feed", "answer": "Rye", "options": ["Rye", "Wheat", "Barley", "Oats", "Milo", "Buckwheat", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_daRDa8qLjvsrZnn", "description": "A cereal grain with 10-13% protein, used as an energy and protein source. Less common in U.S. feeds, it can be harvested as haylage or grain for cattle and sheep."},
        {"question": "Identify the feed", "answer": "Ground Corn", "options": ["Ground Corn", "Whole Kernel Corn", "Cracked Corn", "Oats", "Wheat", "Milo", "Rye", "Buckwheat", "Barley"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_ehNO2twWd5dowbb", "description": "Corn ground to increase nutrient digestibility, rich in starch (70-75%), the most common energy source for livestock like cattle, swine, and poultry."},
        {"question": "Identify the feed", "answer": "Cottonseed Meal", "options": ["Cottonseed Meal", "Corn Gluten Meal", "Fish Meal", "Distiller’s Grain", "Blood Meal", "Wheat Middlings"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_8esYlVAgpexIlyB", "description": "A byproduct of cottonseed oil extraction, high in protein (36-48%), used for ruminants like cattle. Contains gossypol, toxic to monogastrics like swine and poultry."},
        {"question": "Identify the feed", "answer": "Wheat Bran", "options": ["Wheat Bran", "Wheat Middlings", "Wheat", "Barley", "Oats", "Milo"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bIOenYbo9Q5ceVL", "description": "The outer layer of wheat grain, high in fiber (40%) and moderate in protein (15%), used as a palatable roughage and omega fatty acid source in livestock diets."},
        {"question": "Identify the feed", "answer": "Buckwheat", "options": ["Buckwheat", "Wheat", "Barley", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_41JMXdWaByeoA97", "description": "A pseudo-cereal with 12% protein and low fat (2%), primarily a human food crop but fed to livestock as an oat-like energy source, though less common in U.S. diets."},
        {"question": "Identify the feed", "answer": "Barley", "options": ["Barley", "Wheat", "Buckwheat", "Oats", "Milo", "Rye", "Ground Corn", "Whole Kernel Corn"], "image": "https://osu.az1.qualtrics.com/CP/Graphic.php?IM=IM_bee4PEKLZhfTJul", "description": "A major feed grain (10-12% protein), ranked third in U.S. production, high in energy and fiber. Used in beef and dairy diets, with byproducts from brewing also fed to livestock."},
        {"question": "Identify the feed", "answer": "Blood Meal", "options": ["Blood Meal", "Fish Meal", "Cottonseed Meal", "Dried Whey", "Corn Gluten Meal", "Distiller’s Grain"], "image": "https://m.media-amazon.com/images/I/41lGr+Gc9tL._SY445_SX342_.jpg", "description": "Dried animal blood, extremely high in protein (80-85%), rich in lysine, used as a concentrated protein supplement for poultry, swine, and ruminants."}
    ]
}

@app.before_request
def before_request():
    logger.info("Initializing session")
    if 'quiz_state' not in session:
        session['quiz_state'] = {
            'score': 0,
            'question_index': 0,
            'category': '',
            'answered': False,
            'question_order': [],
            'user_id': str(uuid.uuid4())  # Unique ID for this quiz session
        }

def get_quiz_state():
    return session['quiz_state']

@app.route('/')
def home():
    logger.info("Rendering home page")
    quiz_state = get_quiz_state()
    # Clear any old results for this user_id
    if 'user_id' in quiz_state:
        quiz_results[quiz_state['user_id']] = []
    session.modified = True
    return render_template('home.html', categories=questions.keys())

@app.route('/start', methods=['POST'])
def start_quiz():
    quiz_state = get_quiz_state()
    quiz_state['score'] = 0
    quiz_state['question_index'] = 0
    quiz_state['category'] = request.form['category']
    quiz_state['question_order'] = list(range(len(questions[quiz_state['category']])))
    random.shuffle(quiz_state['question_order'])
    quiz_state['answered'] = False
    quiz_state['user_id'] = str(uuid.uuid4())  # New unique ID for this quiz
    quiz_results[quiz_state['user_id']] = []  # Initialize results for this user
    
    session['quiz_state'] = quiz_state
    session.modified = True
    
    current_q = questions[quiz_state['category']][quiz_state['question_order'][quiz_state['question_index']]]
    shuffled_options = random.sample(current_q['options'], len(current_q['options']))
    
    logger.info(f"Start: Q{quiz_state['question_index']+1}/{len(quiz_state['question_order'])}, Score={quiz_state['score']}")
    return render_template('quiz.html', 
                          question=current_q["question"],
                          options=shuffled_options,
                          image=current_q["image"],
                          score=quiz_state['score'],
                          question_num=quiz_state['question_index'] + 1,
                          total=len(quiz_state['question_order']))

@app.route('/answer', methods=['POST'])
def answer():
    quiz_state = get_quiz_state()
    total_questions = len(quiz_state.get('question_order', []))
    logger.info(f"Answer: Q{quiz_state['question_index']+1}/{total_questions}, Score={quiz_state['score']}, Answered={quiz_state['answered']}")

    try:
        current_q = questions[quiz_state['category']][quiz_state['question_order'][quiz_state['question_index']]]
        shuffled_options = random.sample(current_q['options'], len(current_q['options']))

        # Process answer if not yet answered
        if not quiz_state['answered']:
            user_answer = request.form.get('answer')
            if not user_answer:  # Check if answer is None or empty
                logger.warning("No answer provided in form data")
                user_answer = ""  # Fallback to empty string
            
            correct_answer = current_q["answer"]
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            
            if is_correct:
                quiz_state['score'] += 1
                feedback = "Correct!"
                feedback_color = "green"
            else:
                feedback = f"Incorrect. You chose '{user_answer}'. The correct answer is '{correct_answer}'."
                feedback_color = "red"

            # Store results in quiz_results instead of session
            quiz_results[quiz_state['user_id']].append({
                'image': current_q["image"],
                'description': current_q["description"],
                'is_correct': is_correct
            })

            quiz_state['answered'] = True
            session['quiz_state'] = quiz_state
            session.modified = True
            
            logger.info(f"Processed: User='{user_answer}', Correct='{correct_answer}', IsCorrect={is_correct}, NewScore={quiz_state['score']}, Feedback={feedback}")
            
            return render_template('quiz.html',
                                  question=current_q["question"],
                                  options=shuffled_options,
                                  image=current_q["image"],
                                  score=quiz_state['score'],
                                  question_num=quiz_state['question_index'] + 1,
                                  total=total_questions,
                                  feedback=feedback,
                                  feedback_color=feedback_color,
                                  description=current_q["description"])

        # Move to next question if answered
        quiz_state['question_index'] += 1
        if quiz_state['question_index'] >= total_questions:
            session['quiz_state'] = quiz_state
            session.modified = True
            logger.info(f"Quiz complete - Score={quiz_state['score']}")
            return redirect(url_for('results'))

        next_q = questions[quiz_state['category']][quiz_state['question_order'][quiz_state['question_index']]]
        next_shuffled_options = random.sample(next_q['options'], len(next_q['options']))
        
        quiz_state['answered'] = False
        session['quiz_state'] = quiz_state
        session.modified = True
        
        logger.info(f"Next: Q{quiz_state['question_index']+1}/{total_questions}, Score={quiz_state['score']}")
        return render_template('quiz.html',
                              question=next_q["question"],
                              options=next_shuffled_options,
                              image=next_q["image"],
                              score=quiz_state['score'],
                              question_num=quiz_state['question_index'] + 1,
                              total=total_questions)

    except Exception as e:
        logger.error(f"Error in /answer: {str(e)}")
        return "Internal Server Error", 500

@app.route('/results')
def results():
    quiz_state = get_quiz_state()
    total_questions = len(quiz_state.get('question_order', []))
    user_results = quiz_results.get(quiz_state['user_id'], [])
    logger.info(f"Results: Score={quiz_state['score']}/{total_questions}")
    # Clean up quiz_results to avoid memory buildup
    if quiz_state['user_id'] in quiz_results:
        del quiz_results[quiz_state['user_id']]
    return render_template('result.html', 
                          score=quiz_state['score'], 
                          total=total_questions,
                          answers=user_results)

@app.route('/restart')
def restart():
    logger.info("Restarting quiz")
    quiz_state = get_quiz_state()
    # Clean up quiz_results for this user
    if 'user_id' in quiz_state and quiz_state['user_id'] in quiz_results:
        del quiz_results[quiz_state['user_id']]
    session.pop('quiz_state', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    logger.info("Starting Flask app locally")
    app.run(debug=True)
