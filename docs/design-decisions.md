# Design Decisions

This document explains the key architectural and design decisions made in the number combination solver, along with the rationale behind each choice.

## Algorithm Selection

### Why Meet-in-the-Middle for k > 4?

**Decision:** Use meet-in-the-middle algorithm for expressions with more than 4 numbers.

**Rationale:**
- **Exponential speedup:** Reduces O(n^k) to O(n^(k/2))
- **Empirical threshold:** k=4 is the crossover point where meet-in-middle becomes more efficient
- **Scalability:** Enables solving k=6, k=7, k=8 in reasonable time

**Alternatives considered:**
1. **Pure brute force:** Too slow for k>4 (268M operations for k=6)
2. **Dynamic programming:** Doesn't apply well to this problem structure
3. **Branch and bound:** More complex, similar performance

**Trade-offs:**
- ✅ Massive speedup for large k
- ✅ Predictable memory usage
- ❌ More complex implementation
- ❌ Overhead for small k (hence the threshold)

---

### Why Direct Search for k ≤ 4?

**Decision:** Use simple brute-force enumeration for small expressions.

**Rationale:**
- **Simplicity:** Easier to implement and maintain
- **Performance:** Fast enough (~1s for k=4)
- **No overhead:** No memory overhead for subexpressions
- **Correctness:** Straightforward to verify

**Alternatives considered:**
1. **Meet-in-middle for all k:** Unnecessary overhead for small k
2. **Different threshold:** k=4 is empirically optimal

**Trade-offs:**
- ✅ Simple, maintainable code
- ✅ Fast enough for k≤4
- ❌ Not optimal for k=4 (but acceptable)

---

## Deduplication Strategy

### Why Canonical Keys?

**Decision:** Use canonical form strings to detect duplicate expressions.

**Rationale:**
- **Effective:** Catches most duplicates (2 + 3 = 3 + 2)
- **Fast:** O(expression length) computation
- **Simple:** Easy to implement and understand
- **Hash-friendly:** Works with Python sets

**Alternatives considered:**
1. **Expression trees:** More accurate but much more complex
2. **Numerical equivalence:** Misses syntactic duplicates
3. **No deduplication:** Results in many redundant solutions

**Trade-offs:**
- ✅ Catches 80-90% of duplicates
- ✅ Fast and simple
- ❌ Doesn't catch all mathematical equivalences (e.g., 2*3 vs 6)
- ❌ Imperfect for division/subtraction

**Example limitations:**
```python
"2 * 3"  # Not recognised as duplicate of
"6"      # Even though mathematically equivalent
```

This is acceptable because:
- Perfect deduplication is computationally expensive
- Users often want to see different approaches
- The most common duplicates (commutativity) are caught

---

## Optimisation Choices

### Why Limit Results Per Value?

**Decision:** Store only first `m` (default: 3) ways to create each intermediate value.

**Rationale:**
- **Memory reduction:** 50-70% less memory usage
- **Speed improvement:** 2-4x faster
- **Quality preservation:** First few results are usually simplest
- **Diminishing returns:** 100 ways to make "25" doesn't help

**Alternatives considered:**
1. **No limit (exhaustive):** Too slow and memory-intensive
2. **Limit of 1:** Too aggressive, misses good solutions
3. **Adaptive limit:** More complex, marginal benefit

**Trade-offs:**
- ✅ Significant performance improvement
- ✅ Minimal quality impact
- ❌ Might miss some solutions in exhaustive mode
- ❌ Requires tuning (but default of 3 works well)

---

### Why Early Termination?

**Decision:** Stop searching when we have enough good solutions.

**Rationale:**
- **User expectation:** Users typically want a few good solutions, not all solutions
- **Performance:** 30-50% faster on average
- **Quality:** We keep the best solutions (fewest operations)

**Logic:**
```python
if len(solutions) >= top_n and best_op_count <= current_level - 1:
    break  # We have enough good solutions
```

**Alternatives considered:**
1. **Always search all k:** Slower, unnecessary
2. **More aggressive termination:** Might miss better solutions

**Trade-offs:**
- ✅ Faster for most cases
- ✅ Still finds best solutions
- ❌ Might miss some alternative solutions
- ❌ Disabled in exhaustive mode

---

## Expression Handling

### Why Integer Division Only?

