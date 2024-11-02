from typing import List, Optional, Dict
from .memory import Memory
from .llm_client import LLMClient
from .base_tool import BaseTool

class Agent:
    """Main agent class that coordinates the LLM, memory, and tools."""
    
    def __init__(self, llm_api_key: str, tools: Optional[List[BaseTool]] = None):
        self.llm_client = LLMClient(api_key=llm_api_key)
        self.memory = Memory(max_items=10)
        self.tools = tools or []
        
    def _get_tool_descriptions(self) -> str:
        """Generate a formatted string of available tools and their descriptions."""
        if not self.tools:
            return "No tools available."
            
        return "\n".join([
            f"- {tool.name()}: {tool.description()}"
            for tool in self.tools
        ])
        
    def _get_tool_by_name(self, name: str) -> Optional[BaseTool]:
        """Find a tool by its name."""
        for tool in self.tools:
            if tool.name().lower() == name.lower():
                return tool
        return None
        
    def _generate_prompt(self, user_input: str) -> str:
        """Create a prompt for the LLM including context and tools."""
        context = self.memory.get_context()
        tools_desc = self._get_tool_descriptions()
        
        return f"""Context of previous interactions:
{context}

Available tools:
{tools_desc}

User input: {user_input}

You can use multiple tools to respond to the user's request. For each tool you want to use, respond in the format:
USE_TOOL: <tool_name> | <tool_args>
THEN: <next_step_description>

You can chain multiple tool uses by using THEN between them. After using all necessary tools, provide a natural response summarizing the results.

If no tools are needed, respond conversationally.

Example multi-tool response:
USE_TOOL: Time Tool | America/New_York
THEN: Use this time to check weather
USE_TOOL: Weather Tool | New York
THEN: Provide summary to user

Response:"""

    def _parse_tool_sequence(self, llm_response: str) -> List[Dict]:
        """Parse a sequence of tool commands from the LLM response."""
        tool_sequence = []
        current_tool = None
        
        # Split response into lines and process each line
        lines = llm_response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('USE_TOOL:'):
                if current_tool:
                    tool_sequence.append(current_tool)
                
                # Parse tool request
                tool_part = line.replace('USE_TOOL:', '').strip()
                try:
                    tool_name, tool_args = tool_part.split('|', 1)
                    current_tool = {
                        'name': tool_name.strip(),
                        'args': [arg.strip() for arg in tool_args.strip().split(',')],
                        'next_step': None
                    }
                except ValueError:
                    continue
                    
            elif line.startswith('THEN:') and current_tool:
                current_tool['next_step'] = line.replace('THEN:', '').strip()
        
        # Add the last tool if exists
        if current_tool:
            tool_sequence.append(current_tool)
            
        return tool_sequence

    def _execute_tool_sequence(self, tool_sequence: List[Dict]) -> str:
        """Execute a sequence of tools and return combined results."""
        results = []
        
        for tool_command in tool_sequence:
            tool_name = tool_command['name']
            tool_args = tool_command['args']
            next_step = tool_command.get('next_step')
            
            tool = self._get_tool_by_name(tool_name)
            if not tool:
                results.append(f"Error: Tool '{tool_name}' not found.")
                continue
                
            try:
                result = tool.use(*tool_args)
                results.append(result)
                
                if next_step:
                    results.append(f"Next step: {next_step}")
                    
            except Exception as e:
                results.append(f"Error executing {tool_name}: {str(e)}")
        
        return "\n".join(results)

    def _handle_tool_response(self, llm_response: str) -> str:
        """Process LLM response and execute tools if requested."""
        if not llm_response.startswith("USE_TOOL:"):
            return llm_response
            
        # Parse and execute tool sequence
        tool_sequence = self._parse_tool_sequence(llm_response)
        if not tool_sequence:
            return llm_response
            
        # Execute tools and get results
        tool_results = self._execute_tool_sequence(tool_sequence)
        
        # Get final summary from LLM
        summary_prompt = f"""Tool execution results:
{tool_results}

Please provide a natural summary of these results for the user."""
        
        summary = self.llm_client.query(summary_prompt)
        return f"{tool_results}\n\nSummary: {summary}"
            
    def process_input(self, user_input: str) -> str:
        """Process user input and return a response."""
        # Add user input to memory
        self.memory.add(user_input, "user")
        
        # Generate and send prompt to LLM
        prompt = self._generate_prompt(user_input)
        llm_response = self.llm_client.query(prompt, max_tokens=300)  # Increased token limit for multi-tool responses
        
        # Handle tool usage if requested
        response = self._handle_tool_response(llm_response)
        
        # Add response to memory
        self.memory.add(response, "agent")
        
        return response
        
    def run(self):
        """Run an interactive loop for the agent."""
        print("Agent initialized. Type 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                    
                response = self.process_input(user_input)
                print(f"\nAgent: {response}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
                
            except Exception as e:
                print(f"\nError: {str(e)}")