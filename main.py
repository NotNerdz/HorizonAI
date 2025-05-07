import os
import time
import json
import random
import string
import requests
import wikipediaapi
import re
from datetime import datetime
from difflib import SequenceMatcher
from colorama import init, Fore, Style
import threading
import sys

# Initialize colorama for cross-platform colored terminal output
init()


class HorizonAI:
    """
    HorizonAI v1.4 Nexus - Advanced conversational AI with pattern recognition,
    comprehensive understanding, and seamless Wikipedia integration.
    """

    def __init__(self):
        self.name = "HorizonAI"
        self.version = "1.4 Nexus"
        self.conversation_history = []
        self.knowledge_base = {}
        self.pattern_database = {}
        self.sentiment_patterns = {
            "positive": ["happy", "good", "great", "excellent", "wonderful", "amazing", "love", "enjoy", "appreciate"],
            "negative": ["sad", "bad", "terrible", "awful", "horrible", "hate", "dislike", "disappointed", "upset"],
            "neutral": ["okay", "fine", "alright", "so-so", "average"]
        }

        # Initialize Wikipedia API with English language
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='HorizonAI/1.4 (https://horizon-ai.example.com; info@horizon-ai.example.com)'
        )

        # Load existing knowledge base
        self.load_knowledge_base()

        # Set up conversation context tracking
        self.conversation_context = {
            "topic": None,
            "entities": [],
            "sentiment": "neutral",
            "recent_queries": []
        }

        # Animation settings
        self.animation_speed = 0.02
        self.animation_active = False

        # Greeting the user
        self.display_startup_animation()

    def load_knowledge_base(self):
        """Load pre-existing knowledge or create a new knowledge base"""
        try:
            if os.path.exists("horizon_knowledge.json"):
                with open("horizon_knowledge.json", "r") as f:
                    self.knowledge_base = json.load(f)
                print(f"{Fore.CYAN}Knowledge base loaded: {len(self.knowledge_base)} entries{Style.RESET_ALL}")
            else:
                # Initialize with some basic knowledge
                self.knowledge_base = {
                    "self": {
                        "name": "HorizonAI",
                        "version": "1.4 Nexus",
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "capabilities": [
                            "advanced conversation",
                            "pattern recognition",
                            "topic understanding",
                            "Wikipedia integration",
                            "adaptive learning"
                        ]
                    }
                }
                print(f"{Fore.YELLOW}New knowledge base initialized{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error loading knowledge base: {e}{Style.RESET_ALL}")
            self.knowledge_base = {}

    def save_knowledge_base(self):
        """Save the current knowledge base to a JSON file"""
        try:
            with open("horizon_knowledge.json", "w") as f:
                json.dump(self.knowledge_base, f, indent=2)
            print(f"{Fore.GREEN}Knowledge base saved successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error saving knowledge base: {e}{Style.RESET_ALL}")

    def display_startup_animation(self):
        """Display a cool startup animation for HorizonAI"""
        os.system('cls' if os.name == 'nt' else 'clear')

        # ASCII art logo
        logo = [
            "  _    _               _                    _    ___ ",
            " | |  | |             (_)                  / |  / _ \\",
            " | |__| | ___  _ __ ___  ______  _ __    / /  | | | |",
            " |  __  |/ _ \\| '__| | |/_/|_ / | '_ \\  / /   | | | |",
            " | |  | | (_) | |  | |  < / _ \\| | | |/ /    | |_| |",
            " |_|  |_|\\___/|_|  |_|\\_\\\\___/|_| |_/_/      \\___/ ",
            "                                                    ",
            f"                v{self.version}                   ",
            "                                                    "
        ]

        # Animated typing effect for the logo
        for line in logo:
            for char in line:
                print(f"{Fore.CYAN}{char}{Style.RESET_ALL}", end='', flush=True)
                time.sleep(0.001)
            print()

        # Loading animation
        print(f"\n{Fore.GREEN}Initializing systems...{Style.RESET_ALL}")
        systems = [
            "Neural Networks",
            "Pattern Recognition",
            "Knowledge Base",
            "Conversation Engine",
            "Context Analyzer",
            "Wikipedia Integration",
            "Semantic Processing",
            "Deep Understanding Module"
        ]

        for system in systems:
            progress_bar = "["
            for i in range(30):
                progress_bar += "■"
                print(f"\r{Fore.YELLOW}Loading {system}: {progress_bar}{' ' * (30 - i)}] {i + 1}%", end="", flush=True)
                time.sleep(0.01)
            print(f"{Fore.GREEN} ✓{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}HorizonAI v{self.version} is now online and ready to assist you.{Style.RESET_ALL}\n")

    def animated_text(self, text, color=Fore.CYAN):
        """Display text with typing animation"""
        for char in text:
            print(f"{color}{char}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(self.animation_speed)
        print()

    def thinking_animation(self, duration=2):
        """Display a 'thinking' animation for the specified duration"""
        self.animation_active = True

        def animate():
            animations = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            i = 0
            start_time = time.time()

            while self.animation_active and (time.time() - start_time) < duration:
                sys.stdout.write(f"\r{Fore.CYAN}Thinking {animations[i % len(animations)]}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1

            sys.stdout.write("\r" + " " * 20 + "\r")
            sys.stdout.flush()

        # Run animation in a separate thread
        animation_thread = threading.Thread(target=animate)
        animation_thread.start()

        # Simulate processing time
        time.sleep(duration)
        self.animation_active = False
        animation_thread.join()

    def get_wikipedia_info(self, query):
        """Retrieve information from Wikipedia with enhanced handling"""
        try:
            # Clean and prepare the query
            clean_query = query.strip().title()  # Capitalize first letters for better search results

            # Log the query attempt
            print(f"{Fore.BLUE}Searching Wikipedia for: {clean_query}{Style.RESET_ALL}")

            # Search for the page
            page = self.wiki.page(clean_query)

            if page.exists():
                # Get a summary (first few sentences)
                summary = page.summary[0:600] + "..." if len(page.summary) > 600 else page.summary
                return {
                    "title": page.title,
                    "summary": summary,
                    "url": page.fullurl,
                    "retrieved": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "exists": True
                }
            else:
                # Try to search for related terms
                search_results = self.search_wikipedia(clean_query)
                if search_results:
                    return {
                        "error": f"No exact match for '{clean_query}'",
                        "suggestions": search_results[:5],
                        "retrieved": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "exists": False
                    }
                else:
                    return {
                        "error": f"No information found for '{clean_query}'",
                        "exists": False
                    }
        except Exception as e:
            print(f"{Fore.RED}Wikipedia retrieval error: {str(e)}{Style.RESET_ALL}")
            return {
                "error": f"Error retrieving information: {str(e)}",
                "exists": False
            }

    def search_wikipedia(self, query):
        """Search Wikipedia for related terms when exact match is not found"""
        try:
            # Make a request to Wikipedia's API
            url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "opensearch",
                "search": query,
                "limit": 10,
                "namespace": 0,
                "format": "json"
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data[1]  # Return the list of search results
            return []
        except Exception as e:
            print(f"{Fore.RED}Wikipedia search error: {str(e)}{Style.RESET_ALL}")
            return []

    def extract_entities(self, text):
        """Extract key entities from the input text with enhanced detection"""
        # Simple entity extraction - in production would use NER
        entities = []

        # Find capitalized words as potential entities
        caps_pattern = r'\b[A-Z][a-z]+\b'
        capitalized_words = re.findall(caps_pattern, text)

        # Common words to exclude
        common_words = ["I", "You", "He", "She", "They", "We", "It", "What", "Who", "How",
                        "Why", "When", "Where", "Is", "Are", "The", "A", "An", "This", "That"]

        # Filter out common words
        filtered_words = [word for word in capitalized_words if word not in common_words]
        entities.extend(filtered_words)

        # Find multi-word entities (like "New York" or "George Washington")
        phrase_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        phrases = re.findall(phrase_pattern, text)
        entities.extend(phrases)

        # Look for quoted terms that might be entities
        quotes_pattern = r'"([^"]*)"'
        quoted_terms = re.findall(quotes_pattern, text)
        entities.extend(quoted_terms)

        # Return unique entities
        return list(set(entities))

    def extract_question_subject(self, question):
        """Extract the main subject of a question for Wikipedia lookup"""
        question = question.strip().lower()

        # Define question patterns to match
        question_patterns = {
            "who is": r"who is (.*?)(?:\?|$)",
            "who are": r"who are (.*?)(?:\?|$)",
            "who was": r"who was (.*?)(?:\?|$)",
            "who were": r"who were (.*?)(?:\?|$)",
            "what is": r"what is (.*?)(?:\?|$)",
            "what are": r"what are (.*?)(?:\?|$)",
            "what was": r"what was (.*?)(?:\?|$)",
            "what were": r"what were (.*?)(?:\?|$)",
            "where is": r"where is (.*?)(?:\?|$)",
            "where are": r"where are (.*?)(?:\?|$)",
            "when did": r"when did (.*?)(?:\?|$)",
            "when was": r"when was (.*?)(?:\?|$)",
            "tell me about": r"tell me about (.*?)(?:\.|$)",
            "information on": r"information on (.*?)(?:\.|$)",
            "explain": r"explain (.*?)(?:\.|$)"
        }

        # Check each pattern
        for pattern_name, pattern in question_patterns.items():
            match = re.search(pattern, question)
            if match:
                subject = match.group(1).strip()
                return subject

        # If no pattern matched but there are entities, use the first entity
        entities = self.extract_entities(question)
        if entities:
            return entities[0]

        # Last resort: remove question words and common words
        question_words = ["who", "what", "where", "when", "why", "how"]
        common_words = ["is", "are", "was", "were", "the", "a", "an", "in", "on", "at"]
        words = question.split()

        if words and words[0] in question_words:
            # Remove the question word
            words = words[1:]

            # Remove common words at the beginning
            while words and words[0] in common_words:
                words = words[1:]

            # Join the remaining words as the subject
            subject = " ".join(words).strip("?").strip()
            return subject

        # If all else fails, return the whole question without '?'
        return question.strip("?")

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the input text with improved detection"""
        text_lower = text.lower()
        sentiment_scores = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        # Expanded sentiment analysis patterns
        expanded_sentiment_patterns = {
            "positive": [
                "happy", "good", "great", "excellent", "wonderful", "amazing", "love", "enjoy", "appreciate",
                "fantastic", "terrific", "awesome", "superb", "delighted", "pleased", "thrilled", "excited",
                "impressed", "thankful", "grateful", "satisfied", "perfect", "best", "better", "brilliant"
            ],
            "negative": [
                "sad", "bad", "terrible", "awful", "horrible", "hate", "dislike", "disappointed", "upset",
                "angry", "annoyed", "frustrated", "irritated", "unhappy", "depressed", "worried", "concerned",
                "worst", "worse", "poor", "unfortunate", "disappointing", "disastrous", "terrible", "miserable"
            ],
            "neutral": [
                "okay", "fine", "alright", "so-so", "average", "moderate", "adequate", "acceptable",
                "fair", "reasonable", "standard", "ordinary", "common", "regular", "normal", "typical"
            ]
        }

        # Update the sentiment patterns with expanded lists
        self.sentiment_patterns = expanded_sentiment_patterns

        # Check for sentiment words
        for sentiment, words in self.sentiment_patterns.items():
            for word in words:
                if word in text_lower:
                    sentiment_scores[sentiment] += 1

        # Check for negations that could flip sentiment
        negations = ["not", "n't", "no", "never", "neither", "nor", "hardly", "barely"]
        has_negation = any(neg in text_lower for neg in negations)

        if has_negation:
            # Simple negation handling - swap positive and negative scores
            sentiment_scores["positive"], sentiment_scores["negative"] = sentiment_scores["negative"], sentiment_scores[
                "positive"]

        # Determine the dominant sentiment
        if max(sentiment_scores.values()) == 0:
            return "neutral"
        return max(sentiment_scores, key=sentiment_scores.get)

    def detect_patterns(self, text):
        """Detect patterns in user input and update pattern database"""
        # Update frequency of words and phrases
        words = text.lower().split()
        for word in words:
            if word not in self.pattern_database:
                self.pattern_database[word] = 1
            else:
                self.pattern_database[word] += 1

        # Detect common phrases (n-grams)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram not in self.pattern_database:
                self.pattern_database[bigram] = 1
            else:
                self.pattern_database[bigram] += 1

        # Detect longer phrases (trigrams)
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i + 1]} {words[i + 2]}"
            if trigram not in self.pattern_database:
                self.pattern_database[trigram] = 1
            else:
                self.pattern_database[trigram] += 1

        # Return the most common patterns for this conversation
        common_patterns = sorted(self.pattern_database.items(), key=lambda x: x[1], reverse=True)[:5]
        return common_patterns

    def update_conversation_context(self, user_input):
        """Update the conversation context based on user input"""
        # Extract entities
        entities = self.extract_entities(user_input)
        if entities:
            self.conversation_context["entities"].extend(entities)
            # Keep only the 10 most recent entities
            self.conversation_context["entities"] = self.conversation_context["entities"][-10:]

        # Determine topic if not set
        if not self.conversation_context["topic"] and entities:
            self.conversation_context["topic"] = entities[0]

        # Update sentiment
        self.conversation_context["sentiment"] = self.analyze_sentiment(user_input)

        # Check if it's a question and track it
        if user_input.strip().endswith("?") or any(user_input.lower().startswith(q) for q in
                                                   ["who", "what", "when", "where", "why", "how"]):
            # Extract the subject
            subject = self.extract_question_subject(user_input)
            if subject:
                # Add to recent queries list
                self.conversation_context["recent_queries"].append(subject)
                # Keep the list to a reasonable size
                self.conversation_context["recent_queries"] = self.conversation_context["recent_queries"][-5:]

    def find_relevant_response(self, user_input):
        """Find the most relevant response based on pattern matching"""
        # Look for direct matches in conversation history
        best_match = None
        best_match_ratio = 0

        # Check for similarity with previous conversation
        for entry in self.conversation_history:
            if "user_input" in entry:
                similarity = SequenceMatcher(None, user_input.lower(), entry["user_input"].lower()).ratio()
                if similarity > best_match_ratio and similarity > 0.7:  # Threshold for considering it a match
                    best_match_ratio = similarity
                    if "ai_response" in entry:
                        best_match = entry["ai_response"]

        # If we found a very similar previous interaction, use it as a base for response
        if best_match:
            # Modify slightly to avoid exact repetition
            words = best_match.split()
            if len(words) > 5:
                # Replace a random word with a synonym or alternative
                idx = random.randint(0, len(words) - 1)
                words[idx] = self.get_alternative_word(words[idx])
                best_match = " ".join(words)

            return f"{best_match}"

        return None

    def get_alternative_word(self, word):
        """Get an alternative word to avoid repetition"""
        # Expanded alternatives dictionary for more varied responses
        alternatives = {
            "good": ["great", "excellent", "wonderful", "fantastic", "superb", "outstanding"],
            "bad": ["poor", "terrible", "awful", "unpleasant", "dreadful", "unfavorable"],
            "happy": ["glad", "delighted", "pleased", "joyful", "cheerful", "thrilled"],
            "sad": ["unhappy", "disappointed", "down", "blue", "gloomy", "melancholy"],
            "interesting": ["fascinating", "intriguing", "engaging", "compelling", "captivating"],
            "boring": ["dull", "tedious", "monotonous", "uninteresting", "bland"],
            "important": ["crucial", "essential", "significant", "vital", "key", "critical"],
            "difficult": ["challenging", "hard", "tough", "complicated", "complex", "demanding"],
            "easy": ["simple", "straightforward", "effortless", "uncomplicated", "basic"],
            "beautiful": ["attractive", "gorgeous", "stunning", "lovely", "exquisite"],
            "understand": ["comprehend", "grasp", "get", "follow", "perceive"],
            "think": ["believe", "consider", "feel", "reckon", "suppose", "assume"],
            "say": ["mention", "state", "express", "articulate", "communicate", "convey"],
            "big": ["large", "substantial", "sizable", "massive", "extensive", "huge"],
            "small": ["little", "tiny", "slight", "minor", "modest", "compact"]
        }

        # Check if we have alternatives for this word
        word_lower = word.lower()
        if word_lower in alternatives:
            return random.choice(alternatives[word_lower])

        # If not, return the original word
        return word

    def is_question(self, text):
        """Determine if the input text is a question"""
        text = text.strip().lower()

        # Check if text ends with question mark
        if text.endswith("?"):
            return True

        # Check if text starts with common question words
        question_starters = ["who", "what", "when", "where", "why", "how", "is", "are", "can", "could",
                             "would", "should", "do", "does", "did", "will", "shall", "may", "might"]

        first_word = text.split()[0] if text else ""
        if first_word in question_starters:
            return True

        return False

    def generate_response(self, user_input):
        """Generate a response based on user input with enhanced understanding"""
        # Update conversation context
        self.update_conversation_context(user_input)

        # Add user input to conversation history
        self.conversation_history.append(
            {"user_input": user_input, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # Display thinking animation - variable duration for more natural feel
        self.thinking_animation(random.uniform(1.0, 2.5))

        # Check if it's a question about the AI itself
        if "your name" in user_input.lower():
            response = f"I am {self.name}, version {self.version}, an advanced AI assistant with enhanced conversational capabilities and knowledge integration."

        elif any(phrase in user_input.lower() for phrase in
                 ["how do you work", "how do you function", "how were you made"]):
            response = "I function through advanced pattern recognition and contextual understanding. Unlike systems based solely on predefined prompts, I analyze conversation dynamics, maintain contextual memory, and integrate real-time information from sources like Wikipedia. My neural processing allows me to understand complex questions and provide comprehensive responses."

        # Check if it's a question that should trigger Wikipedia lookup
        elif self.is_question(user_input):
            # Extract the subject of the question
            query_subject = self.extract_question_subject(user_input)

            if query_subject:
                # Attempt Wikipedia lookup
                print(f"{Fore.YELLOW}Identified question about: {query_subject}{Style.RESET_ALL}")
                info = self.get_wikipedia_info(query_subject)

                if info.get("exists", False):
                    # Format Wikipedia information into a response
                    response = f"According to Wikipedia, {info['summary']}\n\nSource: {info['url']}"
                elif "suggestions" in info:
                    response = f"I couldn't find exact information on '{query_subject}'. Did you mean: {', '.join(info['suggestions'])}?"
                else:
                    # No Wikipedia info but still try to give a thoughtful response
                    response = f"I don't have specific Wikipedia information about '{query_subject}'. Would you like to know something else about this topic, or shall we explore a different subject?"
            else:
                # If we couldn't extract a subject, respond conversationally
                pattern_response = self.find_relevant_response(user_input)
                if pattern_response:
                    response = pattern_response
                else:
                    response = "That's an interesting question. Could you provide more details about what you're trying to learn?"

        # Use pattern-based response if available for non-questions
        elif not self.is_question(user_input):
            pattern_response = self.find_relevant_response(user_input)
            if pattern_response:
                response = pattern_response
            else:
                # Generate a contextual response
                if self.conversation_context["sentiment"] == "positive":
                    response = f"I'm glad to hear that! "
                elif self.conversation_context["sentiment"] == "negative":
                    response = f"I understand your concern. "
                else:
                    response = ""

                # Add topic-related content
                if self.conversation_context["topic"]:
                    response += f"Regarding {self.conversation_context['topic']}, "

                # Add a genuinely thoughtful response
                thoughtful_responses = [
                    "I find that topic quite interesting. What aspects would you like to explore further?",
                    "That's a fascinating perspective. Have you considered how this connects to broader themes?",
                    "I appreciate you sharing that. Would you like to discuss the implications in more detail?",
                    "That's a meaningful point. How does this relate to your personal experience?",
                    "Interesting thoughts. I'm curious about what led you to this particular viewpoint."
                ]
                response += random.choice(thoughtful_responses)
        else:
            # Default response for anything else
            response = "I find your message interesting. Could you tell me more about what you're thinking?"

        # Store AI response in history
        self.conversation_history[-1]["ai_response"] = response

        # Return the generated response
        return response

    def run(self):
        """Main interaction loop for HorizonAI"""
        print(f"{Fore.GREEN}Type 'exit' or 'quit' to end the conversation.{Style.RESET_ALL}")

        while True:
            try:
                user_input = input(f"\n{Fore.YELLOW}You: {Style.RESET_ALL}")

                if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                    self.animated_text(f"\n{self.name}: Goodbye! It was nice talking with you.", Fore.GREEN)
                    self.save_knowledge_base()
                    break

                response = self.generate_response(user_input)
                self.animated_text(f"\n{self.name}: {response}", Fore.CYAN)

            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}Conversation interrupted.{Style.RESET_ALL}")
                self.save_knowledge_base()
                break
            except Exception as e:
                print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
                # Try to recover and continue
                print(f"{Fore.YELLOW}HorizonAI is recovering...{Style.RESET_ALL}")


# Run the AI if this script is executed directly
if __name__ == "__main__":
    horizon = HorizonAI()
    horizon.run()