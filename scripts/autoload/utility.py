from pytmx.util_pygame import load_pygame
import pygame
import os

def import_font(*path, font_size, font_format="ttf"):
    return pygame.font.Font(os.path.join(*path) + f".{font_format}", font_size)

def import_map(*path):
    full_path = load_pygame(os.path.join(*path))
    return full_path

def import_image(*path, alpha=True, texture_format="png"):
    full_path = os.path.join(*path) + f".{texture_format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path, subfolders, image_names in os.walk(os.path.join(*path)):
        for image_name in sorted(image_names, key = lambda name: int(name.split(".")[0])):
            full_path = os.path.join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def import_sub_folders(*path):
    frame_dict = {}
    for _, sub_folders, __ in os.walk(os.path.join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict