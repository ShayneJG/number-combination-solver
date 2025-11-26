#!/usr/bin/env python3
"""
Streamlit web app for the Number Combinations Solver.
Find expressions using integers and operators to reach a target number.
"""

import streamlit as st
from itertools import product
from typing import List, Set, Tuple, Optional, Dict
from dataclasses import dataclass
from collections import defaultdict
import time


# ============== Core Logic (from number_combinations.py) ==============

def canonical_key(expression: str) -> str:
    """Create a canonical form of an expression for deduplication."""
    expr = expression.replace(" ", "")
    terms = []
    current = ""
    depth = 0
    sign = "+"
    
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == '(':
            depth += 1
            current += c
        elif c == ')':
            depth -= 1
            current += c
        elif c in ('+', '-') and depth == 0 and current:
            terms.append((sign, normalise_mult_term(current)))
            sign = c
            current = ""
        else:
            current += c
        i += 1
    
    if current:
        terms.append((sign, normalise_mult_term(current)))
    
    pos_terms = sorted([t[1] for t in terms if t[0] == '+'])
    neg_terms = sorted([t[1] for t in terms if t[0] == '-'])
    
    result_parts = []
    for t in pos_terms:
        result_parts.append('+' + t)
    for t in neg_terms:
        result_parts.append('-' + t)
    
    return ''.join(result_parts)


def normalise_mult_term(term: str) -> str:
    """Normalise a multiplication/division term by sorting factors."""
    while term.startswith('(') and term.endswith(')'):
        depth = 0
        matches = True
        for i, c in enumerate(term):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            if depth == 0 and i < len(term) - 1:
                matches = False
                break
        if matches:
            term = term[1:-1]
        else:
            break
    
    if '/' not in term and '*' in term:
        factors = term.split('*')
        return '*'.join(sorted(factors))
    
    return term


@dataclass
class Solution:
    expression: str
    result: int
    unique_nums: Tuple[int, ...]
    op_count: int
    _canonical: str = ""
    
    def __post_init__(self):
        object.__setattr__(self, '_canonical', canonical_key(self.expression))
    
    def __lt__(self, other):
        if self.op_count != other.op_count:
            return self.op_count < other.op_count
        return len(self.unique_nums) < len(other.unique_nums)
    
    def __eq__(self, other):
        return self._canonical == other._canonical
    
    def __hash__(self):
        return hash(self._canonical)


@dataclass(frozen=True)
class PartialResult:
    value: int
    expression: str
    nums_used: Tuple[int, ...]
    op_count: int


def evaluate_expression(numbers: List[int], operators: List[str]) -> Optional[int]:
    """Evaluate an expression respecting operator precedence."""
    if not numbers:
        return 0
    if len(numbers) == 1:
        return numbers[0]
    
    nums = list(numbers)
    ops = list(operators)
    
    i = 0
    while i < len(ops):
        if ops[i] in ('*', '/'):
            if ops[i] == '*':
                nums[i] = nums[i] * nums[i + 1]
            else:
                if nums[i + 1] == 0 or nums[i] % nums[i + 1] != 0:
                    return None
                nums[i] = nums[i] // nums[i + 1]
            nums.pop(i + 1)
            ops.pop(i)
        else:
            i += 1
    
    result = nums[0]
    for i, op in enumerate(ops):
        if op == '+':
            result += nums[i + 1]
        else:
            result -= nums[i + 1]
    
    return result


def format_expression(numbers: List[int], operators: List[str]) -> str:
    """Format numbers and operators into a readable expression string."""
    if not numbers:
        return ""
    if len(numbers) == 1:
        return str(numbers[0])
    
    segments: List[str] = []
    current_group: List[str] = [str(numbers[0])]
    in_mult_group = False
    
    for i, op in enumerate(operators):
        if op in ('*', '/'):
            if not in_mult_group:
                in_mult_group = True
            current_group.append(f" {op} {numbers[i + 1]}")
        else:
            if in_mult_group:
                segments.append("(" + "".join(current_group) + ")")
                in_mult_group = False
            else:
                segments.append("".join(current_group))
            segments.append(f" {op} ")
            current_group = [str(numbers[i + 1])]
    
    if in_mult_group:
        segments.append("(" + "".join(current_group) + ")")
    else:
        segments.append("".join(current_group))
    
    return "".join(segments)


