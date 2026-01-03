# Expression Evaluation Flow

This flowchart details how mathematical expressions are evaluated with correct operator precedence.

## Main Evaluation Flow

```mermaid
flowchart TD
    Start([evaluate_expression<br/>numbers, operators]) --> CheckEmpty{numbers empty?}
    
    CheckEmpty -->|Yes| ReturnZero[Return 0]
    CheckEmpty -->|No| CheckSingle{Only 1 number?}
    
    CheckSingle -->|Yes| ReturnNum[Return that number]
    CheckSingle -->|No| CopyLists[Copy numbers and operators<br/>to working lists]
    
    CopyLists --> Pass1[Pass 1: Exponentiation **]
    Pass1 --> Pass2[Pass 2: Multiplication * and Division /]
    Pass2 --> Pass3[Pass 3: Addition + and Subtraction -]
    
    Pass3 --> ReturnResult[Return final result]
    
    ReturnZero --> End([End])
    ReturnNum --> End
    ReturnResult --> End
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style Pass1 fill:#ffe1e1
    style Pass2 fill:#fff5e1
    style Pass3 fill:#e1e5ff
```

## Pass 1: Exponentiation (**)

```mermaid
flowchart TD
    Start([Pass 1: Exponentiation]) --> Init[i = 0]
    
    Init --> Loop{i < len ops?}
    
    Loop -->|No| Done([Pass 1 Complete])
    Loop -->|Yes| CheckOp{ops i == '**'?}
    
    CheckOp -->|No| Increment[i = i + 1]
    Increment --> Loop
    
    CheckOp -->|Yes| Calc[nums i = nums i ** nums i+1]
    
    Calc --> Remove[Remove nums i+1<br/>Remove ops i]
    
    Remove --> Loop
    
    style Start fill:#e1f5e1
    style Done fill:#ffe1e1
```

**Example:**
```
Before: nums=[2, 3, 4], ops=['**', '+']
After Pass 1: nums=[8, 4], ops=['+']
  (2 ** 3 = 8)
```

## Pass 2: Multiplication and Division

```mermaid
flowchart TD
    Start([Pass 2: Mult/Div]) --> Init[i = 0]
    
    Init --> Loop{i < len ops?}
    
    Loop -->|No| Done([Pass 2 Complete])
    Loop -->|Yes| CheckOp{ops i in<br/> *, / ?}
    
    CheckOp -->|No| Increment[i = i + 1]
    Increment --> Loop
    
    CheckOp -->|Yes| WhichOp{Which operator?}
    
    WhichOp -->|*| Mult[nums i = nums i * nums i+1]
    WhichOp -->|/| CheckDiv{Division valid?}
    
    CheckDiv -->|nums i+1 == 0| ReturnNone[Return None<br/>Division by zero]
    CheckDiv -->|nums i % nums i+1 != 0| ReturnNone2[Return None<br/>Non-integer result]
    CheckDiv -->|Valid| Div[nums i = nums i // nums i+1]
    
    Mult --> Remove[Remove nums i+1<br/>Remove ops i]
    Div --> Remove
    
    Remove --> Loop
    
    ReturnNone --> End([End: Invalid])
    ReturnNone2 --> End
    
    style Start fill:#e1f5e1
    style Done fill:#ffe1e1
    style End fill:#ffcccc
```

**Example:**
```
Before: nums=[8, 4, 2], ops=['+', '/']
After Pass 2: nums=[8, 2], ops=['+']
  (4 / 2 = 2)

Invalid example:
nums=[7, 2], ops=['/']
7 % 2 != 0, so return None
```

## Pass 3: Addition and Subtraction

```mermaid
flowchart TD
    Start([Pass 3: Add/Sub]) --> Init[result = nums 0<br/>i = 0]
    
    Init --> Loop{i < len ops?}
    
    Loop -->|No| Done([Return result])
    Loop -->|Yes| CheckOp{ops i?}
    
    CheckOp -->|+| Add[result = result + nums i+1]
    CheckOp -->|-| Sub[result = result - nums i+1]
    
    Add --> Increment[i = i + 1]
    Sub --> Increment
    
    Increment --> Loop
    
    style Start fill:#e1f5e1
    style Done fill:#ffe1e1
```

**Example:**
```
Before: nums=[8, 2, 5], ops=['+', '-']
Step 1: result = 8
Step 2: result = 8 + 2 = 10
Step 3: result = 10 - 5 = 5
Return: 5
```

## Complete Example Walkthrough

