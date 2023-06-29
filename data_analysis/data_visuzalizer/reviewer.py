import matplotlib.pyplot as plt
import data_analyst.analyse as a
import matplotlib as mpl
import sys, codecs
w=codecs.getwriter("utf-8")(sys.stdout.buffer)

mpl.rcParams.update({'font.size': 7})

groups = a.getReviewer()
fig, ax = plt.subplots()
plt.boxplot(groups)
ax.set_xticklabels(['0 - 0.5', '0.5 - 1' , '1 - 1.5', '1.5 - 2.0', '2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5'])
ax.set_yticklabels(['0', '5' , '10', '15', '20', '25', '30', '35'])
ax.set_xlabel('Durchschnittliche Anzahl der Reviewer')
ax.set_ylabel('Durchschnittliche Zeit zum Lösen von Security-Pull Requests in Tagen')
plt.xticks(rotation='horizontal')
#plt.savefig(fname='reviewer.pdf', backend='pgf')
plt.show()

