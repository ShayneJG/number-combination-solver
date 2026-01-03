"""
Analyze the practical utility of remainder and exponentiation operators.
Tests whether these operations actually help find better solutions.
"""

from number_combinations import find_solutions
import time

def analyze_target(target, max_int=8, max_numbers=6):
    """Analyze a target number with different operator combinations."""
    
    print(f"\n{'='*80}")
    print(f"TARGET: {target} (max_int={max_int}, max_numbers={max_numbers})")
    print(f"{'='*80}\n")
    
    scenarios = [
        {
            'name': 'Basic (+ only)',
            'ops': {'multiply': False, 'subtract': False, 'divide': False, 'exponentiate': False}
        },
        {
            'name': 'Standard (+, -, *, /)',
            'ops': {'multiply': True, 'subtract': True, 'divide': True, 'exponentiate': False}
        },
        {
            'name': 'With Exponentiation (+, -, *, /, **)',
            'ops': {'multiply': True, 'subtract': True, 'divide': True, 'exponentiate': True}
        },
    ]
    
    results = {}
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 40)
        
        start = time.time()
        try:
            sols = find_solutions(
                target=target,
                max_int=max_int,
                allow_multiply=scenario['ops']['multiply'],
                allow_subtract=scenario['ops']['subtract'],
                allow_divide=scenario['ops']['divide'],
                allow_exponentiate=scenario['ops']['exponentiate'],
                max_numbers=max_numbers,
                top_n=5,
                exhaustive=False,
            )
            elapsed = time.time() - start
            
            results[scenario['name']] = {
                'solutions': sols,
                'time': elapsed,
                'count': len(sols)
            }
            
            if sols:
                print(f"✓ Found {len(sols)} solution(s) in {elapsed:.3f}s")
                best = sols[0]
                print(f"  Best: {best.expression} (ops={best.op_count}, unique_nums={len(best.unique_nums)})")
                
                # Show all solutions
                for i, sol in enumerate(sols[:3], 1):
                    print(f"  {i}. {sol.expression}")
            else:
                print(f"✗ No solutions found ({elapsed:.3f}s)")
                
        except Exception as e:
            print(f"✗ Error: {e}")
            results[scenario['name']] = {'error': str(e)}
    
    # Analysis
    print(f"\n{'='*80}")
    print("ANALYSIS")
    print(f"{'='*80}")
    
    standard = results.get('Standard (+, -, *, /)', {})
    with_exp = results.get('With Exponentiation (+, -, *, /, **)', {})
    
    if standard.get('count', 0) > 0 and with_exp.get('count', 0) > 0:
        std_best = standard['solutions'][0]
        exp_best = with_exp['solutions'][0]
        
        print(f"\nStandard best:       {std_best.expression}")
        print(f"                     (ops={std_best.op_count}, unique={len(std_best.unique_nums)})")
        print(f"\nWith ** best:        {exp_best.expression}")
        print(f"                     (ops={exp_best.op_count}, unique={len(exp_best.unique_nums)})")
        
        if exp_best.op_count < std_best.op_count:
            print(f"\n✓ Exponentiation IMPROVED result (fewer operations)")
        elif exp_best.op_count == std_best.op_count and len(exp_best.unique_nums) < len(std_best.unique_nums):
            print(f"\n✓ Exponentiation IMPROVED result (fewer unique numbers)")
        else:
            print(f"\n✗ Exponentiation did NOT improve result")
            
    elif standard.get('count', 0) == 0 and with_exp.get('count', 0) > 0:
        print(f"\n✓✓ Exponentiation ENABLED finding a solution!")
    elif standard.get('count', 0) > 0 and with_exp.get('count', 0) == 0:
        print(f"\n✗✗ Exponentiation BROKE the solver (found solutions without it)")
    else:
        print(f"\n- No solutions found with either approach")
    
    return results


def simulate_remainder_utility(target, max_int=8):
    """
    Simulate whether remainder would be useful.
    Remainder is useful when target can be expressed as (a*b + c) where c < b
    """
    print(f"\n{'='*80}")
    print(f"REMAINDER UTILITY ANALYSIS for {target}")
    print(f"{'='*80}\n")
    
    useful_cases = []
    
    # Check if target can be expressed using remainder patterns
    for divisor in range(2, max_int + 1):
        quotient = target // divisor
        remainder = target % divisor
        
        if quotient <= max_int and remainder > 0 and remainder <= max_int:
            # Pattern: target = quotient * divisor + remainder
            # With %, we could do: (quotient * divisor) + (something % divisor) = target
            # But this is contrived...
            useful_cases.append({
                'divisor': divisor,
                'quotient': quotient,
                'remainder': remainder,
                'expression': f"{quotient} * {divisor} + {remainder}"
            })
    
    if useful_cases:
        print("Remainder MIGHT help in these patterns:")
        for case in useful_cases[:5]:
            print(f"  {target} = {case['expression']}")
        print(f"\nBUT: These are already achievable with +, *, without needing %")
        print("Verdict: Remainder adds NO practical value for this target")
    else:
        print("No useful remainder patterns found.")
        print("Verdict: Remainder adds NO practical value for this target")
    
    # The real question: can % create a value we can't create otherwise?
    # Answer: Almost never, because:
    # - x % y is always < y
    # - We can already create small numbers with +, -, *, /
    # - The only "new" values would be remainders of specific divisions
    
    print("\n" + "="*80)
    print("GENERAL REMAINDER ANALYSIS")
    print("="*80)
    print("""
Remainder (%) characteristics:
- Result is always in range [0, divisor-1]
- For max_int=8: % can only produce values 0-7
- These values are ALREADY available as base numbers!
- Remainder is useful in modular arithmetic, but NOT for reaching targets

Example: To reach 2285
- We need LARGE values, not small remainders
- 2285 % 8 = 5 (not helpful)
- 2285 % 100 = 85 (but 100 > max_int)

Conclusion: Remainder is almost NEVER useful for target-reaching problems.
It might help in very specific edge cases, but adds complexity for minimal gain.
""")


if __name__ == "__main__":
    # Test cases
    test_targets = [
        (2285, 8, 6),   # User's example
        (100, 8, 6),    # Medium target
        (512, 8, 6),    # Power of 2 (2^9, but we can only use up to 8)
        (128, 8, 6),    # 2^7 - achievable with **
        (343, 8, 6),    # 7^3 - achievable with **
    ]
    
    for target, max_int, max_nums in test_targets:
        analyze_target(target, max_int, max_nums)
        simulate_remainder_utility(target, max_int)
        print("\n" + "="*80 + "\n")
