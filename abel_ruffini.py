import multiprocessing
from scipy.optimize import root
import numpy as np
from tqdm import tqdm
import random
import time

def quintic_equation_solver(coeffs):
    a, b, c, d, e, f = coeffs
    def equation(x):
        return a * x**5 + b * x**4 + c * x**3 + d * x**2 + e * x + f
    sol = root(equation, 0)
    return sol.x[0]

def solve_with_concurrent_futures(equations):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(quintic_equation_solver, equations), total=len(equations)))
    return results

def solve_with_multiprocessing(equations):
    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap(quintic_equation_solver, equations), total=len(equations)))
    return results

def generate_random_coefficients(num_equations):
    equations = []
    for _ in range(num_equations):
        coeffs = tuple(random.randint(-10, 10) for _ in range(6))  # Generating 6 random coefficients for each equation
        equations.append(coeffs)
    return equations

if __name__ == "__main__":
    num_equations = 10
    equations = generate_random_coefficients(num_equations)

    print("Solving with concurrent.futures...")
    start_time = time.time()
    roots_cf = solve_with_concurrent_futures(equations)
    end_time = time.time()
    print(f"concurrent.futures took {end_time - start_time:.4f} seconds")

    print("\nSolving with multiprocessing...")
    start_time = time.time()
    roots_mp = solve_with_multiprocessing(equations)
    end_time = time.time()
    print(f"multiprocessing took {end_time - start_time:.4f} seconds")

    # Optionally print roots for verification
#    for i, root in enumerate(roots_cf, start=1):
#        print(f"Root of CF equation {i}: {root}")
#    for i, root in enumerate(roots_mp, start=1):
#        print(f"Root of MP equation {i}: {root}")
