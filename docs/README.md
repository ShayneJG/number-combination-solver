# Number Combination Solver Documentation

Welcome to the comprehensive documentation for the Number Combination Solver, a tool designed for the game Beltmatic that finds mathematical expressions to reach target numbers.

## Quick Links

- [Algorithm Overview](algorithm-overview.md) - High-level explanation of how the solver works
- [Complexity Analysis](complexity-analysis.md) - Time and space complexity deep dive
- [Meet-in-the-Middle Algorithm](meet-in-middle.md) - Core algorithm details
- [Optimisations](optimisations.md) - Performance optimisation strategies
- [API Reference](api-reference.md) - Function and class documentation
- [Usage Examples](usage-examples.md) - Practical usage examples
- [Design Decisions](design-decisions.md) - Architecture and rationale

## Flowcharts

- [Overall Flow](flowcharts/overall-flow.md) - Main algorithm flow
- [Meet-in-the-Middle Flow](flowcharts/meet-in-middle-flow.md) - Detailed meet-in-middle process
- [Direct Search Flow](flowcharts/direct-search-flow.md) - Brute force search process
- [Expression Evaluation](flowcharts/expression-evaluation.md) - How expressions are evaluated

## What is This Solver?

The Number Combination Solver finds mathematical expressions that equal a target number using:
- Available integers from 1 to `max_int`
- Configurable operators: `+`, `-`, `*`, `/`, `**`
- Up to `max_numbers` integers in the expression

**Example:**
```python
Target: 2285
Available: 1-25
Result: (5 * 5 * 7 * 13) = 2285
```

## Key Features

- **Hybrid Algorithm**: Uses direct search for small expressions (≤4 numbers) and meet-in-the-middle for larger ones
- **Deduplication**: Canonical form ensures mathematically equivalent expressions aren't duplicated
- **Operator Precedence**: Correctly handles `**` > `*`, `/` > `+`, `-`
- **Optimised Search**: Early termination, limited results per value, integer-only arithmetic
- **Flexible**: Configurable operators, exhaustive vs fast modes

## Getting Started

For quick usage examples, see [Usage Examples](usage-examples.md).

For understanding how it works, start with [Algorithm Overview](algorithm-overview.md).

For performance considerations, see [Complexity Analysis](complexity-analysis.md).

## Project Structure

```
number-combination-solver/
├── number_combinations.py    # Core solver implementation
├── ncs.py                     # Command-line interface
├── streamlit_app.py           # Web interface
├── tests/                     # Test suite
│   └── regression_tests.py
└── docs/                      # This documentation
    ├── README.md
    ├── algorithm-overview.md
    ├── complexity-analysis.md
    ├── meet-in-middle.md
    ├── optimisations.md
    ├── api-reference.md
    ├── usage-examples.md
    ├── design-decisions.md
    └── flowcharts/
        ├── overall-flow.md
        ├── meet-in-middle-flow.md
        ├── direct-search-flow.md
        └── expression-evaluation.md
```

## Contributing

When contributing to this project:
- Follow Australian English spelling conventions
- Add tests for new features
- Update relevant documentation
- Ensure complexity analysis is updated if algorithms change

## License

See the LICENSE file in the project root.
