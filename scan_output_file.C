//Get all histograms from a root file and plot them to quickly inspect the content, simple and dirty 
//nicolaorlandowork@gmail.com https://gitlab.cern.ch/orlando https://github.com/nicola-orlando

/*
First argument enable a flat rebin
Second argument to cd in a folder contained in the root file 
Third argument the full path and filename
Last, plot format
*/

//ROOT
#include "TFile.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TH2.h"
#include "TH2F.h"
#include "TH1.h"
#include "TH1F.h"
#include "TLegend.h"
#include "TKey.h"
//C++
#include <iostream>

void scan_output_file(bool rebin = true, std::string sdirectory="", std::string sFilename="/eos/atlas/user/o/orlando/VLQAnalysisOutputs_test_VLQ_bare_2017_11_11_2218_merged_FCNC_60OP/Wjets22beauty", std::string format="png")
{
  char Filename[1000];  sprintf(Filename,"%s.root",sFilename.c_str());
  TFile *f_Filename = new TFile(Filename);

  std::cout<<"\n --> Opening this file  "<< sFilename <<std::endl;
  
  char directory[1000]; sprintf(directory,"%s",sdirectory.c_str());
  f_Filename->cd(directory);

  gDirectory->ls() ;

  TIter next(gDirectory->GetListOfKeys());            
  
  TKey *m_key=0;    
  TObject *m_iobj=0;
  TCanvas *cnv = new TCanvas();
  char nameplot[1000];

  const int col_sig = kSpring+10;
  //Fancy color setting for 2D plots
  const int Number = 3;
  Double_t Red[Number]    = { 0.50, 0.00, 0.00 };
  Double_t Green[Number]  = { 0.50, 0.80, 0.00 };
  Double_t Blue[Number]   = { 0.50, 0.80, 1.00 };
  Double_t Length[Number] = { 0.00, 0.50, 1.00 };
  Int_t nb=50;
  TColor::CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);
  
  while( ( m_key = (TKey*)next() ) ) 
    {
      m_iobj     = m_key->ReadObj();	  

      if(format=="pdf")sprintf(nameplot,"%s.pdf", m_iobj->GetName() );
      if(format=="png")sprintf(nameplot,"%s.png", m_iobj->GetName() );
      
      if( m_iobj->InheritsFrom(TH2::Class()) ) 
	{ 
	  cnv->SetRightMargin(0.12);
	  if(rebin)((TH2*)m_iobj)->RebinX(15);
	  if(rebin)((TH2*)m_iobj)->RebinY(15);
       	  ((TH2*)m_iobj)->Draw("colz");
       	  cnv->SaveAs(nameplot);
	}
      
      else if( m_iobj->InheritsFrom(TH1::Class()) ) 
	{ 
	  ((TH1F*)m_iobj)->SetFillColor(col_sig);
	  ((TH1F*)m_iobj)->SetLineColor(col_sig);
	  ((TH1F*)m_iobj)->SetFillStyle(3001);
	  ((TH1F*)m_iobj)->GetYaxis()->SetTitleOffset(1.4);
	  ((TH1F*)m_iobj)->GetYaxis()->SetTitle("Entries");
	  if(rebin)((TH1F*)m_iobj)->Rebin(2);

	  ((TH1F*)m_iobj)->Draw("hist");
	  
	  TLegend * leg = new TLegend(0.20,0.89,0.75,0.95);
	  leg -> SetNColumns(1);
	  char leg_entry[1000]; sprintf(leg_entry,"%s",m_iobj->GetName());
	  leg->AddEntry(((TH1F*)m_iobj),leg_entry,"f");
	  leg->SetShadowColor(1);
	  leg->SetBorderSize(0);
	  leg->SetFillStyle(0);
	  leg->SetTextSize(0.035);
	  leg->Draw();

	  cnv->SaveAs(nameplot);
	}
      else std::cout<<"Format not recognized nor a TH2, neither a TH1"<<std::endl;
    } 
  
  return;
  							      
}	
