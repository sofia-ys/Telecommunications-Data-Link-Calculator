import numpy as np
"""CONSTANTS"""
C = 299792458
REARTH = 6371000
T0 = 290
EFFICIENCY = 0.55
BOLTZMANN = 1.380649*10**-23
TSYSUPLINK = 614
POINTINGLOSSGROUND = 0.12 #In DB assumed pointing offset of 0.1alpha as specified in slides
ELEVATION = np.radians(10) #degree

EARTHSUNDIS = 149000*10**6
EARTHMOONDIS = 384400000

RADIUSMOON = 1737.4*10**3

MARSSUNDIS = 206000*10**6
MERCURYSUNDIS = 46000*10**6
SATURNSUNDIS = 1429000*10**6


def DB(input):
    return 10*np.log10(input)

def gainAntenna(frequency, diameter):
    length = C/(frequency*10**9)
    g = (np.pi**2 * diameter**2)/length**2 *EFFICIENCY
    return DB(g)

def spaceLossNormal(altitude, frequency):
    length = C/(frequency*10**9) 
    d = REARTH*((((altitude+REARTH)/REARTH)**2-np.cos(ELEVATION)**2)**0.5-np.sin(ELEVATION))
    loss = 20 *np.log10((4*np.pi*d)/length)
    return loss

def spaceLossDeep(distanceEarthx, distanceSCx, angle, frequency):
    length = C/(frequency*10**9) 
    s = (distanceEarthx**2+distanceSCx**2-2*distanceEarthx*distanceSCx*np.cos(angle))**0.5
    loss = 20*np.log10((4*np.pi*s)/length)
    return loss

def uplink(diameterGround, downlinkFrequency, turnAroundRatio, lossfactorTransmitter, groundPower, orbitAltitude, atmosphericAttenuation, diameterSC, uplinkDatarate, case, elongationAngle=0):
    uplinkFrequency = downlinkFrequency*turnAroundRatio #Convert downlinkfrequncy into uplink frequncy
    gainSC = gainAntenna(uplinkFrequency, diameterSC) #Returns gain of ground antenna in DB
    gainGround = gainAntenna(uplinkFrequency, diameterGround) #Returns gain of ground antenna in DB
    Eirp = gainGround+DB(lossfactorTransmitter)+DB(groundPower)
    if case == 0:
        spaceLoss = spaceLossNormal(orbitAltitude, uplinkFrequency) #Returns non deep space loss of in DB
    elif case == 1:
        spaceLoss = spaceLossDeep(EARTHMOONDIS, orbitAltitude+RADIUSMOON, ELEVATION, uplinkFrequency)
    elif case == 2:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, MARSSUNDIS, np.radians(elongationAngle), uplinkFrequency)
    elif case == 3:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, MERCURYSUNDIS, np.radians(elongationAngle), uplinkFrequency)
    elif case == 4:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, SATURNSUNDIS, np.radians(elongationAngle), uplinkFrequency)
    atmosphereLoss = atmosphericAttenuation/np.sin(ELEVATION)
    gt = gainSC - DB(TSYSUPLINK)
    lossDatarate = DB(uplinkDatarate)
    boltzmannGain = -DB(BOLTZMANN)
    values = [Eirp, POINTINGLOSSGROUND, spaceLoss, atmosphereLoss, gt, lossDatarate, boltzmannGain]
    snr = Eirp - POINTINGLOSSGROUND - spaceLoss - atmosphereLoss + gt - lossDatarate + boltzmannGain
    return snr, values

if __name__ == "__main__":
    print(uplink(0.5, 2.2, 221/240, 0.8, 400, 500000, 0.035, 0.2, 10**8, 0))































# def DB(value):
#     return 10*np.log10(value)


# def gParabolicAnt(d, freq, eff):
#     waveLength = C/(freq*10**9)
#     g = ((np.pi)**2*d**2)/(waveLength**2)*eff
#     return g

# def EIRP(g, power):
#     p = DB(g)-0.5+DB(power)
#     return p

# def lossFreeSpace(h, freq, elev):
#     d = REARTH*((((h+REARTH)/REARTH)**2 - np.cos(elev)**2)**0.5-np.sin(elev))
#     waveLength = C/(freq*10**9)
#     l = (4*np.pi*d)/waveLength
#     return DB(l)

# def tSys(tAnt, loss, noiseF):
#     t = tAnt + T0*(1-loss)/loss+T0*(noiseF-1)
#     return t

# def halfAngleParabolic(freq, d):
#     alpha = 21/(freq*d)
#     return alpha


# def uplinkSNR(diameterGround, downlinkFrequency, turnAroundRatio, lossFactorTransmitter, powerTransmitter, orbitAltitude, 
#               elevation, diameterSC, lossFactorReceiver, tempAntSC, bitRate, pointingOffsetGround, zenithAttenuation, rainLoss=0,  noiseFigureReceiver=3):
#     atmosphericAttenuation = zenithAttenuation/np.sin(elevation)

#     uplinkFrequency = turnAroundRatio*downlinkFrequency
#     gainGround = gParabolicAnt(diameterGround, uplinkFrequency, EFFICIENCY)
#     eirp = EIRP(gainGround,powerTransmitter)
#     lfs = lossFreeSpace(orbitAltitude, uplinkFrequency, elevation)
#     gainSatelite = gParabolicAnt(diameterSC, uplinkFrequency, EFFICIENCY)
#     sytemTempSC = tSys(tempAntSC, lossFactorReceiver, noiseFigureReceiver)
#     gt = DB(gainSatelite/sytemTempSC)
#     halfAngle = halfAngleParabolic(uplinkFrequency, diameterGround)
#     pointingLoss = 12*(pointingOffsetGround/halfAngle)**2
#     snr = eirp - lfs + gt - 10*np.log10(BOLTZMANN*bitRate) - pointingLoss - rainLoss -atmosphericAttenuation
#     values = [eirp, lfs, gt, 10*np.log10(BOLTZMANN*bitRate), pointingLoss, rainLoss, atmosphericAttenuation]
#     return snr, values