def wrap_if_needed(expr: str, for_mult_div: bool = False) -> str:
    """Wrap expression in parentheses if needed for operator precedence."""
    if expr.startswith('(') and expr.endswith(')'):
        return expr
    if ' ' not in expr:
        return expr
    if for_mult_div:
        if '+' in expr or (expr.count('-') > 0 and not expr.startswith('-')):
            return f"({expr})"
    return expr


def generate_all_subexpressions(
    available_numbers: List[int],
    num_count: int,
    operators: List[str],
    max_results_per_value: int = 3
) -> Dict[int, List[PartialResult]]:
    """Generate all possible values from expressions using num_count numbers."""
    results: Dict[int, List[PartialResult]] = defaultdict(list)
    unlimited = (max_results_per_value == 0)
    
    if num_count == 0:
        return results
    
    if num_count == 1:
        for n in available_numbers:
            results[n].append(PartialResult(
                value=n,
                expression=str(n),
                nums_used=(n,),
                op_count=0
            ))
        return results
    
    if num_count <= 3:
        for nums in product(available_numbers, repeat=num_count):
            for ops in product(operators, repeat=num_count - 1):
                value = evaluate_expression(list(nums), list(ops))
                if value is not None:
                    if unlimited or len(results[value]) < max_results_per_value:
                        expr = format_expression(list(nums), list(ops))
                        unique = tuple(sorted(set(nums)))
                        results[value].append(PartialResult(
                            value=value,
                            expression=expr,
                            nums_used=unique,
                            op_count=num_count - 1
                        ))
    else:
        left_count = num_count // 2
        right_count = num_count - left_count
        
        left_vals = generate_all_subexpressions(available_numbers, left_count, operators, max_results_per_value)
        right_vals = generate_all_subexpressions(available_numbers, right_count, operators, max_results_per_value)
        
        for left_val, left_partials in left_vals.items():
            for right_val, right_partials in right_vals.items():
                left_to_try = left_partials if unlimited else left_partials[:1]
                right_to_try = right_partials if unlimited else right_partials[:1]
                
                for lp in left_to_try:
                    for rp in right_to_try:
                        combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                        combined_ops = lp.op_count + rp.op_count + 1
                        
                        for op, val in [
                            ('+', left_val + right_val),
                            ('-', left_val - right_val),
                            ('*', left_val * right_val),
                        ]:
                            if unlimited or len(results[val]) < max_results_per_value:
                                if op == '*':
                                    left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
                                    right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
                                    expr = f"{left_expr} * {right_expr}"
                                else:
                                    expr = f"{lp.expression} {op} {rp.expression}"
                                results[val].append(PartialResult(
                                    value=val,
                                    expression=expr,
                                    nums_used=combined_unique,
                                    op_count=combined_ops
                                ))
                        
                        if right_val != 0 and left_val % right_val == 0:
                            val = left_val // right_val
                            if unlimited or len(results[val]) < max_results_per_value:
                                left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
                                right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
                                expr = f"{left_expr} / {right_expr}"
                                results[val].append(PartialResult(
                                    value=val,
                                    expression=expr,
                                    nums_used=combined_unique,
                                    op_count=combined_ops
                                ))
    
    return results