**Decision:** Only allow division when the result is an exact integer.

**Rationale:**
- **Game mechanics:** Beltmatic uses integer arithmetic
- **Correctness:** Fractional results are invalid
- **Performance:** Skips ~90% of invalid divisions early

**Implementation:**
```python
if nums[i] % nums[i + 1] != 0:
    return None  # Invalid
```

**Alternatives considered:**
1. **Allow floating point:** Not applicable to Beltmatic
2. **Round results:** Mathematically incorrect

**Trade-offs:**
- ✅ Correct for Beltmatic
- ✅ Performance improvement
- ❌ Limits solution space (but correctly)

---

### Why Three-Pass Evaluation?

**Decision:** Evaluate expressions in three passes (**, then */,  then +-).

**Rationale:**
- **Correctness:** Guarantees correct operator precedence
- **Simplicity:** Easy to understand and verify
- **Performance:** O(k) is fast enough

**Alternatives considered:**
1. **Single pass with precedence checking:** More complex, similar performance
2. **Expression tree:** Overkill for this use case
3. **Shunting yard algorithm:** More complex, no benefit

**Trade-offs:**
- ✅ Simple and correct
- ✅ Easy to maintain
- ❌ Three passes instead of one (but k is small)

---

### Why Minimal Parenthesisation?

**Decision:** Add parentheses only when necessary for correct precedence.

**Rationale:**
- **Readability:** `2 + 3 * 4` is clearer than `2 + (3 * 4)`
- **Aesthetics:** Cleaner output
- **Standard:** Matches mathematical convention

**Rules:**
1. Wrap `+` or `-` terms when used in `*` or `/`
2. Wrap `+` or `-` on right side of `-`
3. Remove redundant outer parentheses

**Alternatives considered:**
1. **Always parenthesise:** Cluttered output
2. **Never parenthesise:** Ambiguous expressions

**Trade-offs:**
- ✅ Clean, readable output
- ✅ Mathematically correct
- ❌ Slightly more complex formatting logic

---

## Data Structure Choices

### Why Use Sets for Solutions?

**Decision:** Store solutions in a `Set[Solution]` with custom `__hash__` and `__eq__`.

**Rationale:**
- **Automatic deduplication:** Set handles duplicates automatically
- **Fast lookup:** O(1) average case
- **Clean API:** No manual duplicate checking

**Implementation:**
```python
@dataclass
class Solution:
    def __eq__(self, other):
        return self._canonical == other._canonical
    
    def __hash__(self):
        return hash(self._canonical)
```

**Alternatives considered:**
1. **List with manual deduplication:** Slower, more code
2. **Dictionary:** Unnecessary complexity

**Trade-offs:**
- ✅ Automatic deduplication
- ✅ Fast and clean
- ❌ Requires custom `__hash__` and `__eq__`

---

### Why Frozen Dataclass for PartialResult?

**Decision:** Use `@dataclass(frozen=True)` for `PartialResult`.

**Rationale:**
- **Immutability:** Prevents accidental modification
- **Hashable:** Can be used in sets/dicts if needed
- **Safety:** Guarantees data integrity

**Alternatives considered:**
1. **Mutable dataclass:** Risk of accidental modification
2. **Named tuple:** Less readable

