import numpy as np

# constants
c = 3 * 10**8  # speed of light [m/s]
R_e = 6371  # radius earth [km]
k_B = 1.3806452 * 10**(-23)  # Boltzmann's constant [J/K]

# initial values
eta_ant = 0.55  # antenna efficiency [-]
D_ant = 0.5  # antenna diameter [m]
P = 2  # transmitter power [w]
f = 2.5  # signal frequency (downlink) [GHz]
L_tx = 0.97  # loss factor transmitter [dB]
L_rx = 0.97  # loss factor reciever [dB]
h = 570  # spacecraft orbit altitude [km]
alpha = np.radians(10)  # minimum elevation [rad]
e_tx = 0.25  # pointing offset spacecraft [deg]
'''VERIFY BELOW'''
e_rx = 0.1 * h  # VERIFY pointing offset ground station [rad]
'''VERIFY ABOVE'''
R_G = 10**7  # spacecraft generated data rate [bit/s]
D_C = 0.5  # duty cycle [-]
T_DL = 0.5 / 24  # downlink time ratio [h/h]
L_a = -0.5  # transmission path loss [dB]
gt_rx = 24.4  # reciever G / T [dB K]
BER = 10**(-9)  # required BER 

# transmitter antenna (parabolic) pointing loss
wavelength = c/(f * 10**9)
G_tx = (np.pi**2 * D_ant**2 * eta_ant)/(wavelength**2)
alpha_half = 21 / (f * D_ant)
L_ant = 12 * (e_tx / alpha_half)**2  # [dB]

# transmitter performances
P_tx = 10 * np.log10(P)
EIRP = P_tx - L_tx + G_tx

# free space loss
d = R_e * (np.sqrt(((h + R_e)/R_e)**2 - (np.cos(alpha))**2) - np.sin(alpha))
L_FS = 20 * np.log10((4 * np.pi * d * 10**3)/wavelength)

# atmospheric loss
L_A = 0.035 / np.sin(alpha)

# # downlink budget calculation
# EbN0 = EIRP - L_FS - L_x + (G/T) - 10 * np.log10(k_B * B_r)
