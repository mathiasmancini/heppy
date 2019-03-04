from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance

class MCLeptonFinder(Analyzer):

    '''
    from analyzers.MCLeptonFinder import MCLeptonFinder
    mc_lepton_and_neutrino = cfg.Analyzer(
        MCLeptonFinder,
        sel_leptons = 'sorted_leptons',
        output1 = 'mc_lepton',
        output2 = 'mc_neutrino',
    )
    '''

    def process(self, event):

        def debug():
            for top in tops:
                print "TOP"
                print top
                print
                for top_daughter in top.daughters:
                    print "TOP daughter"
                    print top_daughter
                    print
                    for top_grand_daughter in top_daughter.daughters:
                        print "W-daughter"
                        print top_grand_daughter
                        print
                        for top_grand_grand_daughter in top_grand_daughter.daughters:
                            print "real w daughter"
                            print top_grand_grand_daughter
                            print
                            for top_grand_grand_grand_daughter in top_grand_grand_daughter.daughters:
                                print "top_grand_grand_grand_daughter"
                                print top_grand_grand_grand_daughter
                                print
                            print
                        print
                    print
                print

        def match_lepton(lepton):

            if abs(lepton.pdgid()) in [11, 13]:
                if lepton.status() == 1:
                    setattr(event, self.cfg_ana.output1, lepton)
                    return 1
                else:
                    for stable_lepton in event.genbrowser.descendants(w):
                        if stable_lepton.pdgid() == lepton.pdgid() and stable_lepton.status() == 1:
                            setattr(event, self.cfg_ana.output1, stable_lepton)
                            return 1
                    print "error, didn't find any stable lepton among lepton.descendants"
                    import pdb; pdb.set_trace()
                    return False

            elif abs(lepton.pdgid()) == 15:
                if lepton.status() == 2:
                    setattr(event, self.cfg_ana.output1, lepton)
                    return 1
                else:
                    for stable_lepton in event.genbrowser.descendants(w):
                        if stable_lepton.pdgid() == lepton.pdgid() and stable_lepton.status() == 2:
                            setattr(event, self.cfg_ana.output1, stable_lepton)
                            found = True
                            return 1
                    print "error, didn't find any stable tau among lepton.descendants"
                    import pdb; pdb.set_trace()
                    return False

            elif abs(lepton.pdgid()) in [12, 14, 16]:
                if lepton.status() == 1:
                    setattr(event, self.cfg_ana.output2, lepton)
                    return 1
                else:
                    for stable_lepton in event.genbrowser.descendants(w):
                        if stable_lepton.pdgid() == lepton.pdgid() and stable_lepton.status() == 1:
                            setattr(event, self.cfg_ana.output2, stable_lepton)
                            found = True
                            return 1
                    print "error, didn't find any stable neutrino among lepton.descendants"
                    import pdb; pdb.set_trace()
                    return False

            elif abs(lepton.pdgid()) == 24:
                sum_lep = 0
                for ptc_daughter in lepton.daughters:
                    sum_lep += match_lepton(ptc_daughter)
                return sum_lep
            else:
                return 0


        gen_particles = event.gen_particles

        tops = []
        for gen_ptc in gen_particles:
            if abs(gen_ptc.pdgid()) == 6:
                tops.append(gen_ptc)

        found_leptons = 0
        for top in tops:
            for w in top.daughters:
                # if it's a W boson
                if abs(w.pdgid()) == 24:
                    # check if the daughter is another w or a lepton
                    for ptc in w.daughters:
                        if abs(ptc.pdgid()) == 24:
                            for lepton in ptc.daughters:
                                found_leptons += match_lepton(lepton)

                        else:
                            found_leptons += match_lepton(ptc)

        if found_leptons != 2:
            print "found not right number of leptons ", found_leptons
            return False

        mc_lepton = getattr(event, self.cfg_ana.output1)
        mc_neutrino = getattr(event, self.cfg_ana.output2)

        mc_w_lep = Resonance([mc_lepton, mc_neutrino], 24)
        setattr(event, "mc_w_lep", mc_w_lep)

        leptons = getattr(event, self.cfg_ana.sel_leptons)
        for lepton in leptons:
            if lepton.match == mc_lepton:
                lepton.match_with_mc = 1
            else:
                lepton.match_with_mc = 0
