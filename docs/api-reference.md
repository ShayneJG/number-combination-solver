# API Reference

Complete reference for all public functions and classes in the number combination solver.

## Main Entry Point

### `find_solutions()`

Find mathematical expressions that equal a target number.

**Signature:**
```python
def find_solutions(
    target: int,
    max_int: int,
    allow_multiply: bool = False,
    allow_subtract: bool = False,
    allow_divide: bool = False,
    allow_exponentiate: bool = False,
    exclude: Optional[List[int]] = None,
    max_numbers: int = 6,
    top_n: int = 5,
    exhaustive: bool = False,
    progress_callback = None
) -> List[Solution]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | `int` | Required | The target number to reach |
| `max_int` | `int` | Required | Maximum integer to use (creates range 1 to max_int) |
| `allow_multiply` | `bool` | `False` | Enable multiplication operator (*) |
| `allow_subtract` | `bool` | `False` | Enable subtraction operator (-) |
| `allow_divide` | `bool` | `False` | Enable division operator (/) |
| `allow_exponentiate` | `bool` | `False` | Enable exponentiation operator (**) |
| `exclude` | `Optional[List[int]]` | `None` | List of integers to exclude from available numbers |
| `max_numbers` | `int` | `6` | Maximum number of integers to use in expression |
| `top_n` | `int` | `5` | Maximum number of solutions to return |
| `exhaustive` | `bool` | `False` | If True, find all solutions; if False, use optimisations |
| `progress_callback` | `Callable[[str], None]` | `None` | Optional callback for progress updates |

**Returns:**
- `List[Solution]`: List of Solution objects, sorted by quality (fewest operations first)

**Example:**
```python
solutions = find_solutions(
    target=100,
    max_int=8,
    allow_multiply=True,
    allow_subtract=True,
    max_numbers=6,
    top_n=5
)

for sol in solutions:
    print(f"{sol.expression} = {sol.result}")
```

**Output:**
```
(4 * 5 * 5) = 100
(2 * 8) + (6 * 7 * 2) = 100
```

---

## Search Algorithms

### `meet_in_middle_search()`

Perform meet-in-the-middle search for large expressions (k > 4).

**Signature:**
```python
def meet_in_middle_search(
    target: int,
    available_numbers: List[int],
    operators: List[str],
    total_nums: int,
    top_n: int = 5,
    exhaustive: bool = False
) -> Set[Solution]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `target` | `int` | Target number to reach |
| `available_numbers` | `List[int]` | List of available integers |
| `operators` | `List[str]` | List of operator strings ('+', '-', '*', '/', '**') |
| `total_nums` | `int` | Total number of integers to use |
| `top_n` | `int` | Maximum solutions to find |
| `exhaustive` | `bool` | Whether to use exhaustive search |

**Returns:**
- `Set[Solution]`: Set of unique solutions

**Complexity:**
- Time: O(n^(k/2) × o^(k/2-1))
- Space: O(n^(k/2) × o^(k/2-1))

---

### `direct_search()`

Perform direct brute-force search for small expressions (k ≤ 4).

