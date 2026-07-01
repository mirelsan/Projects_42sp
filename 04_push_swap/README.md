*This project has been created as part of the 42 curriculum by mirelsan and adedias-*

# Push Swap

## Description
Push Swap is a 42 project that challenges students to sort a list of integers using two stacks and a restricted set of operations. The program must produce the smallest possible sequence of instructions to transform the input into a sorted order.

The main goal of this project is to apply algorithmic thinking, understand complexity, and build an efficient sorting strategy for different input sizes. The implementation includes several approaches, such as simple sorting, chunk-based sorting, radix sort, and an adaptive mode that selects the most suitable strategy.

## Contributors
- adedias-: implemented the movement operations, the main sorting algorithm, the radix algorithm, and the adaptive algorithm.
- mirelsan: implemented parsing, the benchmark output, the chunk-based sorting algorithm, validation, options handling, disorder detection, and the main program flow.
- Both collaborators debugged issues together, solved problems collaboratively, and tested the code as a team.

## Instructions
### Compilation
From the project directory, run:

```bash
cd 04_push_swap
make
```

This will generate the executable named push_swap.

### Execution
Run the program with a set of integers:

```bash
./push_swap 2 1 3 6 5 8
```

The program prints a sequence of operations that sorts the stack.

### Available options
- --simple: uses the simple sorting approach
- --medium: uses the chunk-based approach
- --complex: uses the radix approach
- --adaptive: uses the adaptive strategy (default)
- --bench: prints a benchmark summary

### Cleaning
```bash
make clean
make fclean
```

## Resources
- 42 Push Swap subject and project guidelines
- Classical references on stack sorting and radix sort
- Tutorials and explanations about chunk-based sorting strategies
- AI usage: AI tools were used to help understand algorithm choices, debug edge cases, review code structure, and improve the clarity of the implementation. The core logic, algorithms, and final decisions were developed and validated by the team.

## Project Diagram
A simple HTML diagram is available for visual reference:
- Open [04_push_swap/diagram.html](04_push_swap/diagram.html) in a browser to see the project flow.

## Notes
The program expects valid integer input without duplicates and handles invalid input by displaying an error message.
