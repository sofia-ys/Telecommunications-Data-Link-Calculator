import numpy as np

# constants
c = 3 * 10**8  # speed of light [m/s]
R_e = 6371  # radius earth [km]
k_B = 1.3806452 * 10**(-23)  # Boltzmann's constant [J/K]

# from data table
Ptot = 200  # total spacecraft power [W]
P_sc = 2  # transmitter power (spacecraft) [w]
P_gs = 400  # transimitter power (ground station) [W]
L_tx = 0.97  # loss factor transmitter [dB]
L_rx = 0.97  # loss factor reciever [dB]
f = 2.5  # signal frequency (downlink) [GHz]
turnaround = 221/240  # uplink / downlink frequency ratio [-]
D_ant_sc = 0.5  # antenna spacecraft diameter [m]
D_ant_gs = 5  # antenna ground station diameter [m]
h = 570  # spacecraft orbit altitude [km]
elong = 20  # elongation angle (s/c to sun line and earth-sun line) [deg]
e_tx = 0.1  # pointing offset spacecraft [deg]
DR_uplink = 10**8  # required uplink data rate [bit/s]
width_sw = 20  # payload swath width angle [deg]
pixel_size = 0.1  # payload pixel size [arcmin]
pixel_bits = 8  # payload bits per pixel
D_C = 0.5  # payload duty cycle [-]
T_DL = 3  # payload downlink time ratio [hr / day]
BER = 10**(-6)  # required BER 

# assumed values
eta_ant = 0.55  # antenna efficiency [-]
alpha = np.radians(10)  # minimum elevation [rad]
L_a0 = 0.5  # zenith attenuation from graph
T0 = 290  # reference temperature [K]
T_ant = 25  # antenna noise [K]
F = 1  # noise figure [dB]


def downlinkSNR(c, f, D_ant_sc, eta_ant, e_tx, R_e, h, alpha, L_tx, P_sc, L_a0, F, T_ant, width_sw, pixel_size, pixel_bits, bits_image, D_C, T_DL, T0=290):

    # transmitter antenna (parabolic) pointing loss
    wavelength = c/(f * 10**9)
    G_tx = (np.pi**2 * D_ant_sc**2 * eta_ant)/(wavelength**2)
    alpha_half = 21 / (f * D_ant_sc)
    L_ant = 12 * (e_tx / alpha_half)**2  # [dB]

    # free space loss
    d = R_e * (np.sqrt(((h + R_e)/R_e)**2 - (np.cos(alpha))**2) - np.sin(alpha))
    L_FS = 20 * np.log10((4 * np.pi * d * 10**3)/wavelength) # [db]

    # cable losses
    L_cable_tx = 10 * np.log10(L_tx)  # [dB]

    # antenna gain
    G_tx = 10 * np.log10(eta_ant * ((np.pi * D_ant_sc)/wavelength)**2)

    # EIRP calculation
    EIRP_tx = G_tx + L_cable_tx + 10 * np.log10(P_sc)  # [dB]

    # atmospheric loss
    L_A = L_a0 / np.sin(alpha)  # [dB]

    # temperature
    T_cable_tx = T0 * ((1 - L_cable_tx)/L_cable_tx)
    T_amp = T0 * (F - 1)
    T_sys = 10 * np.log10(T_ant + T_amp + T_cable_tx)
    G_over_T = G_tx - T_sys  # [dB]

    # required data rate downlink
    n_pixel = (width_sw * 60)/pixel_size
    bits_image = n_pixel * pixel_bits
    images_DR = bits_image * D_C
    dl_time = T_DL * 3600
    req_DL_dr = images_DR / dl_time

    # downlink budget calculation
    EbN0 = EIRP_tx - L_FS - L_cable_tx - L_A + G_over_T - 10 * np.log10(k_B * req_DL_dr)

    return EbN0