import pygtrie
  
# fetch dataset 
#mushroom = fetch_ucirepo(id=73)
#X = mushroom.data.features

def row_to_transaction(row):
    transaction = set()
    for col, value in row.items():
        item = f"{col}={value}"
        transaction.add(item)
    return transaction

#transactions = [row_to_transaction(row) for _, row in X.iterrows()]
transactions = [{"Atenas", "Oslo", "Roma", "Viena"}, {"Oslo"}, 
                {"Oslo", "Roma", "Viena"}, {"Oslo"}, {"Londres", "Madrid"}, 
                {"Londres", "Madrid", "Oslo"}]
transactions_supp = [(t, 1) for t in transactions]

trie = pygtrie.Trie()

