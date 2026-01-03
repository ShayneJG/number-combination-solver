# Meet-in-the-Middle Algorithm Flow

This flowchart details the meet-in-the-middle search algorithm used for expressions with more than 4 numbers.

## Main Meet-in-Middle Flow

```mermaid
flowchart TD
    Start([meet_in_middle_search<br/>target, available_numbers,<br/>operators, total_nums,<br/>top_n, exhaustive]) --> Init[Initialise solutions set<br/>Set max_per_value]
    
    Init --> LoopSplit{For each split:<br/>left_count + right_count<br/>= total_nums}
    
    LoopSplit --> CheckSplit{left_count ><br/>total_nums+1 // 2?}
    
    CheckSplit -->|Yes, skip| LoopSplit
    CheckSplit -->|No, process| GenLeft[generate_all_subexpressions<br/>left_count numbers]
    
    GenLeft --> GenRight[generate_all_subexpressions<br/>right_count numbers]
    
    GenRight --> CombineAdd[Combine for Addition<br/>target = left + right]
    CombineAdd --> CombineSub[Combine for Subtraction<br/>target = left - right]
    CombineSub --> CombineMult[Combine for Multiplication<br/>target = left × right]
    CombineMult --> CombineDiv[Combine for Division<br/>target = left ÷ right]
    
    CombineDiv --> LoopSplit
    
    LoopSplit -->|All splits done| Return([Return solutions set])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
    style GenLeft fill:#e1e5ff
    style GenRight fill:#e1e5ff
```

## Subexpression Generation Flow

```mermaid
flowchart TD
    Start([generate_all_subexpressions<br/>available_numbers, num_count,<br/>operators, max_results_per_value]) --> InitDict[Initialise results dict<br/>value → list of PartialResults]
    
    InitDict --> CheckBase{num_count == 1?}
    
    CheckBase -->|Yes| BaseCase[For each number n:<br/>results n = PartialResult n, str n]
    BaseCase --> Return([Return results])
    
    CheckBase -->|No| CheckSmall{num_count ≤ 3?}
    
    CheckSmall -->|Yes| DirectEnum[Direct Enumeration:<br/>All number permutations<br/>All operator combinations]
    
    DirectEnum --> EvalLoop[For each combination:<br/>Evaluate expression]
    EvalLoop --> StoreResult[Store in results value]
    StoreResult --> Return
    
    CheckSmall -->|No| RecursiveSplit[Recursive Split:<br/>left_count = num_count // 2<br/>right_count = num_count - left_count]
    
    RecursiveSplit --> RecurseLeft[Recursively generate<br/>left subexpressions]
    RecurseLeft --> RecurseRight[Recursively generate<br/>right subexpressions]
    
    RecurseRight --> CombineLoop[For each left_val, right_val:<br/>For each operator:]
    
    CombineLoop --> CalcVal[Calculate new_val<br/>= left_val op right_val]
    
    CalcVal --> CheckValid{Valid result?<br/>e.g., no div by 0}
    
    CheckValid -->|No| CombineLoop
    CheckValid -->|Yes| CheckLimit{len results new_val<br/>< max_per_value?}
    
    CheckLimit -->|No| CombineLoop
    CheckLimit -->|Yes| AddResult[Create PartialResult<br/>Add to results new_val]
    
    AddResult --> CombineLoop
    CombineLoop -->|All done| Return
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
    style DirectEnum fill:#fff5e1
    style RecursiveSplit fill:#e1e5ff
```

## Addition Combination

```mermaid
flowchart TD
    Start([Combine for Addition<br/>target = left + right]) --> LoopLeft{For each left_val<br/>in left_values}
    
    LoopLeft --> CalcNeeded[needed_right<br/>= target - left_val]
    
    CalcNeeded --> CheckExists{needed_right<br/>in right_values?}
    
    CheckExists -->|No| LoopLeft
    CheckExists -->|Yes| LoopLeftPartial{For each left partial}
    
    LoopLeftPartial --> LoopRightPartial{For each right partial<br/>with needed_right}
    
    LoopRightPartial --> Combine[Combine unique numbers<br/>from both partials]
    
    Combine --> CreateExpr[Create expression:<br/>left.expr + right.expr]
    
    CreateExpr --> CreateSol[Create Solution object<br/>with canonical key]
    
    CreateSol --> AddSol[Add to solutions set<br/>automatic deduplication]
    
    AddSol --> LoopRightPartial
    LoopRightPartial -->|Done| LoopLeftPartial
    LoopLeftPartial -->|Done| LoopLeft
    
    LoopLeft -->|All done| End([Continue to next operator])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
```

## Subtraction Combination

```mermaid
flowchart TD
    Start([Combine for Subtraction<br/>target = left - right]) --> Forward[Forward: target = left - right]
    
    Forward --> LoopLeft1{For each left_val}
    
    LoopLeft1 --> CalcNeeded1[needed_right<br/>= left_val - target]
    
    CalcNeeded1 --> CheckExists1{needed_right<br/>in right_values?}
    
    CheckExists1 -->|Yes| CreateSol1[Create solutions:<br/>left - right = target]
    CheckExists1 -->|No| LoopLeft1
    
    CreateSol1 --> LoopLeft1
    LoopLeft1 -->|Done| Reverse[Reverse: target = right - left]
    
    Reverse --> LoopRight{For each right_val}
    
    LoopRight --> CalcNeeded2[needed_left<br/>= right_val - target]
    
    CalcNeeded2 --> CheckExists2{needed_left<br/>in left_values?}
    
    CheckExists2 -->|Yes| CreateSol2[Create solutions:<br/>right - left = target]
    CheckExists2 -->|No| LoopRight
    
    CreateSol2 --> LoopRight
    LoopRight -->|Done| End([Continue to next operator])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
```

