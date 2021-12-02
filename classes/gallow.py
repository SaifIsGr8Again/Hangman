"""
Module for drawing the gallow.
"""
from random import uniform, randint
from math import sqrt, ceil, sin, cos, radians, copysign
import pygame as pg
from pygame import gfxdraw as gfx

class Gallow:
    """
    Class for modelling the gallow in hangman. It provides methods for drawing the gallow,
    adapting to the screen dimensions.
    """
    black = (0, 0, 0)
    white = (255, 255, 255)
    rope_clr = (255, 215, 51)
    def __init__(self, current_dir, window, origin, size_adjust, base):
        self.current_dir = current_dir
        self.origin = (origin[0], origin[1])
        self.window = window
        self.window_dims = (window.get_rect()[2], window.get_rect()[3])
        self.base = base
        self.gallow_data = {"images": [], "parts": {}}
        self.gallow_data["textures"] = (pg.image.load(self.current_dir + "images\\wood.jpg"),
                                        pg.image.load(self.current_dir + "images\\wood_2.jpg"))
        self.size_adjust = size_adjust
        self.hang_progress = 0
        self.full_rope_length = 0
    def rand_part_of_img(self, width, height, img):
        """
        Adds a random part with the dimensions of (width, height)
        from a given image to self.gallow_images.\n
        @param width: The width of the shape.\n
        @param height: The height of the image.\n
        @param img: The image to crop from.
        """
        self.gallow_data["images"].append(pg.Surface((width, height)))
        width_diff = width - img.get_rect()[2]
        height_diff = height - img.get_rect()[3]
        rand_coords = (uniform(width_diff, 0), uniform(height_diff, 0))
        self.gallow_data["images"][-1].blit(img, rand_coords)
    def pre_load_bases(self):
        """
        Pre-loads random images for the bases of the gallow.
        """
        self.gallow_data["parts"]["base"] = {"x_pos": [0, 0]}
        self.gallow_data["parts"]["base"]["width"] = 20 * self.size_adjust
        self.gallow_data["parts"]["base"]["height"] = 75 * self.size_adjust
        base_width = self.gallow_data["parts"]["base"]["width"]
        base_height = self.gallow_data["parts"]["base"]["height"]
        for i in range(0, 2):
            self.rand_part_of_img(base_width, base_height, self.gallow_data["textures"][0])
            x_pos = (i * 3 + 1) / 7 * self.window_dims[0] - base_width / 2
            self.gallow_data["parts"]["base"]["x_pos"][i] = x_pos
        self.gallow_data["parts"]["base"]["y_pos"] = self.base - base_height
    def pre_load_stage(self):
        """
        Pre-loads a random image for the stage of the gallow.
        """
        x_pos_1 = self.gallow_data["parts"]["base"]["x_pos"][1]
        x_pos_2 = self.gallow_data["parts"]["base"]["x_pos"][0]
        base_width = self.gallow_data["parts"]["base"]["width"]
        self.gallow_data["parts"]["stage"] = {}
        self.gallow_data["parts"]["stage"]["width"] = ceil(x_pos_1 - x_pos_2 + base_width)
        self.gallow_data["parts"]["stage"]["height"] = 20 * self.size_adjust
        stage_width = self.gallow_data["parts"]["stage"]["width"]
        stage_height = self.gallow_data["parts"]["stage"]["height"]
        texture = pg.transform.rotate(self.gallow_data["textures"][0], 90)
        self.rand_part_of_img(stage_width, stage_height, texture)
        base_y = self.gallow_data["parts"]["base"]["y_pos"]
        self.gallow_data["parts"]["stage"]["x_pos"] = self.gallow_data["parts"]["base"]["x_pos"][0]
        self.gallow_data["parts"]["stage"]["y_pos"] = base_y - stage_height
    def pre_load_stares(self):
        """
        Pre-loads a random image for the stares of the gallow.
        """
        self.gallow_data["parts"]["stairs"] = {}
        points = [(self.gallow_data["parts"]["stage"]["x_pos"] + self.origin[0],
                   self.gallow_data["parts"]["stage"]["y_pos"] + self.origin[1])]
        num_stairs = 6
        width = self.gallow_data["parts"]["stage"]["x_pos"]
        height = self.base - self.gallow_data["parts"]["stage"]["y_pos"]
        step_width = width / num_stairs
        step_height = height / num_stairs
        for i in range(1, num_stairs + 1):
            points.append((points[-1][0] - step_width, points[-1][1]))
            points.append((points[-1][0], points[-1][1] + step_height))
        points.append((self.gallow_data["parts"]["stage"]["x_pos"] + self.origin[0],
                       self.gallow_data["parts"]["stage"]["y_pos"] + height + self.origin[1]))
        self.gallow_data["parts"]["stairs"]["points"] = points
        self.gallow_data["parts"]["stairs"]["width"] = width
        self.gallow_data["parts"]["stairs"]["height"] = height
        self.gallow_data["parts"]["stairs"]["step_width"] = step_width
        self.gallow_data["parts"]["stairs"]["step_height"] = step_height
    def pre_load_post(self):
        """
        Pre-loads random images for the post.
        """
        width = 20 * self.size_adjust
        height = 400 * self.size_adjust
        stage_width = self.gallow_data["parts"]["stage"]["width"]
        stage_x_pos = self.gallow_data["parts"]["stage"]["x_pos"]
        stage_y_pos = self.gallow_data["parts"]["stage"]["y_pos"]
        self.gallow_data["parts"]["post"] = {}
        self.gallow_data["parts"]["post"]["width"] = width
        self.gallow_data["parts"]["post"]["height"] = height
        self.gallow_data["parts"]["post"]["x_pos"] = ceil(stage_x_pos + 0.25 * stage_width)
        self.gallow_data["parts"]["post"]["y_pos"] = stage_y_pos - height
        self.rand_part_of_img(width, height, self.gallow_data["textures"][0])
    def pre_load_post_extension(self):
        """
        Pre-loads random images for the post-extension.
        """
        width = 200 * self.size_adjust
        height = 20 * self.size_adjust
        post_width = self.gallow_data["parts"]["post"]["width"]
        post_x_pos = self.gallow_data["parts"]["post"]["x_pos"]
        post_y_pos = self.gallow_data["parts"]["post"]["y_pos"]
        self.gallow_data["parts"]["post_extension"] = {}
        self.gallow_data["parts"]["post_extension"]["width"] = width
        self.gallow_data["parts"]["post_extension"]["height"] = height
        self.gallow_data["parts"]["post_extension"]["x_pos"] = int(post_x_pos + post_width)
        self.gallow_data["parts"]["post_extension"]["y_pos"] = post_y_pos
        texture = pg.transform.rotate(self.gallow_data["textures"][0], 90)
        self.rand_part_of_img(width, height, texture)
    def pre_load_support(self):
        """
        Pre-loads random images for the joint support between the post and its extension.
        """
        self.gallow_data["parts"]["support"] = {}
        width = 10 * self.size_adjust
        side_length = 75 * self.size_adjust
        post_point_x = self.gallow_data["parts"]["post"]["x_pos"]
        post_point_y = self.gallow_data["parts"]["post"]["y_pos"] + side_length
        extension_point_x = self.gallow_data["parts"]["post_extension"]["x_pos"] + side_length
        thickness = self.gallow_data["parts"]["post_extension"]["height"]
        extension_point_y = self.gallow_data["parts"]["post_extension"]["y_pos"] + thickness
        self.gallow_data["parts"]["support"]["points"] = [(post_point_x, post_point_y),
                                                          (extension_point_x, extension_point_y)]
        height = sqrt((post_point_x - extension_point_x)**2 + (post_point_y - extension_point_y)**2)
        self.gallow_data["parts"]["support"]["width"] = width
        self.gallow_data["parts"]["support"]["height"] = height
        self.gallow_data["parts"]["support"]["side_length"] = side_length
        texture = pg.transform.rotate(self.gallow_data["textures"][1], -45)
        self.rand_part_of_img(width, height, texture)
    def pre_load_man(self):
        """
        Pre-loads the parts of the man to be hanged.
        """
        self.gallow_data["parts"]["man"] = {}
        self.gallow_data["parts"]["man"]["rope_thickness"] = round(3 * self.size_adjust)
        thickness = self.gallow_data["parts"]["man"]["rope_thickness"]
        post_extension_x = self.gallow_data["parts"]["post_extension"]["x_pos"]
        stage_y = self.gallow_data["parts"]["stage"]["y_pos"]
        post_extension_width = self.gallow_data["parts"]["post_extension"]["width"]
        mid_stage = (post_extension_x + post_extension_width + self.origin[0],
                     stage_y + self.origin[1])
        leg_intersection = (mid_stage[0] - thickness, mid_stage[1] - 50 * self.size_adjust)
        arm_intersection = (leg_intersection[0], leg_intersection[1] - 65 * self.size_adjust)
        head = (arm_intersection[0],
                arm_intersection[1] - 15 * self.size_adjust)
        self.gallow_data["parts"]["man"]["leg_intersection"] = leg_intersection
        self.gallow_data["parts"]["man"]["arm_intersection"] = arm_intersection
        self.gallow_data["parts"]["man"]["head"] = head
        self.gallow_data["parts"]["man"]["arm_len"] = 50 * self.size_adjust
        self.gallow_data["parts"]["man"]["leg_len"] = 60 * self.size_adjust
        self.gallow_data["parts"]["man"]["arm_1_angle"] = 45
        self.gallow_data["parts"]["man"]["arm_2_angle"] = -45
        self.gallow_data["parts"]["man"]["leg_1_angle"] = 35
        self.gallow_data["parts"]["man"]["leg_2_angle"] = -35
        self.gallow_data["parts"]["man"]["degree_change_speed"] = 10
        self.gallow_data["parts"]["man"]["arm_1_degree_change"] = 0
        self.gallow_data["parts"]["man"]["arm_2_degree_change"] = 0
        self.gallow_data["parts"]["man"]["leg_1_degree_change"] = 0
        self.gallow_data["parts"]["man"]["leg_2_degree_change"] = 0
        self.gallow_data["parts"]["man"]["arm_1_range"] = (10, 135)
        self.gallow_data["parts"]["man"]["arm_2_range"] = (-10, -135)
        self.gallow_data["parts"]["man"]["leg_1_range"] = (10, 75)
        self.gallow_data["parts"]["man"]["leg_2_range"] = (-10, -75)
    def pre_load_gallow_parts(self):
        """
        Pre-loads random images for each part of the gallow.
        """
        self.pre_load_bases()
        self.pre_load_stage()
        self.pre_load_stares()
        self.pre_load_post()
        self.pre_load_post_extension()
        self.pre_load_support()
        self.pre_load_man()
        head_pos_y = self.gallow_data["parts"]["man"]["head"][1]
        post_extension_y = self.gallow_data["parts"]["post_extension"]["y_pos"]
        self.full_rope_length = ceil(head_pos_y - post_extension_y)
    def draw_bases(self):
        """
        Draws the bases of the gallow on the current window.
        """
        base_width = self.gallow_data["parts"]["base"]["width"]
        base_height = self.gallow_data["parts"]["base"]["height"]
        base_x = self.gallow_data["parts"]["base"]["x_pos"]
        base_y = self.gallow_data["parts"]["base"]["y_pos"] + self.origin[1]
        for i in range(0, 2):
            image = self.gallow_data["images"][i]
            self.window.blit(image, (base_x[i] + self.origin[0], base_y, base_width, base_height))
    def draw_stage(self):
        """
        Draws the stage of the gallow on the current window.
        """
        stage_width = self.gallow_data["parts"]["stage"]["width"]
        stage_height = self.gallow_data["parts"]["stage"]["height"]
        stage_x = self.gallow_data["parts"]["stage"]["x_pos"] + self.origin[0]
        stage_y = self.gallow_data["parts"]["stage"]["y_pos"] + self.origin[1]
        image = self.gallow_data["images"][2]
        self.window.blit(image, (stage_x, stage_y, stage_width, stage_height))
    def draw_stairs(self):
        """
        Draws the stairs that lead to the gallow.
        """
        pg.draw.polygon(self.window, Gallow.black, self.gallow_data["parts"]["stairs"]["points"])
    def draw_post(self):
        """
        Draws the post from which the rope descends.
        """
        post_width = self.gallow_data["parts"]["post"]["width"]
        post_height = self.gallow_data["parts"]["post"]["height"]
        post_x = self.gallow_data["parts"]["post"]["x_pos"] + self.origin[0]
        post_y = self.gallow_data["parts"]["post"]["y_pos"] + self.origin[1]
        image = self.gallow_data["images"][3]
        self.window.blit(image, (post_x, post_y, post_width, post_height))
    def draw_post_extension(self):
        """
        Draws the post's extension.
        """
        post_extension_width = self.gallow_data["parts"]["post_extension"]["width"]
        post_extension_height = self.gallow_data["parts"]["post_extension"]["height"]
        post_extension_x = self.gallow_data["parts"]["post_extension"]["x_pos"] + self.origin[0]
        post_extension_y = self.gallow_data["parts"]["post_extension"]["y_pos"] + self.origin[1]
        image = self.gallow_data["images"][4]
        self.window.blit(image, (post_extension_x, post_extension_y,
                                 post_extension_width, post_extension_height))
    def draw_support(self):
        """
        Draws the joint support between the post its extension.
        """
        width = self.gallow_data["parts"]["support"]["width"]
        height = self.gallow_data["parts"]["support"]["height"]
        image = self.gallow_data["images"][5]
        surface = pg.Surface((int(width), int(height)))
        surface.set_colorkey(Gallow.black)
        surface.blit(image, (0, 0))
        surface = pg.transform.rotate(surface, -45)
        rect = surface.get_rect()
        point_1 = (self.gallow_data["parts"]["support"]["points"][0][0] + self.origin[0],
                   self.gallow_data["parts"]["support"]["points"][0][1] + self.origin[1])
        point_2 = (self.gallow_data["parts"]["support"]["points"][1][0] + self.origin[0],
                   self.gallow_data["parts"]["support"]["points"][1][1] + self.origin[1])
        rect.center = ((point_1[0] + point_2[0]) / 2,
                       (point_1[1] + point_2[1]) / 2)
        self.window.blit(surface, rect)
    def tremble(self):
        """
        Makes the man tremble as he gets hanged.
        """
        limb_list = [["arm_1", "arm_2"], ["leg_1", "leg_2"]]
        amount_list = [[0, 0], [0, 0]]
        current_limb_state = self.move_limbs()
        for i in range(0, len(limb_list)):
            for j in range(0, len(limb_list[i])):
                if current_limb_state[i][j]:
                    rand_sign = randint(0, 1)
                    if rand_sign:
                        rand_sign = -1
                    else:
                        rand_sign = 0
                    rand_degree = rand_sign * randint(90, 360)
                    amount_list[i][j] = rand_degree
        self.change_limbs_degree(amount_list)
    def change_limbs_degree(self, amount_list):
        """
        Adds the given degrees to the angle between each limb of the man and his body.
        """
        if amount_list[0][0]:
            self.gallow_data["parts"]["man"]["arm_1_degree_change"] = amount_list[0][0]
        if amount_list[0][1]:
            self.gallow_data["parts"]["man"]["arm_2_degree_change"] = amount_list[0][1]
        if amount_list[1][0]:
            self.gallow_data["parts"]["man"]["leg_1_degree_change"] = amount_list[1][0]
        if amount_list[1][1]:
            self.gallow_data["parts"]["man"]["leg_2_degree_change"] = amount_list[1][1]
    def move_limbs(self):
        """
        Smoothly moves the man's limbs
        """
        names = ["arm", "leg"]
        speed = self.gallow_data["parts"]["man"]["degree_change_speed"]
        return_list = [[False, False]] * 2
        for i in range(1, 3):
            for j in range(0, len(names)):
                current_limb = "{}_{}_".format(names[j], i)
                degree_change = current_limb + "degree_change"
                angle = current_limb + "angle"
                sign = copysign(1, self.gallow_data["parts"]["man"][degree_change])
                limb_degree_change = self.gallow_data["parts"]["man"][degree_change]
                new_degree_change = abs(limb_degree_change) - abs(speed)
                self.gallow_data["parts"]["man"][degree_change] = new_degree_change * sign
                if new_degree_change <= 0:
                    self.gallow_data["parts"]["man"][degree_change] = 0
                    return_list[j][i - 1] = True
                else:
                    current_angle = self.gallow_data["parts"]["man"][angle]
                    angle_range = [self.gallow_data["parts"]["man"][current_limb + "range"][0]]
                    angle_range.append(self.gallow_data["parts"]["man"][current_limb + "range"][1])
                    if angle_range[0] < 0:
                        angle_range.append(angle_range.pop(0))
                    self.gallow_data["parts"]["man"][angle] += sign * speed
                    new_angle = current_angle + speed * sign
                    if new_angle < angle_range[0] or new_angle > angle_range[1]:
                        self.gallow_data["parts"]["man"][degree_change] *= -1
                        self.gallow_data["parts"]["man"][angle] += sign * speed * -1
        return return_list
    def draw_man(self):
        """
        Draws the man to be hanged.
        """
        self.move_limbs()
        thickness = round(5 * self.size_adjust)
        arm_intersection = self.gallow_data["parts"]["man"]["arm_intersection"]
        leg_intersection = self.gallow_data["parts"]["man"]["leg_intersection"]
        head = self.gallow_data["parts"]["man"]["head"]
        arm_1_angle = radians(self.gallow_data["parts"]["man"]["arm_1_angle"])
        arm_2_angle = radians(self.gallow_data["parts"]["man"]["arm_2_angle"])
        arm_len = self.gallow_data["parts"]["man"]["arm_len"]
        hand_1_x = arm_intersection[0] + sin(arm_1_angle) * arm_len
        hand_1_y = arm_intersection[1] + cos(arm_1_angle) * arm_len
        hand_2_x = arm_intersection[0] + sin(arm_2_angle) * arm_len
        hand_2_y = arm_intersection[1] + cos(arm_2_angle) * arm_len
        hands = ((hand_1_x, hand_1_y), (hand_2_x, hand_2_y))
        leg_1_angle = radians(self.gallow_data["parts"]["man"]["leg_1_angle"])
        leg_2_angle = radians(self.gallow_data["parts"]["man"]["leg_2_angle"])
        leg_len = self.gallow_data["parts"]["man"]["leg_len"]
        leg_1_x = leg_intersection[0] + sin(leg_1_angle) * leg_len
        leg_1_y = leg_intersection[1] + cos(leg_1_angle) * leg_len
        leg_2_x = leg_intersection[0] + sin(leg_2_angle) * leg_len
        leg_2_y = leg_intersection[1] + cos(leg_2_angle) * leg_len
        legs = ((leg_1_x, leg_1_y), (leg_2_x, leg_2_y))
        pg.draw.line(self.window, Gallow.black, legs[0], leg_intersection, thickness)
        pg.draw.line(self.window, Gallow.black, legs[1], leg_intersection, thickness)
        pg.draw.line(self.window, Gallow.black, hands[0], arm_intersection, thickness)
        pg.draw.line(self.window, Gallow.black, hands[1], arm_intersection, thickness)
        pg.draw.line(self.window, Gallow.black, leg_intersection, arm_intersection, thickness)
        pg.draw.line(self.window, Gallow.black, arm_intersection, head, thickness)
        radius = round(10 * self.size_adjust)
        gfx.filled_circle(self.window, round(head[0]), round(head[1]), radius, Gallow.black)
        gfx.aacircle(self.window, round(head[0]), round(head[1]), radius, Gallow.black)
    def draw_rope(self):
        """
        Draws the hanging rope from the end of the post's extension.
        """
        thickness = round(3 * self.size_adjust)
        man_x = self.gallow_data["parts"]["man"]["leg_intersection"][0]
        rope_x = man_x + thickness / 2 + self.origin[0]
        post_extension_y = self.gallow_data["parts"]["post_extension"]["y_pos"] + self.origin[1]
        drop_y = (self.hang_progress / 100) * self.full_rope_length + self.origin[1]
        pg.draw.line(self.window, Gallow.rope_clr, (rope_x - thickness / 2, post_extension_y),
                     (rope_x - thickness / 2, drop_y), thickness)
    def draw_all(self):
        """
        Draws all parts of the gallow.
        """
        self.draw_bases()
        self.draw_rope()
        self.draw_man()
        self.draw_stage()
        self.draw_stairs()
        self.draw_support()
        self.draw_post()
        self.draw_post_extension()
        