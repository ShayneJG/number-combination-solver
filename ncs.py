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
            exclude=[10,],
            max_numbers=6,
            top_n=5,
            exhaustive=False,
            progress_callback=update_progress,
    )

    print(sols)
    for solution in sols:
        print(f"{solution.expression} = {solution.result}")
