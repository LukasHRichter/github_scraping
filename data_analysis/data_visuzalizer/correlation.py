import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import data_analyst.analyse as a
import sys, codecs
w=codecs.getwriter("utf-8")(sys.stdout.buffer)

mpl.rcParams.update({'font.size': 7})

df = a.getCorr()
corr = df.corr('spearman', numeric_only=True)
corr.style.background_gradient(cmap='coolwarm').set_properties(**{'font-size': '12pt'})
plt.matshow(corr)
plt.xticks(range(len(corr.columns)), corr.columns, rotation=70)
plt.yticks(range(len(corr.columns)), corr.columns)
for (i, j), z in np.ndenumerate(corr):
    plt.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

#plt.savefig(fname='corr.pdf', backend='pgf')
plt.show()