def meet_in_middle_search(
    target: int,
    available_numbers: List[int],
    operators: List[str],
    total_nums: int,
    top_n: int = 5,
    exhaustive: bool = False
) -> Set[Solution]:
    """Use meet-in-the-middle to find expressions that equal target."""
    solutions: Set[Solution] = set()
    max_per_value = 0 if exhaustive else 3
    
    if total_nums <= 4:
        return direct_search(target, available_numbers, operators, total_nums, top_n)
    
    for left_count in range(1, total_nums):
        right_count = total_nums - left_count
        
        if left_count > (total_nums + 1) // 2:
            continue
        
        left_values = generate_all_subexpressions(available_numbers, left_count, operators, max_per_value)
        right_values = generate_all_subexpressions(available_numbers, right_count, operators, max_per_value)
        
        for left_val, left_partials in left_values.items():
            # Addition
            needed = target - left_val
            if needed in right_values:
                for lp in left_partials:
                    for rp in right_values[needed]:
                        combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                        solutions.add(Solution(
                            expression=f"{lp.expression} + {rp.expression}",
                            result=target,
                            unique_nums=combined_unique,
                            op_count=lp.op_count + rp.op_count + 1
                        ))
            
            # Subtraction
            needed = left_val - target
            if needed in right_values:
                for lp in left_partials:
                    for rp in right_values[needed]:
                        combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                        solutions.add(Solution(
                            expression=f"{lp.expression} - {rp.expression}",
                            result=target,
                            unique_nums=combined_unique,
                            op_count=lp.op_count + rp.op_count + 1
                        ))
            
            # Multiplication
            if left_val != 0 and target % left_val == 0:
                needed = target // left_val
                if needed in right_values:
                    for lp in left_partials:
                        for rp in right_values[needed]:
                            combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                            left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
                            right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
                            solutions.add(Solution(
                                expression=f"{left_expr} * {right_expr}",
                                result=target,
                                unique_nums=combined_unique,
                                op_count=lp.op_count + rp.op_count + 1
                            ))
            
            # Division
            if target != 0 and left_val % target == 0:
                needed = left_val // target
                if needed in right_values and needed != 0:
                    for lp in left_partials:
                        for rp in right_values[needed]:
                            combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                            left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
                            right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
                            solutions.add(Solution(
                                expression=f"{left_expr} / {right_expr}",
                                result=target,
                                unique_nums=combined_unique,
                                op_count=lp.op_count + rp.op_count + 1
                            ))
        
        for right_val, right_partials in right_values.items():
            needed = right_val - target
            if needed in left_values:
                for rp in right_partials:
                    for lp in left_values[needed]:
                        combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                        solutions.add(Solution(
                            expression=f"{rp.expression} - {lp.expression}",
                            result=target,
                            unique_nums=combined_unique,
                            op_count=lp.op_count + rp.op_count + 1
                        ))
            
            if target != 0 and right_val % target == 0:
                needed = right_val // target
                if needed in left_values and needed != 0:
                    for rp in right_partials:
                        for lp in left_values[needed]:
                            combined_unique = tuple(sorted(set(lp.nums_used + rp.nums_used)))
                            left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
                            right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
                            solutions.add(Solution(
                                expression=f"{right_expr} / {left_expr}",
                                result=target,
                                unique_nums=combined_unique,
                                op_count=lp.op_count + rp.op_count + 1
                            ))
    
    return solutions


def direct_search(
    target: int,
    available_numbers: List[int],
    operators: List[str],
    max_nums: int,
    top_n: int
) -> Set[Solution]:
    """Direct brute-force search for small expression sizes."""
    solutions: Set[Solution] = set()
    
    for num_count in range(1, max_nums + 1):
        if num_count == 1:
            for n in available_numbers:
                if n == target:
                    solutions.add(Solution(
                        expression=str(n),
                        result=n,
                        unique_nums=(n,),
                        op_count=0
                    ))
            continue
        
        for nums in product(available_numbers, repeat=num_count):
            for ops in product(operators, repeat=num_count - 1):
                result = evaluate_expression(list(nums), list(ops))
                if result == target:
                    expr = format_expression(list(nums), list(ops))
                    unique = tuple(sorted(set(nums)))
                    solutions.add(Solution(
                        expression=expr,
                        result=target,
                        unique_nums=unique,
                        op_count=num_count - 1
                    ))
    
    return solutions


def find_solutions(
    target: int,
    max_int: int,
    allow_multiply: bool = False,
    allow_subtract: bool = False,
    allow_divide: bool = False,
    exclude: Optional[List[int]] = None,
    max_numbers: int = 6,
    top_n: int = 5,
    exhaustive: bool = False,
    progress_callback=None
) -> List[Solution]:
    """Find combinations of integers that equal the target."""
    if exclude is None:
        exclude = []
    
    available_numbers = [n for n in range(1, max_int + 1) if n not in exclude]
    
    operators = ['+']
    if allow_multiply:
        operators.append('*')
    if allow_subtract:
        operators.append('-')
    if allow_divide:
        operators.append('/')
    
    all_solutions: Set[Solution] = set()
    
    for num_count in range(1, max_numbers + 1):
        if progress_callback:
            progress_callback(f"Searching {num_count} numbers...")
        
        if num_count <= 4:
            new_solutions = direct_search(target, available_numbers, operators, num_count, top_n)
            new_solutions = {s for s in new_solutions if s.op_count == num_count - 1 or (num_count == 1 and s.op_count == 0)}
        else:
            new_solutions = meet_in_middle_search(target, available_numbers, operators, num_count, top_n, exhaustive)
        
        all_solutions.update(new_solutions)
        
        # Early termination
        if all_solutions:
            best_op_count = min(s.op_count for s in all_solutions)
            if best_op_count <= num_count - 1:
                if len(all_solutions) >= top_n:
                    break
                else:
                    next_level_ops = num_count
                    if best_op_count < next_level_ops - 1:
                        break
    
    sorted_solutions = sorted(all_solutions)
    return sorted_solutions[:top_n]


