
#!/usr/bin/python 
# 
# Created by Albert Au Yeung (2010) 
# 
# An implementation of matrix factorization 
# 
try: 
    import numpy 
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
        if error < 0.000001: 
            break 
        previous_e = e 
    print('step to converge: ', step) 
    print('newest approximation error: ', e) 
    print('last approximation error: ', previous_e) 
    return P, Q.T 
 
############################################################################### 
 
if __name__ == "__main__": 
    R = [ 
         [1000,20,10], 
         [100,0,1], 
         [0, 0, 1]
        ] 
 
    R = numpy.array(R) 
 
    N = len(R) 
    M = len(R[0]) 
    K = 3 
 
    P = numpy.random.rand(N,K) 
    Q = numpy.random.rand(M,K) 
 
    nP, nQ = matrix_factorization(R, P, Q, K) 
    nQ_T = numpy.transpose(nQ) 
    print(numpy.dot(nP, nQ_T)) 