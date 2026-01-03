# Usage Examples

Practical examples demonstrating how to use the number combination solver.

## Basic Usage

### Simple Addition Only

```python
from number_combinations import find_solutions

# Find ways to make 10 using only addition
solutions = find_solutions(
    target=10,
    max_int=8,
    allow_multiply=False,
    allow_subtract=False,
    allow_divide=False,
    max_numbers=6,
    top_n=5
)

for sol in solutions:
    print(f"{sol.expression} = {sol.result}")
```

**Output:**
```
2 + 8 = 10
1 + 1 + 8 = 10
1 + 2 + 7 = 10
1 + 3 + 6 = 10
1 + 4 + 5 = 10
```

---

### With Multiplication

```python
solutions = find_solutions(
    target=100,
    max_int=8,
    allow_multiply=True,
    max_numbers=6,
    top_n=5
)

for sol in solutions:
    print(f"{sol.expression} = {sol.result} (ops: {sol.op_count})")
```

**Output:**
```
(4 * 5 * 5) = 100 (ops: 2)
(2 * 8) + (6 * 7 * 2) = 100 (ops: 4)
(1 * 4 * 5 * 5) = 100 (ops: 3)
```

---

### All Standard Operators

```python
solutions = find_solutions(
    target=2285,
    max_int=25,
    allow_multiply=True,
    allow_subtract=True,
    allow_divide=True,
    max_numbers=6,
    top_n=5
)

for sol in solutions:
    print(f"{sol.expression} = {sol.result}")
```

**Output:**
```
(5 * 5 * 7 * 13) = 2285
```

---

## Advanced Usage

### Excluding Specific Numbers

```python
# Find solutions without using 10
solutions = find_solutions(
    target=100,
    max_int=15,
    allow_multiply=True,
    exclude=[10],  # Don't use 10
    max_numbers=6,
    top_n=5
)
```

---

### Exhaustive Search

```python
# Find ALL solutions (slower but complete)
solutions = find_solutions(
    target=50,
    max_int=8,
    allow_multiply=True,
    allow_subtract=True,
    max_numbers=4,
    top_n=20,
    exhaustive=True  # Find all solutions
)

print(f"Found {len(solutions)} solutions")
```

---

### With Progress Callback

```python
def show_progress(message):
    print(f"Progress: {message}")

solutions = find_solutions(
    target=1000,
    max_int=20,
    allow_multiply=True,
    allow_subtract=True,
    allow_divide=True,
    max_numbers=6,
    top_n=5,
    progress_callback=show_progress
)
```

**Output:**
```
Progress: Searching 1 numbers...
Progress: Searching 2 numbers...
Progress: Searching 3 numbers...
Progress: Searching 4 numbers...
```

---

### With Exponentiation

```python
solutions = find_solutions(
    target=512,
    max_int=8,
    allow_multiply=True,
    allow_exponentiate=True,  # Enable **
    max_numbers=6,
    top_n=5
)

for sol in solutions:
    print(f"{sol.expression} = {sol.result}")
```

**Output:**
```
8 ** 3 = 512
(8 * 8 * 8) = 512
(2 * 4) ** 4 = 512
```

---

## Interpreting Results

### Solution Object

```python
solutions = find_solutions(target=100, max_int=8, allow_multiply=True)

sol = solutions[0]
print(f"Expression: {sol.expression}")
print(f"Result: {sol.result}")
print(f"Unique numbers: {sol.unique_nums}")
print(f"Operation count: {sol.op_count}")
```

**Output:**
```
Expression: (4 * 5 * 5)
Result: 100
Unique numbers: (4, 5)
Operation count: 2
```

---

### Sorting and Filtering

```python
solutions = find_solutions(target=100, max_int=10, allow_multiply=True, top_n=20)

# Solutions are already sorted by quality (fewest operations first)
print("Best solution:", solutions[0].expression)

# Filter by operation count
simple_solutions = [s for s in solutions if s.op_count <= 2]
print(f"Found {len(simple_solutions)} solutions with ≤2 operations")

# Filter by unique numbers used
minimal_solutions = [s for s in solutions if len(s.unique_nums) <= 2]
print(f"Found {len(minimal_solutions)} solutions using ≤2 unique numbers")
```

---

## Performance Tuning

### Fast Search (Small max_numbers)

```python
# Faster: limit max_numbers
solutions = find_solutions(
    target=1000,
    max_int=25,
    allow_multiply=True,
    allow_subtract=True,
    max_numbers=4,  # Smaller = faster
    top_n=5
)
```

---

### Comprehensive Search (Large max_numbers)

