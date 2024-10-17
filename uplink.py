import numpy as np
"""CONSTANTS"""
C = 299792458
REARTH = 6371000
T0 = 290
EFFICIENCY = 0.55
BOLTZMANN = 1.380649*10**-23

def DB(value):
    return 20*np.log10(value)


def gParabolicAnt(d, freq, eff):
    waveLength = C/(freq*10**9)
    g = ((np.pi)**2*d**2)/(waveLength**2)*eff
    return g

def EIRP(g, power):
    p = DB(g)-0.5+DB(power)
    return p

def lossFreeSpace(h, freq, elev):
    d = REARTH*((((h+REARTH)/REARTH)**2 - np.cos(elev)**2)**0.5-np.sin(elev))
    waveLength = C/(freq*10**9)
    l = (4*np.pi*d)/waveLength
    return DB(l)

def tSys(tAnt, loss, noiseF):
    t = tAnt + T0*(1-loss)/loss+T0*(noiseF-1)
    return t

def halfAngleParabolic(freq, d):
    alpha = 21/(freq*d)
    return alpha


def uplinkSNR(diameterGround, downlinkFrequency, turnAroundRatio, lossFactorTransmitter, powerTransmitter, orbitAltitude, 
              elevation, diameterSC, lossFactorReceiver, tempAntSC, bitRate, pointingOffsetGround, zenithAttenuation, rainLoss=0,  noiseFigureReceiver=3):
    atmosphericAttenuation = zenithAttenuation/np.sin(elevation)

    uplinkFrequency = turnAroundRatio*downlinkFrequency
    gainGround = gParabolicAnt(diameterGround, uplinkFrequency, EFFICIENCY)
    eirp = EIRP(gainGround,powerTransmitter)
    lfs = lossFreeSpace(orbitAltitude, uplinkFrequency, elevation)
    gainSatelite = gParabolicAnt(diameterSC, uplinkFrequency, EFFICIENCY)
    sytemTempSC = tSys(tempAntSC, lossFactorReceiver, noiseFigureReceiver)
    gt = DB(gainSatelite/sytemTempSC)
    halfAngle = halfAngleParabolic(uplinkFrequency, diameterGround)
    pointingLoss = 12*(pointingOffsetGround/halfAngle)**2
    snr = eirp - lfs + gt - 10*np.log10(BOLTZMANN*bitRate) - pointingLoss - rainLoss -atmosphericAttenuation
    values = [eirp, lfs, gt, 10*np.log10(BOLTZMANN*bitRate), pointingLoss, rainLoss, atmosphericAttenuation]
    return snr, values
