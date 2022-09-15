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

day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time = ["Morning", "Afternoon"]

class Point:
    def __init__(self, pos: tuple[int,int], name: str, pygame_properties: dict, pupil=None):
        self.x = pos[0]
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
    
    SCHOOL_PUPIL = await pupil_classes.create_Pupil(-1, "School", "GU1 3BB", False, False, 0, [])
    school = Point(
        (size_window / 2, size_window / 2),
        "School",
        {
            "color": (255,255,255)
        },
        SCHOOL_PUPIL
    )
    objects.append([school])

    def draw_obj(obj: list[Point]):
        for i,point in enumerate(obj): # draw lines in a bit
            pygame.draw.circle(
                surface = screen,
                color = point.pygame_properties["color"],
                center = (point.x,point.y),
                radius = point_radius
            )
            
            if i == len(obj)-1:
                pygame.draw.line(
                    surface = screen,
                    color = point.pygame_properties["color"],
                    start_pos = (point.x,point.y),
                    end_pos = (school.x,school.y)
                )
            else:
                pygame.draw.line(
                    surface = screen,
                    color = point.pygame_properties["color"],
                    start_pos = (point.x,point.y),
                    end_pos = (obj[i+1].x,obj[i+1].y)
                )

    current_selection = 9
    title = None

    def update_selection(right: bool, current_choice: int):
        updated_choice = (current_choice + (1 if right else -1)) % 10
        title = font.render(f"{day[updated_choice // 2]} {time[updated_choice % 2]}")

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
                

    objects = [objects[0]] # need to go together otherwise end up using global keyword 
    current_selection, grouped_points, title = update_selection(True, current_selection)
    objects = [*objects, *grouped_points]

    while running:
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        if closest_point is not None and closest_length <= point_radius:
            pupil = closest_point.pupil
            pupil_group = copy.copy(group_associated)
            pupil_group.remove(closest_point)
            details = f"""{pupil.name}
{pupil.postcode}
Wants to share: {("No", "Yes")[int(pupil.will_share_others)]}
Wants to freeload: {("No", "Yes")[int(pupil.will_join_others)]}
Spare seats: {pupil.spare_seats}
Location: {pupil.latitude}, {pupil.longitude}
Riding with: {"Nobody" if len(pupil_group) == 0 else ", ".join([point.pupil.name for point in pupil_group])}
Driver: {group_associated[0].pupil.name}"""

            offset = 50
            for line in details.split("\n"):
                img = font.render(line, True, (255,255,255))
                screen.blit(img,(size_window-100,offset))
                offset += font_size + 5

        for obj in objects[::-1]: # reversed so school point is on top
            draw_obj(obj)

        pygame.display.update()
    
    pygame.quit()
        
if __name__ == "__main__":
    asyncio.run(visualize([]))