from json import tool
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide" # just for nice stdout

import pygame
import pupil_classes
import asyncio
import random
import math
import copy

size_window = 800
tooltip_extra_size = 300
point_radius = 3
font_size = 20
button_offset = 25
button_size = 50

day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time = ["Morning", "Afternoon"]

class Point:
    def __init__(self, pos: tuple[int,int], name: str, pygame_properties: dict, pupil=None):
        self.x = (400-pos[0])*1.59655 + 400 # ratio between lat and long
        self.y = pos[1]
        self.name = name
        self.pupil = pupil

        self.pygame_properties = pygame_properties # was initially meant to hold more but now only holds the colour

    def __repr__(self):
        return f"{self.name}"

async def visualize(results: list[dict]):
    pygame.init()

    font = pygame.font.SysFont(None, font_size)

    screen = pygame.display.set_mode([size_window+tooltip_extra_size,size_window]) # +300 to offset for tooltips
    pygame.display.set_caption("visualizer")

    running = True
    objects = []
    
    SCHOOL_PUPIL = await pupil_classes.create_Pupil(-1, "School", "GU1 3BB", False, False, 0, [(0,0)] * 5)
    school = Point(
        (size_window / 2, size_window / 2),
        "School",
        {
            "color": (255,255,255)
        },
        SCHOOL_PUPIL
    )
    objects.append([school])

    current_selection = 9
    title = None

    def draw_obj(obj: list[Point], do_bold=False, closest_point=None, closest_length=None):
        if current_selection % 2 == 1:
            obj = obj[::-1]

        for i,point in enumerate(obj): # draw lines in a bit
            bold = False
            if do_bold and closest_point is not None and closest_length <= point_radius+2:
                bold = closest_point.pupil == point.pupil
            width = [1, 4][bold]
            point_radius_extra = [0, 3][bold]
            pygame.draw.circle(
                surface = screen,
                color = point.pygame_properties["color"],
                center = (point.x,point.y),
                radius = point_radius + point_radius_extra
            )
            
            if current_selection % 2 == 0: # ugly
                if i == len(obj)-1:
                    pygame.draw.line(
                        surface = screen,
                        color = point.pygame_properties["color"],
                        start_pos = (point.x,point.y),
                        end_pos = (school.x,school.y),
                        width = width
                    )
                else:
                    pygame.draw.line(
                        surface = screen,
                        color = point.pygame_properties["color"],
                        start_pos = (point.x,point.y),
                        end_pos = (obj[i+1].x,obj[i+1].y),
                        width = width
                    )
            else:
                if i == 0:
                    pygame.draw.line(
                        surface = screen,
                        color = point.pygame_properties["color"],
                        start_pos = (point.x,point.y),
                        end_pos = (school.x,school.y),
                        width = width
                    )
                else:
                    pygame.draw.line(
                        surface = screen,
                        color = point.pygame_properties["color"],
                        start_pos = (point.x,point.y),
                        end_pos = (obj[i-1].x,obj[i-1].y),
                        width = width
                    )

    def update_selection(right: bool, current_choice: int):
        updated_choice = (current_choice + (1 if right else -1)) % 10
        title = font.render(f"{day[updated_choice // 2]} {time[updated_choice % 2]}", True, (255,255,255))

        selection = results[updated_choice]
        groups = selection["groups"]

        all_grouped_points = []

        for time_allocation in groups:
            for group in time_allocation:
                group_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                group_points = []
                for person in group.people:
                    x = person.latitude - SCHOOL_PUPIL.latitude
                    y = person.longitude - SCHOOL_PUPIL.longitude

                    offsetX = round(x / 0.00125)
                    offsetY = round(y / 0.00125) # 0.467 = 400, rounded to 0.5 for ease
                    personal_point = Point(
                        ((size_window / 2) + offsetX, (size_window / 2) + offsetY),
                        person.name,
                        {
                            "color": group_color
                        },
                        person
                    )
                    group_points.append(personal_point)
                all_grouped_points.append(group_points)
        return updated_choice,all_grouped_points,title
    
    def draw_buttons():
        left_btn = pygame.draw.rect(
            surface = screen,
            color = (255,255,255),
            rect = pygame.Rect(button_offset,size_window - button_offset - button_size,button_size, button_size)
        )
        left = font.render("<", True, (0,0,0))
        screen.blit(left,(int(button_offset + (9/20)*button_size), int(size_window - button_offset - (25/40)*button_size))) # what are these numbers

        right_btn = pygame.draw.rect(
            surface = screen,
            color = (255,255,255),
            rect = pygame.Rect(size_window+tooltip_extra_size-button_offset - button_size, size_window - button_offset - button_size, button_size, button_size) # pep8
        )
        right = font.render(">", True, (0,0,0))
        screen.blit(right,(int(size_window+tooltip_extra_size-button_offset-(11/20)*(button_size)),int(size_window-button_offset-(25/40)*button_size)))

        return left_btn,right_btn

    objects = [objects[0]] # need to go together otherwise end up using global keyword 
    current_selection, grouped_points, title = update_selection(True, current_selection)
    objects = [*objects, *grouped_points]

    while running:
        screen.fill((0,0,0))

        # title
        screen.blit(title, ((size_window+200)/2, 50))

        # buttons
        left_btn,right_btn = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if left_btn.collidepoint(pos):
                    objects = [objects[0]] # need to go together otherwise end up using global keyword
                    current_selection, grouped_points, title = update_selection(False, current_selection)
                    objects = [*objects, *grouped_points]
                elif right_btn.collidepoint(pos):
                    objects = [objects[0]] # need to go together otherwise end up using global keyword 
                    current_selection, grouped_points, title = update_selection(True, current_selection)
                    objects = [*objects, *grouped_points]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    objects = [objects[0]] # need to go together otherwise end up using global keyword
                    current_selection, grouped_points, title = update_selection(False, current_selection)
                    objects = [*objects, *grouped_points]
                elif event.key == pygame.K_RIGHT:
                    objects = [objects[0]] # need to go together otherwise end up using global keyword 
                    current_selection, grouped_points, title = update_selection(True, current_selection)
                    objects = [*objects, *grouped_points]

        closest_point = None
        closest_length = 800
        group_associated = None
        mouse_pos = pygame.mouse.get_pos()

        for group in objects:
            for point in group:
                dist_x = mouse_pos[0] - point.x
                dist_y = mouse_pos[1] - point.y

                if math.hypot(dist_x,dist_y) < closest_length:
                    closest_point = point
                    closest_length = math.hypot(dist_x,dist_y)
                    group_associated = group

        if closest_point is not None and closest_length <= point_radius+2:
            pupil = closest_point.pupil
            pupil_group = copy.copy(group_associated)
            pupil_group.remove(closest_point)
            school_time = pupil.times[current_selection // 2][current_selection % 2]
            formatted_time = f"{'' if len(str(school_time // 60)) == 2 else '0'}{school_time // 60}:{'' if len(str(school_time % 60)) == 2 else '0'}{school_time % 60}"
            details = f"""{pupil.name}
{pupil.postcode}
Wants to share: {("No", "Yes")[int(pupil.will_share_others)]}
Wants to freeload: {("No", "Yes")[int(pupil.will_join_others)]}
Spare seats: {pupil.spare_seats}
{["Arrival", "Departure"][current_selection % 2]} time: {formatted_time}
Location: {pupil.latitude}, {pupil.longitude}
Riding with: {"Nobody" if len(pupil_group) == 0 else ", ".join([point.pupil.name for point in pupil_group])}
Driver: {group_associated[0].pupil.name}"""

            offset = 50
            for line in details.split("\n"):
                img = font.render(line, True, (255,255,255))
                screen.blit(img,(size_window-80,offset))
                offset += font_size + 5

        for j, obj in enumerate(objects[::-1]): # reversed so school point is on top
            draw_obj(obj, True, closest_point, closest_length)

        pygame.display.update()
    
    pygame.quit()
        
if __name__ == "__main__":
    asyncio.run(visualize([]))