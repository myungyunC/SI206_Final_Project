import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

a = pd.read_csv("keywords.csv")
#a = sns.load_dataset("flights")
sns.relplot(x="keyword",y="occurance",data=a)
plt.show()