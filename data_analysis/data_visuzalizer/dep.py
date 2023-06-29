import matplotlib.pyplot as plt
import matplotlib as mpl
import data_analyst.analyse as a
import sys, codecs
w=codecs.getwriter("utf-8")(sys.stdout.buffer)

mpl.rcParams.update({'font.size': 7})

df = a.getDep()
ax = df.plot.bar(xlabel = 'Nutzt Dependabot', ylabel='Durchschnittliche Zeit zum Lösen von Pull Requests in Tagen')
ax.set_yticklabels(['0', '5' , '10', '15', '20', '25', '30', '35', '40'])
ax.set_xticklabels(['Nein', 'Ja'])
ax.legend(['Normale Pull Requests', 'Security Pull Requests'])
plt.xticks(rotation='horizontal')
#plt.savefig(fname='dep1.pdf', backend='pgf')
plt.show()
