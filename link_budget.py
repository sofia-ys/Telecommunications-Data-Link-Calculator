from uplink import uplinkSNR
from downlink import downlinkSNR
import pdfplumber

# pdf path on my laptop
pdf_path = 'C:\Users\syane\OneDrive\Documents\GitHub\Telecommunications-Data-Link-Calculator\Space Tutorial and Preparation - Spacecraft Tutorial Assignment.pdf'

# Initialize empty lists to store the values for each category
total_spacecraft_power = []
transmitter_power_spacecraft = []
transmitter_power_ground = []
loss_factor_transmitter = []
loss_factor_receiver = []
downlink_frequency = []
turnaround_ratio = []
antenna_diameter_spacecraft = []
antenna_diameter_ground = []
orbit_altitude = []
elongation_angle = []
pointing_offset_angle = []
uplink_data_rate = []
payload_swath_width = []
payload_pixel_size = []
payload_bits_per_pixel = []
payload_duty_cycle = []
payload_downlink_time = []
modulation_coding_type = []
required_ber = []

# Open the PDF
with pdfplumber.open(pdf_path) as pdf:
    # Iterate through the pages
    for page in pdf.pages:
        # Extract text from the page
        text = page.extract_text()

        # Search for the table where the data is listed
        if "Total spacecraft power" in text:
            # Split the text into lines
            lines = text.split('\n')
            
            # Loop through each line to find the relevant data
            for line in lines:
                if "Total spacecraft power" in line:
                    total_spacecraft_power = [int(value) for value in line.split()[-5:]]
                elif "Transmitter power" in line and "spacecraft" in line:
                    transmitter_power_spacecraft = [int(value) for value in line.split()[-5:]]
                elif "Transmitter power" in line and "ground station" in line:
                    transmitter_power_ground = [int(value) for value in line.split()[-5:]]
                elif "Loss factor transmitter" in line:
                    loss_factor_transmitter = [float(value) for value in line.split()[-5:]]
                elif "Loss factor receiver" in line:
                    loss_factor_receiver = [float(value) for value in line.split()[-5:]]
                elif "Downlink frequency" in line:
                    downlink_frequency = [float(value.replace("S-Band", "").replace("X-Band", "")) for value in line.split()[-5:]]
                elif "Turn around ratio" in line:
                    turnaround_ratio = [value for value in line.split()[-5:]]
                elif "Antenna diameter spacecraft" in line:
                    antenna_diameter_spacecraft = [float(value) for value in line.split()[-5:]]
                elif "Antenna diameter ground" in line:
                    antenna_diameter_ground = [float(value) for value in line.split()[-5:]]
                elif "Orbit altitude" in line:
                    orbit_altitude = [int(value) for value in line.split()[-5:]]
                elif "Elongation angle" in line:
                    elongation_angle = [value if value != "N/A" else None for value in line.split()[-5:]]
                elif "Pointing offset angle" in line:
                    pointing_offset_angle = [float(value) for value in line.split()[-5:]]
                elif "Required uplink data rate" in line:
                    uplink_data_rate = [int(value) for value in line.split()[-5:]]
                elif "Payload swath width" in line:
                    payload_swath_width = [int(value) for value in line.split()[-5:]]
                elif "Payload pixel size" in line:
                    payload_pixel_size = [float(value) for value in line.split()[-5:]]
                elif "Payload bits per pixel" in line:
                    payload_bits_per_pixel = [int(value) for value in line.split()[-5:]]
                elif "Payload duty cycle" in line:
                    payload_duty_cycle = [value.replace("%", "") for value in line.split()[-5:]]
                elif "Payload downlink time" in line:
                    payload_downlink_time = [value for value in line.split()[-5:]]
                elif "Modulation/coding type" in line:
                    modulation_coding_type = [value for value in line.split()[-5:]]
                elif "Required BER" in line:
                    required_ber = [value for value in line.split()[-5:]]

# Print out all the extracted data lists
print(f"Total spacecraft power: {total_spacecraft_power}")
print(f"Transmitter power (spacecraft): {transmitter_power_spacecraft}")
print(f"Transmitter power (ground): {transmitter_power_ground}")
print(f"Loss factor transmitter: {loss_factor_transmitter}")
print(f"Loss factor receiver: {loss_factor_receiver}")
print(f"Downlink frequency: {downlink_frequency}")
print(f"Turnaround ratio: {turnaround_ratio}")
print(f"Antenna diameter (spacecraft): {antenna_diameter_spacecraft}")
print(f"Antenna diameter (ground): {antenna_diameter_ground}")
print(f"Orbit altitude: {orbit_altitude}")
print(f"Elongation angle: {elongation_angle}")
print(f"Pointing offset angle: {pointing_offset_angle}")
print(f"Required uplink data rate: {uplink_data_rate}")
print(f"Payload swath width: {payload_swath_width}")
print(f"Payload pixel size: {payload_pixel_size}")
print(f"Payload bits per pixel: {payload_bits_per_pixel}")
print(f"Payload duty cycle: {payload_duty_cycle}")
print(f"Payload downlink time: {payload_downlink_time}")
print(f"Modulation/coding type: {modulation_coding_type}")
print(f"Required BER: {required_ber}")


uplinkSNR()
downlinkSNR()