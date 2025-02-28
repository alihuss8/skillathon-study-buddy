from flask import Flask, render_template, request, redirect, url_for, session
import random
import logging
import uuid
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'abc123xyz'

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
    ],
    "Questions": {
        "Livestock Feed and Nutrition": [
            {"question": "A mature beef cow needs what percent protein in her diet daily?", "answer": "8-10%", "options": ["2-4%", "8-10%", "15-20%", "25-30%"], "description": "Mature beef cows need 8-10% protein daily for maintenance and production."},
            {"question": "Which is a good source of protein for livestock?", "answer": "Soybean meal", "options": ["Soybean meal", "Corn stalks", "Wheat straw", "Rice hulls"], "description": "Soybean meal provides 44-48% protein for livestock."},
            {"question": "Vitamins are needed in what amount in an animal’s diet?", "answer": "Small", "options": ["Large", "Small", "Medium", "None"], "description": "Vitamins are needed in small amounts but are vital for health."},
            {"question": "What nutrient is the main source of energy for animals?", "answer": "Carbohydrates", "options": ["Proteins", "Carbohydrates", "Fats", "Minerals"], "description": "Carbohydrates provide the most energy for animals."},
            {"question": "What does TDN stand for in animal nutrition?", "answer": "Total Digestible Nutrients", "options": ["Total Dietary Needs", "Total Digestible Nutrients", "Total Dry Nutrition", "Total Dairy Nutrition"], "description": "TDN measures the energy value of feed that animals can digest."},
            {"question": "Which mineral is critical for bone growth?", "answer": "Calcium", "options": ["Sodium", "Calcium", "Iron", "Potassium"], "description": "Calcium builds strong bones in growing animals."},
            {"question": "What vitamin prevents rickets in young animals?", "answer": "Vitamin D", "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "description": "Vitamin D helps bones grow strong and prevents rickets."},
            {"question": "What is a common energy feed for livestock?", "answer": "Corn", "options": ["Hay", "Corn", "Salt", "Soybean meal"], "description": "Corn is high in starch and provides energy for livestock."},
            {"question": "Which nutrient helps build muscle in animals?", "answer": "Protein", "options": ["Carbohydrates", "Protein", "Fats", "Vitamins"], "description": "Protein is key for muscle growth and repair."},
            {"question": "What is the term for a feed that provides all nutrients?", "answer": "Balanced ration", "options": ["Partial ration", "Balanced ration", "Energy ration", "Roughage"], "description": "A balanced ration meets all an animal’s nutrient needs."},
            {"question": "What type of feed is hay considered?", "answer": "Roughage", "options": ["Concentrate", "Roughage", "Supplement", "Grain"], "description": "Hay is a roughage feed, high in fiber for digestion."},
            {"question": "Which feed is high in fiber?", "answer": "Alfalfa", "options": ["Corn", "Alfalfa", "Molasses", "Fish meal"], "description": "Alfalfa is a high-fiber feed good for digestion."},
            {"question": "What does a deficiency of phosphorus cause in cattle?", "answer": "Weak bones", "options": ["Hair loss", "Weak bones", "Fever", "Diarrhea"], "description": "Phosphorus deficiency leads to weak bones in cattle."},
            {"question": "What is the main purpose of water in an animal’s diet?", "answer": "Hydration", "options": ["Energy", "Hydration", "Protein", "Vitamins"], "description": "Water keeps animals hydrated and healthy."},
            {"question": "Which nutrient is stored in fat tissues?", "answer": "Fat", "options": ["Protein", "Carbohydrates", "Fat", "Minerals"], "description": "Fat is stored in the body for energy reserves."},
            {"question": "What vitamin improves eyesight in animals?", "answer": "Vitamin A", "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "description": "Vitamin A helps animals see better."},
            {"question": "What is a byproduct feed from corn processing?", "answer": "Distillers grains", "options": ["Soybean hulls", "Distillers grains", "Wheat bran", "Cottonseed meal"], "description": "Distillers grains come from corn used in ethanol production."},
            {"question": "What mineral prevents grass tetany in cattle?", "answer": "Magnesium", "options": ["Calcium", "Magnesium", "Iron", "Sodium"], "description": "Magnesium prevents muscle issues like grass tetany."},
            {"question": "What feed supplement provides quick energy?", "answer": "Molasses", "options": ["Salt", "Molasses", "Urea", "Limestone"], "description": "Molasses is sugary and gives animals quick energy."},
            {"question": "What is the term for undigested feed in manure?", "answer": "Fiber", "options": ["Protein", "Fiber", "Starch", "Sugar"], "description": "Fiber passes through and helps digestion."}
        ],
        "Animal Health": [
            {"question": "Which is a sign that an animal may be unhealthy?", "answer": "Dull hair coat", "options": ["Bright eyes", "Dull hair coat", "Good appetite", "Alert behavior"], "description": "A dull hair coat can signal poor health or nutrition."},
            {"question": "What is a common external parasite on livestock?", "answer": "Ticks", "options": ["Worms", "Ticks", "Bacteria", "Viruses"], "description": "Ticks live on the skin and can spread disease."},
            {"question": "What does a rapid breathing rate indicate?", "answer": "Unhealthy", "options": ["Healthy", "Unhealthy", "Tired", "Happy"], "description": "Rapid breathing can mean an animal is sick or stressed."},
            {"question": "What is the term for an animal’s normal body heat?", "answer": "Temperature", "options": ["Pulse", "Temperature", "Respiration", "Weight"], "description": "Temperature shows if an animal is healthy or feverish."},
            {"question": "What tool measures an animal’s temperature?", "answer": "Thermometer", "options": ["Scale", "Thermometer", "Stethoscope", "Syringe"], "description": "A thermometer checks for fever in animals."},
            {"question": "What is a sign of dehydration in livestock?", "answer": "Sunken eyes", "options": ["Shiny coat", "Sunken eyes", "Alertness", "Good appetite"], "description": "Sunken eyes show an animal needs water."},
            {"question": "What disease causes coughing in cattle?", "answer": "Pneumonia", "options": ["Bloat", "Pneumonia", "Scours", "Foot rot"], "description": "Pneumonia affects the lungs and causes coughing."},
            {"question": "What is an internal parasite in sheep?", "answer": "Worms", "options": ["Fleas", "Worms", "Ticks", "Mites"], "description": "Worms live inside sheep and can make them sick."},
            {"question": "What vaccine prevents tetanus in livestock?", "answer": "Tetanus toxoid", "options": ["Rabies shot", "Tetanus toxoid", "Flu vaccine", "Wormer"], "description": "Tetanus toxoid protects against lockjaw."},
            {"question": "What is the term for pus-filled swelling?", "answer": "Abscess", "options": ["Tumor", "Abscess", "Cyst", "Bruise"], "description": "An abscess is an infection with pus."},
            {"question": "What mineral deficiency causes white muscle disease?", "answer": "Selenium", "options": ["Calcium", "Selenium", "Iron", "Magnesium"], "description": "Selenium lack causes muscle stiffness in young animals."},
            {"question": "What is a common treatment for worms?", "answer": "Dewormer", "options": ["Antibiotic", "Dewormer", "Vaccine", "Vitamin"], "description": "Dewormers kill internal parasites like worms."},
            {"question": "What causes bloat in cattle?", "answer": "Gas buildup", "options": ["Overeating grain", "Gas buildup", "Worms", "Fever"], "description": "Gas buildup in the stomach causes bloat."},
            {"question": "What is a sign of foot rot in sheep?", "answer": "Limping", "options": ["Coughing", "Limping", "Fever", "Diarrhea"], "description": "Limping shows foot rot, a painful infection."},
            {"question": "What prevents disease by building immunity?", "answer": "Vaccination", "options": ["Feeding", "Vaccination", "Washing", "Exercise"], "description": "Vaccinations help animals fight diseases."},
            {"question": "What is the term for difficulty giving birth?", "answer": "Dystocia", "options": ["Colic", "Dystocia", "Bloat", "Scours"], "description": "Dystocia means a tough birth for animals."},
            {"question": "What is a common bacterial disease in swine?", "answer": "Erysipelas", "options": ["Erysipelas", "Rabies", "Tetanus", "Flu"], "description": "Erysipelas causes fever and skin lesions in pigs."},
            {"question": "What does a high fever indicate in livestock?", "answer": "Infection", "options": ["Hunger", "Infection", "Cold", "Tiredness"], "description": "A high fever usually means an infection."},
            {"question": "What is the term for inflammation of the udder?", "answer": "Mastitis", "options": ["Colic", "Mastitis", "Bloat", "Pneumonia"], "description": "Mastitis is udder swelling, often from infection."},
            {"question": "What protects newborn calves from disease?", "answer": "Colostrum", "options": ["Water", "Colostrum", "Grain", "Hay"], "description": "Colostrum is the first milk, full of antibodies."}
        ],
        "Breeding and Genetics": [
            {"question": "What term refers to mating animals of different breeds?", "answer": "Crossbreeding", "options": ["Inbreeding", "Crossbreeding", "Linebreeding", "Purebreeding"], "description": "Crossbreeding improves vigor by combining breed traits."},
            {"question": "What is mating closely related animals called?", "answer": "Inbreeding", "options": ["Inbreeding", "Crossbreeding", "Outbreeding", "Hybridizing"], "description": "Inbreeding keeps traits but can reduce health."},
            {"question": "What carries genetic information in animals?", "answer": "Genes", "options": ["Bones", "Genes", "Blood", "Muscles"], "description": "Genes pass traits from parents to offspring."},
            {"question": "What is the term for an animal’s visible traits?", "answer": "Phenotype", "options": ["Genotype", "Phenotype", "Allele", "Chromosome"], "description": "Phenotype is what you see, like coat color."},
            {"question": "What is an animal’s genetic makeup called?", "answer": "Genotype", "options": ["Genotype", "Phenotype", "Trait", "Marker"], "description": "Genotype is the DNA behind an animal’s traits."},
            {"question": "What term means an animal is purebred?", "answer": "Homozygous", "options": ["Heterozygous", "Homozygous", "Hybrid", "Mixed"], "description": "Homozygous means the same genes from both parents."},
            {"question": "What improves hybrid vigor in offspring?", "answer": "Crossbreeding", "options": ["Inbreeding", "Crossbreeding", "Linebreeding", "Cloning"], "description": "Crossbreeding boosts health and growth."},
            {"question": "What is the term for a female parent?", "answer": "Dam", "options": ["Sire", "Dam", "Calf", "Foal"], "description": "Dam is the mother of an animal."},
            {"question": "What is the male parent called?", "answer": "Sire", "options": ["Sire", "Dam", "Bull", "Stud"], "description": "Sire is the father of an animal."},
            {"question": "What is mating within the same breed called?", "answer": "Purebreeding", "options": ["Crossbreeding", "Purebreeding", "Inbreeding", "Outcrossing"], "description": "Purebreeding keeps breed traits consistent."},
            {"question": "What predicts offspring performance based on parents?", "answer": "EPD", "options": ["DNA", "EPD", "GPA", "BMI"], "description": "EPD stands for Expected Progeny Difference."},
            {"question": "What is the removal of testicles called?", "answer": "Castration", "options": ["Docking", "Castration", "Spaying", "Clipping"], "description": "Castration stops males from breeding."},
            {"question": "What is the term for a castrated male pig?", "answer": "Barrow", "options": ["Gilt", "Barrow", "Boar", "Sow"], "description": "A barrow is a neutered male pig."},
            {"question": "What is artificial insemination?", "answer": "Breeding without mating", "options": ["Natural mating", "Breeding without mating", "Cloning", "Castration"], "description": "Artificial insemination uses semen to breed."},
            {"question": "What trait is passed from parent to offspring?", "answer": "Inherited", "options": ["Learned", "Inherited", "Acquired", "Trained"], "description": "Inherited traits come from genes."},
            {"question": "What is the term for a young animal in the womb?", "answer": "Fetus", "options": ["Calf", "Fetus", "Lamb", "Piglet"], "description": "A fetus develops inside the mother."},
            {"question": "What hormone triggers estrus in females?", "answer": "Estrogen", "options": ["Testosterone", "Estrogen", "Progesterone", "Insulin"], "description": "Estrogen signals a female is ready to breed."},
            {"question": "What is the gestation period for cattle?", "answer": "9 months", "options": ["6 months", "9 months", "12 months", "3 months"], "description": "Cattle carry calves for about 9 months."},
            {"question": "What is selecting animals for breeding called?", "answer": "Selection", "options": ["Culling", "Selection", "Weaning", "Feeding"], "description": "Selection picks the best animals to breed."},
            {"question": "What improves milk production in dairy cattle?", "answer": "Genetics", "options": ["Exercise", "Genetics", "Water", "Light"], "description": "Good genetics boost milk yield."}
        ],
        "Livestock Management": [
            {"question": "What is the term for moving animals from summer to winter pasture?", "answer": "Migration", "options": ["Migration", "Confinement", "Rotation", "Weaning"], "description": "Migration is seasonal movement of livestock."},
            {"question": "What is the process of separating young from mothers?", "answer": "Weaning", "options": ["Castration", "Weaning", "Branding", "Docking"], "description": "Weaning stops young from nursing."},
            {"question": "What is a common way to identify livestock?", "answer": "Ear tag", "options": ["Collar", "Ear tag", "Paint", "Shaving"], "description": "Ear tags help track individual animals."},
            {"question": "What is the term for a fenced livestock area?", "answer": "Pasture", "options": ["Barn", "Pasture", "Pen", "Shed"], "description": "A pasture is a fenced area for grazing."},
            {"question": "What reduces stress in handled livestock?", "answer": "Calm handling", "options": ["Loud noises", "Calm handling", "Fast movement", "Crowding"], "description": "Calm handling keeps animals relaxed."},
            {"question": "What is the term for cutting off a lamb’s tail?", "answer": "Docking", "options": ["Shearing", "Docking", "Castration", "Clipping"], "description": "Docking removes the tail for cleanliness."},
            {"question": "What is a group of cattle called?", "answer": "Herd", "options": ["Flock", "Herd", "Pack", "Gaggle"], "description": "A herd is a group of cattle."},
            {"question": "What protects livestock from weather?", "answer": "Shelter", "options": ["Fence", "Shelter", "Feed", "Water"], "description": "Shelter keeps animals safe from rain or heat."},
            {"question": "What is rotational grazing?", "answer": "Moving animals between pastures", "options": ["Feeding grain", "Moving animals between pastures", "Keeping animals in pens", "Watering daily"], "description": "Rotational grazing manages pasture use."},
            {"question": "What is the term for a young animal’s first feed?", "answer": "Colostrum", "options": ["Grain", "Colostrum", "Hay", "Water"], "description": "Colostrum is the first milk for newborns."},
            {"question": "What improves meat quality in finishing cattle?", "answer": "Grain feeding", "options": ["Grass only", "Grain feeding", "Hay only", "Water only"], "description": "Grain feeding adds fat for better meat."},
            {"question": "What is the term for removing horns?", "answer": "Dehorning", "options": ["Docking", "Dehorning", "Shearing", "Castration"], "description": "Dehorning prevents injury from horns."},
            {"question": "What is a common bedding material for livestock?", "answer": "Straw", "options": ["Gravel", "Straw", "Sand", "Concrete"], "description": "Straw keeps animals comfortable and dry."},
            {"question": "What is the term for raising animals indoors?", "answer": "Confinement", "options": ["Pasturing", "Confinement", "Rotation", "Migration"], "description": "Confinement keeps animals in barns or pens."},
            {"question": "What prevents disease spread in herds?", "answer": "Quarantine", "options": ["Feeding", "Quarantine", "Exercise", "Branding"], "description": "Quarantine isolates sick animals."},
            {"question": "What is the term for a livestock birth?", "answer": "Parturition", "options": ["Weaning", "Parturition", "Castration", "Migration"], "description": "Parturition is the act of giving birth."},
            {"question": "What is a common fencing material?", "answer": "Wire", "options": ["Wood", "Wire", "Stone", "Plastic"], "description": "Wire fencing keeps livestock contained."},
            {"question": "What is the purpose of ear notching in pigs?", "answer": "Identification", "options": ["Decoration", "Identification", "Health", "Growth"], "description": "Ear notching marks pigs for tracking."},
            {"question": "What is the term for a castrated male sheep?", "answer": "Wether", "options": ["Ram", "Ewe", "Wether", "Lamb"], "description": "A wether is a neutered male sheep."},
            {"question": "What improves pasture growth?", "answer": "Fertilizer", "options": ["Salt", "Fertilizer", "Sand", "Water"], "description": "Fertilizer adds nutrients to grass."}
        ],
        "Meat Science": [
            {"question": "What is the most tender retail cut of beef?", "answer": "Tenderloin", "options": ["Tenderloin", "Chuck roast", "Round steak", "Brisket"], "description": "Tenderloin is tender due to minimal muscle use."},
            {"question": "What gas is used to preserve meat color?", "answer": "Carbon monoxide", "options": ["Oxygen", "Carbon monoxide", "Nitrogen", "Helium"], "description": "Carbon monoxide keeps meat red and fresh-looking."},
            {"question": "What is the term for meat aging?", "answer": "Dry aging", "options": ["Freezing", "Dry aging", "Curing", "Smoking"], "description": "Dry aging improves flavor and tenderness."},
            {"question": "What protein gives meat its red color?", "answer": "Myoglobin", "options": ["Hemoglobin", "Myoglobin", "Collagen", "Actin"], "description": "Myoglobin stores oxygen in muscle, making meat red."},
            {"question": "What is the purpose of marbling in beef?", "answer": "Flavor", "options": ["Strength", "Flavor", "Color", "Weight"], "description": "Marbling is fat that adds flavor to beef."},
            {"question": "What cut comes from the shoulder of a pig?", "answer": "Boston butt", "options": ["Ham", "Boston butt", "Loin", "Belly"], "description": "Boston butt is a tasty shoulder cut."},
            {"question": "What is the term for preserving meat with salt?", "answer": "Curing", "options": ["Freezing", "Curing", "Smoking", "Grilling"], "description": "Curing uses salt to keep meat fresh longer."},
            {"question": "What grade indicates top-quality beef?", "answer": "Prime", "options": ["Choice", "Prime", "Select", "Standard"], "description": "Prime beef has the best marbling and flavor."},
            {"question": "What is the main muscle in a pork chop?", "answer": "Longissimus", "options": ["Psoas", "Longissimus", "Gluteus", "Biceps"], "description": "Longissimus runs along the back for pork chops."},
            {"question": "What cooking method tenderizes tough meat?", "answer": "Slow cooking", "options": ["Grilling", "Slow cooking", "Frying", "Boiling"], "description": "Slow cooking breaks down tough fibers."},
            {"question": "What is the term for a young lamb’s meat?", "answer": "Lamb", "options": ["Mutton", "Lamb", "Veal", "Chevon"], "description": "Lamb is meat from a young sheep."},
            {"question": "What federal agency inspects meat?", "answer": "USDA", "options": ["FDA", "USDA", "EPA", "CDC"], "description": "USDA ensures meat is safe to eat."},
            {"question": "What is the purpose of chilling meat after slaughter?", "answer": "Prevent spoilage", "options": ["Add flavor", "Prevent spoilage", "Increase weight", "Change color"], "description": "Chilling keeps meat fresh."},
            {"question": "What is the term for fat on the outside of meat?", "answer": "Cover fat", "options": ["Marbling", "Cover fat", "Lean", "Gristle"], "description": "Cover fat is the outer layer of fat."},
            {"question": "What cut of beef is used for ground beef?", "answer": "Chuck", "options": ["Rib", "Chuck", "Loin", "Round"], "description": "Chuck is often ground for burgers."},
            {"question": "What is the term for meat from a young calf?", "answer": "Veal", "options": ["Lamb", "Veal", "Mutton", "Chevon"], "description": "Veal is tender meat from young calves."},
            {"question": "What improves juiciness in cooked meat?", "answer": "Fat", "options": ["Protein", "Fat", "Water", "Salt"], "description": "Fat keeps meat juicy when cooked."},
            {"question": "What is the term for smoking meat to preserve it?", "answer": "Smoking", "options": ["Curing", "Smoking", "Freezing", "Drying"], "description": "Smoking adds flavor and preserves meat."},
            {"question": "What nutrient is high in meat?", "answer": "Protein", "options": ["Carbohydrates", "Protein", "Fiber", "Sugar"], "description": "Meat is a great source of protein."},
            {"question": "What is the term for meat from an older sheep?", "answer": "Mutton", "options": ["Lamb", "Mutton", "Veal", "Pork"], "description": "Mutton comes from mature sheep."}
        ],
        "Dairy": [
            {"question": "What is the primary sugar in milk?", "answer": "Lactose", "options": ["Glucose", "Fructose", "Lactose", "Sucrose"], "description": "Lactose is the main sugar in milk."},
            {"question": "What is the term for milk fat separation?", "answer": "Creaming", "options": ["Curdling", "Creaming", "Churning", "Skimming"], "description": "Creaming separates fat to make cream."},
            {"question": "What process kills bacteria in milk?", "answer": "Pasteurization", "options": ["Homogenization", "Pasteurization", "Fermentation", "Cooling"], "description": "Pasteurization heats milk to kill germs."},
            {"question": "What dairy product is made from whey?", "answer": "Cheese", "options": ["Butter", "Cheese", "Yogurt", "Cream"], "description": "Cheese can use whey in processing."},
            {"question": "What is the term for a dairy cow’s milk production?", "answer": "Lactation", "options": ["Gestation", "Lactation", "Weaning", "Milking"], "description": "Lactation is when a cow produces milk."},
            {"question": "What machine milks cows?", "answer": "Milking machine", "options": ["Tractor", "Milking machine", "Pump", "Churn"], "description": "Milking machines make milking faster."},
            {"question": "What nutrient is high in milk?", "answer": "Calcium", "options": ["Iron", "Calcium", "Fiber", "Sugar"], "description": "Milk is rich in calcium for strong bones."},
            {"question": "What is the term for milk with fat removed?", "answer": "Skim milk", "options": ["Whole milk", "Skim milk", "Cream", "Buttermilk"], "description": "Skim milk has little to no fat."},
            {"question": "What dairy product is churned from cream?", "answer": "Butter", "options": ["Cheese", "Butter", "Yogurt", "Ice cream"], "description": "Butter is made by churning cream."},
            {"question": "What is the term for a cow before her first calf?", "answer": "Heifer", "options": ["Heifer", "Cow", "Bull", "Calf"], "description": "A heifer hasn’t had a calf yet."},
            {"question": "What process breaks fat into small droplets in milk?", "answer": "Homogenization", "options": ["Pasteurization", "Homogenization", "Fermentation", "Churning"], "description": "Homogenization mixes fat evenly."},
            {"question": "What vitamin is added to milk?", "answer": "Vitamin D", "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "description": "Vitamin D is added to help bones."},
            {"question": "What is the term for milk turning sour?", "answer": "Spoilage", "options": ["Creaming", "Spoilage", "Churning", "Curdling"], "description": "Spoilage happens when milk goes bad."},
            {"question": "What dairy product is fermented milk?", "answer": "Yogurt", "options": ["Butter", "Yogurt", "Cream", "Cheese"], "description": "Yogurt is made by fermenting milk."},
            {"question": "What is the first milk from a cow after calving?", "answer": "Colostrum", "options": ["Skim milk", "Colostrum", "Whole milk", "Cream"], "description": "Colostrum helps newborns stay healthy."},
            {"question": "What is the term for a dairy cow’s udder?", "answer": "Udder", "options": ["Teat", "Udder", "Flank", "Hock"], "description": "The udder holds milk in a cow."},
            {"question": "What improves milk yield in dairy cows?", "answer": "Good feed", "options": ["Loud music", "Good feed", "Cold water", "Dim light"], "description": "Good feed boosts milk production."},
            {"question": "What is the term for milk solids?", "answer": "Curd", "options": ["Whey", "Curd", "Cream", "Fat"], "description": "Curd is the solid part of milk."},
            {"question": "What dairy breed is known for high milk production?", "answer": "Holstein", "options": ["Jersey", "Holstein", "Guernsey", "Ayrshire"], "description": "Holsteins give lots of milk."},
            {"question": "What is the term for a cow drying off before calving?", "answer": "Dry period", "options": ["Milk period", "Dry period", "Wet period", "Rest period"], "description": "Dry period is a rest before calving."}
        ],
        "Poultry": [
            {"question": "What is the term for a young female chicken?", "answer": "Pullet", "options": ["Rooster", "Hen", "Pullet", "Broiler"], "description": "A pullet is a young female chicken."},
            {"question": "What is a male chicken called?", "answer": "Rooster", "options": ["Hen", "Rooster", "Pullet", "Chick"], "description": "A rooster is an adult male chicken."},
            {"question": "What part of the egg provides nutrients to the embryo?", "answer": "Yolk", "options": ["White", "Yolk", "Shell", "Membrane"], "description": "The yolk feeds the growing chick."},
            {"question": "What is the term for egg-laying chickens?", "answer": "Layers", "options": ["Broilers", "Layers", "Roasters", "Chicks"], "description": "Layers are chickens raised for eggs."},
            {"question": "What disease affects poultry breathing?", "answer": "Infectious bronchitis", "options": ["Marek’s disease", "Infectious bronchitis", "Fowl pox", "Coccidiosis"], "description": "Infectious bronchitis harms poultry lungs."},
            {"question": "What is the term for a chicken raised for meat?", "answer": "Broiler", "options": ["Layer", "Broiler", "Pullet", "Hen"], "description": "Broilers grow fast for meat."},
            {"question": "What protects eggs from bacteria?", "answer": "Shell", "options": ["Yolk", "Shell", "White", "Membrane"], "description": "The shell keeps eggs safe from germs."},
            {"question": "What is the term for a group of chickens?", "answer": "Flock", "options": ["Herd", "Flock", "Pack", "Gaggle"], "description": "A flock is a group of chickens."},
            {"question": "What nutrient is high in eggs?", "answer": "Protein", "options": ["Carbohydrates", "Protein", "Fiber", "Sugar"], "description": "Eggs are full of protein."},
            {"question": "What is the term for hatching eggs?", "answer": "Incubation", "options": ["Brooding", "Incubation", "Laying", "Hatching"], "description": "Incubation keeps eggs warm to hatch."},
            {"question": "What vitamin in eggs improves eyesight?", "answer": "Vitamin A", "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "description": "Vitamin A in eggs helps eyes."},
            {"question": "What is the term for a baby chicken?", "answer": "Chick", "options": ["Pullet", "Chick", "Hen", "Rooster"], "description": "A chick is a newly hatched chicken."},
            {"question": "What is the purpose of a chicken’s comb?", "answer": "Cooling", "options": ["Hearing", "Cooling", "Seeing", "Pecking"], "description": "The comb helps a chicken stay cool."},
            {"question": "What is a common poultry feed ingredient?", "answer": "Corn", "options": ["Hay", "Corn", "Grass", "Straw"], "description": "Corn gives poultry energy."},
            {"question": "What is the term for an egg with two yolks?", "answer": "Double yolk", "options": ["Single yolk", "Double yolk", "No yolk", "Cracked yolk"], "description": "Double yolk eggs have two centers."},
            {"question": "What disease causes tumors in chickens?", "answer": "Marek’s disease", "options": ["Fowl pox", "Marek’s disease", "Coccidiosis", "Bronchitis"], "description": "Marek’s disease affects chicken nerves."},
            {"question": "What is the term for feathers falling out?", "answer": "Molting", "options": ["Pecking", "Molting", "Growing", "Clucking"], "description": "Molting is when chickens lose old feathers."},
            {"question": "What keeps chicks warm after hatching?", "answer": "Brooder", "options": ["Nest", "Brooder", "Coop", "Pen"], "description": "A brooder provides heat for chicks."},
            {"question": "What is the term for a chicken’s egg-laying cycle?", "answer": "Clutch", "options": ["Flock", "Clutch", "Roost", "Peck"], "description": "A clutch is a group of eggs laid together."},
            {"question": "What improves egg shell strength?", "answer": "Calcium", "options": ["Protein", "Calcium", "Fat", "Sugar"], "description": "Calcium makes egg shells hard."}
        ],
        "Sheep and Goats": [
            {"question": "What is the process of removing wool from sheep called?", "answer": "Shearing", "options": ["Shearing", "Docking", "Castration", "Branding"], "description": "Shearing removes wool for textile use."},
            {"question": "What is a female sheep called?", "answer": "Ewe", "options": ["Ram", "Ewe", "Wether", "Lamb"], "description": "A ewe is an adult female sheep."},
            {"question": "What is the term for a young sheep?", "answer": "Lamb", "options": ["Kid", "Lamb", "Calf", "Foal"], "description": "A lamb is a baby sheep."},
            {"question": "What is a male goat called?", "answer": "Buck", "options": ["Doe", "Buck", "Wether", "Kid"], "description": "A buck is an adult male goat."},
            {"question": "What fiber comes from goats?", "answer": "Mohair", "options": ["Wool", "Mohair", "Cotton", "Silk"], "description": "Mohair is soft hair from Angora goats."},
            {"question": "What is the term for a castrated male goat?", "answer": "Wether", "options": ["Buck", "Wether", "Doe", "Kid"], "description": "A wether is a neutered male goat."},
            {"question": "What disease causes abortion in sheep?", "answer": "Toxoplasmosis", "options": ["Foot rot", "Toxoplasmosis", "Scrapie", "Bloat"], "description": "Toxoplasmosis can harm unborn lambs."},
            {"question": "What is the gestation period for sheep?", "answer": "5 months", "options": ["3 months", "5 months", "7 months", "9 months"], "description": "Sheep carry lambs for about 5 months."},
            {"question": "What is a common feed for goats?", "answer": "Browse", "options": ["Grain", "Browse", "Hay", "Silage"], "description": "Browse is plants goats eat, like shrubs."},
            {"question": "What is the term for a young goat?", "answer": "Kid", "options": ["Lamb", "Kid", "Calf", "Piglet"], "description": "A kid is a baby goat."},
            {"question": "What is the purpose of docking a lamb’s tail?", "answer": "Cleanliness", "options": ["Growth", "Cleanliness", "Strength", "Beauty"], "description": "Docking keeps the tail area clean."},
            {"question": "What mineral deficiency causes swayback in lambs?", "answer": "Copper", "options": ["Calcium", "Copper", "Iron", "Selenium"], "description": "Copper lack causes swayback, a spine issue."},
            {"question": "What is the term for a female goat?", "answer": "Doe", "options": ["Buck", "Doe", "Wether", "Nanny"], "description": "A doe is an adult female goat."},
            {"question": "What breed of sheep is known for wool?", "answer": "Merino", "options": ["Suffolk", "Merino", "Hampshire", "Dorset"], "description": "Merino sheep produce fine wool."},
            {"question": "What is the term for meat from a goat?", "answer": "Chevon", "options": ["Lamb", "Chevon", "Mutton", "Veal"], "description": "Chevon is goat meat."},
            {"question": "What protects sheep from predators?", "answer": "Fencing", "options": ["Barns", "Fencing", "Dogs", "Lights"], "description": "Fencing keeps sheep safe from harm."},
            {"question": "What is the term for a group of goats?", "answer": "Herd", "options": ["Flock", "Herd", "Pack", "Gaggle"], "description": "A herd is a group of goats."},
            {"question": "What disease affects sheep brains?", "answer": "Scrapie", "options": ["Foot rot", "Scrapie", "Bloat", "Pneumonia"], "description": "Scrapie is a fatal brain disease in sheep."},
            {"question": "What is the term for wool from a lamb’s first shearing?", "answer": "Hogget", "options": ["Fleece", "Hogget", "Shorn", "Clip"], "description": "Hogget is a lamb’s first wool cut."},
            {"question": "What improves wool quality in sheep?", "answer": "Good nutrition", "options": ["Cold weather", "Good nutrition", "Short days", "Exercise"], "description": "Good nutrition makes wool soft and strong."}
        ],
        "Swine": [
            {"question": "What is the term for a female pig that has not given birth?", "answer": "Gilt", "options": ["Boar", "Sow", "Gilt", "Barrow"], "description": "A gilt is a young female pig."},
            {"question": "What is a male pig called?", "answer": "Boar", "options": ["Sow", "Boar", "Gilt", "Barrow"], "description": "A boar is an adult male pig."},
            {"question": "What is the term for a castrated male pig?", "answer": "Barrow", "options": ["Boar", "Sow", "Gilt", "Barrow"], "description": "A barrow is a neutered male pig."},
            {"question": "What is a female pig that has given birth called?", "answer": "Sow", "options": ["Gilt", "Sow", "Boar", "Piglet"], "description": "A sow is a mother pig."},
            {"question": "What is the term for a baby pig?", "answer": "Piglet", "options": ["Calf", "Piglet", "Lamb", "Kid"], "description": "A piglet is a young pig."},
            {"question": "What is the gestation period for swine?", "answer": "3 months", "options": ["3 months", "5 months", "7 months", "9 months"], "description": "Pigs carry piglets for about 3 months."},
            {"question": "What disease causes diamond-shaped lesions in pigs?", "answer": "Erysipelas", "options": ["Swine flu", "Erysipelas", "Foot rot", "Mange"], "description": "Erysipelas leaves diamond marks on pig skin."},
            {"question": "What is a common feed for swine?", "answer": "Corn", "options": ["Hay", "Corn", "Grass", "Silage"], "description": "Corn gives pigs energy to grow."},
            {"question": "What is the term for a group of pigs?", "answer": "Herd", "options": ["Flock", "Herd", "Pack", "Litter"], "description": "A herd is a group of pigs."},
            {"question": "What is the purpose of tail docking in pigs?", "answer": "Prevent biting", "options": ["Growth", "Prevent biting", "Cleanliness", "Health"], "description": "Tail docking stops pigs from biting tails."},
            {"question": "What mineral deficiency causes rickets in pigs?", "answer": "Vitamin D", "options": ["Calcium", "Vitamin D", "Iron", "Magnesium"], "description": "Vitamin D lack causes weak bones in pigs."},
            {"question": "What is the term for a pig’s birth process?", "answer": "Farrowing", "options": ["Weaning", "Farrowing", "Gestation", "Lactation"], "description": "Farrowing is when pigs give birth."},
            {"question": "What improves pork quality in swine?", "answer": "Good feed", "options": ["Cold weather", "Good feed", "Exercise", "Water"], "description": "Good feed makes pork tasty."},
            {"question": "What is the term for a pig raised for meat?", "answer": "Market hog", "options": ["Breeder", "Market hog", "Feeder", "Sow"], "description": "Market hogs are grown for pork."},
            {"question": "What protects piglets from chilling?", "answer": "Heat lamp", "options": ["Blanket", "Heat lamp", "Hay", "Fan"], "description": "A heat lamp keeps piglets warm."},
            {"question": "What is a common swine identification method?", "answer": "Ear notch", "options": ["Tattoo", "Ear notch", "Collar", "Brand"], "description": "Ear notches mark pigs for tracking."},
            {"question": "What disease affects pig intestines?", "answer": "Swine dysentery", "options": ["Swine flu", "Swine dysentery", "Erysipelas", "Mange"], "description": "Swine dysentery causes diarrhea in pigs."},
            {"question": "What is the term for a pig’s litter size?", "answer": "Farrow", "options": ["Clutch", "Farrow", "Herd", "Pack"], "description": "Farrow is the number of piglets born."},
            {"question": "What improves growth rate in swine?", "answer": "Protein", "options": ["Carbohydrates", "Protein", "Fat", "Fiber"], "description": "Protein helps pigs grow fast."},
            {"question": "What is the term for swine housing?", "answer": "Pen", "options": ["Barn", "Pen", "Pasture", "Coop"], "description": "A pen keeps pigs contained."}
        ],
        "Beef": [
            {"question": "What is the ideal fat thickness for slaughter cattle?", "answer": "0.4-0.6 inches", "options": ["0.1-0.2 inches", "0.4-0.6 inches", "0.8-1.0 inches", "1.2-1.4 inches"], "description": "0.4-0.6 inches of fat ensures quality beef."},
            {"question": "What is a young steer called?", "answer": "Calf", "options": ["Bull", "Calf", "Cow", "Heifer"], "description": "A calf is a young beef animal."},
            {"question": "What is the term for a castrated male beef animal?", "answer": "Steer", "options": ["Bull", "Steer", "Cow", "Heifer"], "description": "A steer is a neutered male for beef."},
            {"question": "What is a female beef animal before her first calf?", "answer": "Heifer", "options": ["Cow", "Heifer", "Bull", "Steer"], "description": "A heifer hasn’t had a calf yet."},
            {"question": "What is an adult female beef animal called?", "answer": "Cow", "options": ["Bull", "Cow", "Heifer", "Steer"], "description": "A cow is a mature female beef animal."},
            {"question": "What is an uncastrated male beef animal called?", "answer": "Bull", "options": ["Steer", "Bull", "Cow", "Calf"], "description": "A bull is a male used for breeding."},
            {"question": "What feed finishes beef cattle for slaughter?", "answer": "Grain", "options": ["Hay", "Grain", "Grass", "Silage"], "description": "Grain adds fat for tasty beef."},
            {"question": "What is the term for beef cattle birth?", "answer": "Calving", "options": ["Farrowing", "Calving", "Lambing", "Kidding"], "description": "Calving is when beef cows give birth."},
            {"question": "What disease causes lameness in cattle?", "answer": "Foot rot", "options": ["Bloat", "Foot rot", "Pneumonia", "Scours"], "description": "Foot rot makes cattle limp."},
            {"question": "What is the gestation period for beef cattle?", "answer": "9 months", "options": ["6 months", "9 months", "12 months", "3 months"], "description": "Beef cattle carry calves for 9 months."},
            {"question": "What is a common beef breed?", "answer": "Angus", "options": ["Holstein", "Angus", "Jersey", "Guernsey"], "description": "Angus is known for quality beef."},
            {"question": "What improves marbling in beef?", "answer": "Grain feeding", "options": ["Grass feeding", "Grain feeding", "Hay feeding", "Water"], "description": "Grain feeding adds fat streaks in beef."},
            {"question": "What is the term for a group of beef cattle?", "answer": "Herd", "options": ["Flock", "Herd", "Pack", "Gaggle"], "description": "A herd is a group of beef cattle."},
            {"question": "What protects calves from disease at birth?", "answer": "Colostrum", "options": ["Water", "Colostrum", "Grain", "Hay"], "description": "Colostrum gives calves immunity."},
            {"question": "What is the term for beef cattle raised on grass?", "answer": "Grass-fed", "options": ["Grain-fed", "Grass-fed", "Silage-fed", "Hay-fed"], "description": "Grass-fed cattle eat pasture."},
            {"question": "What mineral prevents bloat in cattle?", "answer": "Salt", "options": ["Calcium", "Salt", "Magnesium", "Iron"], "description": "Salt helps control digestion."},
            {"question": "What is the term for removing cattle horns?", "answer": "Dehorning", "options": ["Docking", "Dehorning", "Castration", "Shearing"], "description": "Dehorning keeps cattle safe."},
            {"question": "What improves beef flavor?", "answer": "Aging", "options": ["Freezing", "Aging", "Boiling", "Salting"], "description": "Aging makes beef tastier."},
            {"question": "What is the term for a beef animal ready for slaughter?", "answer": "Finished", "options": ["Weaned", "Finished", "Growing", "Started"], "description": "Finished cattle are ready for meat."}
        ]
    }
}

# In-memory storage for answer histories, keyed by session ID
answer_histories = {}

def get_quiz_state():
    if 'quiz_state' not in session:
        session['quiz_state'] = {
            'score': 0,
            'question_index': 0,
            'category': '',
            'subsection': None,  # Added for nested Questions structure
            'answered': False,
            'question_order': [],
            'session_id': str(uuid.uuid4()),
            'last_active': datetime.now().isoformat()
        }
    return session['quiz_state']

@app.before_request
def before_request():
    logger.info("Initializing session")
    quiz_state = get_quiz_state()  # Ensures session_id exists
    now = datetime.now()
    # Cleanup old sessions (inactive > 1 hour)
    to_remove = []
    for sid, history in answer_histories.items():
        if sid != quiz_state['session_id']:  # Skip current session
            try:
                last_active = datetime.fromisoformat(answer_histories.get(sid + '_time', now.isoformat()))
                if now - last_active > timedelta(hours=1):
                    to_remove.append(sid)
            except:
                to_remove.append(sid)  # Clean up malformed entries
    for sid in to_remove:
        answer_histories.pop(sid, None)
        answer_histories.pop(sid + '_time', None)
    quiz_state['last_active'] = now.isoformat()
    session['quiz_state'] = quiz_state
    session.modified = True

@app.route('/')
def home():
    logger.info("Rendering home page")
    quiz_state = get_quiz_state()
    session_id = quiz_state['session_id']
    answer_histories[session_id] = []  # Reset for this user
    answer_histories[session_id + '_time'] = datetime.now().isoformat()  # Timestamp
    return render_template('home.html', categories=questions.keys())

@app.route('/start', methods=['POST'])
def start_quiz():
    quiz_state = get_quiz_state()
    session_id = quiz_state['session_id']
    answer_histories[session_id] = []  # Reset for this user
    answer_histories[session_id + '_time'] = datetime.now().isoformat()
    quiz_state['score'] = 0
    quiz_state['question_index'] = 0
    category = request.form['category']
    quiz_state['category'] = category
    
    if category == "Questions":
        subsection = request.form['subsection']  # Expecting this from second dropdown
        quiz_state['subsection'] = subsection
        question_list = questions["Questions"][subsection]
    else:
        quiz_state['subsection'] = None
        question_list = questions[category]
    
    quiz_state['question_order'] = list(range(len(question_list)))
    random.shuffle(quiz_state['question_order'])
    quiz_state['answered'] = False
    
    session['quiz_state'] = quiz_state
    session.modified = True
    
    current_q = question_list[quiz_state['question_order'][quiz_state['question_index']]]
    shuffled_options = random.sample(current_q['options'], len(current_q['options']))
    
    logger.info(f"Start: Q{quiz_state['question_index']+1}/{len(quiz_state['question_order'])}, Score={quiz_state['score']}")
    return render_template('quiz.html', 
                          question=current_q["question"],
                          options=shuffled_options,
                          image=current_q.get("image", ""),  # Default to empty string if no image
                          score=quiz_state['score'],
                          question_num=quiz_state['question_index'] + 1,
                          total=len(quiz_state['question_order']))

@app.route('/answer', methods=['POST'])
def answer():
    quiz_state = get_quiz_state()
    session_id = quiz_state['session_id']
    total_questions = len(quiz_state.get('question_order', []))
    logger.info(f"Answer: Q{quiz_state['question_index']+1}/{total_questions}, Score={quiz_state['score']}, Answered={quiz_state['answered']}")

    try:
        if quiz_state['category'] == "Questions":
            question_list = questions["Questions"][quiz_state['subsection']]
        else:
            question_list = questions[quiz_state['category']]
        
        current_q = question_list[quiz_state['question_order'][quiz_state['question_index']]]
        shuffled_options = random.sample(current_q['options'], len(current_q['options']))

        # Process answer if not yet answered
        if not quiz_state['answered']:
            user_answer = request.form.get('answer', '')
            if not user_answer:
                logger.warning(f"No answer provided for Q{quiz_state['question_index']+1}")

            correct_answer = current_q["answer"]
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            
            if is_correct:
                quiz_state['score'] += 1
                feedback = "Correct!"
                feedback_color = "green"
            else:
                feedback = f"Incorrect. You chose '{user_answer}'. The correct answer is '{correct_answer}'."
                feedback_color = "red"

            # Store in user's history
            if session_id not in answer_histories:
                answer_histories[session_id] = []
            answer_histories[session_id].append({
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'image': current_q.get("image", ""),
                'description': current_q["description"]
            })
            answer_histories[session_id + '_time'] = datetime.now().isoformat()

            quiz_state['answered'] = True
            session['quiz_state'] = quiz_state
            session.modified = True
            
            logger.info(f"Processed: User='{user_answer}', Correct='{correct_answer}', IsCorrect={is_correct}, NewScore={quiz_state['score']}, Feedback={feedback}")
            
            return render_template('quiz.html',
                                  question=current_q["question"],
                                  options=shuffled_options,
                                  image=current_q.get("image", ""),
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

        next_q = question_list[quiz_state['question_order'][quiz_state['question_index']]]
        next_shuffled_options = random.sample(next_q['options'], len(next_q['options']))
        
        quiz_state['answered'] = False
        session['quiz_state'] = quiz_state
        session.modified = True
        
        logger.info(f"Next: Q{quiz_state['question_index']+1}/{total_questions}, Score={quiz_state['score']}")
        return render_template('quiz.html',
                              question=next_q["question"],
                              options=next_shuffled_options,
                              image=next_q.get("image", ""),
                              score=quiz_state['score'],
                              question_num=quiz_state['question_index'] + 1,
                              total=total_questions)

    except Exception as e:
        logger.error(f"Error in /answer: {str(e)}")
        return "Internal Server Error", 500

@app.route('/results')
def results():
    quiz_state = get_quiz_state()
    session_id = quiz_state['session_id']
    total_questions = len(quiz_state.get('question_order', []))
    answers = answer_histories.get(session_id, [])
    logger.info(f"Results: Score={quiz_state['score']}/{total_questions}")
    return render_template('result.html', 
                          score=quiz_state['score'], 
                          total=total_questions,
                          answers=answers)

@app.route('/restart')
def restart():
    quiz_state = get_quiz_state()
    session_id = quiz_state['session_id']
    answer_histories[session_id] = []
    answer_histories[session_id + '_time'] = datetime.now().isoformat()
    logger.info("Restarting quiz")
    session.pop('quiz_state', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    logger.info("Starting Flask app locally")
    app.run(debug=True)