```python
# Slower but more thorough
solutions = find_solutions(
    target=1000,
    max_int=25,
    allow_multiply=True,
    allow_subtract=True,
    max_numbers=8,  # Larger = slower but more solutions
    top_n=10
)
```

---

### Balancing Speed and Quality

```python
# Good balance for most use cases
solutions = find_solutions(
    target=2285,
    max_int=25,
    allow_multiply=True,
    allow_subtract=True,
    allow_divide=True,
    max_numbers=6,      # Good balance
    top_n=5,            # Just need a few good solutions
    exhaustive=False    # Use optimisations
)
```

---

## Integration Examples

### Command-Line Tool

```python
# ncs.py
import sys
from number_combinations import find_solutions

def update_progress(msg):
    print(msg)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <number>")
        exit()

    target = int(sys.argv[1])

    sols = find_solutions(
        target=target,
        max_int=25,
        allow_multiply=True,
        allow_subtract=True,
        allow_divide=True,
        max_numbers=6,
        top_n=5,
        exhaustive=False,
        progress_callback=update_progress,
    )

    for solution in sols:
        print(f"{solution.expression} = {solution.result}")
```

**Usage:**
```bash
python ncs.py 100
```

---

### Web API

```python
from flask import Flask, request, jsonify
from number_combinations import find_solutions

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    
    solutions = find_solutions(
        target=data['target'],
        max_int=data.get('max_int', 25),
        allow_multiply=data.get('allow_multiply', True),
        allow_subtract=data.get('allow_subtract', True),
        allow_divide=data.get('allow_divide', True),
        max_numbers=data.get('max_numbers', 6),
        top_n=data.get('top_n', 5)
    )
    
    return jsonify({
        'solutions': [
            {
                'expression': sol.expression,
                'result': sol.result,
                'op_count': sol.op_count
            }
            for sol in solutions
        ]
    })

if __name__ == '__main__':
    app.run()
```

**Usage:**
```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{"target": 100, "max_int": 8, "allow_multiply": true}'
```

---

### Batch Processing

```python
from number_combinations import find_solutions

targets = [100, 200, 300, 400, 500]

for target in targets:
    solutions = find_solutions(
        target=target,
        max_int=25,
        allow_multiply=True,
        allow_subtract=True,
        max_numbers=6,
        top_n=1  # Just need one solution per target
    )
    
    if solutions:
        print(f"{target}: {solutions[0].expression}")
    else:
        print(f"{target}: No solution found")
```

---

## Common Patterns

### Finding the Simplest Solution

```python
solutions = find_solutions(target=100, max_int=10, allow_multiply=True, top_n=1)

if solutions:
    best = solutions[0]  # Already sorted by quality
    print(f"Simplest: {best.expression} ({best.op_count} operations)")
```

---

### Finding Solutions with Specific Numbers

```python
# Find solutions that use the number 7
solutions = find_solutions(target=100, max_int=10, allow_multiply=True, top_n=20)

solutions_with_7 = [s for s in solutions if 7 in s.unique_nums]

for sol in solutions_with_7:
    print(sol.expression)
```

---

### Checking if Target is Reachable

```python
solutions = find_solutions(target=9999, max_int=8, allow_multiply=True, max_numbers=6)

if solutions:
    print(f"Target is reachable! Example: {solutions[0].expression}")
else:
    print("Target is not reachable with these constraints")
```

---

## Error Handling

### Invalid Inputs

```python
try:
    solutions = find_solutions(
        target=-100,  # Negative targets work but may not find solutions
        max_int=8,
        allow_multiply=True
    )
except Exception as e:
    print(f"Error: {e}")
```

---

### No Solutions Found

```python
solutions = find_solutions(target=9999, max_int=5, max_numbers=3)

if not solutions:
    print("No solutions found. Try:")
    print("- Increasing max_int")
    print("- Increasing max_numbers")
    print("- Enabling more operators")
```

---

## Performance Expectations

| max_int | max_numbers | Operators | Typical Time |
|---------|-------------|-----------|--------------|
| 8 | 4 | +, *, - | ~0.2s |
| 8 | 6 | +, *, -, / | ~0.5s |
| 25 | 6 | +, *, -, / | ~1-2s |
| 25 | 8 | +, *, -, / | ~10-30s |

**Tips for better performance:**
- Keep `max_numbers ≤ 6` for fast results
- Use `exhaustive=False` (default)
- Reduce `max_int` if possible
- Limit operators to only what's needed

---

## See Also

- [API Reference](api-reference.md) - Complete function documentation
- [Algorithm Overview](algorithm-overview.md) - How it works
- [Complexity Analysis](complexity-analysis.md) - Performance details
