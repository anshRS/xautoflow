import logging
import structlog
from typing import Any, Dict

def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    return structlog.get_logger(name)

class TaskLogger:
    def __init__(self, task_id: str):
        self.logger = get_logger("task")
        self.task_id = task_id
    
    def log_state_change(self, status: str, details: Dict[str, Any] = None):
        self.logger.info(
            "task_state_change",
            task_id=self.task_id,
            status=status,
            details=details
        )
    
    def log_agent_interaction(self, agent: str, action: str, details: Dict[str, Any] = None):
        self.logger.info(
            "agent_interaction",
            task_id=self.task_id,
            agent=agent,
            action=action,
            details=details
        )
    
    def log_tool_execution(self, tool: str, params: Dict[str, Any], result: Dict[str, Any]):
        self.logger.info(
            "tool_execution",
            task_id=self.task_id,
            tool=tool,
            params=params,
            result=result
        )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        self.logger.error(
            "task_error",
            task_id=self.task_id,
            error=str(error),
            error_type=type(error).__name__,
            context=context
        )