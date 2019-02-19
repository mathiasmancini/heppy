'''Example configuration file for an ee->ZH->mumubb analysis in heppy, with the FCC-ee
    
    While studying this file, open it in ipython as well as in your editor to
    get more information:
    
    ipython
    from analysis_ee_ZH_cfg import *
    '''

import os
import copy
import heppy.framework.config as cfg
import logging

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)


# global logging level for the heppy framework.
# in addition, all the analyzers declared below have their own logger,
# an each of them can be set to a different logging level.
logging.basicConfig(level=logging.WARNING)

# setting the random seed for reproducible results
import heppy.statistics.rrandom as random
# do not forget to comment out the following line if you want to produce and combine
# several samples of events 
random.seed(0xdeadbeef)

# loading the FCC event data model library to decode
# the format of the events in the input file
# help(Events) for more information 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

# setting the event printout
# help(Event) for more information
from heppy.framework.event import Event
# comment the following line to see all the collections stored in the event 
# if collection is listed then print loop.event.papasevent will include the collections
Event.print_patterns=['zeds*', 'higgs*', 'rec_particles', 'gen_particles_stable', 'recoil*', 'collections']

# definition of the collider
# help(Collider) for more information
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 360.

# definition of an input sample (also called a component)
comp = cfg.Component(
                     'ee_ttbar',
                     files = [
                              # here we have a single input root file.
                              # the absolute path must be used to be able to run on the batch.
                              os.path.abspath('ee_ttbar.root')
                              ]
                     )

# selecting the list of components to be processed. Here only one. 
selectedComponents = [comp]

# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
                      Reader,
                      gen_particles = 'GenParticle',
                      gen_vertices = 'GenVertex'
                      )

# importing the papas simulation and reconstruction sequence,
# as well as the detector used in papas
# check papas_cfg.py for more information
from heppy.test.papas_cfg import papas, papas_sequence, detector

from heppy.test.papas_cfg import papasdisplaycompare as display 

# Use a Selector to select leptons from the output of papas simulation.
# Currently, we're treating electrons and muons transparently.
# we could use two different instances for the Selector module
# to get separate collections of electrons and muons
# help(Selector) for more information
from heppy.analyzers.Selector import Selector
leptons_true = cfg.Analyzer(
                            Selector,
                            'sel_leptons',
                            output = 'leptons_true',
                            input_objects = 'rec_particles',
                            filter_func = lambda ptc: ptc.e()>10. and abs(ptc.pdgid()) in [11, 13]
                            )

#muons_true = cfg.Analyzer(
#                          Selector,
#                          'sel_muons',
#                          output = 'muons_true',
#                          input_objects = 'rec_particles',
#                          filter_func = lambda ptc: ptc.e()>10. and abs(ptc.pdgid()) in [13]
#                          )
#
#
#electrons_true = cfg.Analyzer(
#                              Selector,
#                              'sel_electrons',
#                              output = 'electrons_true',
#                              input_objects = 'rec_particles',
#                              filter_func = lambda ptc: ptc.e()>10. and abs(ptc.pdgid()) in [11]
#                              )

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
                           IsolationAnalyzer,
                           candidates = 'leptons_true',
                           particles = 'rec_particles',
                           iso_area = EtaPhiCircle(0.4)
                           )

#iso_muons = cfg.Analyzer(
#                         IsolationAnalyzer,
#                         candidates = 'muons_true',
#                         particles = 'rec_particles',
#                         iso_area = EtaPhiCircle(0.4)
#                         )
#
#iso_electrons = cfg.Analyzer(
#                             IsolationAnalyzer,
#                             candidates = 'electrons_true',
#                             particles = 'rec_particles',
#                             iso_area = EtaPhiCircle(0.4)
#                             )


# Select isolated leptons with a Selector
# one can pass a function like this one to the filter:
def relative_isolation(lepton):
    sumpt = lepton.iso_211.sumpt + lepton.iso_22.sumpt + lepton.iso_130.sumpt
    sumpt /= lepton.pt()
    return sumpt

# ... or use a lambda statement as done below. 
sel_iso_leptons = cfg.Analyzer(
                               Selector,
                               'sel_iso_leptons',
                               output = 'sel_iso_leptons',
                               input_objects = 'leptons_true',
                               # filter_func = relative_isolation
                               filter_func = lambda lep : lep.iso.sumpt/lep.pt()<0.3 # fairly loose
                               )

sel_iso_muons = cfg.Analyzer(
                             Selector,
                             'sel_iso_muons',
                             output = 'sel_iso_muons',
                             input_objects = 'sel_iso_leptons',
                             # filter_func = relative_isolation
                             filter_func = lambda ptc: abs(ptc.pdgid()) in [13]
                             )

sel_iso_electrons = cfg.Analyzer(
                                 Selector,
                                 'sel_iso_electrons',
                                 output = 'sel_iso_electrons',
                                 input_objects = 'sel_iso_leptons',
                                 # filter_func = relative_isolation
                                 filter_func = lambda ptc: abs(ptc.pdgid()) in [11]
                                 )





sqrts = Collider.SQRTS

from heppy.analyzers.Masker import Masker
particles_not_lep = cfg.Analyzer(
                                 Masker,
                                 output = 'particles_not_lep',
                                 input = 'rec_particles',
                                 mask = 'sel_iso_leptons',
                                 )

# Make jets from the particles not used to build the best zed.
# Here the event is forced into 2 jets to target ZH, H->b bbar)
# help(JetClusterizer) for more information
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
                    JetClusterizer,
                    output = 'jets',
                    particles = 'particles_not_lep',
                    fastjet_args = dict( njets = 2)
                    )


#TODO add b tagging, gen jets, gen jet matching


# Just a basic analysis-specific event Selection module.
# this module implements a cut-flow counter
# After running the example as
#    heppy_loop.py Trash/ analysis_ee_ZH_cfg.py -f -N 100 
# this counter can be found in:
#    Trash/example/heppy.analyzers.examples.zh.selection.Selection_cuts/cut_flow.txt
# Counter cut_flow :
#         All events                                     100      1.00    1.0000
#         At least 2 leptons                              87      0.87    0.8700
#         Both leptons e>30                               79      0.91    0.7900
# For more information, check the code of the Selection class
# in heppy/analyzers/examples/zh/selection.py
from heppy.analyzers.examples.zh.selection import Selection
selection = cfg.Analyzer(
                         Selection,
                         instance_label='cuts'
                         )

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py


from heppy.test.pdebug_cfg import pdebug

# now make ntuple:
from MySimpleTreeProducer import MySimpleTreeProducer
tree = cfg.Analyzer(
                    MySimpleTreeProducer,
                    jets = 'jets',
                    leptons = 'sel_iso_leptons'#,
                    #                    muons = 'sel_iso_muons',
                    #                    electrons = 'sel_iso_electrons'
                    
                    )

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
                        source,
                        pdebug,
                        papas_sequence,
                        leptons_true,
                        iso_leptons,
                        sel_iso_leptons,
                        sel_iso_muons,
                        sel_iso_electrons,
                        particles_not_lep,
                        jets,
                        tree,
                        display
                        )

# Specifics to read FCC events 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
                    components = selectedComponents,
                    sequence = sequence,
                    services = [],
                    events_class = Events
                    )
