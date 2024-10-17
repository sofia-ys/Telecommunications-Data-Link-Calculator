import pandas as pd 
import numpy as np
from uplink import uplinkSNR
from downlink import downlinkSNR

# assumed values
eta_ant = 0.55  # antenna efficiency [-]
elevation = np.radians(10)  # minimum elevation [rad]
zenith_attenuation = [0.035, 0.035, 0.48, 0.48, 0.49]  # zenith attenuation from graph
T0 = 290  # reference temperature [K]
tempAntSC = 25  # antenna noise [K]
noiseFigureReceiver = 1  # noise figure [dB]

# constants
c = 3 * 10**8  # speed of light [m/s]
R_e = 6371000  # radius earth [m]
k_B = 1.3806452 * 10**(-23)  # Boltzmann's constant [J/K]

# reading excel file
teleD = pd.read_excel("telemetryData.xlsx", sheet_name="Sheet1")

# putting data into list
total_spacecraft_power = teleD.iloc[0, 1:6].tolist()  
transmitter_power_spacecraft = teleD.iloc[1, 1:6].tolist()  
transmitter_power_ground = teleD.iloc[2, 1:6].tolist()  
loss_factor_transmitter = teleD.iloc[3, 1:6].tolist()  
loss_factor_receiver = teleD.iloc[4, 1:6].tolist()  
downlink_frequency = teleD.iloc[5, 1:6].tolist()  
turnaround_ratio = teleD.iloc[6, 1:6].tolist()  
antenna_diameter_spacecraft = teleD.iloc[7, 1:6].tolist()  
antenna_diameter_ground = teleD.iloc[8, 1:6].tolist()  
orbit_altitude = teleD.iloc[9, 1:6].tolist()  
elongation_angle = teleD.iloc[10, 1:6].tolist()  
pointing_offset_angle = teleD.iloc[11, 1:6].tolist()  
uplink_data_rate = teleD.iloc[12, 1:6].tolist()  
payload_swath_width = teleD.iloc[13, 1:6].tolist()  
payload_pixel_size = teleD.iloc[14, 1:6].tolist()  
payload_bits_per_pixel = teleD.iloc[15, 1:6].tolist()  
payload_duty_cycle = teleD.iloc[16, 1:6].tolist()  
payload_downlink_time = teleD.iloc[17, 1:6].tolist()  
required_ber = teleD.iloc[18, 1:6].tolist()
zenith_attenuation = [0.035, 0.035, 0.48, 0.48, 0.49]

case = int(input("Which case study? "))

print("Uplink is: ", 
      uplinkSNR(antenna_diameter_ground[case], downlink_frequency[case], turnaround_ratio[case], loss_factor_transmitter[case], 
                transmitter_power_ground[case], orbit_altitude[case], elevation, antenna_diameter_spacecraft[case], loss_factor_receiver[case], 
                 tempAntSC, uplink_data_rate[case], pointing_offset_angle[case], rainLoss=0))
print("Downlink is: ", 
     downlinkSNR(c, noiseFigureReceiver, antenna_diameter_spacecraft[case], eta_ant, pointing_offset_angle[case], R_e, orbit_altitude[case], 
                 elevation, loss_factor_transmitter[case], transmitter_power_spacecraft[case], zenith_attenuation[case], noiseFigureReceiver, 
                 tempAntSC, payload_swath_width[case], payload_pixel_size[case], payload_bits_per_pixel[case], payload_duty_cycle[case], 
                 payload_downlink_time[case], T0))