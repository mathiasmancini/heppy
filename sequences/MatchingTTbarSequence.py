import heppy.framework.config as cfg

from heppy.analyzers.MCLeptonFinder import MCLeptonFinder
mc_lepton_and_neutrino = cfg.Analyzer(
    MCLeptonFinder,
    sel_leptons = 'sel_iso_leptons',
    output1 = 'mc_lepton',
    output2 = 'mc_neutrino',
)

from heppy.analyzers.MCbQuarks import MCbQuarks
mc_b_quarks = cfg.Analyzer(
    MCbQuarks,
    output = 'mc_b_quarks',
    jets = 'jets',
)

matching_ttbar_sequence = [
    mc_lepton_and_neutrino,
    mc_b_quarks
]
