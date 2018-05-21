#!/bin/env python

description = """
Given an input file it rescales each histogram based on the sample name and region to match the total yields in direct tagging vs TRF.
A few things to be changed by hand.
"""

usage = """
    %prog norm_factors.txt in.root

Rescaled histograms are over-written to in.root.

The rescaling factors are collected in norm_factors.txt.

Example:
$ %prog --generate-config > norm_factors.txt

# Edit norm_factors.txt
# If needed, print all the normalisation factors you are using
$ %prog --print-norm 

# then
$ %prog norm_factors.txt  

# to check the significance of the DT/TRF correction
$ %prog --print-sig

https://gitlab.cern.ch/orlando https://github.com/nicola-orlando nicolaorlandowork@gmail.com
"""

import collections
import optparse
import os
import sys
import ROOT as R
from subprocess import call

R.gROOT.SetBatch(1)

#--To be changed by hand 
samples_to_rescale=['ttbarlight','ttbarcc','ttbarbb','uHbW','uHcW']

#--To be changed by hand 
histograms_to_rescale=['c1lep4jex2bex_FcncDiscriminant','c1lep4jex3bex_FcncDiscriminant','c1lep4jex4bin_FcncDiscriminant','c1lep5jex2bex_FcncDiscriminant','c1lep5jex3bex_FcncDiscriminant','c1lep5jex4bin_FcncDiscriminant','c1lep6jin2bex_FcncDiscriminant','c1lep6jin3bex_FcncDiscriminant','c1lep6jin4bin_FcncDiscriminant']

#--To be changed by hand 
dt_nominal_folder = '/nfs/at3/scratch2/orlando/fcnc/output/VLQAnalysisOutputs_new_dis_feb_run_1'
trf_nominal_folder = '/nfs/at3/scratch2/orlando/fcnc/output/VLQAnalysisOutputs_new_dis_feb_trf_run_1'

#--To be changed by hand 
files_to_be_modified = '/nfs/at3/scratch2/orlando/fcnc/output/VLQAnalysisOutputs_new_dis_feb_run_1_trf_all/'
files_to_be_written = '/nfs/at3/scratch2/orlando/fcnc/output/VLQAnalysisOutputs_new_dis_feb_run_1_trf_all_rescaled_signals'

def main():

    parser = optparse.OptionParser(description=description, usage=usage)
    parser.add_option('-g', '--generate-config', action='store_true', help='print an example merge configuration')
    parser.add_option('-p', '--print-norm', action='store_true', help='print the norm factors')
    parser.add_option('-s', '--print-sig', action='store_true', help='print the significance of the correction')
    (opts, args) = parser.parse_args()
    
    if opts.generate_config:
        print derive_normalisation_factors(dt_nominal_folder,trf_nominal_folder)
        return
    elif opts.print_norm:
        if len(args)<1 : parser.error('provide an input file')
        print '\n Using normalisation factors %s'%(input_file_string)
        return
    elif opts.print_sig:
        print_significance(dt_nominal_folder,trf_nominal_folder)
        return

    input_file_string = args[0]
    input_folder = files_to_be_modified
    
    call(["mkdir", files_to_be_written])

    for file_name in os.listdir(input_folder) :
        #--Skipping non interesting files
        if not skip_files(file_name) :
            print 'Opening file %s '%(file_name)
            #--Output file
            output_file_name=files_to_be_written+'/'+file_name
            output_file = R.TFile.Open(output_file_name, 'recreate')
            output_file.cd()
            #--Avoid strange things to happen, e.g. .sh or ~ files in the input file folder 
            if file_name.endswith(".root") :
                input_root_file=input_folder+'/'+file_name
                file_to_rescale = R.TFile.Open(input_root_file)
                file_to_rescale.cd()
                key_list = R.gDirectory.GetListOfKeys()
                
                for key in key_list : 
                    obj_histo = key.ReadObj()
                    histo_name_prefix = obj_histo.GetName().split("_")[0]
                    #print 'Opening histogram %s '%obj_histo.GetName()
                    #print histo_name_prefix
                    normalisation_correction=grab_normalisation_correction(file_name,histo_name_prefix)
                    #print 'Grabbed normalisation correction %s'%(normalisation_correction)
                    obj_histo.Scale(float(normalisation_correction))
                    output_file.cd()
                    new_histo = obj_histo.Clone()
                    #new_histo.Smooth()
                    new_histo.SetDirectory(output_file)
                    new_histo.Write()
            
                output_file.Close()

