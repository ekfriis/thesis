#!/usr/bin/env python
#import re
import ROOT
import math
#import pprint
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")

# Version copied from /afs/cern.ch/user/t/tvickey/public/out.mhmax.root on Nov16
#_FILE_NAME = '/afs/cern.ch/user/f/friis/public/out.mhmax.Nov16.root'
_FILE_NAME = 'out.mhmax_7.root'

picobarns = 1.0
femtobarns = 1e-3*picobarns

def square(x):
    return x*x

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def lookup_value_impl(ma, tanb, histo):
    bin = histo.FindBin(ma, tanb)
    return histo.GetBinContent(bin)
    #return histo.Interpolate(ma, tanb)

_FILE = []
def _get_file():
    " Load file "
    if not _FILE:
        _FILE.append(ROOT.TFile(_FILE_NAME))
    return _FILE[0]

def lookup_value(ma, tanb, histo):
    try:
        return lookup_value_impl(ma, tanb, _get_file().Get(histo))
    except AttributeError:
        print "Caught exception getting", histo


def query(mA, tan_beta):
    higgs_types = [ 'h', 'A', 'H' ]
    # Curry lookup
    lookup = lambda histo : lookup_value(mA, tan_beta, histo)
    # Build emtpy dictionaries for each
    output = {
        'mA' : mA,
        'tan_beta' : tan_beta,
        'higgses' : {
            'h' : {},
            'A' : {},
            'H' : {}
        }
    }
    def add_br(input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR'] = lookup("h_brtautau_%s" % type)

    def add_mass(input):
        " Lookup the mass for a given higgs type "
        type, type_info = input
        if type == 'A':
            type_info['mass'] = mA
            return
        type_info['mass'] = lookup("h_m%s" % type)

    def add_xsec(input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [
            ('ggF', picobarns), ('bbH', femtobarns), ('bbH4f', femtobarns)]:
            type_info['xsec'][prod_type] = unit*lookup(
                "h_%s_xsec_%s" % (prod_type, type))

    def add_mu(input):
        type, type_info = input
        type_info.setdefault('mu', {})
        for prod_type in ['bbH']:
            type_info['mu'][prod_type] = {
                1 : lookup('h_%s_muup_%s' % (prod_type, type))*femtobarns,
                -1 : lookup('h_%s_mudown_%s' % (prod_type, type))*femtobarns,
                0 : 0,
            }
        type_info['mu']['bbH4f'] = {
            -1 : (lookup('h_bbH4f_xsec_%s_low' % type) -
                   lookup('h_bbH4f_xsec_%s' % type))*femtobarns,
            1 : (lookup('h_bbH4f_xsec_%s_high' % type) -
                   lookup('h_bbH4f_xsec_%s' % type))*femtobarns,
            0 : 0,
        }
        type_info['mu']['ggF'] = {
            -1 : (lookup('h_ggF_xsec20_%s' % type) -
                   lookup('h_ggF_xsec_%s' % type))*picobarns,
            1 : (lookup('h_ggF_xsec05_%s' % type) -
                   lookup('h_ggF_xsec_%s' % type))*picobarns,
            0 : 0,
        }


    def add_pdf(input):
        type, type_info = input
        type_info.setdefault('pdf', {})
        for prod_type in ['bbH']:
            type_info['pdf'][prod_type] = {
                1 : lookup('h_%s_pdfalphas68up_%s' % (prod_type, type))*femtobarns,
                -1 : lookup('h_%s_pdfalphas68down_%s' % (prod_type, type))*femtobarns,
                0 : 0,
            }
        # Supposedly negligble compared to scale
        type_info['pdf']['bbH4f'] = {
            -1 : 0,
            1 : 0,
            0 : 0,
        }
        ggF_alphasdown = lookup('h_ggF_alphasdown_%s' % type)
        ggF_pdfdown = lookup('h_ggF_pdfdown_%s' % type)

        ggF_alphasup = lookup('h_ggF_alphasup_%s' % type)
        ggF_pdfup = lookup('h_ggF_pdfup_%s' % type)

        type_info['pdf']['ggF'] = {
            -1 : quad(ggF_alphasdown, ggF_pdfdown)*picobarns,
            1 : quad(ggF_alphasup, ggF_pdfup)*picobarns,
            0 : 0,
        }

    map(add_br, output['higgses'].iteritems())
    map(add_mass, output['higgses'].iteritems())
    map(add_xsec, output['higgses'].iteritems())
    map(add_mu, output['higgses'].iteritems())
    map(add_pdf, output['higgses'].iteritems())
    return output

# Functions that determine whether or not a Higgs (h, H, A) is non-negligble
inclusion_ranges = {
    'A' : lambda massA: True,
    'H' : lambda massA: massA >= 130,
    'h' : lambda massA: massA <= 130,
}

def effective_cross_section(mA, tanB, use_4flavor=False,
                            uncertainties = 0,
                            verbose=False):
    output = 0.0
    bb_prod_type = use_4flavor and 'bbH4f' or 'bbH'
    mssm_info = query(mA, tanB)
    total_correction = 0
    if verbose:
        print " Querying cross section - mA = %0.0f tanbeta = %0.0f" % (
            mA, tanB)
        if use_4flavor:
            print " (using four flavor xsections)"
    for higgs_type in ['H', 'A', 'h']:
        linear_uncertainties = 0
        quadratic_uncertainties = 0
        for production_mechanism in ['ggF', bb_prod_type]:
            # Check if it's relevant
            if inclusion_ranges[higgs_type](mA):
                higgs_info = mssm_info['higgses'][higgs_type]
                br = higgs_info['BR']
                linear_uncertainties += \
                        higgs_info['mu'][production_mechanism][uncertainties]*br
                quadratic_uncertainties += square(
                    higgs_info['pdf'][production_mechanism][uncertainties]*br
                )
                xsec = (higgs_info['xsec'][production_mechanism]/picobarns)
                output += br*xsec
                if verbose:
                    print "--- %s-%s contributes %0.2f * %0.2fpb = %0.2f" % (
                        higgs_type, production_mechanism, br, xsec, br*xsec)
        correction = linear_uncertainties + uncertainties*math.sqrt(
            quadratic_uncertainties)
        total_correction += correction
    if verbose:
        print "Total cross section: %0.2f" % output
    return output + total_correction

def get_tanb_for_xsec(xsec, xsec_from_tanb_func):
    graph = ROOT.TGraph(55)
    for tanb in range(5, 60+1):
        eff_xsec = xsec_from_tanb_func(tanb)
        graph.SetPoint(tanb-1, eff_xsec, tanb)
    return graph.Eval(xsec)

if __name__ == "__main__":
    # Parse arguments
    #mA = sys.argv[1]
    #tanB = sys.argv[2]
    #result = query(130, 30)
    #pprint.pprint(result)
    masses = [ 90, 90., 120., 130., 160., 200., 250., 300.]
    #limits = [
        #147.745, 112.300, 39.611, 25.398, 18.199,
        #11.370, 9.785, 8.708, 5.773, 4.360, 3.602, 2.855, 2.406, 2.101 ]

    obs_limits = [ 1000, 394.7, 86.5, 59.9, 28.3, 16.4, 12.9, 9.4 ]
    exp_limits = [ 1000, 621.9, 59.8, 40.5, 19.0, 11.2, 7.6, 5.7 ]


    five_flavor_graph = {
        'exp' : ROOT.TGraph(len(masses)),
        'obs' : ROOT.TGraph(len(masses)),
    }

    four_flavor_graph = {
        'exp' : ROOT.TGraph(len(masses)),
        'obs' : ROOT.TGraph(len(masses)),
    }

    for key, graph in five_flavor_graph.iteritems():
        graph.SetLineColor(ROOT.EColor.kBlue)
        graph.SetLineWidth(2)
        if '1' in key:
            graph.SetLineStyle(2)

    for key, graph in four_flavor_graph.iteritems():
        graph.SetLineColor(ROOT.EColor.kRed)
        graph.SetLineWidth(2)
        if '1' in key:
            graph.SetLineStyle(2)

    five_flavor_graph['exp'].SetLineStyle(2)

    for type, limit_collection in [('exp', exp_limits), ('obs', obs_limits)]:
        for index, (mass, limit) in enumerate(zip(masses, limit_collection)):

            def five_flavor_query(tanb):
                return effective_cross_section(mass, tanb, False, 0)
            def four_flavor_query(tanb):
                return effective_cross_section(mass, tanb, True, 0)
            def five_flavor_query_up(tanb):
                return effective_cross_section(mass, tanb, False, -1)
            def five_flavor_query_down(tanb):
                return effective_cross_section(mass, tanb, False, +1)
            def four_flavor_query_up(tanb):
                return effective_cross_section(mass, tanb, True, -1)
            def four_flavor_query_down(tanb):
                return effective_cross_section(mass, tanb, True, +1)


            five_flavor = get_tanb_for_xsec(limit, five_flavor_query)
            #five_flavor_up = get_tanb_for_xsec(limit, five_flavor_query_up)
            #five_flavor_down = get_tanb_for_xsec(limit, five_flavor_query_down)

            five_flavor_graph[type].SetPoint(index, mass, five_flavor)


            four_flavor = get_tanb_for_xsec(limit, four_flavor_query)
            #four_flavor_up = get_tanb_for_xsec(limit, four_flavor_query_up)
            #four_flavor_down = get_tanb_for_xsec(limit, four_flavor_query_down)

            four_flavor_graph[type].SetPoint(index, mass, four_flavor)


            diff = (five_flavor - four_flavor)/five_flavor

            print "mass: %3.0f 5flavor: %3.2f 4flavor: %3.2f diff: %2.2f%%" % (
                mass,
                five_flavor,
                four_flavor,
                diff*100.0
            )
            #print "mass: %3.0f 5flavor: %3.2f (+%3.2f)(-%3.2f) "\
                    #"4flavor: %3.2f (+%3.2f)(-%3.2f) diff 5-4: %2.2f%%" % (
                        #mass,
                        #five_flavor,
                        #five_flavor_up,
                        #five_flavor_down,
                        #four_flavor,
                        #four_flavor_up,
                        #four_flavor_down,
                        #diff*100.0
                    #)

    tev_masses = [ 90,  100,  110,  120,  130,  140,  150,  160,  170,  180,  190, 200, 201, 210 ]
    tev_limits = [ 31,  46,   43,   34,   29,   30,   31,   33,   38,   42,   48,  55, 60., 65 ]

    tev_graph = ROOT.TGraph(len(tev_limits))
    for i, (mass, limit) in enumerate(zip(tev_masses, tev_limits)):
        tev_graph.SetPoint(i, mass, limit)

    canvas = ROOT.TCanvas("blah", "blah", 800, 600)
    canvas.SetBottomMargin(0.13)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)

    legend = ROOT.TLegend(0.55, 0.15, 0.9, 0.42, "", "brNDC")
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    # make exclusion zone look good
    five_flavor_graph['obs'].SetPoint(0, 80, 43)
    five_flavor_graph['exp'].SetPoint(0, 80, 55)

    tev_graph.SetLineColor(ROOT.EColor.kAzure -1)
    tev_graph.SetFillColor(ROOT.EColor.kAzure -1)
    #tev_graph.SetLineWidth(9902)
    tev_graph.SetFillStyle(1001)

    five_flavor_graph['exp'].SetLineColor(ROOT.EColor.kRed)
    five_flavor_graph['obs'].SetLineColor(ROOT.EColor.kAzure -4)

    #legend.AddEntry(four_flavor_graph['central'], "Four Flavor", "l")
    five_flavor_graph['obs'].SetLineWidth(9902)
    five_flavor_graph['obs'].SetFillStyle(1001)
    five_flavor_graph['obs'].SetFillColor(
        five_flavor_graph['obs'].GetLineColor())
    five_flavor_graph['obs'].SetLineColor(1)

    five_flavor_graph['obs'].Draw("al")
    five_flavor_graph['exp'].Draw("l,same")

    five_flavor_graph['exp'].SetLineWidth(3)

    #tev_graph.SetLineWidth(9904)
    tev_graph.SetLineWidth(4)
    tev_graph.SetFillStyle(3003)
    tev_graph.SetFillColor(tev_graph.GetLineColor())
    tev_graph.Draw("l,same")

    legend.AddEntry(five_flavor_graph['obs'], "Excluded", "f")
    legend.AddEntry(five_flavor_graph['exp'], "Expected limit", "l")
    legend.AddEntry(tev_graph, "Tevatron excluded", "l")

    label = ROOT.TPaveText(0.12, 0.17, 0.5, 0.28, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.AddText("MSSM m_{h}^{max} scenario")
    label.AddText("95% C.L. excluded regions")
    label.Draw()

    histo = five_flavor_graph['obs'].GetHistogram()
    histo.GetXaxis().SetRangeUser(90, 300)
    histo.SetMinimum(0)
    histo.GetXaxis().SetTitle("m_{A} (GeV/c^{2})")
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetNdivisions(110)

    histo.GetYaxis().SetTitle("tan #beta")
    histo.SetTitle("")
    histo.SetMaximum(60)
    histo.Draw("axissame")
    #for key, graph in five_flavor_graph.iteritems():
        #if 'central' in key:
            #graph.Draw('lp')
    #for key, graph in four_flavor_graph.iteritems():
        #if 'central' in key:
            #graph.Draw('lp')
    legend.Draw()

    canvas.SaveAs('tan_beta.pdf')

    effective_cross_section(120, 30, verbose=True)
    effective_cross_section(120, 30, True, verbose=True)
    effective_cross_section(250, 30, verbose=True)
    effective_cross_section(250, 30, True, verbose=True)

