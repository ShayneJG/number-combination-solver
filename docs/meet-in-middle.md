# Meet-in-the-Middle Algorithm

## Overview

The meet-in-the-middle algorithm is a divide-and-conquer technique that reduces exponential time complexity by splitting the problem into two smaller subproblems. For the number combination solver, this provides a dramatic speedup for expressions with more than 4 numbers.

## Core Concept

Instead of generating all possible k-number expressions (which grows as n^k), we:

1. **Split** the problem into two halves
2. **Generate** all possible values from each half independently
3. **Combine** the halves by finding pairs that produce the target

**Key insight:** Generating two sets of size n^(k/2) and combining them is much faster than generating one set of size n^k.

## Mathematical Foundation

### Traditional Brute Force

```
Search space = n^k × o^(k-1)

Example (k=6, n=8, o=4):
  8^6 × 4^5 = 268,435,456 expressions
```

### Meet-in-the-Middle

```
Left half:  n^(k/2) × o^(k/2-1)
Right half: n^(k/2) × o^(k/2-1)
Combine:    Left × Right lookups (with hash table)

Example (k=6, n=8, o=4):
  Left:  8^3 × 4^2 = 8,192
  Right: 8^3 × 4^2 = 8,192
  Combine: 8,192 × 4 = 32,768 lookups
  
Total: ~49,000 operations vs 268 million
Speedup: ~5,461x
```

## Algorithm Steps

### Step 1: Split the Problem

Given `k` numbers to use, split into:
- `left_count` = k // 2 (integer division)
- `right_count` = k - left_count

**Example:** k=6 → left=3, right=3

**Optimisation:** Only generate splits where `left_count ≤ (k+1)//2` to avoid duplicate work (since left=3,right=3 is the same as left=3,right=3 reversed).

### Step 2: Generate Left Subexpressions

Generate all possible values using `left_count` numbers:

```python
def generate_all_subexpressions(available_numbers, num_count, operators):
    results = {}  # value → [PartialResult objects]
    
    if num_count == 1:
        # Base case: single numbers
        for n in available_numbers:
            results[n] = [PartialResult(n, str(n), (n,), 0)]
        return results
    
    if num_count <= 3:
        # Small enough for direct enumeration
        for nums in product(available_numbers, repeat=num_count):
            for ops in product(operators, repeat=num_count-1):
                value = evaluate_expression(nums, ops)
                if value is not None:
                    expr = format_expression(nums, ops)
                    results[value].append(PartialResult(...))
    else:
        # Recursive meet-in-middle
        left_vals = generate_all_subexpressions(..., num_count//2, ...)
        right_vals = generate_all_subexpressions(..., num_count-num_count//2, ...)
        
        # Combine left and right
        for left_val, left_partials in left_vals.items():
            for right_val, right_partials in right_vals.items():
                for op in operators:
                    new_val = apply_operator(left_val, op, right_val)
                    if new_val is not None:
                        results[new_val].append(...)
    
    return results
```

**Data structure:**
```python
results = {
    100: [
        PartialResult(value=100, expression="(4 * 5 * 5)", nums_used=(4,5), op_count=2),
        PartialResult(value=100, expression="(2 * 8) + (6 * 7 * 2)", nums_used=(2,6,7,8), op_count=4),
    ],
    50: [...],
    25: [...],
    ...
}
```

### Step 3: Generate Right Subexpressions

Same process as Step 2, but for `right_count` numbers.

### Step 4: Combine to Find Target

For each operator, find pairs of (left_value, right_value) that combine to the target:

#### Addition: target = left + right

```python
for left_val, left_partials in left_values.items():
    needed_right = target - left_val
    if needed_right in right_values:
        for lp in left_partials:
            for rp in right_values[needed_right]:
                solution = f"{lp.expression} + {rp.expression}"
                solutions.add(Solution(solution, target, ...))
```

**Example:**
```
Target: 100
Left: 25 from "5 * 5"
Needed right: 100 - 25 = 75
Right: 75 from "3 * 5 * 5"
Solution: "(5 * 5) + (3 * 5 * 5)" = 100
```

#### Subtraction: target = left - right

