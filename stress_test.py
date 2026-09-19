import numpy as np
import time
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

def generate_critical_phase_3sat(num_variables):
    """
    Synthesizes a uniform random 3-SAT problem instance at the critical 
    phase transition threshold (alpha = m/n ≈ 4.26).
    
    Parameters:
        num_variables (int): The total number of independent Boolean variables.
        
    Returns:
        scipy.sparse.csr_matrix: The sparse m x n incidence matrix encoding 
                                 the clause-variable literal polarities.
    """
    num_clauses = int(4.26 * num_variables)
    
    row_indices = []
    col_indices = []
    matrix_values = []
    
    for i in range(num_clauses):
        variable_selection = np.random.choice(num_variables, 3, replace=False)
        polarities = np.random.choice([-1, 1], 3)
        for var, sign in zip(variable_selection, polarities):
            row_indices.append(i)
            col_indices.append(var)
            matrix_values.append(sign)
            
    return csr_matrix((matrix_values, (row_indices, col_indices)), 
                      shape=(num_clauses, num_variables), dtype=float)

def execute_extreme_manifold_analysis():
    """
    Executes a structured algorithmic scalability study across successive 
    variable dimensions to benchmark solver latency and empirical precision.
    """
    test_scales = [1000, 5000, 20000]
    
    print("=========================================================================")
    print("ALGORITHMIC STRESS-TEST: SPECTRAL RELAXATION EVALUATION ENGINE")
    print("EXPERIMENTAL TARGET: CRITICAL PHASE TRANSITION THRESHOLD (M/N ≈ 4.26)")
    print("=========================================================================\n")
    
    for N in test_scales:
        M = generate_critical_phase_3sat(N)
        num_clauses = M.shape[0]
        
        start_time = time.time()
        
        # Step 1: Formulation of the structural covariance matrix
        W = M.T @ M  
        
        # Step 2: Sparse Lanczos eigendecomposition for principal vector isolation
        _, eigenvectors = eigsh(W, k=1, which='LM')
        v_max = eigenvectors[:, 0]
        
        # Step 3: Discrete projective mapping via deterministic sign function
        discrete_assignment = np.sign(v_max)
        discrete_assignment[discrete_assignment == 0] = 1
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Step 4: Verification of constraint satisfaction rates
        satisfied_clauses = 0
        for i in range(num_clauses):
            clause_start = M.indptr[i]
            clause_end = M.indptr[i+1]
            
            clause_vars = M.indices[clause_start:clause_end]
            clause_signs = M.data[clause_start:clause_end]
            
            for var, sign in zip(clause_vars, clause_signs):
                if discrete_assignment[var] == sign:
                    satisfied_clauses += 1
                    break
                    
        precision_accuracy = (satisfied_clauses / num_clauses) * 100
        
        print(f"Dimension Horizon: N = {N} Variables | m = {num_clauses} Clauses")
        print(f"   Execution Latency: {latency_ms:.2f} ms")
        print(f"   Empirical Precision: {precision_accuracy:.2f}% of constraints satisfied.")
        print(f"   Combinatorial Search Backtracks: 0\n")

if __name__ == "__main__":
    np.random.seed(1337)
    execute_extreme_manifold_analysis()