**Signature:**
```python
def direct_search(
    target: int,
    available_numbers: List[int],
    operators: List[str],
    max_nums: int,
    top_n: int
) -> Set[Solution]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `target` | `int` | Target number to reach |
| `available_numbers` | `List[int]` | List of available integers |
| `operators` | `List[str]` | List of operator strings |
| `max_nums` | `int` | Maximum number of integers to use |
| `top_n` | `int` | Maximum solutions to find |

**Returns:**
- `Set[Solution]`: Set of unique solutions

**Complexity:**
- Time: O(n^k × o^(k-1))
- Space: O(k + |solutions|)

---

### `generate_all_subexpressions()`

Generate all possible values from expressions using a specific number of integers.

**Signature:**
```python
def generate_all_subexpressions(
    available_numbers: List[int],
    num_count: int,
    operators: List[str],
    max_results_per_value: int = 3
) -> Dict[int, List[PartialResult]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `available_numbers` | `List[int]` | List of available integers |
| `num_count` | `int` | Number of integers to use |
| `operators` | `List[str]` | List of operator strings |
| `max_results_per_value` | `int` | Maximum ways to store for each value (0 = unlimited) |

**Returns:**
- `Dict[int, List[PartialResult]]`: Dictionary mapping values to lists of PartialResult objects

**Example:**
```python
results = generate_all_subexpressions(
    available_numbers=[1, 2, 3, 4, 5],
    num_count=2,
    operators=['+', '*'],
    max_results_per_value=3
)

# results[6] might contain:
# [
#   PartialResult(6, "2 * 3", (2, 3), 1),
#   PartialResult(6, "1 + 5", (1, 5), 1),
#   PartialResult(6, "2 + 4", (2, 4), 1)
# ]
```

---

## Expression Handling

### `evaluate_expression()`

Evaluate an expression with correct operator precedence.

**Signature:**
```python
def evaluate_expression(
    numbers: List[int],
    operators: List[str]
) -> Optional[int]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `numbers` | `List[int]` | List of numbers in the expression |
| `operators` | `List[str]` | List of operators (length = len(numbers) - 1) |

**Returns:**
- `Optional[int]`: Result of evaluation, or `None` if invalid (e.g., division by zero)

**Precedence:**
1. `**` (exponentiation) - highest
2. `*`, `/` (multiplication, division)
3. `+`, `-` (addition, subtraction) - lowest

**Example:**
```python
result = evaluate_expression([2, 3, 4], ['+', '*'])
# Evaluates: 2 + 3 * 4 = 2 + 12 = 14
print(result)  # 14

result = evaluate_expression([7, 2], ['/'])
# 7 / 2 is not an integer
print(result)  # None
```

---

### `format_expression()`

Format numbers and operators into a readable expression string with minimal parentheses.

**Signature:**
```python
def format_expression(
    numbers: List[int],
    operators: List[str]
) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `numbers` | `List[int]` | List of numbers |
| `operators` | `List[str]` | List of operators |

**Returns:**
- `str`: Formatted expression string

**Example:**
```python
expr = format_expression([2, 3, 4], ['+', '*'])
print(expr)  # "2 + (3 * 4)"

expr = format_expression([4, 5, 5], ['*', '*'])
print(expr)  # "(4 * 5 * 5)"
```

---

## Deduplication

### `canonical_key()`

Create a canonical form of an expression for deduplication.

**Signature:**
```python
def canonical_key(expression: str) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `expression` | `str` | Expression string to normalise |

**Returns:**
- `str`: Canonical form of the expression

**Example:**
```python
key1 = canonical_key("2 + 3")
key2 = canonical_key("3 + 2")
print(key1 == key2)  # True (both → "+2+3")

key3 = canonical_key("(2 * 3) + 1")
key4 = canonical_key("1 + (3 * 2)")
print(key3 == key4)  # True (both → "+1+2*3")
```

---

### `normalise_mult_term()`

Normalise a multiplication/division term by sorting factors.

**Signature:**
```python
def normalise_mult_term(term: str) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `term` | `str` | Term to normalise |

**Returns:**
- `str`: Normalised term

**Example:**
```python
norm = normalise_mult_term("3*2*5")
print(norm)  # "2*3*5"

norm = normalise_mult_term("(5*2)")
print(norm)  # "2*5"
```

---

## Utility Functions

### `wrap_if_needed()`

Wrap expression in parentheses if needed for operator precedence.

**Signature:**
```python
def wrap_if_needed(expr: str, for_mult_div: bool = False) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `expr` | `str` | Expression to potentially wrap |
| `for_mult_div` | `bool` | Whether wrapping for multiplication/division context |

**Returns:**
- `str`: Expression, wrapped if necessary

**Example:**
```python
wrapped = wrap_if_needed("2 + 3", for_mult_div=True)
print(wrapped)  # "(2 + 3)"

wrapped = wrap_if_needed("2 * 3", for_mult_div=True)
print(wrapped)  # "2 * 3" (no wrapping needed)
```

---

### `wrap_for_subtraction()`

Wrap expression in parentheses if it contains + or - (for right side of subtraction).

**Signature:**
```python
def wrap_for_subtraction(expr: str) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `expr` | `str` | Expression to potentially wrap |

**Returns:**
- `str`: Expression, wrapped if necessary

**Example:**
```python
wrapped = wrap_for_subtraction("2 + 3")
print(wrapped)  # "(2 + 3)"

wrapped = wrap_for_subtraction("5")
print(wrapped)  # "5" (no wrapping needed)
```

---

## Data Classes

### `Solution`

Represents a complete solution to the target problem.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `expression` | `str` | The formatted expression string |
| `result` | `int` | The result of the expression (should equal target) |
| `unique_nums` | `Tuple[int, ...]` | Sorted tuple of unique numbers used |
| `op_count` | `int` | Number of operators used |
| `_canonical` | `str` | Canonical form for deduplication (computed automatically) |

**Methods:**

- `__lt__(self, other)`: Compare solutions (fewer operations is better)
- `__eq__(self, other)`: Check equality based on canonical form
- `__hash__(self)`: Hash based on canonical form (enables set storage)

**Example:**
```python
sol = Solution(
    expression="(4 * 5 * 5)",
    result=100,
    unique_nums=(4, 5),
    op_count=2
)

print(sol.expression)  # "(4 * 5 * 5)"
print(sol.op_count)    # 2
print(sol._canonical)  # "+4*5*5" (computed in __post_init__)
```

---

### `PartialResult`

Represents an intermediate subexpression result.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | `int` | The numeric value of the subexpression |
| `expression` | `str` | The formatted expression string |
| `nums_used` | `Tuple[int, ...]` | Sorted tuple of unique numbers used |
| `op_count` | `int` | Number of operators used |

**Example:**
```python
partial = PartialResult(
    value=25,
    expression="(5 * 5)",
    nums_used=(5,),
    op_count=1
)

print(partial.value)       # 25
print(partial.expression)  # "(5 * 5)"
```

---

## Type Hints

The module uses the following type imports:

```python
from typing import List, Set, Tuple, Optional, Dict
from dataclasses import dataclass
```

All functions include proper type hints for parameters and return values.

---

## See Also

- [Usage Examples](usage-examples.md) - Practical usage examples
- [Algorithm Overview](algorithm-overview.md) - How the algorithms work
- [Complexity Analysis](complexity-analysis.md) - Performance characteristics