# ============== Streamlit UI ==============

st.set_page_config(
    page_title="Number Combinations Solver",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Number Combinations Solver")
st.markdown("Find expressions using integers and operators to reach a target number.")

# Input section
col1, col2 = st.columns(2)

with col1:
    target = st.number_input("Target Number", value=100, min_value=1, step=1)
    max_int = st.number_input("Maximum Integer", value=9, min_value=1, max_value=20, step=1)

with col2:
    max_numbers = st.slider("Max Numbers in Expression", min_value=2, max_value=10, value=6)
    top_n = st.slider("Number of Solutions", min_value=1, max_value=20, value=5)

# Operators
st.subheader("Operators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    use_add = st.checkbox("Addition (+)", value=True, disabled=True)
with col2:
    use_multiply = st.checkbox("Multiplication (×)", value=True)
with col3:
    use_subtract = st.checkbox("Subtraction (−)", value=True)
with col4:
    use_divide = st.checkbox("Division (÷)", value=False)

# Exclude numbers
exclude_input = st.text_input(
    "Exclude Numbers (comma-separated)", 
    placeholder="e.g., 10, 11, 12",
    help="Numbers to exclude from available integers"
)

exclude = []
if exclude_input.strip():
    try:
        exclude = [int(x.strip()) for x in exclude_input.split(",") if x.strip()]
    except ValueError:
        st.error("Invalid exclude list. Please enter comma-separated numbers.")

# Mode
exhaustive = st.checkbox(
    "Exhaustive Search", 
    value=False,
    help="Guaranteed optimal results but slower. Use for important searches."
)

# Search button
if st.button("🔍 Find Solutions", type="primary", use_container_width=True):
    # Build description
    available = [n for n in range(1, max_int + 1) if n not in exclude]
    
    if not available:
        st.error("No numbers available after exclusions!")
    else:
        ops_list = ["addition"]
        if use_multiply:
            ops_list.append("multiplication")
        if use_subtract:
            ops_list.append("subtraction")
        if use_divide:
            ops_list.append("division")
        
        st.info(f"Searching for **{target}** using integers {', '.join(map(str, available[:5]))}{'...' if len(available) > 5 else ''} with {', '.join(ops_list)}")
        
        progress_placeholder = st.empty()
        
        def update_progress(msg):
            progress_placeholder.text(msg)
        
        start_time = time.time()
        
        with st.spinner("Searching..."):
            solutions = find_solutions(
                target=target,
                max_int=max_int,
                allow_multiply=use_multiply,
                allow_subtract=use_subtract,
                allow_divide=use_divide,
                exclude=exclude,
                max_numbers=max_numbers,
                top_n=top_n,
                exhaustive=exhaustive,
                progress_callback=update_progress
            )
        
        elapsed = time.time() - start_time
        progress_placeholder.empty()
        
        if not solutions:
            st.warning(f"No solutions found. (searched in {elapsed:.2f}s)")
        else:
            st.success(f"Found {len(solutions)} solution(s) in {elapsed:.2f}s")
            
            for i, sol in enumerate(solutions, 1):
                unique_str = ", ".join(str(n) for n in sol.unique_nums)
                
                with st.container():
                    st.markdown(f"""
                    **{i}.** `{sol.expression}` = **{sol.result}**
                    
                    <small>Unique integers: {unique_str} ({len(sol.unique_nums)}) • Operations: {sol.op_count}</small>
                    """, unsafe_allow_html=True)
                    st.divider()

# Footer
st.markdown("---")
st.markdown(
    "<small>Uses meet-in-the-middle algorithm for fast searching. "
    "Enable 'Exhaustive Search' for guaranteed optimal results.</small>",
    unsafe_allow_html=True
)
