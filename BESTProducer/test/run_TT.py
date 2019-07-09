import FWCore.ParameterSet.Config as cms

process = cms.Process("run")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer16MiniAODv3/ZprimeToWW_width0p3_M-3000_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/110000/DE74918A-80BC-E811-A7B7-7CD30AC0311A.root'
#        '/store/mc/RunIIFall17MiniAODv2/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/702C798E-5742-E811-B83B-0025905C95F8.root'
#        '/store/mc/RunIISummer16MiniAODv3/RadionToZZ_width0p1_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/22D31D21-5AD2-E811-AF27-0242AC130002.root'
#        '/store/mc/RunIIFall17MiniAODv2/TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/10000/44B2C08A-636B-E811-8957-90B11C443319.root',
        )
                            )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.selectedAK8Jets = cms.EDFilter('PATJetSelector',
    src = cms.InputTag('slimmedJetsAK8'),
    cut = cms.string('pt > 100.0 && abs(eta) < 2.4'),
    filter = cms.bool(True)
)

process.countAK8Jets = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(99999),
    src = cms.InputTag("selectedAK8Jets"),
    filter = cms.bool(True)
)

process.run = cms.EDProducer('BESTProducer',
	inputJetColl = cms.string('selectedAK8Jets'),
	pdgIDforMatch = cms.int32(6),
	NNtargetX = cms.int32(1),
	NNtargetY = cms.int32(1),
	isMC = cms.int32(1),
        isQCD = cms.int32(0),
	doMatch = cms.int32(0),
	usePuppi = cms.int32(1)

)
process.TFileService = cms.Service("TFileService", fileName = cms.string("histo_BESTprod.root") )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("ana_out.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
								      'keep *_fixedGridRhoAll_*_*',
                                                                      'keep *_run_*_*',
                                                                      #, 'keep *_goodPatJetsCATopTagPF_*_*'
                                                                      #, 'keep recoPFJets_*_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.p = cms.Path(process.selectedAK8Jets*process.countAK8Jets*process.run)
