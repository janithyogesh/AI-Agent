import os
import json
import re
import requests
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import wikipedia
import math

class AIAgent:
    def __init__(self):
        # Use a better model that's still free and relatively small
        self.model_name = "microsoft/DialoGPT-medium"  # Better for conversations
        # Alternative: "facebook/blenderbot-400M-distill" for more conversational AI
        
        print("Loading AI model (this may take a moment)...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Add padding token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Create text generation pipeline
        self.generator = pipeline(
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Available tools
        self.tools = {
            "calculator": self.calculator,
            "wikipedia": self.search_wikipedia,
            "weather": self.get_weather,
            "datetime": self.get_datetime,
            "help": self.show_help
        }
        
        print("Enhanced AI Agent Ready!")
        print("Try: 'calculate 25 * 4', 'search python programming', 'what time is it?'")
        print("Type 'help' for available commands or 'exit' to quit.\n")

    def detect_intent(self, user_input):
        """Detect what the user wants to do based on their input"""
        user_input_lower = user_input.lower()
        
        # Calculator patterns
        if any(word in user_input_lower for word in ["calculate", "compute", "math", "+", "-", "*", "/", "="]):
            return "calculator"
        
        # Wikipedia search patterns
        if any(word in user_input_lower for word in ["search", "wiki", "tell me about", "what is", "who is"]):
            return "wikipedia"
        
        # Weather patterns
        if any(word in user_input_lower for word in ["weather", "temperature", "forecast"]):
            return "weather"
        
        # Time/date patterns
        if any(word in user_input_lower for word in ["time", "date", "today", "now"]):
            return "datetime"
        
        # Help patterns
        if any(word in user_input_lower for word in ["help", "commands", "what can you do"]):
            return "help"
        
        return "chat"

    def calculator(self, expression):
        """Safe calculator function"""
        try:
            # Extract numbers and basic operations
            expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Use eval safely for basic math (in production, use a proper math parser)
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculator error: Invalid expression. Try something like '25 * 4' or '100 / 5'"

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            # Remove search trigger words
            query = re.sub(r'\b(search|wiki|tell me about|what is|who is)\b', '', query, flags=re.IGNORECASE).strip()
            
            if not query:
                return "Please specify what you'd like to search for."
            
            # Search Wikipedia
            summary = wikipedia.summary(query, sentences=3)
            return f"Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Try being more specific: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query}'. Try a different search term."
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_weather(self, location=""):
        """Get weather information (using a free API would require API key)"""
        # For demo purposes - in real implementation, use OpenWeatherMap free tier
        return "Weather service requires API setup. Try: 'Free weather APIs: OpenWeatherMap, WeatherAPI'"

    def get_datetime(self, query=""):
        """Get current date and time"""
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    def show_help(self, query=""):
        """Show available commands"""
        help_text = """
Available Commands:
• Calculator: 'calculate 25 * 4', 'what's 100 / 5?'
• Wikipedia: 'search python', 'tell me about AI', 'who is Einstein?'
• Time: 'what time is it?', 'current date'
• Weather: 'weather' (demo - needs API setup)
• Help: 'help', 'what can you do?'
• Chat: Just talk normally for general conversation!
        """
        return help_text.strip()

    def generate_response(self, user_input):
        """Generate AI response using the language model"""
        try:
            # Prepare conversation context
            context = ""
            if self.conversation_history:
                # Include last few exchanges for context
                recent_history = self.conversation_history[-4:]  # Last 2 exchanges
                for exchange in recent_history:
                    context += f"Human: {exchange['user']}\nAI: {exchange['ai']}\n"
            
            # Add current input
            prompt = f"{context}Human: {user_input}\nAI:"
            
            # Generate response
            response = self.generator(
                prompt, 
                max_new_tokens=100, 
                do_sample=True, 
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )[0]['generated_text']
            
            # Extract just the AI's response
            ai_response = response.split("AI:")[-1].strip()
            
            # Clean up the response
            ai_response = ai_response.split("Human:")[0].strip()
            
            return ai_response if ai_response else "I'm not sure how to respond to that."
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def process_input(self, user_input):
        """Process user input and return appropriate response"""
        # Detect intent
        intent = self.detect_intent(user_input)
        
        # Handle with appropriate tool or generate AI response
        if intent in self.tools:
            response = self.tools[intent](user_input)
        else:
            # Use AI model for general chat
            response = self.generate_response(user_input)
        
        # Store in conversation history
        self.conversation_history.append({
            "user": user_input,
            "ai": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history manageable
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return response

    def run(self):
        """Main conversation loop"""
        while True:
            try:
                user_input = input("\nAsk me: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("Goodbye! Thanks for chatting!")
                    break
                
                if not user_input:
                    continue
                
                # Process and respond
                response = self.process_input(user_input)
                print(f"AI Agent: {response}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Create and run the AI agent
    agent = AIAgent()
    agent.run()