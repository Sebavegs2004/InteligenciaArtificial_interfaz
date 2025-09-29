import os
import pygame


class ResourceManager:
    proyect_folder = os.path.dirname(__file__)
    resources_folder = os.path.join(os.path.dirname(proyect_folder), 'resources')

    @staticmethod
    def image_load(file_name):
        get_image_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            return pygame.image.load(get_image_path)
        except pygame.error as e:
            print(f"No se pudo cargar la imagen {file_name}: {e}")
            return None

    @staticmethod
    def sound_load(file_name):
        get_sound_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            return pygame.mixer.Sound(get_sound_path)
        except pygame.error as e:
            print(f"No se pudo cargar el sonido {file_name}: {e}")
            return None

    @staticmethod
    def music_load(file_name):
        get_music_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            pygame.mixer.music.load(get_music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # bucle infinito
            print(f"Música {file_name} cargada y reproducida.")
        except pygame.error as e:
            print(f"No se pudo cargar la música {file_name}: {e}")

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()
