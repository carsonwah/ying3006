This is a HTML prototype for our portfolio recommendation news assistant(PRENA)
The prototype can be found at:

This functionality, once embedded in stock brokeage account, takes advantage of the meta data of the firm to save clients' time in extracting portfolio-relevant news feed

Mechanism:
we take the current portfolio of a client as input
and give news of a list of recommendated stocks(up to 5)
by applying latent factor model on the aggregate portfolio data of all clients.

For a particular client, this model can fill the unpurchased stocks with a score, based on the entire data set, with the objective to factorize the matrix with minimized error. This operation, aims to highlight stocks that are held by investors who have similar portfolio with the client, but not the client himself.

This model is first implemented in commendation systems of Netflix and Amazon and resulted in satisfactory accuracy.

 



