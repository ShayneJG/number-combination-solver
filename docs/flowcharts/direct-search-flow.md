# Direct Search Algorithm Flow

This flowchart details the direct search (brute force) algorithm. In practice, `find_solutions()` calls this algorithm when `num_count ≤ 4`, but the algorithm itself can handle any value of `max_nums`.

## Main Direct Search Flow

```mermaid
flowchart TD
    Start([direct_search<br/>target, available_numbers,<br/>operators, max_nums, top_n]) --> Init[Initialise solutions set]
    
    Init --> LoopK{For num_count<br/>1 to max_nums}
    
    LoopK --> CheckOne{num_count == 1?}
    
    CheckOne -->|Yes| SingleNum[Check each number<br/>if it equals target]
    SingleNum --> AddSingle[Add matching numbers<br/>as solutions]
    AddSingle --> LoopK
    
    CheckOne -->|No| GenPerms[Generate all permutations<br/>of num_count numbers<br/>with replacement]
    
    GenPerms --> LoopPerms{For each<br/>number permutation}
    
    LoopPerms --> GenOps[Generate all combinations<br/>of num_count-1 operators]
    
    GenOps --> LoopOps{For each<br/>operator combination}
    
    LoopOps --> Eval[Evaluate expression<br/>respecting precedence]
    
    Eval --> CheckResult{Result == target?}
    
    CheckResult -->|No| LoopOps
    CheckResult -->|Yes| Format[Format expression<br/>with minimal parentheses]
    
    Format --> CreateSol[Create Solution object<br/>with canonical key]
    
    CreateSol --> AddSol[Add to solutions set<br/>automatic deduplication]
    
    AddSol --> LoopOps
    LoopOps -->|Done| LoopPerms
    LoopPerms -->|Done| LoopK
    
    LoopK -->|All k done| Return([Return solutions set])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
    style Eval fill:#fff5e1
```

## Number Permutation Generation

```mermaid
flowchart TD
    Start([Generate Permutations<br/>num_count]) --> Product[Use itertools.product<br/>available_numbers,<br/>repeat=num_count]
    
    Product --> Example[Example: num_count=3, available= 1-8]
    
    Example --> List[Generates:<br/> 1,1,1 <br/> 1,1,2 <br/> 1,1,3 <br/>...<br/> 8,8,8]
    
    List --> Total[Total: n^num_count permutations<br/>e.g., 8^3 = 512]
    
    Total --> Return([Return iterator])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
```

## Operator Combination Generation

```mermaid
flowchart TD
    Start([Generate Operator Combinations<br/>num_count-1]) --> Product[Use itertools.product<br/>operators,<br/>repeat=num_count-1]
    
    Product --> Example[Example: num_count=3, operators= +,-,*,/]
    
    Example --> List[Generates:<br/> +,+ <br/> +,- <br/> +,* <br/> +,/ <br/>...<br/> /,/]
    
    List --> Total[Total: o^num_count-1 combinations<br/>e.g., 4^2 = 16]
    
    Total --> Return([Return iterator])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
```

## Expression Evaluation Flow

See [Expression Evaluation](expression-evaluation.md) for detailed flow.

## Expression Formatting Flow

```mermaid
flowchart TD
    Start([format_expression<br/>numbers, operators]) --> Init[Initialise segments list<br/>current_group = first number<br/>in_mult_group = False]
    
    Init --> LoopOps{For each operator}
    
    LoopOps --> CheckMult{Operator is<br/>* or /?}
    
    CheckMult -->|Yes| SetMult[in_mult_group = True<br/>Add to current_group]
    SetMult --> LoopOps
    
    CheckMult -->|No| CheckGroup{in_mult_group?}
    
    CheckGroup -->|Yes| WrapGroup[Wrap current_group<br/>in parentheses<br/>Add to segments]
    CheckGroup -->|No| AddPlain[Add current_group<br/>to segments]
    
    WrapGroup --> AddOp[Add operator to segments<br/>Start new current_group]
    AddPlain --> AddOp
    
    AddOp --> LoopOps
    
    LoopOps -->|Done| FinalCheck{in_mult_group?}
    
    FinalCheck -->|Yes| FinalWrap[Wrap final group<br/>in parentheses]
    FinalCheck -->|No| FinalPlain[Add final group<br/>as-is]
    
    FinalWrap --> Join[Join all segments]
    FinalPlain --> Join
    
    Join --> Return([Return formatted expression])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
```

## Example Walkthrough

**Target:** 100, **k:** 3, **Available:** {1-8}, **Operators:** {+, -, *, /}

### Step 1: Generate Number Permutations

```
Sample permutations (out of 8^3 = 512):
[1, 1, 1]
[1, 1, 2]
...
[4, 5, 5]  ← Will find solution
...
[8, 8, 8]
```

