import unittest
import sys
import os

# Add parent directory to path to import number_combinations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from number_combinations import (
    evaluate_expression,
    canonical_key,
    normalise_mult_term,
    wrap_if_needed,
    wrap_for_subtraction,
    find_solutions,
    Solution
)

class TestEvaluation(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(evaluate_expression([10, 5], ['+']), 15)
        self.assertEqual(evaluate_expression([10, 5], ['-']), 5)
        self.assertEqual(evaluate_expression([10, 5], ['*']), 50)
        self.assertEqual(evaluate_expression([10, 5], ['/']), 2)
        
    def test_integer_division(self):
        # 10 / 3 should be None (not integer division in this context, logic returns None if not divisible)
        self.assertIsNone(evaluate_expression([10, 3], ['/']))
        # 0 / 5 should be 0
        self.assertEqual(evaluate_expression([0, 5], ['/']), 0)
        # 5 / 0 should return None (handle divide by zero)
        self.assertIsNone(evaluate_expression([5, 0], ['/']))

    def test_precedence(self):
        # 2 + 3 * 4 = 14 (not 20)
        self.assertEqual(evaluate_expression([2, 3, 4], ['+', '*']), 14)
        # 2 * 3 + 4 = 10
        self.assertEqual(evaluate_expression([2, 3, 4], ['*', '+']), 10)
        # 10 - 2 * 3 = 4
        self.assertEqual(evaluate_expression([10, 2, 3], ['-', '*']), 4)

    def test_exponentiation(self):
        # 2 ** 3 = 8
        self.assertEqual(evaluate_expression([2, 3], ['**']), 8)
        # 2 + 3 ** 2 = 11 (precedence check)
        self.assertEqual(evaluate_expression([2, 3, 2], ['+', '**']), 11)
        # 2 * 3 ** 2 = 18 (exponentiation higher than mult)
        self.assertEqual(evaluate_expression([2, 3, 2], ['*', '**']), 18)

class TestHelpers(unittest.TestCase):
    def test_wrap_if_needed(self):
        # For multiplication/division, we need to wrap addition/subtraction
        self.assertEqual(wrap_if_needed("2 + 3", for_mult_div=True), "(2 + 3)")
        self.assertEqual(wrap_if_needed("5 - 2", for_mult_div=True), "(5 - 2)")
        self.assertEqual(wrap_if_needed("4 * 5", for_mult_div=True), "4 * 5") # Already high prec
        self.assertEqual(wrap_if_needed("-5", for_mult_div=True), "-5") # Unary minus usually fine
        
    def test_wrap_for_subtraction(self):
        # This is the BUG FIX verification
        # Right side of subtraction needs wrapping if it has + or -
        
        # Case 1: Right side is simple number
        self.assertEqual(wrap_for_subtraction("5"), "5")
        
        # Case 2: Right side is addition (needs wrap: A - (B+C))
        self.assertEqual(wrap_for_subtraction("2 + 3"), "(2 + 3)")
        
        # Case 3: Right side is subtraction (needs wrap: A - (B-C))
        self.assertEqual(wrap_for_subtraction("5 - 2"), "(5 - 2)")
        
        # Case 4: Right side is multiply (no wrap: A - B*C)
        self.assertEqual(wrap_for_subtraction("2 * 3"), "2 * 3")
        
        # Case 5: Already wrapped
        self.assertEqual(wrap_for_subtraction("(2 + 3)"), "(2 + 3)")

    def test_canonical_key(self):
        # Commutative addition
        self.assertEqual(canonical_key("2 + 3"), canonical_key("3 + 2"))
        # Commutative multiplication
        self.assertEqual(canonical_key("2 * 3"), canonical_key("3 * 2"))
        # Mixed
        self.assertEqual(canonical_key("1 + 2 * 3"), canonical_key("1 + 3 * 2"))

class TestFindSolutions(unittest.TestCase):
    def test_target_reached(self):
        # Simple target 10 from [5, 5]
        sols = find_solutions(10, 5, allow_multiply=False, allow_subtract=True, exclude=[1,2,3,4], max_numbers=2)
        found = any(s.result == 10 for s in sols)
        self.assertTrue(found)

    def test_exclude_respected(self):
        # Target 5, Max 5, but Exclude 5. 
        # Must reach 5 using other numbers (e.g. 2+3, 4+1)
        sols = find_solutions(5, 5, allow_multiply=True, exclude=[5], max_numbers=2)
        for sol in sols:
            self.assertNotIn(5, sol.unique_nums)

    def test_operator_flags(self):
        # Target 6. 
        # If multiply allowed: 2*3 possible.
        # If multiply disabled: must use 2+4 or 1+5 etc.
        
        # Disable multiply
        sols = find_solutions(6, 6, allow_multiply=False, allow_subtract=False, max_numbers=2)
        for sol in sols:
            self.assertNotIn('*', sol.expression)
            
        # Disable subtract
        sols = find_solutions(1, 5, allow_multiply=False, allow_subtract=False, max_numbers=2)
        # Cannot make 1 from integers [1..5] with 2 numbers using only + (min is 1+2=3) unless we use 1 itself but this searches for expressions.
        # Actually simplest is just number 1 if num_count=1 allowed.
        # Let's check logic: if subtract is OFF, we shouldn't see '-'
        
        # Force a case where subtraction is the natural answer but disabled
        # Target 2 using [5, 3]. 5-3=2. If subtract off, impossible.
        sols = find_solutions(2, 5, allow_multiply=False, allow_subtract=False, exclude=[1,2,4], max_numbers=2)
        # Only available: 3, 5. 3+3=6, 3+5=8. No way to get 2.
        self.assertEqual(len(sols), 0)
        
        # Enable subtract
        sols = find_solutions(2, 5, allow_multiply=False, allow_subtract=True, exclude=[1,2,4], max_numbers=2)
        # Should match 5-3
        found = any("5 - 3" in s.expression or "3 - 5" in s.expression for s in sols) # 3-5 is -2
        # Actually exact match logic might vary, but result==2 is key
        self.assertTrue(any(s.result == 2 for s in sols))

    def test_max_numbers(self):
        # Max numbers 2. Should not find 1+1+1
        sols = find_solutions(3, 5, allow_multiply=False, max_numbers=2)
        for sol in sols:
            # count numbers in expression roughly
            # or just rely on op_count. 2 numbers = 1 op.
            self.assertLessEqual(sol.op_count, 1)

if __name__ == '__main__':
    unittest.main()
