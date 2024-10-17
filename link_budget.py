import pandas as pd 
import numpy as np
from uplink import uplink
from downlink import downlinkSNR

# assumed values
eta_ant = 0.55  # antenna efficiency [-]
elevation = np.radians(10)  # minimum elevation [rad]
zenith_attenuation = [0.035, 0.035, 0.48, 0.48, 0.49]  # zenith attenuation from graph
T0 = 290  # reference temperature [K]
tempAntSC = 25  # antenna noise [K]
noiseFigureReceiverTX = 1  # noise figure [dB]

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
zenith_attenuation = [0.035, 0.035, 0.048, 0.048, 0.049]

case = int(input("Which case study? "))-1


uplinkData =  uplink(antenna_diameter_ground[case], downlink_frequency[case], turnaround_ratio[case], loss_factor_transmitter[case], 
                transmitter_power_ground[case], orbit_altitude[case], zenith_attenuation[case], antenna_diameter_spacecraft[case],
                uplink_data_rate[case], case, elongation_angle[case])
print(f"The SNR of uplink is {round(uplinkData[0], 2)}")
print(f"The EIRP is {round(uplinkData[1][0], 2)}")
print(f"The Pointing loss is {round(uplinkData[1][1], 2)}")
print(f"The Free space loss is {round(uplinkData[1][2], 2)}")
print(f"The atmospheric loss is {round(uplinkData[1][3], 2)}")
print(f"The G/T is {round(uplinkData[1][4], 2)}")
print(f"The Required data rate is {round(uplinkData[1][5], 2)}")
print(f"The Boltzmann is {round(uplinkData[1][6], 2)}")



print("Downlink is: ", 
     downlinkSNR(c, downlink_frequency[case], antenna_diameter_spacecraft[case], eta_ant, pointing_offset_angle[case], R_e, orbit_altitude[case], 
                 elevation, loss_factor_transmitter[case], transmitter_power_spacecraft[case], zenith_attenuation[case], noiseFigureReceiverTX, 
                 tempAntSC, payload_swath_width[case], payload_pixel_size[case], payload_bits_per_pixel[case], payload_duty_cycle[case], 
                 payload_downlink_time[case], T0))