# Free AI Agent - Built from Scratch

A powerful, locally-running AI agent built entirely with free tools and no API keys required! This project demonstrates how to create an intelligent conversational AI with built-in tools using Hugging Face transformers.

## Features

- **Local AI Model**: Runs completely offline after initial setup
- **Smart Calculator**: Handles mathematical expressions and calculations
- **Wikipedia Integration**: Search and get summaries from Wikipedia
- **Date/Time Functions**: Get current date and time information
- **Conversational Memory**: Maintains context across conversations
- **Intent Detection**: Automatically detects what you want to do
- **Extensible Architecture**: Easy to add new tools and capabilities
- **100% Free**: No API keys, credit cards, or subscriptions needed

## Quick Start

### Prerequisites

- Python 3.7 or higher
- 4GB+ RAM (recommended for better performance)
- Internet connection (only for initial model download)

### Installation

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd ai-agent
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv ai_agent_env
   
   # Activate on Windows
   ai_agent_env\Scripts\activate
   
   # Activate on Linux/Mac
   source ai_agent_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the AI agent**
   ```bash
   python main.py
   ```

## How to Use

### Basic Commands

| Command Type | Examples |
|-------------|----------|
| **Calculator** | `calculate 25 * 4`, `what's 100 / 5?`, `compute 2^8` |
| **Wikipedia Search** | `search python programming`, `tell me about AI`, `who is Einstein?` |
| **Date/Time** | `what time is it?`, `current date`, `today` |
| **Help** | `help`, `what can you do?`, `commands` |
| **General Chat** | Just type naturally for conversation! |

### Example Conversation

```
You: calculate 15 * 24
AI Agent: Result: 360

You: tell me about machine learning
AI Agent: Wikipedia: Machine learning is a method of data analysis that automates analytical model building...

You: what time is it?
AI Agent: Current time: 2025-06-06 14:30:25

You: hello, how are you?
AI Agent: Hello! I'm doing well, thank you for asking. I'm ready to help you with calculations, searches, or just chat!
```

## Project Structure

```
ai-agent/
├── main.py              # Main AI agent code
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── ai_agent_env/       # Virtual environment (created after setup)
```

## Technical Details

### Models Used
- **Primary**: `microsoft/DialoGPT-medium` - Optimized for conversations
- **Size**: ~350MB download
- **Alternative**: `facebook/blenderbot-400M-distill` (more personality)

### Architecture
- **Intent Detection**: Pattern matching to identify user goals
- **Tool System**: Modular functions for different capabilities
- **Memory Management**: Maintains conversation context
- **Error Handling**: Graceful handling of edge cases

## Customization

### Adding New Tools

1. **Create your tool function** in the `AIAgent` class:
   ```python
   def my_custom_tool(self, query):
       # Your tool logic here
       return "Tool response"
   ```

2. **Add it to the tools dictionary**:
   ```python
   self.tools = {
       # ... existing tools
       "mytool": self.my_custom_tool
   }
   ```

3. **Update intent detection**:
   ```python
   if "trigger_word" in user_input_lower:
       return "mytool"
   ```

### Switching AI Models

Replace the model name in `main.py`:
```python
# For more personality (larger download)
self.model_name = "facebook/blenderbot-400M-distill"

# For smaller size (faster but less capable)
self.model_name = "distilgpt2"

# For better coding help
self.model_name = "microsoft/CodeGPT-small-py"
```

## Use Cases

- **Learning Tool**: Understand how AI agents work
- **Personal Assistant**: Calculator, search, time queries
- **Development Base**: Foundation for more complex agents
- **Offline AI**: Works without internet after setup
- **Educational**: Great for AI/ML students and enthusiasts

## Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'transformers'`
**Solution**: Make sure you activated your virtual environment and ran `pip install -r requirements.txt`

**Problem**: Model download is slow
**Solution**: The first run downloads ~350MB. Subsequent runs are instant.

**Problem**: Out of memory errors
**Solution**: Try using a smaller model like `distilgpt2` or close other applications.

**Problem**: Responses are weird or cut off
**Solution**: This is normal for smaller models. Try different prompts or switch to `facebook/blenderbot-400M-distill`.

### Performance Tips

- **RAM**: 8GB+ recommended for smooth operation
- **Storage**: Ensure 2GB+ free space for model files
- **CPU**: Multi-core processors will run models faster

## Future Enhancements

Potential features to add:
- [ ] File reading and summarization
- [ ] Web scraping capabilities
- [ ] Task scheduling and reminders
- [ ] Image analysis with vision models
- [ ] Voice input/output
- [ ] Plugin system for community tools
- [ ] Better conversation memory
- [ ] Multiple personality modes

## Learning Resources

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [Building AI Agents Guide](https://docs.anthropic.com)


## Acknowledgments

- **Hugging Face** for providing free transformer models
- **Microsoft** for the DialoGPT model
- **Wikipedia** for the free knowledge API
- **PyTorch** community for the excellent framework

---

