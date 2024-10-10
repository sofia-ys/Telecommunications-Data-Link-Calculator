import numpy as np

# initial values
P = 2  # transmitter power [w]
f = 2.5  # signal frequency (downlink) [GHz]
G_tx = 19.7  # antenna gain [dB]
L_tx = 0.97  # loss factor transmitter [dB]
L_rx = 0.97  # loss factor reciever [dB]
eta = 0.55  # antenna efficiency [-]
h = 570  # spacecraft orbit altitude [km]
alpha = np.radians(10)  # minimum elevation [rad]
e_tx = 0.25  # pointing offset spacecraft [rad]
'''VERIFY BELOW'''
e_rx = 0.1 * h  # VERIFY pointing offset ground station [rad]
'''VERIFY ABOVE'''
R_G = 10**7  # spacecraft generated data rate [bit/s]
D_C = 0.5  # duty cycle [-]
T_DL = 0.5 / 24  # downlink time ratio [h/h]
L_a = -0.5  # transmission path loss [dB]
gt_rx = 24.4  # reciever G / T [dB K]
BER = 10**(-9)  # required BER 
c = 3 * 10**8  # speed of light [m/s]
R_e = 6371  # radius earth [km]

# transmitter performances
P_tx = 10 * np.log10(P)
EIRP = P_tx - L_tx + G_tx

# transmitter antenna pointing loss
wavelength = c/(f * 10**9)
G_tx_linear = 10**(G_tx/10)
D_t = np.sqrt((G_tx_linear * wavelength**2)/(np.pi**2 * eta))
alpha_half = 21 / (f * D_t)
L_tx = 12 * (e_tx / alpha_half)**2

# free space loss
d = R_e * (np.sqrt(((h + R_e)/R_e)**2 - (np.cos(alpha))**2) - np.sin(alpha))
L_FS = 20 * np.log10((4 * np.pi * d * 10**3)/wavelength)
print(L_FS)

# atmospheric loss
L_A = 0.035 / np.sin(alpha)

