from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple_mod import *

from ROOT import TFile

class TreeTTSemilep(Analyzer):

    def beginLoop(self, setup):
        super(TreeTTSemilep, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName, 'tree.root']), 'recreate')
        self.tree = Tree('events', '')

        var(self.tree, 'ev_number', int)

        bookMyParticle(self.tree, 'mc_lepton')
        bookMyParticle(self.tree, 'mc_neutrino')
        bookMyParticle(self.tree, 'mc_w_lep')

        bookMyLepton(self.tree, 'lep1')

        bookMyJet(self.tree, 'jet1')
        bookMyJet(self.tree, 'jet2')
        bookMyJet(self.tree, 'jet3')
        bookMyJet(self.tree, 'jet4')

        bookMCbQuark(self.tree, 'mc_bquark1')
        bookMCbQuark(self.tree, 'mc_bquark2')

        bookJetsInvariantMasses(self.tree)
        bookJetsShape(self.tree)
        bookChargedTracks(self.tree)
        bookMissingEnergy(self.tree)

        bookTopConstrainer(self.tree)


    def process(self, event):
        self.tree.reset()

        fill(self.tree, 'ev_number', event.iEv)

        if hasattr(event, 'mc_lepton'):
            mc_lepton = getattr(event, self.cfg_ana.mc_lepton)
            fillMyParticle(self.tree, 'mc_lepton', mc_lepton)
        if hasattr(event, 'mc_neutrino'):
            mc_neutrino = getattr(event, self.cfg_ana.mc_neutrino)
            fillMyParticle(self.tree, 'mc_neutrino', mc_neutrino)
        if hasattr(event, 'mc_w_lep'):
            mc_w_lep = getattr(event, "mc_w_lep")
            fillMyParticle(self.tree, 'mc_w_lep', mc_w_lep)

        leptons = getattr(event, self.cfg_ana.leptons)
        fillMyLepton(self.tree, 'lep1', leptons[0])

        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == 4:
                break
            fillMyJet(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

        if hasattr(event, self.cfg_ana.mc_b_quarks):
            mc_b_quarks = getattr(event, self.cfg_ana.mc_b_quarks)
            for iquark, quark in enumerate(mc_b_quarks):
                if iquark == 2:
                    break
                fillMCbQuark(self.tree, 'mc_bquark{iquark}'.format(iquark=iquark+1), quark)

        fillJetsInvariantMasses(self.tree, event)
        fillMissingEnergy(self.tree, event)
        fillJetsShape(self.tree, event)
        fillChargedTracks(self.tree, event)
        fillTopConstrainer(self.tree, event)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
