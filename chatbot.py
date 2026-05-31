import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import random
import nltk
from nltk.stem import WordNetLemmatizer
import json
import os

# Ensure NLTK data is available
def setup_nltk():
    try:
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading punkt...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            print("Downloading wordnet...")
            nltk.download('wordnet', quiet=True)
            
    except Exception as e:
        print(f"Warning: NLTK Download failed: {e}. Chatbot functionality may be limited.")

class MLChatbot:
    def __init__(self):
        setup_nltk()
        self.lemmatizer = WordNetLemmatizer()
        self.intents = {
            "greetings": {
                "patterns": ["hi", "hello", "hey", "good morning", "good evening", "how are you", "what's up", "yo"],
                "responses": ["Hello, {name}! How can I help you today?", "Hi there, {name}! Ready to learn something new?", "Greetings! How are you feeling, {name}?", "Hi! I'm your AI learning friend. What shall we do today, {name}?"]
            },
            "learning_help": {
                "patterns": ["how to learn", "help with english", "what should i do", "start activity", "give me a task", "educational toys", "learning modules", "where to start"],
                "responses": ["You can start by visiting the English Hub, {name}! It has games for words and grammar.", "Try the Respectful Learner activity to learn social skills.", "The games hub has many fun activities to help you learn focusing and memory, {name}."]
            },
            "about_bot": {
                "patterns": ["who are you", "what are you", "what can you do", "are you a robot", "tell me about yourself"],
                "responses": ["I am your AI Learning Coach! I'm here to help you practice communication, social skills, and play fun learning games.", "I'm a friendly robot designed to help you master new skills on this platform, {name}!"]
            },
            "emotions_sad": {
                "patterns": ["i am sad", "i feel lonely", "i am upset", "i want to cry", "unhappy", "feeling blue"],
                "responses": ["I'm sorry you're feeling sad, {name}. Remember, it's okay to have big feelings. Maybe a fun game like 'Memory Match' could cheer you up?", "I'm here for you, {name}. You are doing a great job! Would you like to practice talking with the sentence builder?"]
            },
            "emotions_happy": {
                "patterns": ["i am happy", "i feel great", "today is good", "awesome day", "i am smiling"],
                "responses": ["That's wonderful! Your happiness makes me happy too!", "Great to hear! Let's keep that positive energy going with some learning!"]
            },
            "aac_help": {
                "patterns": ["how to talk", "aac", "where is the talk section", "help me speak", "speech tool"],
                "responses": ["You can use the 'Talk' section (AAC) to build sentences! Click words to say them out loud.", "The Talk tool helps you express yourself. You can even save your favorite phrases!"]
            },
            "games_quest": {
                "patterns": ["play game", "where are games", "fun stuff", "puzzles", "game hub"],
                "responses": ["Head over to the Game Hub! We have Memory Match, Routine Builder, and more.", "Games are a great way to learn. Which one is your favorite?"]
            },
            "respect": {
                "patterns": ["what is respect", "how to be respectful", "polite words", "being nice", "manners"],
                "responses": ["Respect is about listening to others and being kind.", "Using words like 'please' and 'thank you' is a great start!", "Check out our 'Respectful Learner' module for more tips."]
            },
            "goodbye": {
                "patterns": ["bye", "see you later", "goodbye", "i am leaving", "exit", "stop"],
                "responses": ["Goodbye! See you next time.", "Have a great day! Keep practicing.", "Bye! Come back soon."]
            },
            "thanks": {
                "patterns": ["thank you", "thanks", "that was helpful", "awesome", "cool", "nice"],
                "responses": ["You're very welcome!", "Happy to help!", "Glad you found it useful!"]
            },
            "emotion_help": {
                "patterns": ["emotion matcher", "feelings game", "how to read faces", "emotion help"],
                "responsesgit commit -m "Initial commit"": ["Check out the Emotion Matcher in the Game Hub! It's a fun way to learn about feelings.", "Recognizing emotions is a superpower! Our games can help you practice."]
            },
            "social_help": {
                "patterns": ["social skills", "how to behave", "being with friends", "social helper", "public places", "people rules"],
                "responses": ["The social adventure games can help you practice everyday situations!", "Being a good friend is about listening and sharing. You can practice this in our Learning Hub.", "Check out the Public Social Rules module to learn about behaving in stores and parks!"]
            },
            "math_help": {
                "patterns": ["math", "numbers", "counting", "adding", "math magic", "arithmetic"],
                "responses": ["You can practice your numbers in the 'Math Magic' game! It uses fun emojis to help you count.", "Numbers are like puzzles. Want to try the Math Magic module in the Learning Hub?"]
            },
            "grammar_help": {
                "patterns": ["grammar", "words", "prefix", "suffix", "builder", "word builder", "sentence builder", "english words"],
                "responses": ["Mastering words is fun! Try the 'Word Builder' to learn about prefixes and suffixes.", "The Sentence Builder and Word Builder games are great for practicing your English skills."]
            },
            "weather_help": {
                "patterns": ["weather", "clothes", "sunny", "rainy", "snowy", "what to wear", "weather matcher"],
                "responses": ["Stay safe and comfortable by learning about the weather in our 'Weather Matcher' game!", "The Weather Matcher helps you decide what to wear for different days. Give it a try!"]
            },
            "social_practice_greeting": {
                "patterns": ["practice saying hi", "start a conversation", "how to greet someone", "practice greeting", "hello practice"],
                "responses": ["Great idea! Let's practice. I'll be the friend. I say: 'Hi, how are you?'. Now you try answering!", "To start a chat, you can say: 'Hello! I like your shirt.' or 'Hi, how is your day?'. Want to try one?"]
            },
            "social_practice_day": {
                "patterns": ["ask about someone's day", "how to ask how are you", "what to say after hi"],
                "responses": ["You can ask: 'What did you do today?' or 'What was the best part of your day?'. These are great ways to show you care!", "Try asking me: 'How was your morning?'. I'll answer and we can practice!"]
            },
            "social_practice_request": {
                "patterns": ["how to ask for help", "may i have", "can i use", "asking for something"],
                "responses": ["When we want something, we use 'Please'. For example: 'May I please have a turn?' or 'Could you help me with this, please?'. Shall we practice?"]
            },
            "respect_manners": {
                "patterns": ["please", "thank you", "you are welcome", "sorry", "pardon", "may i", "excuse me", "kindness"],
                "responses": ["It's so wonderful to use polite words! You're a very respectful learner, {name}.", "Manners make the world a better place. Thank you for being so polite!", "Using words like 'please' and 'thank you' is a sign of a great hero!"]
            },
            # --- Parent & caregiver information intents ---
            "parent_overview": {
                "patterns": ["i am a parent", "as a parent", "for parents", "guide for parents", "my child was diagnosed", "my kid has autism"],
                "responses": [
                    "This platform is designed to support autistic children and their families. As a parent, you can use the Clinical Insights and Parent Support sections to track progress and get practical ideas for home.",
                    "For parents, the most important things are safety, communication, and predictable routines. The Parent Support page gives you calm tips and curated resources to get started."
                ]
            },
            "therapy_questions": {
                "patterns": ["what therapy", "which therapy", "aba", "speech therapy", "occupational therapy", "ot therapy", "how much therapy", "how often therapy"],
                "responses": [
                    "Common therapies include speech-language therapy, occupational therapy (OT), and behavioral supports like ABA. The right mix depends on your child's strengths, challenges, and what feels respectful and sustainable for your family.",
                    "Therapy should be individualized. A good team will explain clear goals, how progress is measured, and how you can practice simple skills at home in short, manageable steps."
                ]
            },
            "school_support": {
                "patterns": ["school plan", "iep", "504", "support at school", "help at school", "teacher meeting"],
                "responses": [
                    "At school, many autistic students have an individualized plan (often called an IEP or 504 plan) that lists supports like extra time, visual schedules, or quiet spaces. Bringing data or summaries from this platform can help guide those conversations.",
                    "For school meetings, it helps to bring a short list of your child's strengths, current challenges, and 2‑3 priorities. Ask how the school will measure progress and how they will keep you updated."
                ]
            },
            "behavior_meltdown": {
                "patterns": ["meltdown", "tantrum", "behavior issue", "problem behavior", "challenging behavior", "aggressive", "self injur", "head bang"],
                "responses": [
                    "Meltdowns are usually a sign of overload, not bad behavior. The safest first steps are: reduce noise and demands, offer a calm space, and make sure everyone is physically safe before talking about rules.",
                    "After things are calm, try to notice patterns: Was your child hungry, tired, overwhelmed, or confused? Tracking triggers over time (for example in a journal) can help your therapy team adjust supports."
                ]
            },
            "diagnosis_info": {
                "patterns": ["how is autism diagnosed", "diagnosis process", "who can diagnose", "get a diagnosis", "assessment"],
                "responses": [
                    "Autism is typically diagnosed by a specialist such as a developmental pediatrician, child psychiatrist, neurologist, or psychologist using interviews, observation, and developmental history.",
                    "If you are seeking a diagnosis, ask your pediatrician for a referral to a specialist who regularly evaluates autistic children, and bring notes about your child's communication, play, behavior, and sensory needs."
                ]
            },
            "sleep_and_routine": {
                "patterns": ["sleep problem", "sleep issues", "bedtime", "routine help", "daily routine", "schedule"],
                "responses": [
                    "Many autistic children sleep better with a very consistent routine: same steps, same order, same time each night, and low light and noise in the bedroom.",
                    "Visual schedules and timers can make transitions easier. Start with a short, predictable sequence like bath → pajamas → one story → lights out, and practice it the same way every night."
                ]
            },
            "diet_and_sensory": {
                "patterns": ["picky eating", "food issues", "diet", "sensory food", "my child only eats", "texture"],
                "responses": [
                    "Picky eating is often linked to sensory differences in taste, texture, or smell. Pushing hard can backfire; slow, low‑pressure exposure is usually safer.",
                    "You can offer one safe food plus a very small portion of a new food on the same plate, without forcing bites. If growth or nutrition are concerns, a pediatrician or dietitian with autism experience is important."
                ]
            },
            "platform_help": {
                "patterns": ["how to use this app", "what does clinical insights mean", "how to use parent support", "explain this platform", "what is this app"],
                "responses": [
                    "The Home page shows your child's day‑to‑day progress. Clinical Insights gives more detailed graphs for professionals, while Parent Support gives you plain‑language tips and links to outside resources.",
                    "You can use Games and Academy with your child, and then review the Clinical Insights or Parent Support sections on your own to plan next steps with teachers or therapists."
                ]
            }
        }
        self.train_model()

    def clean_text(self, text):
        tokens = nltk.word_tokenize(text.lower())
        return " ".join([self.lemmatizer.lemmatize(token) for token in tokens])

    def train_model(self):
        X = []
        y = []
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                X.append(self.clean_text(pattern))
                y.append(intent)
        
        self.vectorizer = TfidfVectorizer()
        X_vec = self.vectorizer.fit_transform(X)
        self.model = SVC(kernel='linear', probability=True)
        self.model.fit(X_vec, y)

    def get_response(self, user_input, username="Student", context=None):
        """
        Context-aware response generation. 
        Context can include: 'mood', 'stress_level', 'recent_activity', 'lowest_domain'
        """
        cleaned_input = self.clean_text(user_input)
        input_lower = user_input.lower()
        
        # 1. Contextual awareness (The "Responsibility" Layer)
        context_prefix = ""
        if context:
            mood = context.get('mood')
            stress = context.get('stress_level', 1)
            
            if stress >= 4:
                context_prefix = "I'm noticing things might feel a bit overwhelming right now. Let's take it slow. "
            elif mood == "Sad":
                context_prefix = "I'm here for you if you're feeling a bit down. You're doing a great job just by being here. "
            elif mood == "Happy":
                context_prefix = "It's wonderful to see you in such a great mood! Let's channel that energy into something fun. "

        # 2. Empathy & Sentiment Layer (Detecting Mood from current input)
        sentiment_response = context_prefix
        sad_keywords = ["sad", "upset", "cry", "lonely", "unhappy", "bad", "angry", "mad", "frustrated", "hurt", "broke"]
        happy_keywords = ["happy", "good", "great", "awesome", "fun", "excited", "smile", "proud", "yay", "cool"]
        frustrated_keywords = ["hard", "difficult", "impossible", "can't", "stress", "stuck", "fail", "wrong"]
        lonely_keywords = ["alone", "nobody", "lonely", "miss", "quiet", "ignored"]
        
        if any(word in input_lower for word in frustrated_keywords):
            sentiment_response = f"I understand it feels tough right now, {username}. Learning new things can be hard, but taking a deep breath helps. You are very brave for trying! "
        elif any(word in input_lower for word in lonely_keywords):
            sentiment_response = f"I am right here with you, {username}. You are never truly alone when we are learning together. I'm your AI friend and I'm always ready to talk! "
        elif any(word in input_lower for word in sad_keywords):
            sentiment_response = f"I'm here for you, {username}. It's okay to feel this way, and I'm listening closely. How can I help make your day a little brighter? "
        elif any(word in input_lower for word in happy_keywords):
            sentiment_response = f"I'm so glad to see you're having a great time, {username}! Your smile makes me happy too, and your hard work is really paying off! "

        # 2. Keyword-First Matching (The "If-Else" Layer for Reliability)
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                if pattern in input_lower:
                    response = random.choice(data['responses'])
                    return self.personalize(sentiment_response + response, username)

        # 3. ML Classifier Fallback
        input_vec = self.vectorizer.transform([cleaned_input])
        probs = self.model.predict_proba(input_vec)[0]
        max_prob_idx = np.argmax(probs)
        confidence = probs[max_prob_idx]
        
        if confidence < 0.4:
            if sentiment_response:
                return f"{sentiment_response} I'm listening closely to your feelings. Can you tell me more about that so I can help you better?"
            return f"I'm not quite sure about that last part, {username}. However, I'm always here to help you with games, talking, or just a friendly chat! What shall we do next?"
        
        intent = self.model.classes_[max_prob_idx]
        response = random.choice(self.intents[intent]['responses'])
        return self.personalize(sentiment_response + response, username)

    def personalize(self, response, username):
        if "{name}" in response:
            response = response.replace("{name}", username)
        
        # Responsible persona addition: always encouraging
        encouragements = [
            "You are doing brilliantly!",
            "I'm so proud of your progress today.",
            "Remember, every small step counts.",
            "You have a real talent for this!"
        ]
        
        if random.random() > 0.8:
            response = f"{response} {random.choice(encouragements)}"
        
        if random.random() > 0.7 and "{name}" not in response: 
            response = f"{response}, {username}!"
            
        return response

# Initialize singleton
chatbot = MLChatbot()
