import numpy
import csv
import pandas as pd
pd.set_option('display.max_columns', None)
import io

###############################################################################
class LatentFactorModel():

    def __init__(self):
        self.R = [
             [0, 0, 0, 0, 21.39, 0, 3.2, 0, 0, 0, 0, 1.22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.81, 0, 0, 0, 0, 0, 0, 0, 17.82, 0, 0, 0, 0, 0, 0, 0, 16.83, 9.76, 0, 0, 0, 6.65, 0, 3.27, 4.81, 1.34, 7.88], 
             [0, 35.2, 27.08, 0, 0, 21.37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6.56, 0, 0, 0, 0, 0, 9.79, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 9.35, 0, 0, 0, 6.29, 17.41, 6.34, 0, 0, 0, 0, 4.83, 4.61, 0, 0, 0, 0, 0, 0, 0, 0, 10.4, 0, 0, 15.56, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7.23, 17.96, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [8.71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.23, 0, 3.2, 2.02, 0, 0, 0.73, 0.95, 1.09, 2, 2.26, 0.37, 5.15, 0, 0, 33.03, 2.12, 0, 0, 3.53, 5.14, 0, 16.76, 1.12, 0, 1.27, 2.06, 0, 0, 0, 0, 1.31, 2.68, 1.93, 0, 1.37, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        # print(numpy.shape(numpy.array(self.R)))
        self.df = pd.DataFrame(self.R)

        self.R = numpy.array(self.R)

        N = len(self.R)
        M = len(self.R[0])
        self.K = 10

        self.P = numpy.random.rand(N,self.K)
        self.Q = numpy.random.rand(M,self.K)
        self.nP, self.nQ = self.matrix_factorization(self.R, self.P, self.Q, self.K)

        # stock info
        f = io.open('./stock_info.txt','r', encoding='utf8')
        self.codes = map(lambda x: x[0:4], f.readline().strip().split('\t'))
        self.names = f.readline().strip().split('\t')
        self.prices = f.readline().strip().split('\t')
        self.percentage_changes = f.readline().strip().split('\t')
        f.close()


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
    def update(self):
        self.matrix_factorization(self.R, self.P, self.Q, self.K, steps=2000000, alpha=0.0002, beta=0.02)

    def matrix_factorization(self, R, P, Q, K, steps=2000000, alpha=0.0002, beta=0.02):
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
    #         print(error)
            if error < 0.05:
                break
            previous_e = e
    #     print('step to converge: ', step)
    #     print('newest approximation error: ', e)
    #     print('last approximation error: ', previous_e)
        self.nP = P
        self.nQ = Q.T
        self.nQ_T = numpy.transpose(self.nQ)
        approximate_matrix = numpy.dot(self.nP, self.nQ_T)
        self.approximate_df = pd.DataFrame(approximate_matrix)
        # numpy.savetxt('approximate_matrix.csv', approximate_matrix, delimiter=',')
        return P, Q.T

    def predict(self, i):
        return(self.approximate_df[self.df==0].iloc[i].sort_values(ascending=False, na_position = 'last').to_frame().T.iloc[:,0:5])

    def update_user_by_code(self, user, code, share):
        index = self.codes.index(code)
        value = share * float(self.prices[index])
        self.R[user][index] += share
        if self.R[user][index] < 0.0:
            self.R[user][index] = 0

    ###############################################################################

if __name__ == "__main__":

    model = LatentFactorModel()
    prediction = model.predict(1) # return top 5 with index
    print(prediction.columns.values)
    model.update_user_by_code(0, '0700', 1000)
    model.update()
    new_prediction = model.predict(1)
    print(new_prediction.columns.values)
