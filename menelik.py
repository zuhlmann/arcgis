import numpy as np
import pandas as pd
import copy
import math

def mru_scam(start, start_incr, ratchet, ratchet_add, num_sales):
    price_row, incr_row, n_row=[],[],[]
    for n in range(num_sales):
        if n==0:
            last_price=copy.copy(start)
        incr = start_incr + math.floor(last_price/ratchet) * ratchet_add
        price = last_price + incr
        last_price = copy.copy(price)
        price_row.append(price)
        incr_row.append(incr)
        n_row.append(n+1)
        cols = ['Transaction', 'Increment', 'Price']
    df=pd.DataFrame(np.column_stack([n_row, incr_row, price_row]),
                    columns=cols)
    df.to_csv(r'C:\Users\UhlmannZachary\Documents\staging\menelik_scam.csv')
    return(df)
s=0
i=1
r=10
rv=2
n=100

df = mru_scam(s,i,r,rv,n)
df
print('whatever')