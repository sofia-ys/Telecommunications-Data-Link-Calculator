import numpy as np

# constants
c = 3 * 10**8  # speed of light [m/s]
R_e = 6371  # radius earth [km]
k_B = 1.3806452 * 10**(-23)  # Boltzmann's constant [J/K]

def downlinkSNR(c, f, antenna_diameter_spacecraft, eta_ant, pointing_offset_angle, R_e, orbit_altitude, elevation, loss_factor_transmitter, 
                transmitter_power_spacecraft, zenith_attenuation, noiseFigureReceiver, tempAntSC, payload_swath_width, payload_pixel_size, 
                payload_bits_per_pixel, payload_duty_cycle, payload_downlink_time, T0):

    # transmitter antenna (parabolic) pointing loss
    wavelength = c/(f * 10**9)
    G_tx = (np.pi**2 * antenna_diameter_spacecraft**2 * eta_ant)/(wavelength**2)
    alpha_half = 21 / (f * antenna_diameter_spacecraft)
    L_ant = 12 * (pointing_offset_angle / alpha_half)**2  # [dB]

    # free space loss
    d = R_e * (np.sqrt(((orbit_altitude + R_e)/R_e)**2 - (np.cos(elevation))**2) - np.sin(elevation))
    L_FS = 20 * np.log10((4 * np.pi * d)/wavelength) # [db]

    """CHECK THIS"""
    # cable losses
    L_cable_tx = 0.5

    # antenna gain
    G_tx = 10 * np.log10(eta_ant * ((np.pi * antenna_diameter_spacecraft)/wavelength)**2)

    # EIRP calculation
    EIRP_tx = G_tx + L_cable_tx + 10 * np.log10(transmitter_power_spacecraft)  # [dB]

    # atmospheric loss
    L_A = zenith_attenuation / np.sin(elevation)  # [dB]

    # temperature
    T_cable_tx = T0 * ((1 - loss_factor_transmitter)/loss_factor_transmitter)
    T_amp = T0 * (noiseFigureReceiver - 1)
    T_sys = 10 * np.log10(tempAntSC + T_amp + T_cable_tx)
    G_over_T = G_tx - T_sys  # [dB]

    # required data rate downlink
    n_pixel = (payload_swath_width * 60)/payload_pixel_size
    bits_image = n_pixel * payload_bits_per_pixel
    images_DR = bits_image * payload_duty_cycle
    dl_time = payload_downlink_time * 3600
    req_DL_dr = images_DR / dl_time

    # downlink budget calculation
    EbN0 = EIRP_tx - L_FS - L_cable_tx - L_A - L_ant + G_over_T - 10 * np.log10(k_B * req_DL_dr)
    values = [EIRP_tx, L_FS, G_over_T, 10 * np.log10(k_B * req_DL_dr), L_ant, L_A]

    return EbN0, values