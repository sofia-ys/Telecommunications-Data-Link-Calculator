import pygame as pg
import pandas as pd
import sys
from link import uplink
from link import downlink

pg.init()

# reading excel file
teleD = pd.read_excel("telemetryData.xlsx", sheet_name="Sheet1", engine='openpyxl')

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
zenith_attenuation = [0.035, 0.035, 0.048, 0.048, 0.049]  # 0.09
SNR = [10.5, 10.5, 10.5, 10.5, 10.5]

# constants
white = (255, 255, 255)
grey = (200, 200, 200)
brat = (137, 204, 4)
black = (0, 0, 0)
scrWidth, scrHeight = 600, 750
buttonWidth, buttonHeight = 200, 50
font = pg.font.SysFont('Arial Narrow', 24)

# screen setup
scr = pg.display.set_mode((scrWidth, scrHeight))
pg.display.set_caption("Link Budget Calculator")
clock = pg.time.Clock()

# making text on screen
def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

# creating a button on screen
def createButton(x, y, w, h, text, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    
    # change colour on hover
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(scr, brat, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pg.draw.rect(scr, white, (x, y, w, h))
    
    drawText(text, font, black, scr, x + w / 2 - font.size(text)[0] / 2, y + h / 2 - font.size(text)[1] / 2)

# input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = grey
        self.text = text
        self.txt_surface = font.render(text, True, white)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = black if self.active else grey
        
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, white)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

# Global state to track current screen
current_screen = "main"
uplink_results = []
downlink_results = []
margin = []
selected_option = None

# Labels for the input boxes
uplink_labels = [
    "Antenna diameter ground station:",
    "Downlink frequency:",
    "Turn around ratio:",
    "Loss factor transmitter:",
    "Transmitter power (ground station):",
    "Orbit altitude:",
    "Atmospheric attenuation:",
    "Antenna diameter spacecraft:",
    "Required uplink data rate:",
    "Elongation angle:",
    "Required SNR:"  # New input label for uplink
]

downlink_labels = [
    "Antenna diameter spacecraft:",
    "Downlink frequency:",
    "Antenna diameter ground station:",
    "Loss factor transmitter:",
    "Transmitter power (spacecraft):",
    "Orbit altitude:",
    "Atmospheric attenuation:",
    "Payload swath width angle:",
    "Payload bits per pixel:",
    "Payload pixel size:",
    "Pointing offset angle (spacecraft):",
    "Payload duty cycle:",
    "Payload downlink time:",
    "Elongation angle:",
    "Required SNR:"  # New input label for downlink
]

# Case study input box
case_study_input = InputBox(200, 150, 200, 50)

# Input box creation logic
input_boxes = []

def create_input_boxes(labels):
    global input_boxes
    input_boxes = []
    for i, label in enumerate(labels):
        input_box = InputBox(350, 50 + i * 40, 200, 30)  # Adjust x for input box placement
        input_boxes.append(input_box)

def input_values_screen():
    global current_screen
    current_screen = "select_uplink_downlink"

def case_study_screen():
    global current_screen
    current_screen = "case_study"

def submit_case_study():
    global current_screen, uplink_results, downlink_results, margin
    case_number = case_study_input.text
    if case_number.isdigit() and 1 <= int(case_number) <= 5:
        
        case = int(case_number) - 1

        uplinkData = uplink(antenna_diameter_ground[case], downlink_frequency[case], turnaround_ratio[case], loss_factor_transmitter[case], 
                            transmitter_power_ground[case], orbit_altitude[case], zenith_attenuation[case], antenna_diameter_spacecraft[case], 
                            uplink_data_rate[case], case, elongation_angle[case])
        downlinkData = downlink(antenna_diameter_spacecraft[case], downlink_frequency[case], antenna_diameter_ground[case], 
                                loss_factor_transmitter[case], transmitter_power_spacecraft[case], orbit_altitude[case], zenith_attenuation[case], 
                                payload_swath_width[case], payload_bits_per_pixel[case], payload_pixel_size[case], pointing_offset_angle[case], 
                                case, payload_duty_cycle[case], payload_downlink_time[case], elongation_angle[case])
        margin.append(uplinkData[0] - SNR[case])
        margin.append(downlinkData[0] - SNR[case])
        uplink_results = uplinkData
        downlink_results = downlinkData
        current_screen = "results"
    else:
        print("Invalid case study number")

def select_uplink():
    global current_screen, selected_option
    selected_option = "uplink"
    create_input_boxes(uplink_labels)
    current_screen = "input_values"

def select_downlink():
    global current_screen, selected_option
    selected_option = "downlink"
    create_input_boxes(downlink_labels)
    current_screen = "input_values"

def submit_input_values():
    global current_screen, uplink_results, downlink_results
    values = [box.text for box in input_boxes]
    # Validate if inputs are numeric if needed
    if all(values) and all(value.replace('.', '', 1).isdigit() for value in values):
        if selected_option == "uplink":
            uplink_results = uplink(values)  # Simulate uplink function
        elif selected_option == "downlink":
            downlink_results = downlink(values)  # Simulate downlink function
        current_screen = "results"
    else:
        print("Please fill all fields with valid numeric values.")

def results_screen():
    drawText("Link Budget", font, white, scr, scrWidth // 2 - font.size("Link budget")[0] // 2, 50)

    # Display Uplink Results
    drawText(f'Uplink: {uplink_results[0]}', font, brat, scr, 50, 100)
    drawText(f'Uplink margin: {margin[0]}', font, brat, scr, 50, 130)
    
    # Display individual uplink results
    drawText(f"EIRP: {uplink_results[1][0]}", font, white, scr, 50, 170)
    drawText(f"Pointingloss: {uplink_results[1][1]}", font, white, scr, 50, 200)
    drawText(f"Spaceloss: {uplink_results[1][2]}", font, white, scr, 50, 230)
    drawText(f"Atmosphereloss: {uplink_results[1][3]}", font, white, scr, 50, 260)
    drawText(f"Gain over T: {uplink_results[1][4]}", font, white, scr, 50, 290)
    drawText(f"Data Rate Loss: {uplink_results[1][5]}", font, white, scr, 50, 320)
    drawText(f"Boltzmann Gain: {uplink_results[1][6]}", font, white, scr, 50, 350)

    # Display Downlink Results
    drawText(f'Downlink: {downlink_results[0]}', font, brat, scr, 50, 390)
    drawText(f'Downlink margin: {margin[1]}', font, brat, scr, 50, 420)

    # Display individual downlink results
    drawText(f"EIRP: {downlink_results[1][0]}", font, white, scr, 50, 460)
    drawText(f"Pointingloss: {downlink_results[1][1]}", font, white, scr, 50, 490)
    drawText(f"Spaceloss: {downlink_results[1][2]}", font, white, scr, 50, 520)
    drawText(f"Atmosphereloss: {downlink_results[1][3]}", font, white, scr, 50, 550)
    drawText(f"Gain over T: {downlink_results[1][4]}", font, white, scr, 50, 580)
    drawText(f"Data Rate Loss: {downlink_results[1][5]}", font, white, scr, 50, 610)
    drawText(f"Boltzmann Gain: {downlink_results[1][6]}", font, white, scr, 50, 640)

    # Add a button to return to the main menu
    createButton(scrWidth // 2 - buttonWidth // 2, scrHeight - 80, buttonWidth, buttonHeight, "Main Menu", return_to_main)


def return_to_main():
    global current_screen
    current_screen = "main"

# Main loop
running = True
while running:
    scr.fill(black)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if current_screen == "main":
            pass
        elif current_screen == "case_study":
            case_study_input.handle_event(event)
        elif current_screen == "select_uplink_downlink":
            pass
        elif current_screen == "input_values":
            for box in input_boxes:
                box.handle_event(event)
        elif current_screen == "results":
            pass

    if current_screen == "main":
        drawText("Calculate link budget", font, white, scr, scrWidth // 2 - font.size("Calculate link budget")[0] // 2, 50)
        createButton(scrWidth // 2 - buttonWidth // 2, 150, buttonWidth, buttonHeight, "Case Study", case_study_screen)
        createButton(scrWidth // 2 - buttonWidth // 2, 250, buttonWidth, buttonHeight, "Input Values", input_values_screen)

    elif current_screen == "case_study":
        drawText("Which case study? (1-5)", font, white, scr, scrWidth // 2 - font.size("Which case study? (1-5)")[0] // 2, 100)
        case_study_input.update()
        case_study_input.draw(scr)
        createButton(scrWidth // 2 - buttonWidth // 2, 300, buttonWidth, buttonHeight, "Submit", submit_case_study)

    elif current_screen == "select_uplink_downlink":
        drawText("Select Uplink or Downlink", font, white, scr, scrWidth // 2 - font.size("Select Uplink or Downlink")[0] // 2, 100)
        createButton(scrWidth // 2 - buttonWidth // 2, 200, buttonWidth, buttonHeight, "Uplink", select_uplink)
        createButton(scrWidth // 2 - buttonWidth // 2, 300, buttonWidth, buttonHeight, "Downlink", select_downlink)

    elif current_screen == "input_values":
        for i, label in enumerate(uplink_labels if selected_option == "uplink" else downlink_labels):
            drawText(label, font, white, scr, 50, 50 + i * 40)
        for box in input_boxes:
            box.update()
            box.draw(scr)
        createButton(scrWidth // 2 - buttonWidth // 2, scrHeight - 80, buttonWidth, buttonHeight, "Submit", submit_input_values)

    elif current_screen == "results":
        results_screen()

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
