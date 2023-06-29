import sys 
sys.dont_write_bytecode = True
import data_store as store

def getMetadata(id, *args):
    data = []
    for arg in args:
        data.append(store.getData(id, arg))

    return data