
#!/usr/bin/python 
# 
# Created by Albert Au Yeung (2010) 
# 
# An implementation of matrix factorization 
# 
try: 
    import numpy
    import csv
except: 
    print("This implementation requires the numpy module.") 
    exit(0) 
 
############################################################################### 
 
""" 
@INPUT: 
    R     : a matrix to be factorized, dimension N x M 
    P     : an initial matrix of dimension N x K 
    Q     : an initial matrix of dimension M x K 
    K     : the number of latent features 
    steps : the maximum number of steps to perform the optimisation 
    alpha : the learning rate 
    beta  : the regularization parameter 
@OUTPUT: 
    the final matrices P and Q 
""" 
def matrix_factorization(R, P, Q, K, steps=2000000, alpha=0.0002, beta=0.02): 
    Q = Q.T 
    previous_e = 0 
    for step in range(steps): 
        for i in range(len(R)): 
            for j in range(len(R[i])): 
                if R[i][j] > 0: 
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j]) 
                    for k in range(K): 
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k]) 
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j]) 
        eR = numpy.dot(P,Q) 
        e = 0 
        for i in range(len(R)): 
            for j in range(len(R[i])): 
                if R[i][j] > 0: 
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2) 
                    for k in range(K): 
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) ) 
        error = abs(previous_e - e)
        print(error)
        if error < 0.	01: 
            break 
        previous_e = e 
    print('step to converge: ', step) 
    print('newest approximation error: ', e) 
    print('last approximation error: ', previous_e) 
    return P, Q.T 
 
############################################################################### 
 
if __name__ == "__main__": 
    R = [
         [0,0,0,0,21.39,0,3.2,0,0,0,0,1.22,0,0,0,0,0,0,0,0,0,0,0,5.81,0,0,0,0,0,0,0,17.82,0,0,0,0,0,0,0,16.83,9.76,0,0,0,6.65,0,3.27,4.81,1.34,7.88],
         [0,35.2,27.08,0,0,21.37,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6.56,0,0,0,0,0,9.79,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,9.35,0,0,0,6.29,17.41,6.34,0,0,0,0,4.83,4.61,0,0,0,0,0,0,0,0,10.4,0,0,15.56,0,0,0,0,0,0,0,0,0,7.23,17.96,0,0,0,0,0,0,0,0,0,0,0],
         [8.71,0,0,0,0,0,0,0,0,0,1.23,0,3.2,2.02,0,0,0.73,0.95,1.09,2,2.26,0.37,5.15,0,0,33.03,2.12,0,0,3.53,5.14,0,16.76,1.12,0,1.27,2.06,0,0,0,0,1.31,2.68,1.93,0,1.37,0,0,0,0]
        ]
    # R = [ 
    #      [1000,20,10], 
    #      [100,0,1], 
    #      [0, 0, 1]
    #     ] 
 
    R = numpy.array(R) 
 
    N = len(R) 
    M = len(R[0]) 
    K = 10
 
    P = numpy.random.rand(N,K) 
    Q = numpy.random.rand(M,K) 
 
    nP, nQ = matrix_factorization(R, P, Q, K) 
    nQ_T = numpy.transpose(nQ)
    approximate_matrix = numpy.dot(nP, nQ_T)
    numpy.savetxt('approximate_matrix.csv', approximate_matrix, delimiter=',')

    print(approximate_matrix) 