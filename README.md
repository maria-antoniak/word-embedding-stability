*Warning: This code has not been formatted for public use. Please contact me with questions!*

Code for the paper [Evaluating the Stability of Embedding-based Word Similarities](https://maria-antoniak.github.io/publications) (Antoniak & Mimno, 2018).

# Scripts

`run.py` -- the main file that loops through all the corpora, models, etc. and submits scripts as condor jobs

The above script submits the following to condor:  
`process.sh` -- prepares the corpora for training  
`train.sh` -- trains the models  
`evaluate.sh` -- gets the most similar words  

# Output Structure

`/out/corpus/document_size/corpus_size/{evaluation|models|data|plots}`

`/out/corpus/document_size/corpus_size/results/{ppmi|word2vec|glove}/{fixed|shuffled}bootstrap}`  
`/out/corpus/document_size/corpus_size/models/{ppmi|word2vec|glove}/{fixed|shuffled}bootstrap}`  
`/out/corpus/document_size/corpus_size/data/{fixed|shuffled}bootstrap}`  
`/out/corpus/document_size/corpus_size/plots/{ppmi|word2vec|glove}`  
