"""Calculator tool implementation."""

from typing import Dict, Any
import re

from .base_tool import BaseTool


class CalculatorTool(BaseTool):
    """Tool for performing basic mathematical calculations."""
    
    def _get_name(self) -> str:
        """Get the tool name."""
        return "calculator"
    
    def _get_description(self) -> str:
        """Get the tool description."""
        return "Perform basic mathematical calculations including arithmetic operations."
    
    def _check_availability(self) -> bool:
        """Calculator is always available."""
        return True
    
    def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """Execute a mathematical expression safely.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Dict containing calculation result
        """
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Basic safety check - only allow specific characters
            if not self._is_safe_expression(expression):
                return {
                    "success": False,
                    "message": "Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed.",
                    "result": None
                }
            
            # Evaluate the expression safely
            result = eval(expression)
            
            return {
                "success": True,
                "message": f"Calculation completed: {expression} = {result}",
                "result": result
            }
            
        except ZeroDivisionError:
            return {
                "success": False,
                "message": "Error: Division by zero",
                "result": None
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Error: Invalid mathematical expression - {str(e)}",
                "result": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in calculation: {str(e)}",
                "result": None
            }
    
    def _is_safe_expression(self, expression: str) -> bool:
        """Check if the expression contains only safe characters.
        
        Args:
            expression: Expression to validate
            
        Returns:
            True if expression is safe, False otherwise
        """
        # Allow numbers, operators, parentheses, and whitespace
        allowed_pattern = r'^[0-9+\-*/.() \t]+$'
        
        if not re.match(allowed_pattern, expression):
            return False
        
        # Additional checks for common attack patterns
        dangerous_patterns = [
            '__', 'import', 'exec', 'eval', 'open', 'file',
            'input', 'raw_input', 'compile', 'globals', 'locals'
        ]
        
        expression_lower = expression.lower()
        for pattern in dangerous_patterns:
            if pattern in expression_lower:
                return False
        
        return True
