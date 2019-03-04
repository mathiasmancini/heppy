import os, sys
import ROOT


# output file
outfile = ROOT.TFile("outputhistos.root")
outfile.cd() # necessary to save file
histojetdeltaphi = ROOT.TH1D("histojetdeltaphi","histojetdeltaphi",100,-3.1415,3.1415)

#creer chain object
ch = ROOT.TChain("events","events") # de naam van de tree is belangrijk! Dat is hoe root die in the file vindt!

# voeg de files toe (meerdere .root files!) met een abs path to file
test_directory = "/user/mmancini/FCCee/heppy/worktest/small_samples/test2/ee_ttbar/MySimpleTreeProducer.MySimpleTreeProducer_1/"
ch.Add(test_directory+"tree.root")

# print wat er in die tree zit
ch.Print()

# direct iets plotten:
ch.Draw("lep2_pt")

# of nog interessanter: code schrijven die ingewikkelder dingen doet, per event
nevents=ch.GetEntries()
if nevents==0 :
    print "bummer, the tree is empty. Probably the wrong tree name or wrong file name?"

print "this tree has ",nevents," events"

ii = 0
for iev in ch: # dit is de event loop
    if ii % 100 ==0 :
        print ii, "/", nevents
        ii+=1

    # nu kan je over alle dingen itereren:
    if iev.misenergy_pt > 50 :
        # een extra variabele, de hoek tussen de jets?
        newvariable = iev.jet1_phi - iev.jet2_phi
        # en die kan je bijvoorbeeld ook in een histogram stoppen
        histojetdeltaphi.Fill(newvariable)



# buiten de event loop kan je plots maken
canvas = ROOT.TCanvas()
canvas.cd()
histojetdeltaphi.Draw()

outfile.Write() # or save/close ..
