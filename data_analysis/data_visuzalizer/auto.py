import matplotlib.pyplot as plt
import matplotlib as mpl
import sys, codecs
import data_analyst.analyse as a
w=codecs.getwriter("utf-8")(sys.stdout.buffer)

mpl.rcParams.update({'font.size': 7})

df = a.getAutomation()
ax = df.plot.bar(xlabel = 'Nutzt Automatisierung', ylabel='Durchschnittliche Zeit zum Lösen von Pull Requests in Tagen')
ax.set_yticklabels(['0', '5' , '10', '15', '20', '25'])
ax.set_xticklabels(['Nein', 'Ja'])
ax.legend(['Normale Pull Requests', 'Security Pull Requests'])
plt.xticks(rotation='horizontal')
#plt.savefig(fname='autoPull.pdf', backend='pgf')
plt.show()