### Step 2: Generate Operator Combinations

```
For each permutation, try all 4^2 = 16 operator combinations:
[+, +]
[+, -]
[+, *]  ← Will find solution with [4, 5, 5]
[+, /]
...
[/, /]
```

### Step 3: Evaluate Expression

```
Numbers: [4, 5, 5]
Operators: [+, *]

Evaluation (respecting precedence):
  Step 1: Handle * first
    5 * 5 = 25
    Numbers: [4, 25]
    Operators: [+]
  
  Step 2: Handle +
    4 + 25 = 29
  
Result: 29 ≠ 100 (not a solution)

---

Numbers: [4, 5, 5]
Operators: [*, *]

Evaluation:
  Step 1: Handle * (left to right)
    4 * 5 = 20
    Numbers: [20, 5]
    Operators: [*]
  
  Step 2: Handle remaining *
    20 * 5 = 100
  
Result: 100 == 100 ✓ (solution found!)
```

### Step 4: Format Expression

```
Numbers: [4, 5, 5]
Operators: [*, *]

Formatting:
  Start: "4"
  Operator *: in_mult_group = True, current_group = "4 * 5"
  Operator *: still in_mult_group, current_group = "4 * 5 * 5"
  End: in_mult_group = True, wrap in parentheses
  
Result: "(4 * 5 * 5)"
```

### Step 5: Create Solution

```python
Solution(
    expression="(4 * 5 * 5)",
    result=100,
    unique_nums=(4, 5),  # sorted unique
    op_count=2,
    _canonical="+4*5*5"  # computed in __post_init__
)
```

## Complexity Analysis

### Time Complexity

```
For num_count = k:
  Number permutations: n^k
  Operator combinations: o^(k-1)
  Evaluation per expression: O(k)
  
Total: O(n^k × o^(k-1) × k)
```

**Examples:**

| n | k | o | Permutations | Op Combos | Total | Time |
|---|---|---|--------------|-----------|-------|------|
| 8 | 1 | 4 | 8 | 1 | 8 | <1ms |
| 8 | 2 | 4 | 64 | 4 | 256 | <5ms |
| 8 | 3 | 4 | 512 | 16 | 8,192 | ~50ms |
| 8 | 4 | 4 | 4,096 | 64 | 262,144 | ~1s |

### Space Complexity

```
Storage:
  Current expression: O(k)
  Solutions set: O(|solutions|)
  
Total: O(k + |solutions|)
```

Typically: O(100) - O(10,000)

## When Direct Search is Used

**Called by `find_solutions()` when:**
- `num_count ≤ 4`

**Important:** The `direct_search()` function itself accepts any `max_nums` value and will search from 1 to `max_nums`. The threshold of 4 is a decision made by `find_solutions()` about *when* to call this function, not a limitation of the function itself.

**Rationale for the threshold:**
- Search space is manageable for k≤4 (≤ 262,144 expressions for k=4)
- Simple implementation
- No memory overhead for subexpressions
- Faster than meet-in-middle for small k due to lower overhead

**Crossover point:** k=4 is empirically determined as the point where meet-in-middle becomes more efficient.

## Optimisations Applied

1. **Early evaluation termination:** If evaluate_expression returns None (invalid), skip formatting
2. **Canonical deduplication:** Automatic via Solution set
3. **Minimal parenthesisation:** Only add parentheses when needed for precedence
4. **Iterator-based generation:** Uses itertools.product for memory efficiency

## Comparison with Meet-in-Middle

| Aspect | Direct Search | Meet-in-Middle |
|--------|--------------|----------------|
| **Time (k=4)** | O(n^4 × o^3) | O(n^2 × o) |
| **Time (k=6)** | O(n^6 × o^5) | O(n^3 × o^2) |
| **Space** | O(k) | O(n^(k/2) × o^(k/2-1)) |
| **Implementation** | Simple | Complex |
| **Best for** | k ≤ 4 | k > 4 |

**For k=4, n=8, o=4:**
- Direct: 8^4 × 4^3 = 262,144 (~1s)
- Meet-in-middle: 2 × 8^2 × 4 = 512 (~0.01s)

Even though meet-in-middle is faster, direct search is used for k≤4 because:
1. Implementation is simpler
2. Performance is acceptable (~1s)
3. No memory overhead
4. Code is easier to maintain

## See Also

- [Overall Flow](overall-flow.md) - Main algorithm flow
- [Expression Evaluation](expression-evaluation.md) - Evaluation details
- [Algorithm Overview](../algorithm-overview.md) - High-level explanation
- [Complexity Analysis](../complexity-analysis.md) - Performance details
