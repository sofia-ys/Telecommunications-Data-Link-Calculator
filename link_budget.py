import pandas as pd 
from link import uplink, downlink

"""CODING TYPES"""
UNCODED = 10.5
REEDSOLOMON = 6.4
CONVOLUTIONAL = 4.8
TURBOCODE = 1
AWGN = 0.2

MARGIN = 3

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
print('\n')

uplinkData = uplink(antenna_diameter_ground[case], downlink_frequency[case], turnaround_ratio[case], loss_factor_transmitter[case], transmitter_power_ground[case],
                    orbit_altitude[case], zenith_attenuation[case], antenna_diameter_spacecraft[case], uplink_data_rate[case], case, elongation_angle[case])

downlinkData = downlink(antenna_diameter_spacecraft[case], downlink_frequency[case], antenna_diameter_ground[case], loss_factor_transmitter[case], transmitter_power_spacecraft[case], orbit_altitude[case],
                        zenith_attenuation[case], payload_swath_width[case], payload_bits_per_pixel[case], payload_pixel_size[case], pointing_offset_angle[case], case,
                        payload_duty_cycle[case], payload_downlink_time[case], elongation_angle[case])

print(f'Uplink: {uplinkData[0]}')
print('\n')
if (uplinkData[0]-MARGIN)> UNCODED: print('Closed with uncoded'); print(f"Margin: {uplinkData[0]-UNCODED}")
elif (uplinkData[0]-MARGIN)> REEDSOLOMON: print('Closed with reed solomon'); print(f"Margin: {uplinkData[0]-REEDSOLOMON}")
elif (uplinkData[0]-MARGIN)> CONVOLUTIONAL: print('Closed with convolutional'); print(f"Margin: {uplinkData[0]-CONVOLUTIONAL}")
elif (uplinkData[0]-MARGIN)> TURBOCODE: print('Closed with turbo code'); print(f"Margin: {uplinkData[0]-TURBOCODE}")
elif (uplinkData[0]-MARGIN)> AWGN: print('Closed with awgn'); print(f"Margin: {uplinkData[0]-AWGN}")
else: print('not closed')
print('\n')

print(f"EIRP: {uplinkData[1][0]}")
print(f"Pointingloss: {uplinkData[1][1]}")
print(f"Spaceloss: {uplinkData[1][2]}")
print(f"atmosphereloss: {uplinkData[1][3]}")
print(f"gain over t: {uplinkData[1][4]}")
print(f"data rate loss: {uplinkData[1][5]}")
print(f"boltzmanngain: {uplinkData[1][6]}")

print('\n')
print('\n')
print('\n')

print(f'Downlink: {downlinkData[0]}')
print('\n')
if (downlinkData[0]-MARGIN)> UNCODED: print('Closed with uncoded');print(f"Margin: {downlinkData[0]-UNCODED}")
elif (downlinkData[0]-MARGIN)> REEDSOLOMON: print('Closed with reed solomon');print(f"Margin: {downlinkData[0]-REEDSOLOMON}")
elif (downlinkData[0]-MARGIN)> CONVOLUTIONAL: print('Closed with convolutional');print(f"Margin: {downlinkData[0]-CONVOLUTIONAL}")
elif (downlinkData[0]-MARGIN)> TURBOCODE: print('Closed with turbo code');print(f"Margin: {downlinkData[0]-TURBOCODE}")
elif (downlinkData[0]-MARGIN)> AWGN: print('Closed with awgn');print(f"Margin: {downlinkData[0]-AWGN}")
else: print('not closed')
print('\n')

print(f"EIRP: {downlinkData[1][0]}")
print(f"Pointingloss: {downlinkData[1][1]}")
print(f"Spaceloss: {downlinkData[1][2]}")
print(f"atmosphereloss: {downlinkData[1][3]}")
print(f"gain over t: {downlinkData[1][4]}")
print(f"data rate loss: {downlinkData[1][5]}")
print(f"boltzmanngain: {downlinkData[1][6]}")
print('\n')