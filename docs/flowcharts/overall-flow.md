# Overall Algorithm Flow

This flowchart shows the high-level flow of the number combination solver.

## Main Algorithm Flow

```mermaid
flowchart TD
    Start([Start: find_solutions]) --> Init[Initialise parameters<br/>target, max_int, operators, max_numbers]
    Init --> SetupNums[Create available_numbers list<br/>1 to max_int, excluding excluded]
    SetupNums --> SetupOps[Build operators list<br/>based on allow_* flags]
    SetupOps --> InitSols[Initialise empty solutions set]
    
    InitSols --> LoopStart{For num_count<br/>1 to max_numbers}
    
    LoopStart -->|num_count ≤ 4| DirectPath[Use Direct Search]
    LoopStart -->|num_count > 4| MeetPath[Use Meet-in-Middle]
    
    DirectPath --> DirectSearch[direct_search<br/>target, num_count]
    MeetPath --> MeetSearch[meet_in_middle_search<br/>target, num_count]
    
    DirectSearch --> Filter[Filter solutions<br/>by op_count]
    MeetSearch --> Filter
    
    Filter --> UpdateSols[Add new solutions<br/>to all_solutions]
    
    UpdateSols --> CheckEarly{Early termination?<br/>Have enough<br/>good solutions?}
    
    CheckEarly -->|Yes| Sort[Sort solutions<br/>by op_count, unique_nums]
    CheckEarly -->|No| LoopStart
    
    LoopStart -->|Done all k| Sort
    
    Sort --> TopN[Return top_n solutions]
    TopN --> End([End])
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style DirectPath fill:#e1e5ff
    style MeetPath fill:#fff5e1
    style CheckEarly fill:#ffe1f5
```

## Early Termination Logic

```mermaid
flowchart TD
    Start([Check Early Termination]) --> HasSols{Have any<br/>solutions?}
    
    HasSols -->|No| Continue[Continue searching]
    HasSols -->|Yes| FindBest[Find best_op_count<br/>= min op_count in solutions]
    
    FindBest --> CompareOps{best_op_count ≤<br/>num_count - 1?}
    
    CompareOps -->|No| Continue
    CompareOps -->|Yes| CheckCount{len solutions<br/>≥ top_n?}
    
    CheckCount -->|Yes| Stop[Stop searching<br/>Return solutions]
    CheckCount -->|No| CheckNext{best_op_count <<br/>next_level - 1?}
    
    CheckNext -->|Yes| Stop
    CheckNext -->|No| Continue
    
    Continue --> End([Continue to next k])
    Stop --> End2([Stop iteration])
    
    style Start fill:#e1f5e1
    style End fill:#e1e5ff
    style End2 fill:#ffe1e1
    style Stop fill:#ffcccc
```

## Algorithm Selection Logic

```mermaid
flowchart TD
    Start([Determine Algorithm]) --> CheckK{num_count ≤ 4?}
    
    CheckK -->|Yes| Direct[Use Direct Search<br/>Brute force enumeration]
    CheckK -->|No| Meet[Use Meet-in-Middle<br/>Divide and conquer]
    
    Direct --> DirectReason[Reason: Small search space<br/>n^k × o^k-1 is manageable<br/>Simple implementation]
    Meet --> MeetReason[Reason: Large search space<br/>Meet-in-middle provides<br/>exponential speedup]
    
    DirectReason --> DirectExample[Example k=4, n=8, o=4:<br/>8^4 × 4^3 = 262,144<br/>~1 second]
    MeetReason --> MeetExample[Example k=6, n=8, o=4:<br/>2 × 8^3 × 4^2 = 16,384<br/>~0.2 seconds]
    
    DirectExample --> End([Execute chosen algorithm])
    MeetExample --> End
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style Direct fill:#e1e5ff
    style Meet fill:#fff5e1
```

## Solution Deduplication Flow

```mermaid
flowchart TD
    Start([New Solution Found]) --> CreateSol[Create Solution object<br/>with expression, result, etc.]
    
    CreateSol --> CalcCanon[Calculate canonical_key<br/>in __post_init__]
    
    CalcCanon --> AddToSet{Add to solutions set}
    
    AddToSet -->|New canonical key| Added[Solution added<br/>to set]
    AddToSet -->|Duplicate canonical key| Rejected[Solution rejected<br/>already exists]
    
    Added --> End([Continue])
    Rejected --> End
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style Added fill:#ccffcc
    style Rejected fill:#ffcccc
```

## Canonical Key Generation

```mermaid
flowchart TD
    Start([canonical_key expression]) --> RemoveSpace[Remove all whitespace]
    
    RemoveSpace --> SplitTerms[Split into terms<br/>at top-level + and -]
    
    SplitTerms --> NormTerms[For each term:<br/>normalise_mult_term]
    
    NormTerms --> SortPos[Sort positive terms<br/>alphabetically]
    SortPos --> SortNeg[Sort negative terms<br/>alphabetically]
    
    SortNeg --> Combine[Combine:<br/>all +terms, then all -terms]
    
    Combine --> Return([Return canonical string])
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
```

## normalise_mult_term Flow

```mermaid
flowchart TD
    Start([normalise_mult_term term]) --> StripParen[Strip redundant<br/>outer parentheses]
    
    StripParen --> HasDiv{Contains<br/>division?}
    
    HasDiv -->|Yes| ReturnAsIs[Return as-is<br/>division not commutative]
    HasDiv -->|No| HasMult{Contains<br/>multiplication?}
    
    HasMult -->|No| ReturnAsIs
    HasMult -->|Yes| SplitFactors[Split by *<br/>into factors]
    
    SplitFactors --> SortFactors[Sort factors<br/>alphabetically]
    
    SortFactors --> Join[Join with *]
    
    Join --> Return([Return normalised term])
    ReturnAsIs --> Return
    
    style Start fill:#e1f5e1
    style Return fill:#ffe1e1
```

## Performance Characteristics

| Component | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| **Overall (k≤4)** | O(n^k × o^(k-1)) | O(k + solutions) |
| **Overall (k>4)** | O(n^(k/2) × o^(k/2-1)) | O(n^(k/2) × o^(k/2-1)) |
| **Canonical key** | O(expression length) | O(expression length) |
| **Set operations** | O(1) average | O(solutions) |

## See Also

- [Algorithm Overview](../algorithm-overview.md) - High-level explanation
- [Direct Search Flow](direct-search-flow.md) - Direct search details
- [Meet-in-Middle Flow](meet-in-middle-flow.md) - Meet-in-middle details
- [Expression Evaluation](expression-evaluation.md) - Evaluation details
