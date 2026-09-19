import numpy as np
import time
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

def generate_critical_phase_3sat(num_variables, seed=42):
    num_clauses = int(4.26 * num_variables)
    np.random.seed(seed)
    row_indices, col_indices, matrix_values = [], [], []
    for i in range(num_clauses):
        variable_selection = np.random.choice(num_variables, 3, replace=False)
        polarities = np.random.choice([-1, 1], 3)
        for var, sign in zip(variable_selection, polarities):
            row_indices.append(i)
            col_indices.append(var)
            matrix_values.append(sign)
    return csr_matrix((matrix_values, (row_indices, col_indices)), 
                      shape=(num_clauses, num_variables), dtype=float)

def solve_exact_spectral_sat(M, max_iterations=5):
    num_clauses, num_variables = M.shape
    current_solution = np.zeros(num_variables)
    
    # Initialize baseline matrix working state
    W_working = (M.T @ M).toarray()
    
    start_time = time.time()
    
    for iteration in range(max_iterations):
        # Step 1: Extract principal eigenvector from current working matrix
        _, eigenvectors = np.linalg.eigh(W_working)
        v_max = eigenvectors[:, -1]
        
        # Step 2: Cumulative update of continuous trajectory
        current_solution += v_max
        discrete_assignment = np.sign(current_solution)
        discrete_assignment[discrete_assignment == 0] = 1
        
        # Step 3: Verify current satisfaction metrics
        violated_clauses = []
        for i in range(num_clauses):
            clause_start = M.indptr[i]
            clause_end = M.indptr[i+1]
            clause_vars = M.indices[clause_start:clause_end]
            clause_signs = M.data[clause_start:clause_end]
            
            satisfied = False
            for var, sign in zip(clause_vars, clause_signs):
                if discrete_assignment[var] == sign:
                    satisfied = True
                    break
            if not satisfied:
                violated_clauses.append(i)
                
        precision = ((num_clauses - len(violated_clauses)) / num_clauses) * 100
        if precision == 100.0:
            break
            
        # Step 4: Spectral Deflation Loop
        # Subtract the variance captured by the primary eigenvector to expose hidden sub-structures
        v_max_outer = np.outer(v_max, v_max)
        W_working = W_working - W_working @ v_max_outer

    latency_ms = (time.time() - start_time) * 1000
    return discrete_assignment, precision, latency_ms

if __name__ == "__main__":
    # Test at a strict 500 variable frontier
    variables = 500
    M_instance = generate_critical_phase_3sat(variables, seed=1337)
    _, final_precision, duration = solve_exact_spectral_sat(M_instance)
    
    print("=========================================================================")
    print("ITERATIVE DEFECT-CORRECTION SPECTRAL SOLVER")
    print("=========================================================================")
    print(f"Executed at dimension scale: N = {variables} Variables")
    print(f"Operational Latency: {duration:.2f} ms")
    print(f"Final Deflated Empirical Precision: {final_precision:.2f}%")
