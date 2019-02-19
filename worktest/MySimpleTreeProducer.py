'''Test analyzer creating a simple root tree.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *

from ROOT import TFile

class MySimpleTreeProducer(Analyzer):
    '''Test analyzer creating a simple root tree.
    
    Example::
    
        tree = cfg.Analyzer(
          MySimpleTreeProducer,
          tree_name = 'events',
          tree_title = 'A simple test tree'
        )
    
    The TTree is written to the file C{simple_tree.root} in the analyzer directory.
    
    @param tree_name: Name of the tree (Key in the output root file).
    @param tree_title: Title of the tree.
    '''
    def beginLoop(self, setup):
        super(MySimpleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
            
        self.tree = Tree( 'events', '')
        bookParticle(self.tree, 'jet1')
        bookParticle(self.tree, 'jet2')
        bookLepton(self.tree, 'lep1', pflow=True)
        bookLepton(self.tree, 'lep2', pflow=True)
        
    def process(self, event):
        '''Process the event.
        
        The input data must contain a variable called "var1",
        which is the case of the L{test tree<heppy.utils.debug_tree>}. 
        
        The event must contain:
         - var_random, which is the case if the L{RandomAnalyzer<heppy.analyzers.examples.simple.RandomAnalyzer.RandomAnalyzer>}
         has processed the event. 
         
        '''
        
        self.tree.reset()
            #        muons = getattr(event, self.cfg_ana.muons)
            #        electrons = getattr(event, self.cfg_ana.electrons)
        leptons = getattr(event, self.cfg_ana.leptons)
        jets = getattr(event, self.cfg_ana.jets)
        
#        if len(leptons)<=2:
#            return

        for ijet, jet in enumerate(jets):
            if ijet==2:
                break
            fillParticle(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

        for imu, muon in enumerate(leptons):
            if imu==2:
                break
            fillLepton(self.tree, 'lep{imu}'.format(imu=imu+1), muon)

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