**Trade-offs:**
- ✅ Immutable and safe
- ✅ Hashable
- ❌ Cannot modify after creation (but we don't need to)

---

## API Design

### Why So Many Boolean Flags?

**Decision:** Separate `allow_*` flags for each operator type.

**Rationale:**
- **Flexibility:** Users can enable exactly the operators they want
- **Clarity:** Explicit is better than implicit
- **Beltmatic mapping:** Matches game buildings (Adder, Multiplier, etc.)

**Alternatives considered:**
1. **Single `operators` parameter:** Less clear what's available
2. **Operator string list:** More flexible but less discoverable

**Trade-offs:**
- ✅ Clear and explicit
- ✅ Matches game mechanics
- ❌ More parameters (but with good defaults)

---

### Why Default to Minimal Operators?

**Decision:** All operators default to `False` except addition.

**Rationale:**
- **Safety:** Users opt-in to complexity
- **Performance:** Fewer operators = faster search
- **Clarity:** Explicit about what's enabled

**Alternatives considered:**
1. **Enable all by default:** Surprising behaviour
2. **Require all to be specified:** Verbose

**Trade-offs:**
- ✅ Safe defaults
- ✅ Explicit opt-in
- ❌ More verbose for common cases (but acceptable)

---

### Why `top_n` Instead of Returning All?

**Decision:** Return only the top N solutions by default.

**Rationale:**
- **User expectation:** Users typically want a few good solutions
- **Performance:** Can terminate early
- **Memory:** Limits memory usage

**Alternatives considered:**
1. **Return all solutions:** Memory intensive, slower
2. **Pagination:** More complex API

**Trade-offs:**
- ✅ Fast and memory-efficient
- ✅ Meets typical use case
- ❌ Requires `exhaustive=True` for all solutions

---

## Performance Decisions

### Why Not Parallelise?

**Decision:** Single-threaded implementation (for now).

**Rationale:**
- **Simplicity:** Easier to implement and debug
- **GIL limitations:** Python's GIL limits threading benefits
- **Fast enough:** Current performance is acceptable

**Future consideration:** Could parallelise left/right subexpression generation for 1.5-2x speedup.

**Alternatives considered:**
1. **Threading:** Limited by GIL
2. **Multiprocessing:** Overhead for data transfer
3. **Async:** Doesn't help for CPU-bound work

**Trade-offs:**
- ✅ Simple implementation
- ✅ No concurrency bugs
- ❌ Doesn't utilise multiple cores

---

### Why Not Cache Subexpressions?

**Decision:** Don't cache subexpressions across different targets.

**Rationale:**
- **Use case:** Targets are typically searched independently
- **Memory:** Cache would be large
- **Complexity:** More complex implementation

**Future consideration:** Could implement for batch processing mode.

**Trade-offs:**
- ✅ Simple implementation
- ✅ No memory overhead
- ❌ Recomputes subexpressions for each target

---

## Testing Decisions

### Why Regression Tests?

**Decision:** Focus on regression tests for known bugs.

**Rationale:**
- **Real-world bugs:** Tests actual issues found in use
- **Confidence:** Prevents regressions
- **Documentation:** Tests document expected behaviour

**Example:**
```python
def test_bug_373_subtraction_disabled(self):
    """Regression test for bug where subtraction was used despite being disabled"""
    solutions = find_solutions(target=373, allow_subtract=False, ...)
    for sol in solutions:
        self.assertNotIn('-', sol.expression)
```

**Alternatives considered:**
1. **Property-based testing:** More comprehensive but slower
2. **Unit tests only:** Misses integration issues

**Trade-offs:**
- ✅ Catches real bugs
- ✅ Fast to run
- ❌ Doesn't cover all edge cases

---

## Documentation Decisions

### Why Australian English?

**Decision:** Use Australian English spelling throughout documentation.

**Rationale:**
- **User preference:** Specified by user
- **Consistency:** Single spelling convention
- **Professionalism:** Consistent style

**Examples:**
- "optimisation" not "optimization"
- "behaviour" not "behavior"
- "analyse" not "analyze"

---

### Why Mermaid Diagrams?

**Decision:** Use Mermaid for flowcharts in documentation.

**Rationale:**
- **Text-based:** Version control friendly
- **Readable:** Renders nicely in Markdown viewers
- **Maintainable:** Easy to update
- **Standard:** Widely supported

**Alternatives considered:**
1. **Image files:** Hard to update, not version-control friendly
2. **ASCII art:** Less readable
3. **External tools:** Requires additional software

**Trade-offs:**
- ✅ Version control friendly
- ✅ Easy to maintain
- ❌ Requires Mermaid support in viewer

---

## Future Considerations

### Potential Improvements

1. **Parallel processing:** 1.5-2x speedup for large searches
2. **Adaptive `max_results_per_value`:** Better performance for easy targets
3. **Value range pruning:** 20-40% speedup with careful bounds
4. **Remainder operator:** For completeness (but minimal practical value)

### Decisions to Revisit

1. **k=4 threshold:** Could be tuned based on more benchmarks
2. **Default `max_results_per_value=3`:** Could be adaptive
3. **Canonical key algorithm:** Could be improved for better deduplication

---

## See Also

- [Algorithm Overview](algorithm-overview.md) - How the algorithms work
- [Optimisations](optimisations.md) - Optimisation strategies
- [Complexity Analysis](complexity-analysis.md) - Performance analysis