#--Derive normalisation factors based
def derive_normalisation_factors(dt_nominal_folder,trf_nominal_folder):
        for sample in samples_to_rescale:
            dt_input_file_name = dt_nominal_folder+'/'+sample+'.root'
            trf_input_file_name = trf_nominal_folder+'/'+sample+'.root'
            dt_file = R.TFile.Open(dt_input_file_name)
            trf_file = R.TFile.Open(trf_input_file_name)
            for histogram in histograms_to_rescale: 
                h_dt = dt_file.Get(histogram)
                h_trf = trf_file.Get(histogram)
                histogram_prefix=histogram.split("_")[0]
                print '%s %s %f'%(sample,histogram_prefix,h_dt.Integral()/h_trf.Integral())
        print '\n'

#--Skip files you don't want to renormalise to DT, e.g. V+jets
def skip_files(input_file):
    skip_files_action=True
    for sample in samples_to_rescale : 
        if sample in input_file :
            skip_files_action=False
    return skip_files_action

#--Open text file with stored values of the non-closure correction factors 
def grab_normalisation_correction(input_file,histogram_prefix):
    #--Each line contains three strings separated by a space, the first is the sample, the second is the region, the last is the DT/TRF correction factor
    normalisation_factors_file=open('norm_factors.txt', 'r') 
    normalisation_factors_file_all=normalisation_factors_file.readlines() 
    #--Loop over the normalisation factors 
    for correction in normalisation_factors_file_all : 
        if correction.split(" ")[0] in input_file : 
            if correction.split(" ")[1] in histogram_prefix :
                return correction.split(" ")[2]
    #--Return 1. is the region is not found in the list, e.g. 4jin2bin / might want to fix this eventually .. 
    return 1.

#--Print the significance of the correction
def print_significance(dt_nominal_folder,trf_nominal_folder):
        for sample in samples_to_rescale:
            print '--'
            dt_input_file_name = dt_nominal_folder+'/'+sample+'.root'
            trf_input_file_name = trf_nominal_folder+'/'+sample+'.root'
            dt_file = R.TFile.Open(dt_input_file_name)
            trf_file = R.TFile.Open(trf_input_file_name)
            for histogram in histograms_to_rescale: 
                h_dt = dt_file.Get(histogram)
                h_trf = trf_file.Get(histogram)
                #--Only working for FCNC 
                bin_edge_low=h_dt.FindBin(0.0)
                bin_edge_high=h_dt.FindBin(1.0)
                error_dt=R.Double(0)
                h_dt.IntegralAndError(bin_edge_low,bin_edge_high,error_dt)
                significance = abs(h_dt.Integral(bin_edge_low,bin_edge_high)-h_trf.Integral(bin_edge_low,bin_edge_high))/error_dt
                histogram_prefix=histogram.split("_")[0]
                if significance < 2: 
                    print '%s %s %f %f'%(sample,histogram_prefix,h_dt.Integral(bin_edge_low,bin_edge_high)/h_trf.Integral(bin_edge_low,bin_edge_high),significance)
                else: 
                    print '---> Significant: %s %s %f %f'%(sample,histogram_prefix,h_dt.Integral(bin_edge_low,bin_edge_high)/h_trf.Integral(bin_edge_low,bin_edge_high),significance)
        print '\n'

if __name__=='__main__':
    main()
