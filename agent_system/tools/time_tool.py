from datetime import datetime
import sys

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    from backports.zoneinfo import ZoneInfo

from agent_system.core.base_tool import BaseTool

class TimeTool(BaseTool):
    """Tool for handling timezone-based time operations."""
    
    def name(self) -> str:
        return "Time Tool"
    
    def description(self) -> str:
        return "Provides current time for a given timezone (e.g., Europe/London, America/New_York)"
    
    def use(self, *args, **kwargs) -> str:
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        current_time = datetime.now()
        
        if args and args[0]:
            try:
                current_time = current_time.astimezone(ZoneInfo(args[0]))
            except Exception as e:
                return f"Error: Invalid timezone - {str(e)}"
                
        return f"The current time is {current_time.strftime(format)}."