```python
for left_val, left_partials in left_values.items():
    needed_right = left_val - target
    if needed_right in right_values:
        for lp in left_partials:
            for rp in right_values[needed_right]:
                solution = f"{lp.expression} - {rp.expression}"
                solutions.add(Solution(solution, target, ...))
```

**Example:**
```
Target: 100
Left: 125 from "5 * 5 * 5"
Needed right: 125 - 100 = 25
Right: 25 from "5 * 5"
Solution: "(5 * 5 * 5) - (5 * 5)" = 100
```

**Also check reverse:** target = right - left

```python
for right_val, right_partials in right_values.items():
    needed_left = right_val - target
    if needed_left in left_values:
        # Generate: right - left = target
```

#### Multiplication: target = left × right

```python
for left_val, left_partials in left_values.items():
    if left_val != 0 and target % left_val == 0:
        needed_right = target // left_val
        if needed_right in right_values:
            for lp in left_partials:
                for rp in right_values[needed_right]:
                    solution = f"{lp.expression} * {rp.expression}"
                    solutions.add(Solution(solution, target, ...))
```

**Example:**
```
Target: 100
Left: 4 from "2 * 2"
Check: 100 % 4 == 0 ✓
Needed right: 100 // 4 = 25
Right: 25 from "5 * 5"
Solution: "(2 * 2) * (5 * 5)" = 100
```

#### Division: target = left / right

```python
for left_val, left_partials in left_values.items():
    if target != 0 and left_val % target == 0:
        needed_right = left_val // target
        if needed_right != 0 and needed_right in right_values:
            for lp in left_partials:
                for rp in right_values[needed_right]:
                    solution = f"{lp.expression} / {rp.expression}"
                    solutions.add(Solution(solution, target, ...))
```

**Example:**
```
Target: 100
Left: 400 from "8 * 8 * 6 + 16"
Check: 400 % 100 == 0 ✓
Needed right: 400 // 100 = 4
Right: 4 from "2 * 2"
Solution: "(8 * 8 * 6 + 16) / (2 * 2)" = 100
```

**Also check reverse:** target = right / left

## Optimisations

### 1. Limited Results Per Value

Instead of storing ALL ways to create each value, store only the first `m` (default: 3):

```python
if len(results[value]) >= max_results_per_value:
    continue  # Skip adding more
```

**Impact:**
- Reduces memory by 50-70%
- Reduces combination time by 2-4x
- Minimal impact on solution quality (we still find good solutions)

**Rationale:** If we have 100 ways to create the value "25", we don't need all 100. The first few are usually the simplest.

### 2. Recursive Meet-in-Middle

For `num_count > 3`, we recursively apply meet-in-middle:

```python
if num_count <= 3:
    # Direct enumeration
else:
    # Recursive split
    left_vals = generate_all_subexpressions(..., num_count//2, ...)
    right_vals = generate_all_subexpressions(..., num_count-num_count//2, ...)
```

**Example:** k=7
- Split into 3 + 4
- The 4-part splits again into 2 + 2
- All parts use direct enumeration (≤3)

### 3. Hash Table Lookups

Using a dictionary (hash table) for `right_values` enables O(1) lookups:

```python
needed_right = target - left_val
if needed_right in right_values:  # O(1) lookup
    # Found a match!
```

Without hash table, we'd need O(n^(k/2)) search for each left value.

### 4. Integer Division Validation

Only consider division when the result is exact:

```python
if target != 0 and left_val % target == 0:
    # Only then calculate needed_right
```

This skips ~90% of division attempts.

### 5. Parenthesisation

Expressions are wrapped with minimal parentheses:

```python
def wrap_if_needed(expr, for_mult_div=False):
    if for_mult_div and ('+' in expr or '-' in expr):
        return f"({expr})"
    return expr

# Usage:
left_expr = wrap_if_needed(lp.expression, for_mult_div=True)
right_expr = wrap_if_needed(rp.expression, for_mult_div=True)
solution = f"{left_expr} * {right_expr}"
```

**Example:**
```
Left: "2 + 3" → "(2 + 3)"
Right: "4" → "4"
Result: "(2 + 3) * 4"  [correct precedence]
```

## Example Walkthrough

**Problem:** Find expressions for target=100 using up to 6 numbers from {1-8}, operators {+, -, *, /}

