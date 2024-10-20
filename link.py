import numpy as np
"""CONSTANTS"""
C = 299792458

T0 = 290 #slides
EFFICIENCY = 0.55 #slides
BOLTZMANN = 1.380649*10**-23
TSYSUPLINK = 614 #SLIDES
TSYSDOWNLINK = 135 #SLIDES
POINTINGLOSSGROUND = 0.12 #In DB assumed pointing offset of 0.1alpha as specified in slides
ELEVATION = np.radians(10) #degree slides

EARTHSUNDIS = 149000*10**6
EARTHMOONDIS = 384400000

RADIUSMOON = 1737.4*10**3
REARTH = 6371000
RMARS = 3389.5*10**3
RMERCURY = 2439.7*10**3
RSATURN = 58232*10**3

MUEARTH = 3.986004418*10**14
MUMOON = 4.9048695*10**12
MUMARS = 4.282837*10**13
MUMERCURY = 2.2032*10**13
MUSATURN = 3.7931187*10**16

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
    print(s)
    loss = 20*np.log10((4*np.pi*s)/length)
    return loss


def dataRateSC(swatWidthAngle, altitude, bitsPerPixel, pixelSizeArcmin, dutyCycle, downlinkTime, case):
    swatWidth = 2*altitude*np.tan(np.radians(swatWidthAngle/2))
    pixelAngle = 1/60*pixelSizeArcmin
    pixelSize = 2*altitude*np.tan(np.radians(pixelAngle/2))
    if case == 0: v = (MUEARTH/(REARTH+altitude))**0.5
    elif case == 1: v = (MUMOON/(RADIUSMOON+altitude))**0.5
    elif case == 2: v = (MUMARS/(RMARS+altitude))**0.5
    elif case == 3: v = (MUMERCURY/(RMERCURY+altitude))**0.5
    elif case == 4: v = (MUSATURN/(RSATURN+altitude))**0.5
    br = bitsPerPixel*(swatWidth*v)/(pixelSize**2)
    rbr = br*(dutyCycle)/(downlinkTime/24)
    return rbr


def uplink(diameterGround, downlinkFrequency, turnAroundRatio, lossfactorTransmitter, groundPower, orbitAltitude, atmosphericAttenuation, 
           diameterSC, uplinkDatarate, case, elongationAngle=0):
    uplinkFrequency = downlinkFrequency*turnAroundRatio #Convert downlinkfrequncy into uplink frequncy
    gainSC = gainAntenna(uplinkFrequency, diameterSC) #Returns gain of ground antenna in DB
    gainGround = gainAntenna(uplinkFrequency, diameterGround) #Returns gain of ground antenna in DB
    Eirp = gainGround+DB(lossfactorTransmitter)+DB(groundPower)
    if case == 0:
        spaceLoss = spaceLossNormal(orbitAltitude, uplinkFrequency) #Returns non deep space loss of in DB
    elif case == 1:
        spaceLoss = spaceLossDeep(EARTHMOONDIS, REARTH, ELEVATION+np.radians(90), uplinkFrequency)
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

def downlink(diameterSC, downlinkFrequency, diameterGround, lossfactorTransmitter, scPower, orbitAltitude, atmosphericAttenuation, 
    swathWidthAngle, bitsPixel, pixelsizeangle, pointingInacuracy, case, dutyCycle, downlinkTime, elongationAngle = 0):
    gainSC = gainAntenna(downlinkFrequency, diameterSC)
    gainGround = gainAntenna(downlinkFrequency, diameterGround)
    Eirp = gainSC+DB(lossfactorTransmitter)+DB(scPower)
    if case == 0:
        spaceLoss = spaceLossNormal(orbitAltitude, downlinkFrequency) #Returns non deep space loss of in DB
    elif case == 1:
        spaceLoss = spaceLossDeep(EARTHMOONDIS, REARTH, ELEVATION+np.radians(90), downlinkFrequency)
    elif case == 2:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, MARSSUNDIS, np.radians(elongationAngle), downlinkFrequency)
    elif case == 3:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, MERCURYSUNDIS, np.radians(elongationAngle), downlinkFrequency)
    elif case == 4:
        spaceLoss = spaceLossDeep(EARTHSUNDIS, SATURNSUNDIS, np.radians(elongationAngle), downlinkFrequency)
    atmosphereLoss = atmosphericAttenuation/np.sin(ELEVATION)
    halfAngle = 21/(downlinkFrequency*diameterSC)
    pointingLoss = 12*(pointingInacuracy/halfAngle)**2
    gt = gainGround - DB(TSYSDOWNLINK)
    rdr = dataRateSC(swathWidthAngle, orbitAltitude, bitsPixel, pixelsizeangle,dutyCycle,downlinkTime, case)
    lossDatarate = DB(rdr)
    boltzmannGain = -DB(BOLTZMANN)
    values = [Eirp, pointingLoss, spaceLoss, atmosphereLoss, gt, lossDatarate, boltzmannGain]
    snr = Eirp - pointingLoss - spaceLoss - atmosphereLoss + gt - lossDatarate + boltzmannGain
    return snr, values



if __name__ == "__main__":
    # print(uplink(0.5, 2.2, 221/240, 0.8, 400, 500000, 0.035, 0.2, 10**8, 0))
    # print(downlink(0.2, 2.2, 0.5, 0.8, 50, 500000, 0.035, 20, 8, 0.1, 0.1, 0, 0.6, 3))
    print(dataRateSC(10, 400000, 8, 0.05, 0.15,))































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