## Multiplication Combination

```mermaid
flowchart TD
    Start([Combine for Multiplication<br/>target = left × right]) --> LoopLeft{For each left_val}
    
    LoopLeft --> CheckZero{left_val != 0?}
    
    CheckZero -->|No| LoopLeft
    CheckZero -->|Yes| CheckDiv{target %<br/>left_val == 0?}
    
    CheckDiv -->|No| LoopLeft
    CheckDiv -->|Yes| CalcNeeded[needed_right<br/>= target // left_val]
    
    CalcNeeded --> CheckExists{needed_right<br/>in right_values?}
    
    CheckExists -->|No| LoopLeft
    CheckExists -->|Yes| WrapExprs[Wrap expressions<br/>if needed for precedence]
    
    WrapExprs --> CreateSol[Create solutions:<br/>left × right = target]
    
    CreateSol --> LoopLeft
    LoopLeft -->|Done| End([Continue to next operator])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
```

## Division Combination

```mermaid
flowchart TD
    Start([Combine for Division<br/>target = left ÷ right]) --> Forward[Forward: target = left ÷ right]
    
    Forward --> LoopLeft1{For each left_val}
    
    LoopLeft1 --> CheckTarget1{target != 0?}
    
    CheckTarget1 -->|No| LoopLeft1
    CheckTarget1 -->|Yes| CheckDiv1{left_val %<br/>target == 0?}
    
    CheckDiv1 -->|No| LoopLeft1
    CheckDiv1 -->|Yes| CalcNeeded1[needed_right<br/>= left_val // target]
    
    CalcNeeded1 --> CheckZero1{needed_right != 0?}
    
    CheckZero1 -->|No| LoopLeft1
    CheckZero1 -->|Yes| CheckExists1{needed_right<br/>in right_values?}
    
    CheckExists1 -->|Yes| CreateSol1[Create solutions:<br/>left ÷ right = target]
    CheckExists1 -->|No| LoopLeft1
    
    CreateSol1 --> LoopLeft1
    LoopLeft1 -->|Done| Reverse[Reverse: target = right ÷ left]
    
    Reverse --> LoopRight{For each right_val}
    
    LoopRight --> CheckTarget2{target != 0?}
    
    CheckTarget2 -->|No| LoopRight
    CheckTarget2 -->|Yes| CheckDiv2{right_val %<br/>target == 0?}
    
    CheckDiv2 -->|No| LoopRight
    CheckDiv2 -->|Yes| CalcNeeded2[needed_left<br/>= right_val // target]
    
    CalcNeeded2 --> CheckZero2{needed_left != 0?}
    
    CheckZero2 -->|No| LoopRight
    CheckZero2 -->|Yes| CheckExists2{needed_left<br/>in left_values?}
    
    CheckExists2 -->|Yes| CreateSol2[Create solutions:<br/>right ÷ left = target]
    CheckExists2 -->|No| LoopRight
    
    CreateSol2 --> LoopRight
    LoopRight -->|Done| End([All operators done])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
```

## Example Walkthrough

**Target:** 100, **k:** 6, **Available:** {1-8}, **Operators:** {+, -, *, /}

### Split: left=3, right=3

**Left subexpressions (sample):**
```
value → expressions
25 → ["(5 * 5)", "1 + 24", "2 + 23"]
50 → ["(2 * 5 * 5)", "1 + 49", ...]
75 → ["(3 * 5 * 5)", ...]
```

**Right subexpressions (sample):**
```
value → expressions
25 → ["(5 * 5)", ...]
50 → ["(2 * 5 * 5)", ...]
75 → ["(3 * 5 * 5)", ...]
```

### Addition: 100 = left + right

```
left_val = 25, needed_right = 100 - 25 = 75
✓ 75 exists in right_values
Solution: "(5 * 5) + (3 * 5 * 5)" = 100

left_val = 50, needed_right = 100 - 50 = 50
✓ 50 exists in right_values
Solution: "(2 * 5 * 5) + (2 * 5 * 5)" = 100
```

### Multiplication: 100 = left × right

```
left_val = 4, check: 100 % 4 == 0 ✓
needed_right = 100 // 4 = 25
✓ 25 exists in right_values
Solution: "(2 * 2) * (5 * 5)" = 100
```

## Complexity Analysis

### Time Complexity

```
Subexpression generation:
  Left:  O(n^(k/2) × o^(k/2-1))
  Right: O(n^(k/2) × o^(k/2-1))

Combination (for each operator):
  For each left value: O(n^(k/2))
    Hash lookup: O(1)
    For each matching pair: O(m²) where m = max_per_value
  
Total: O(o × n^(k/2) × m²)

Overall: O(n^(k/2) × o^(k/2-1))
```

### Space Complexity

```
Left subexpressions:  O(n^(k/2) × o^(k/2-1) × m)
Right subexpressions: O(n^(k/2) × o^(k/2-1) × m)
Solutions:            O(|solutions|)

Total: O(n^(k/2) × o^(k/2-1) × m)
```

## Optimisations Applied

1. **Hash table lookups:** O(1) instead of O(n^(k/2)) search
2. **Limited results per value:** Reduces m from ∞ to 3
3. **Integer division validation:** Skips invalid divisions early
4. **Canonical deduplication:** Automatic via Solution.__hash__
5. **Expression wrapping:** Minimal parentheses for readability

## See Also

- [Overall Flow](overall-flow.md) - Main algorithm flow
- [Algorithm Overview](../algorithm-overview.md) - High-level explanation
- [Meet-in-the-Middle Algorithm](../meet-in-middle.md) - Detailed explanation
- [Complexity Analysis](../complexity-analysis.md) - Performance details
