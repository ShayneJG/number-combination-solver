# Algorithm Overview

## Problem Statement

Given:
- A target number `T`
- A set of available integers `{1, 2, ..., max_int}`
- A set of allowed operators `O` (subset of `{+, -, *, /, **}`)
- Maximum number of integers to use `k`

Find: Mathematical expressions using up to `k` integers from the available set and operators from `O` that evaluate to `T`.

**Example:**
```
Target: 100
Available: {1, 2, 3, 4, 5, 6, 7, 8}
Operators: {+, -, *, /}
Max numbers: 6

Solutions:
- (4 * 5 * 5) = 100
- (2 * 8) + (6 * 7 * 2) = 100
- (10 * 10) = 100  [if max_int ≥ 10]
```

## Solution Approach

The solver uses a **hybrid algorithm** that adapts based on the expression size:

### Small Expressions (k ≤ 4): Direct Search
For small numbers of integers, a brute-force approach is efficient:
1. Generate all permutations of `k` numbers (with replacement)
2. Generate all combinations of `k-1` operators
3. Evaluate each expression
4. Keep those that equal the target

The search space is small enough for exhaustive enumeration.

### Large Expressions (k > 4): Meet-in-the-Middle
For larger expressions, we use a divide-and-conquer approach:
1. Split `k` into two halves: `left_count` and `right_count`
2. Generate all possible values from `left_count` numbers
3. Generate all possible values from `right_count` numbers
4. For each operator, find pairs that combine to the target
5. Combine matching pairs into complete expressions

Instead of O(n^k), we get O(n^(k/2)), which is exponentially faster.

## Key Algorithms

### 1. Expression Evaluation

Expressions are evaluated respecting standard operator precedence:
1. **Exponentiation (`**`)** - Highest precedence, right-to-left
2. **Multiplication (`*`) and Division (`/`)** - Medium precedence, left-to-right
3. **Addition (`+`) and Subtraction (`-`)** - Lowest precedence, left-to-right

**Example:**
```
2 + 3 * 4 ** 2
= 2 + 3 * 16      [4 ** 2 first]
= 2 + 48          [3 * 16 next]
= 50              [2 + 48 last]
```



### 2. Deduplication via Canonical Keys

To avoid duplicate solutions like `2 + 3` and `3 + 2`, we create a canonical form:

1. **Normalise addition/subtraction terms:**
   - Split expression at top-level `+` and `-`
   - Sort positive terms alphabetically
   - Sort negative terms alphabetically
   - Combine: all positive terms, then all negative terms

2. **Normalise multiplication terms:**
   - For pure multiplication (no division), sort factors alphabetically
   - Example: `3 * 2 * 5` → `2 * 3 * 5`

3. **Remove redundant parentheses:**
   - Strip outer parentheses when they don't affect meaning
   - Example: `((2 + 3))` → `2 + 3`

**Example:**
```
Original expressions:
- "3 + 2"
- "2 + 3"
- "(2 + 3)"

Canonical form: "+2+3"
Result: All three are recognised as duplicates
```
**Note:** In the canonical form, each number also has an operator for the sake of simplicity, e.g., `+2+3` instead of `2+3`, so that we can handle the case of `2+3` and `3+2` as duplicates. Without the operator, 2 and +2 would be considered different. 

### 3. Meet-in-the-Middle Search

The core optimisation for large expressions:

**Traditional Approach (Brute Force):**
```
For k=6, n=8, o=4:
Total combinations = 8^6 × 4^5 = 262,144 × 1,024 ≈ 268 million
```

**Meet-in-the-Middle Approach:**
```
Split into k=3 + k=3:
Left half:  8^3 × 4^2 = 512 × 16 = 8,192 subexpressions
Right half: 8^3 × 4^2 = 512 × 16 = 8,192 subexpressions

For each operator, lookup matching pairs:
- Addition:       target = left + right  →  right = target - left
- Subtraction:    target = left - right  →  right = left - target
- Multiplication: target = left * right  →  right = target / left
- Division:       target = left / right  →  right = left / target

Total lookups: ~8,192 × 4 = ~32,768 (with hash table O(1) lookups)
```

**Speedup:** From ~268 million to ~33 thousand operations = **~8,000x faster!**

## Algorithm Selection Logic

```python
def find_solutions(target, max_int, operators, max_numbers):
    for num_count in range(1, max_numbers + 1):
        if num_count <= 4:
            # Use direct search (brute force)
            solutions = direct_search(target, num_count)
        else:
            # Use meet-in-the-middle
            solutions = meet_in_middle_search(target, num_count)
        
        # Early termination if we have enough good solutions
        if sufficient_solutions_found(solutions):
            break
    
    return best_solutions(solutions)
```

**Threshold of 4:** The crossover point where meet-in-the-middle becomes more efficient than brute force.

## Search Space Pruning

Several strategies reduce the search space:

### 1. Integer Division Only
Only allow division when the result is an exact integer:
```python
if nums[i] % nums[i + 1] != 0:
    return None  # Skip this expression
```

### 2. Limited Results Per Value
Store only the first `max_results_per_value` (default: 3) ways to create each intermediate value:
```python
if len(results[value]) >= max_results_per_value:
    continue  # Skip adding more ways to create this value
```

### 3. Early Termination
Stop searching when we have enough solutions with minimal operations:
```python
if len(solutions) >= top_n and best_op_count < current_level:
    break  # We have enough good solutions
```

### 4. Operator Validation
Skip invalid operations early:
- Division by zero
- Non-integer division results
- Exponentiation overflow (if implemented with limits)

## Expression Formatting

Expressions are formatted with minimal parentheses:

**Rules:**
1. Parenthesise multiplication/division operands if they contain `+` or `-`
2. Parenthesise subtraction right operand if it contains `+` or `-`
3. Remove redundant outer parentheses

**Examples:**
```
(2 + 3) * 4       ← Parentheses needed
2 * 3 + 4         ← No parentheses needed
5 - (2 + 3)       ← Parentheses needed on right
(5 - 2) + 3       ← No parentheses needed (left-to-right)
```

## Performance Characteristics

| Expression Size | Algorithm | Typical Time | Search Space |
|----------------|-----------|--------------|--------------|
| k = 1 | Direct | <1ms | n |
| k = 2 | Direct | <10ms | n² × o |
| k = 3 | Direct | <100ms | n³ × o² |
| k = 4 | Direct | ~1s | n⁴ × o³ |
| k = 5 | Meet-in-middle | ~1s | 2 × n^2.5 × o^1.5 |
| k = 6 | Meet-in-middle | ~5s | 2 × n³ × o² |

*Assuming n=8, o=4*

## Next Steps

- For detailed complexity analysis, see [Complexity Analysis](complexity-analysis.md)
- For meet-in-the-middle details, see [Meet-in-the-Middle Algorithm](meet-in-middle.md)
- For optimisation strategies, see [Optimisations](optimisations.md)
- For visual flowcharts, see [Flowcharts](flowcharts/overall-flow.md)
