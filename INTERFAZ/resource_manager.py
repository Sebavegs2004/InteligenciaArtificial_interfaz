import os
import pygame


class ResourceManager:
    """
    Clase para gestionar recursos del juego (imágenes, sonidos y música) de manera centralizada.

    Atributos de clase:
        proyect_folder (str): Carpeta donde se encuentra este archivo.
        resources_folder (str): Carpeta principal donde se almacenan los recursos del proyecto.
    """

    proyect_folder = os.path.dirname(__file__)
    resources_folder = os.path.join(os.path.dirname(proyect_folder), 'resources')

    @staticmethod
    def image_load(file_name):
        """
        Carga una imagen desde la carpeta de recursos.

        Parámetros:
            file_name (str): Nombre del archivo de imagen (con extensión).

        Retorna:
            pygame.Surface: Surface de Pygame con la imagen cargada.
            None: Si la imagen no se pudo cargar.
        """
        get_image_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            return pygame.image.load(get_image_path)
        except pygame.error as e:
            print(f"No se pudo cargar la imagen {file_name}: {e}")
            return None

    @staticmethod
    def sound_load(file_name):
        """
        Carga un efecto de sonido desde la carpeta de recursos.

        Parámetros:
            file_name (str): Nombre del archivo de sonido (con extensión).

        Retorna:
            pygame.mixer.Sound: Objeto Sound cargado.
            None: Si el sonido no se pudo cargar.
        """
        get_sound_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            return pygame.mixer.Sound(get_sound_path)
        except pygame.error as e:
            print(f"No se pudo cargar el sonido {file_name}: {e}")
            return None

    @staticmethod
    def music_load(file_name):
        """
        Carga y reproduce música de fondo en bucle.

        Parámetros:
            file_name (str): Nombre del archivo de música (con extensión).

        Acciones:
            - Carga la música.
            - Ajusta el volumen al 20%.
            - Reproduce en bucle infinito.
        """
        get_music_path = os.path.join(ResourceManager.resources_folder, file_name)
        try:
            pygame.mixer.music.load(get_music_path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)  # bucle infinito
            print(f"Música {file_name} cargada y reproducida.")
        except pygame.error as e:
            print(f"No se pudo cargar la música {file_name}: {e}")

    @staticmethod
    def stop_music():
        """
        Detiene la música de fondo actualmente reproducida.
        """
        pygame.mixer.music.stop()
        print("Música detenida.")
