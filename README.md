# AI Agent System

A flexible and extensible AI agent system that combines LLM capabilities with custom tools for interactive task execution. The system supports multi-tool operations, memory retention, and natural language interactions.

## Project Structure

```
ai_agent_system_from_scratch/
│
├── README.md
├── requirements.txt
├── .env
├── main.py
│
├── agent_system/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base_tool.py
│   │   ├── memory.py
│   │   ├── llm_client.py
│   │   └── agent.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── time_tool.py
│       └── weather_tool.py
```

## Key Components

### Core Components

1. **Agent (`agent.py`)**
   - Main orchestrator of the system
   - Manages tool execution and response generation
   - Supports multi-tool operations with sequential execution
   - Maintains conversation context through memory system

2. **Memory System (`memory.py`)**
   - Stores conversation history
   - Maintains a fixed-size memory buffer
   - Provides contextual information for LLM queries

3. **LLM Client (`llm_client.py`)**
   - Handles communication with OpenAI's API
   - Manages prompt generation and response parsing
   - Supports customizable model selection

4. **Base Tool (`base_tool.py`)**
   - Abstract base class for all tools
   - Defines standard interface for tool implementation

### Available Tools

1. **Time Tool (`time_tool.py`)**
   - Provides timezone-aware time information
   - Supports all standard timezone formats
   - Example: "Get time in America/New_York"

2. **Weather Tool (`weather_tool.py`)**
   - Fetches current weather information
   - Uses OpenWeatherMap API
   - Provides temperature and weather conditions
   - Example: "Get weather in London"

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_agent_system_from_scratch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. update `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

## Usage

1. Run the agent:
```bash
python main.py
```

2. Interact with the agent using natural language. Examples:
```
You: What's the current time in London?
You: How's the weather in New York?
You: What's the time in Tokyo and how's the weather there?
```

3. The agent can handle multiple operations in a single query:
```
You: Compare the weather in London and New York, and tell me the local time in each city.
```

## Adding New Tools

1. Create a new tool class in the `tools` directory
2. Inherit from `BaseTool`
3. Implement required methods:
   - `name()`
   - `description()`
   - `use()`

Example:
```python
from agent_system.core.base_tool import BaseTool

class NewTool(BaseTool):
    def name(self) -> str:
        return "New Tool"
    
    def description(self) -> str:
        return "Description of what the tool does"
    
    def use(self, *args, **kwargs):
        # Implement tool functionality
        return "Tool result"
```

## Memory System

The memory system maintains conversation context with:
- Maximum memory items (default: 10)
- Timestamp tracking
- Source attribution (user/agent)
- Formatted context generation

## Error Handling

The system includes comprehensive error handling for:
- Invalid tool requests
- API failures
- Invalid parameters
- Missing API keys

## Requirements

- Python 3.7+
- OpenAI API key
- OpenWeatherMap API key
- Required packages listed in `requirements.txt`

## Future Enhancements

Potential areas for expansion:
- Additional tools integration
- Enhanced memory management
- Tool result caching
- Conversation summarization
- Multi-turn planning
- Custom tool pipelines

---
Remember to update your API keys and maintain secure practices when handling sensitive information.