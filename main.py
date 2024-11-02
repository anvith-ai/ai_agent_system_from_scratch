import os
from dotenv import load_dotenv
from agent_system.core.agent import Agent
from agent_system.tools.time_tool import TimeTool
from agent_system.tools.weather_tool import WeatherTool

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize agent with tools
    agent = Agent(
        llm_api_key=os.getenv("OPENAI_API_KEY"),
        tools=[
            TimeTool(),
            WeatherTool(api_key=os.getenv("OPENWEATHERMAP_API_KEY"))
        ]
    )
    
    # Run the agent
    agent.run()

if __name__ == "__main__":
    main()