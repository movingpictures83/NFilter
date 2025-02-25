#!/usr/bin/python2

import sys
import os
import datetime

t0 = datetime.datetime.now()
################################################################################
def compress(seq):
    cps_seq = seq[0]
    pos_ls=[]
    len_ls = []
    r=0
    ref_s = seq[0]
    i=0
    for s in seq:
        if not ref_s == s:
            if r>1:
                len_ls.append(str(r))
                pos_ls.append(str(i)) 
            cps_seq = cps_seq + s
            r=1
            ref_s = s
            i+=1
        else:
            r+=1
    if r>1:
        len_ls.append(str(r))
        pos_ls.append(str(i)) 
    return cps_seq,pos_ls,len_ls            
################################################################################

import PyPluMA
import PyIO
class NFilterPlugin:
 def input(self, inputfile):
     self.parameters = PyIO.readParameters(inputfile)
 def run(self):
     pass
 def output(self, outputfile):
  MinNonN = int(self.parameters["MinNonN"])
  MaxN = int(self.parameters["MaxN"])
  filetype = self.parameters["filetype"]
  inseq_filename = PyPluMA.prefix()+"/"+self.parameters["inseq_filename"]
  outseq_prefix = outputfile

  ################################################################################
  if (filetype == "fa"):
    start_char = ">"
  elif (filetype == "fq"):
    start_char = "@"    

  inseq=open(inseq_filename,'r')
  outseq=open(outseq_prefix+'cps','w')
  idx = open(outseq_prefix+'idx','w')

  line = inseq.readline()
  readname = line[1:-1]
  if (line[0] != start_char):
    print(line)
    print("Err:  invalid file format: " + inseq_filename)
    exit(1)
  line_type = 1
  while(True):
    line = inseq.readline()
    if (line == ""):
        break
    if (line_type == 0):
        if (line[0] != start_char):
            print(line)
            print("Err:  invalid file format: " + inseq_filename)
            exit(1)
        cps_seq, pos_ls, len_ls = compress(seq)
        NN = cps_seq.count('N')
        if len(cps_seq)-NN>=MinNonN and NN<=MaxN:
            outseq.write(">"+readname+'\n' + cps_seq+'\n')
            idx.write(readname + "\t" + ','.join(pos_ls) + '\t' + ','.join(len_ls) + '\n')
        readname = line[1:-1]
        
    elif (line_type == 1):
        seq= line.strip().upper()
        if (filetype == "fq"):
            line = inseq.readline()  # skip quality lines
            line = inseq.readline()
    line_type = 1 - line_type

  print(str(datetime.datetime.now()-t0))
  cps_seq, pos_ls, len_ls = compress(seq)  
  NN = cps_seq.count('N')
  if len(cps_seq)-NN>=MinNonN and NN<=MaxN:
    outseq.write(">"+readname+'\n' + cps_seq+'\n')
    idx.write(readname + "\t" + ','.join(pos_ls) + '\t' + ','.join(len_ls) + '\n')

  inseq.close()
  outseq.close()
  idx.close()
  print("finsish genome")

  ################################################################################

