import numpy
import csv
import pandas as pd
pd.set_option('display.max_columns', None)
import io

###############################################################################
class LatentFactorModel():

    def __init__(self):
        self.R = [
            [0,0,0,0,21390,0,3200,0,0,0,0,1220,0,0,0,0,0,0,0,0,0,0,0,5810,0,0,0,0,0,0,0,17820,0,0,0,0,0,0,0,16830,9760,0,0,0,6650,0,3270,4810,1340,7880],
            [0,35200,27080,0,0,21370,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6560,0,0,0,0,0,9790,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,9350,0,0,0,6290,17410,6340,0,0,0,0,4830,4610,0,0,0,0,0,0,0,0,10400,0,0,15560,0,0,0,0,0,0,0,0,0,7230,17960,0,0,0,0,0,0,0,0,0,0,0],
            [8710,0,0,0,0,0,0,0,0,0,1230,0,3200,2020,0,0,730,950,1090,2000,2260,370,5150,0,0,33030,2120,0,0,3530,5140,0,16760,1120,0,1270,2060,0,0,0,0,1310,2680,1930,0,1370,0,0,0,0],
            # [0, 0, 33000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 0, 0, 0, 17000, 0, 0, 0, 0, 0, 0, 17000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            # [0, 0, 33000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 0, 0, 0, 17000, 0, 0, 0, 0, 0, 0, 17000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19000, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            [8710,0,0,0,0,0,0,0,0,0,0,0,3200,2020,0,0,0,0,1090,2000,2260,0,0,0,0,0,2120,0,0,0,5140,0,16760,0,0,0,0,0,0,0,0,0,0,1930,0,0,0,0,0,0],
            [8710,0,0,0,0,0,0,0,0,0,0,0,3200,2020,0,0,0,0,1090,2000,2260,0,0,0,0,0,2120,0,0,0,5140,0,16760,0,0,0,0,0,0,0,0,0,0,1930,0,0,0,0,0,0]
            ]
        # print(numpy.shape(numpy.array(self.R)))
        self.df = pd.DataFrame(self.R)

        self.R = numpy.array(self.R, dtype=numpy.float64)

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
        R = numpy.divide(R, R.sum(axis=1)[:,None], where=R.sum(axis=1)[:,None]>=0.01)
        new_R = []
        for row in numpy.copy(R):
            if sum(row) <= 0.01:
                new_R.append(row)
            else:
                row /= sum(row)
                new_R.append(row)
        R = new_R
        # R = numpy.copy(R)
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
            if error < 0.0005:
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
        print 'update user', user
        print 'share:', share
        print 'price:', float(self.prices[index])
        print 'new value is: ', value
        self.R[user][index] += value
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
