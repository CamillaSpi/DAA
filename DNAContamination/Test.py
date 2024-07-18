from heap_priority_queue import HeapPriorityQueue
from DNAContamination import DNAContamination
"""This function reads DNA strings from the dataset target_batcha.fasta and 
    returns the indices of the k contaminants in the dataset with larger
    degree of contamination in s, assuming l as contamination threshold.
    The function returns a string containing these indices in increasing order
    separated by comma"""
def test(s,k,l):
    DNAC = DNAContamination(s, l)
    fp = open("target_batch.fasta", "r")
    index = fp.readline()[1:-1]
    c = fp.readline()[:-1]
    contaminants = {}
    while c !="" and index !="":
        contaminants[c] = int(index)
        DNAC.addContaminant(c)
        index = fp.readline()[1:-1]
        c = fp.readline()[:-1]
    fp.close()
    tup = DNAC.getContaminants(k)
    q = HeapPriorityQueue()
    for i in tup:
        q.add(contaminants.get(i),i)
    ret = ""
    while not q.is_empty():
        ret += q.remove_min()[0].__str__()
        if not q.is_empty():
            ret += ", "
    return ret





