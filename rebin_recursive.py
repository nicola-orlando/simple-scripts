#!/bin/env python                                                                                                                              

description = """                                                                                                                              
Recursively open all root files and histograms in a certain folder, look for a a set of name patterns and rebin the corresponding histograms. 
Need to define: name patterns, binning, input folder, output folder. Simple but functional :) .  To be eventually turned into a function. 
Need to edit the following 

input_folder --folder with your inputs
patterns_and_binnings --histogram names patterns and new binning
names_to_skip --patterns in histograms name that you want to skip
merge_last_bin_as_overflow --to add the last bin content and error to the second to last one, useful when want to move last bin in overflow

Based on 
https://root.cern.ch/doc/master/classTH1.html#aff6520fdae026334bf34fa1800946790
with trick 
https://root-forum.cern.ch/t/how-to-rebin-a-hisstogram-in-python/25482

Setup as 

setupATLAS
lsetup root

https://gitlab.cern.ch/orlando https://github.com/nicola-orlando nicolaorlandowork@gmail.com
October 2018
"""

import collections
import optparse
import os
import sys
import ROOT as R
from subprocess import call
import array
import math

R.gROOT.SetBatch(1)

input_folder='/nfs/at3/scratch2/orlando/fcnc/output/VLQAnalysisOutputs_prod_september_run_1'
output_folder = input_folder+'_rebinned_overflow'

call(["mkdir", output_folder])

#--Names and new binnings
patterns_and_binnings = [
    ('c1lep4jex2bex_hthad',array.array('d',[100,150,200,250,300,350,400,450,500,550,600,2000])),
    ('c1lep4jex3bex_hthad',array.array('d',[100,150,200,250,300,350,400,450,500,550,600,2000])),
    ('c1lep5jex3bex_hthad',array.array('d',[150,200,250,300,350,400,450,500,550,600,2000])),
    ('c1lep4jex2bex_met',array.array('d',[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000])),
    ('c1lep4jex3bex_met',array.array('d',[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000])),
    ('c1lep5jex3bex_met',array.array('d',[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000])),
    ('c1lep4jex2bex_leps_pt',array.array('d',[20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000])),
    ('c1lep4jex3bex_leps_pt',array.array('d',[20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000])),
    ('c1lep5jex3bex_leps_pt',array.array('d',[20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,1000]))
]

#--Patterns to skip
names_to_skip = ['zoom', '_phi', '_sig']

merge_last_bin_as_overflow = True

#--Main part of the script

for file_name in os.listdir(input_folder) : 
    #--Avoid strange things to happen, e.g. .sh or ~ files in the input file folder  
    if file_name.endswith(".root") :
        print 'opening file %s'%file_name
        #--Create an output root file per input file
        output_file_name=output_folder+'/'+file_name
        output_file=R.TFile.Open(output_file_name, 'recreate')
        output_file.cd()
        ##--
        input_root_file=input_folder+'/'+file_name
        file_to_rebin = R.TFile.Open(input_root_file)
        file_to_rebin.cd()
        key_list = R.gDirectory.GetListOfKeys()
            
        for key in key_list :
            obj_histo = key.ReadObj()
            histo_name = obj_histo.GetName()
            for pattern_and_binning in patterns_and_binnings :
                if pattern_and_binning[0] in histo_name : 
                    #--Evaluate if a certain histo has to be skipped
                    skip_histo=False
                    for to_be_skipped in names_to_skip :
                        if to_be_skipped in histo_name :
                            skip_histo=True
                    if skip_histo : 
                        continue
                    print histo_name
                    #--Writing the histo on file
                    output_file.cd()
                    new_histo= obj_histo.Clone().Rebin(len(pattern_and_binning[1])-1,"",pattern_and_binning[1])
                    ##--Adding last bin as overflow 
                    if merge_last_bin_as_overflow : 
                        merged_content = new_histo.GetBinContent( len(pattern_and_binning[1])-1 ) + new_histo.GetBinContent( len(pattern_and_binning[1])-2 ) 
                        merged_content_error = math.sqrt(
                            new_histo.GetBinError( len(pattern_and_binning[1])-1 ) * new_histo.GetBinError( len(pattern_and_binning[1])-1 ) + 
                            new_histo.GetBinError( len(pattern_and_binning[1])-2 ) * new_histo.GetBinError( len(pattern_and_binning[1])-2 ) 
                            )
                        new_histo.SetBinContent( len(pattern_and_binning[1])-2 , merged_content )
                        new_histo.SetBinError( len(pattern_and_binning[1])-2 , merged_content_error )
                    new_histo.SetDirectory(output_file)
                    new_histo.Write()
        
        output_file.Close()
        file_to_rebin.Close()