### Step 1: Split

k=6 → left=3, right=3

### Step 2: Generate Left Subexpressions (k=3)

Sample results:
```python
left_values = {
    1: [PartialResult(1, "1", (1,), 0)],
    2: [PartialResult(2, "2", (2,), 0), PartialResult(2, "1 + 1", (1,), 1)],
    ...
    25: [PartialResult(25, "(5 * 5)", (5,), 1)],
    ...
    125: [PartialResult(125, "(5 * 5 * 5)", (5,), 2)],
    ...
}
```

Total: ~8,192 subexpressions

### Step 3: Generate Right Subexpressions (k=3)

Same as left: ~8,192 subexpressions

### Step 4: Combine for Addition

```python
for left_val in [1, 2, 3, ..., 125, ...]:
    needed_right = 100 - left_val
    
    # Example: left_val = 25
    needed_right = 100 - 25 = 75
    
    if 75 in right_values:  # Check hash table
        # Found: right has 75 from "(3 * 5 * 5)"
        solution = "(5 * 5) + (3 * 5 * 5)" = 100
```

### Step 5: Combine for Multiplication

```python
for left_val in [1, 2, 3, ..., 25, ...]:
    if 100 % left_val == 0:
        needed_right = 100 // left_val
        
        # Example: left_val = 4
        needed_right = 100 // 4 = 25
        
        if 25 in right_values:  # Check hash table
            # Found: right has 25 from "(5 * 5)"
            # left has 4 from "(2 * 2)"
            solution = "(2 * 2) * (5 * 5)" = 100
```

### Result

Found solutions:
1. `(4 * 5 * 5)` = 100 [from direct search at k=3]
2. `(5 * 5) + (3 * 5 * 5)` = 100 [from meet-in-middle]
3. `(2 * 2) * (5 * 5)` = 100 [from meet-in-middle]
4. ... (more solutions)

## Complexity Analysis

### Time Complexity

**Subexpression generation:**
```
Left:  O(n^(k/2) × o^(k/2-1))
Right: O(n^(k/2) × o^(k/2-1))
```

**Combination:**
```
For each operator (o):
  For each left value (~n^(k/2)):
    Hash lookup: O(1)
    For each matching pair:
      Create solution: O(1)

Total: O(o × n^(k/2) × average_matches)
```

**Overall:** O(n^(k/2) × o^(k/2-1))

Compare to brute force: O(n^k × o^(k-1))

**Speedup:** O(n^(k/2) / n^k) = O(1 / n^(k/2))

For n=8, k=6: 1 / 8^3 = 1/512 ≈ **512x faster**

### Space Complexity

**Storage:**
```
Left subexpressions:  O(n^(k/2) × o^(k/2-1) × m)
Right subexpressions: O(n^(k/2) × o^(k/2-1) × m)
Solutions:            O(|solutions|)

Total: O(n^(k/2) × o^(k/2-1) × m)
```

Where m = `max_results_per_value`

**Example (k=6, n=8, o=4, m=3):**
```
Left:  8^3 × 4^2 × 3 ≈ 12,000 results
Right: 8^3 × 4^2 × 3 ≈ 12,000 results
Total: ~24,000 PartialResult objects ≈ 1-2 MB
```

## Advantages

1. **Exponential speedup** for large k
2. **Predictable memory usage** (controlled by m)
3. **Parallelisable** (left and right can be generated independently)
4. **Scalable** (works well even for k=10+)

## Disadvantages

1. **Overhead for small k** (k≤4 better with direct search)
2. **Memory usage** (must store all subexpressions)
3. **Complexity** (more complex implementation than brute force)

## When to Use

**Use meet-in-middle when:**
- k > 4
- n is large (>10)
- Memory is available (~1-100 MB)

**Use direct search when:**
- k ≤ 4
- n is small (<5)
- Memory is very limited

## See Also

- [Algorithm Overview](algorithm-overview.md) - High-level explanation
- [Complexity Analysis](complexity-analysis.md) - Detailed complexity
- [Optimisations](optimisations.md) - Optimisation strategies
- [Flowcharts](flowcharts/meet-in-middle-flow.md) - Visual representation