**Expression:** `2 + 3 * 4 ** 2`

**Input:**
```
numbers = [2, 3, 4, 2]
operators = ['+', '*', '**']
```

### Pass 1: Exponentiation

```
i=0: ops[0] = '+' (not **), i++
i=1: ops[1] = '*' (not **), i++
i=2: ops[2] = '**' ✓
  nums[2] = 4 ** 2 = 16
  Remove nums[3], ops[2]
  
After: nums=[2, 3, 16], ops=['+', '*']
```

### Pass 2: Multiplication/Division

```
i=0: ops[0] = '+' (not * or /), i++
i=1: ops[1] = '*' ✓
  nums[1] = 3 * 16 = 48
  Remove nums[2], ops[1]
  
After: nums=[2, 48], ops=['+']
```

### Pass 3: Addition/Subtraction

```
result = nums[0] = 2
i=0: ops[0] = '+' ✓
  result = 2 + 48 = 50
  
Return: 50
```

**Result:** `2 + 3 * 4 ** 2 = 50` ✓

## Operator Precedence Table

| Precedence | Operators | Associativity | Pass |
|------------|-----------|---------------|------|
| 1 (Highest) | `**` | Right-to-left* | Pass 1 |
| 2 | `*`, `/` | Left-to-right | Pass 2 |
| 3 (Lowest) | `+`, `-` | Left-to-right | Pass 3 |

*Note: Current implementation processes `**` left-to-right, which differs from standard mathematical convention. This could be updated if needed.

## Validation Checks

### Division by Zero

```mermaid
flowchart TD
    Start([Division Operation]) --> CheckZero{divisor == 0?}
    
    CheckZero -->|Yes| Invalid[Return None<br/>Invalid expression]
    CheckZero -->|No| CheckInt{dividend %<br/>divisor == 0?}
    
    CheckInt -->|No| Invalid2[Return None<br/>Non-integer result]
    CheckInt -->|Yes| Valid[Perform division<br/>result = dividend // divisor]
    
    Invalid --> End([End])
    Invalid2 --> End
    Valid --> End
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style Invalid fill:#ffcccc
    style Invalid2 fill:#ffcccc
```

### Integer Division Requirement

**Why:** Beltmatic uses integer arithmetic only.

**Examples:**
```
8 / 2 = 4 ✓ (exact integer)
7 / 2 = 3.5 ✗ (not an integer, return None)
10 / 3 = 3.33... ✗ (not an integer, return None)
```

## Edge Cases

### Empty Expression

```
Input: numbers=[], operators=[]
Output: 0
```

### Single Number

```
Input: numbers=[42], operators=[]
Output: 42
```

### All Same Operator

```
Input: numbers=[2, 3, 4, 5], operators=['+', '+', '+']
Evaluation: 2 + 3 + 4 + 5 = 14
```

### Mixed Precedence

```
Input: numbers=[2, 3, 4, 5], operators=['+', '*', '-']
Expression: 2 + 3 * 4 - 5

Pass 1 (**: none
Pass 2 (*): 3 * 4 = 12
  → numbers=[2, 12, 5], operators=['+', '-']
Pass 3 (+, -):
  result = 2
  result = 2 + 12 = 14
  result = 14 - 5 = 9
  
Output: 9
```

## Complexity Analysis

### Time Complexity

```
Pass 1 (**: O(k) where k = number of operators
Pass 2 (*, /): O(k)
Pass 3 (+, -): O(k)

Total: O(k) = O(num_count - 1)
```

### Space Complexity

```
Working copies of numbers and operators: O(k)
```

## Implementation Notes

### Why Three Passes?

**Alternative:** Single pass with precedence checking

**Chosen approach:** Three passes for simplicity and clarity
- Easy to understand and maintain
- Correct precedence guaranteed
- Performance overhead is minimal (O(k) is fast)

### Why Modify Lists In-Place?

**Benefit:** Simulates the evaluation process naturally
- As we evaluate `3 * 4`, we replace it with `12`
- The list shrinks as we combine terms
- Final list has one element: the result

**Example:**
```
Start:    [2, 3, 4, 5] with ['+', '*', '-']
After *:  [2, 12, 5] with ['+', '-']
After +:  [14, 5] with ['-']
After -:  [9] with []
Result:   9
```

## See Also

- [Overall Flow](overall-flow.md) - Main algorithm flow
- [Direct Search Flow](direct-search-flow.md) - Direct search details
- [Algorithm Overview](../algorithm-overview.md) - High-level explanation
