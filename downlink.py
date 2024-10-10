import numpy as np

P = 2  # transmitter power [w]
f = 2.5  # signal frequency (downlink) [GHz]
G_tx = 19.7  # antenna gain [dB]
L_tx = 0.97  # loss factor transmitter [dB]
L_rx = 0.97  # loss factor reciever [dB]
efficiency = 0.55  # antenna efficiency [-]
altitude = 570  # spacecraft orbit altitude [km]
elevation = np.radians(10)  # minimum elevation [rad]
point_sc = np.radians(0.25)  # pointing offset spacecraft [rad]
point_gs = 0.1 * elevation  # VERIFY pointing offset ground station [rad]
DR = 10**7  # spacecraft generated data rate [bit/s]
duty = 0.5  # duty cycle [-]
time_dl = 0.5 / 24  # downlink time ratio [h/h]
path_loss = -0.5  # transmission path loss [dB]
gt_rx = 24.4  # reciever G / T [dB K]
BER = 10**(-9)  # required BER 