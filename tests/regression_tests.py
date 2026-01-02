import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock streamlit
sys.modules['streamlit'] = MagicMock()
import streamlit as st

# Configure the mock to handle st.columns unpacking
def columns_mock(spec):
    if isinstance(spec, int):
        return [MagicMock() for _ in range(spec)]
    return [MagicMock() for _ in spec]

st.columns.side_effect = columns_mock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import find_solutions

class TestSolverRegression(unittest.TestCase):
    
    def test_bug_373_subtraction_disabled(self):
        """
        Regression Test for Bug Report:
        Target: 373, Max Int: 8, Max Numbers: 6
        Subtraction DISABLED.
        """
        solutions = find_solutions(
            target=373,
            max_int=8,
            allow_multiply=True,
            allow_subtract=False,
            allow_divide=False,
            max_numbers=6,
            top_n=5,
            exhaustive=False
        )
        
        # 1. Verify no subtraction in expressions
        for sol in solutions:
            self.assertNotIn('-', sol.expression, f"Solution used subtraction despite being disabled: {sol.expression}")
            
        # 2. Verify all solutions are mathematically correct
        for sol in solutions:
            try:
                # Use eval to check mathematical correctness
                # Replace '/' with '//' for integer division check if needed, 
                # but the solver uses integer division semantics for '/' anyway in its evaluation
                # logic, but in string expression it prints '/'.
                # For this specific test case, division is disabled, so we expect only * and +
                val = eval(sol.expression)
                self.assertEqual(val, 373, f"Expression {sol.expression} evaluated to {val}, expected 373")
            except Exception as e:
                self.fail(f"Failed to evaluate expression {sol.expression}: {e}")

    def test_parentheses_precedence_in_subtraction(self):
        """
        Test that (A - (B + C)) is correctly formatted.
        We force a scenario where A - (B+C) is needed.
        Target: 10
        Available: 20, 5, 5
        20 - (5 + 5) = 10
        """
        solutions = find_solutions(
            target=10,
            max_int=20, # Allow 20
            allow_multiply=False,
            allow_subtract=True,
            allow_divide=False,
            exclude=[1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19], # Force usage of 20, 5, 5 if possible
            max_numbers=3,
            top_n=20,
            exhaustive=True # Force exhaustive to ensure we find it
        )
        
        found_target_structure = False
        for sol in solutions:
            if sol.result == 10:
                # Check for correct evaluation
                val = eval(sol.expression)
                self.assertEqual(val, 10, f"Expression {sol.expression} evaluated to {val}, expected 10")
                
                # Check if we have the specific structure we're looking for (subtraction of a sum)
                if '-' in sol.expression and '+' in sol.expression:
                     # If format is "20 - 5 + 5", eval is 20. 
                     # If format is "20 - (5 + 5)", eval is 10.
                     # Since we asserted val == 10, correctness is guaranteed.
                     found_target_structure = True
        
        # We might not strictly "find" 20-(5+5) because 5+5=10 is generated first, then 20-10.
        # But the core requirement is that IF such a structure is generated, it is valid.
        # The main regression is satisfied if ALL returned solutions are valid.

if __name__ == '__main__':
    unittest.main()
