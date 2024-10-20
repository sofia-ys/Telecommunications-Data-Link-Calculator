import pygame as pg
import pandas as pd
import sys
from link import uplink
from link import downlink

pg.init()

# constants
white = (255, 255, 255)
grey = (200, 200, 200)
brat = (137, 204, 4)
black = (31, 31, 31)
scrWidth, scrHeight = 600, 730
buttonWidth, buttonHeight = 200, 50
font = pg.font.SysFont('Arial Narrow', 30)

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

# screen setup
scr = pg.display.set_mode((scrWidth, scrHeight))
pg.display.set_caption("Link Budget Calculator")
clock = pg.time.Clock()

# making text on screen
def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
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
    
    drawText(text, font, black, scr, x + w / 2, y + h / 2)

# input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)   # Defines the box's position and size
        self.color = grey                 # Default color of the box (gray)
        self.text = text                  # The current text inside the box
        self.txt_surface = font.render(text, True, white)  # Rendered version of the text for display
        self.active = False               # Whether the box is active (selected for input)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Activate the box if clicked
            else:
                self.active = False            # Deactivate if clicked outside
            self.color = black if self.active else grey  # Change color based on active status
        
        if event.type == pg.KEYDOWN:
            if self.active:  # Only accept input if the box is active
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]  # Delete the last character
                else:
                    self.text += event.unicode  # Add the new character
                self.txt_surface = font.render(self.text, True, white)  # Update the rendered text

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)  # Dynamically adjust the box width
        self.rect.w = width

    def draw(self, screen):
        # Draw the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Draw the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

# Global state to track current screen
current_screen = "main"
uplink_results = []
downlink_results = []
selected_option = None  # New variable to track the user's choice between Uplink/Downlink

# List of input boxes for the "input values" screen
input_boxes = []
for i in range(19):
    input_box = InputBox(50, 50 + i * 30, 200, 30)  # stacks the boxes vertically since the y value changes 
    input_boxes.append(input_box)

# Case study input box
case_study_input = InputBox(50, 150, 200, 50)  # x position, y positon, box width, box height

# Handle case study button action
def case_study_screen():
    global current_screen
    current_screen = "case_study"

def input_values_screen():
    global current_screen
    current_screen = "select_uplink_downlink"  # New screen for selecting between uplink and downlink

def submit_case_study():
    global current_screen, uplink_results, downlink_results
    case_number = case_study_input.text
    if case_number.isdigit() and 1 <= int(case_number) <= 5:
        case = int(case_number) - 1

        # Call uplink and downlink once
        uplinkData = uplink(
            antenna_diameter_ground[case], downlink_frequency[case], turnaround_ratio[case], 
            loss_factor_transmitter[case], transmitter_power_ground[case], orbit_altitude[case], 
            zenith_attenuation[case], antenna_diameter_spacecraft[case], uplink_data_rate[case], 
            case, elongation_angle[case]
        )

        downlinkData = downlink(
            antenna_diameter_spacecraft[case], downlink_frequency[case], antenna_diameter_ground[case], 
            loss_factor_transmitter[case], transmitter_power_spacecraft[case], orbit_altitude[case], 
            zenith_attenuation[case], payload_swath_width[case], payload_bits_per_pixel[case], 
            payload_pixel_size[case], pointing_offset_angle[case], case, payload_duty_cycle[case], 
            payload_downlink_time[case], elongation_angle[case]
        )

        # Store the results
        uplink_results = uplinkData
        downlink_results = downlinkData
        current_screen = "results"
    else:
        print("Invalid case study number")

def select_uplink():
    global current_screen, selected_option, input_boxes
    selected_option = "uplink"
    current_screen = "input_values"
    input_boxes = []  # Reset input boxes
    for i in range(10):  # Generate 10 boxes for Uplink
        input_box = InputBox(50, 50 + i * 30, 200, 30)
        input_boxes.append(input_box)

def select_downlink():
    global current_screen, selected_option, input_boxes
    selected_option = "downlink"
    current_screen = "input_values"
    input_boxes = []  # Reset input boxes
    for i in range(14):  # Generate 14 boxes for Downlink
        input_box = InputBox(50, 50 + i * 30, 200, 30)
        input_boxes.append(input_box)

def submit_input_values():
    global current_screen, uplink_results, downlink_results
    values = [box.text for box in input_boxes]
    if all(values):
        if selected_option == "uplink":
            uplinkData = uplink(values)
            uplink_results = uplinkData
        elif selected_option == "downlink":
            downlinkData = downlink(values)
            downlink_results = downlinkData
        current_screen = "results"
    else:
        print("Please fill all fields")

def results_screen():
    drawText("Link Budget", font, white, scr, scrWidth // 2, 50)
    if selected_option == "uplink":
        drawText("Uplink:", font, white, scr, scrWidth // 2, 100)
        for i, result in enumerate(uplink_results):
            drawText(f"{result}", font, white, scr, scrWidth // 2, 140 + i * 30)
    elif selected_option == "downlink":
        drawText("Downlink:", font, white, scr, scrWidth // 2, 300)
        for i, result in enumerate(downlink_results):
            drawText(f"{result}", font, white, scr, scrWidth // 2, 340 + i * 30)
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
            pass  # No event handling needed here
        elif current_screen == "input_values":
            for box in input_boxes:
                box.handle_event(event)
        elif current_screen == "results":
            pass

    if current_screen == "main":
        # Main screen buttons (same as before)
        createButton(scrWidth // 2 - buttonWidth // 2, 150, buttonWidth, buttonHeight, "Case Study", case_study_screen)
        createButton(scrWidth // 2 - buttonWidth // 2, 250, buttonWidth, buttonHeight, "Input Values", input_values_screen)

    elif current_screen == "case_study":
        drawText("Which case study? (1-5)", font, white, scr, scrWidth // 2, 100)
        case_study_input.update()
        case_study_input.draw(scr)
        createButton(scrWidth // 2 - buttonWidth // 2, 300, buttonWidth, buttonHeight, "Submit", submit_case_study)

    elif current_screen == "select_uplink_downlink":
        drawText("Select Uplink or Downlink", font, white, scr, scrWidth // 2, 100)
        createButton(scrWidth // 2 - buttonWidth // 2, 200, buttonWidth, buttonHeight, "Uplink", select_uplink)
        createButton(scrWidth // 2 - buttonWidth // 2, 300, buttonWidth, buttonHeight, "Downlink", select_downlink)

    elif current_screen == "input_values":
        drawText(f"Input Values for {selected_option.capitalize()}", font, white, scr, scrWidth // 2, 20)
        for box in input_boxes:
            box.update()
            box.draw(scr)
        createButton(scrWidth // 2 - buttonWidth // 2, scrHeight - 80, buttonWidth, buttonHeight, "Submit", submit_input_values)

    elif current_screen == "results":
        results_screen()

    pg.display.flip()
    clock.tick(30)

pg.quit()
sys.exit()