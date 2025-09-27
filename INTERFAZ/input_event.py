import pygame


def left_click(events):
    """
    Detecta si se ha presionado el botón izquierdo del mouse una vez.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si se detecta un click izquierdo, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return True
    return False


def left_hold():
    """
    Detecta si el botón izquierdo del mouse está siendo sostenido.

    Retorna:
        bool: True si el botón izquierdo está presionado, False en caso contrario.
    """
    return pygame.mouse.get_pressed()[0] == 1


def right_click(events):
    """
    Detecta si se ha presionado el botón derecho del mouse una vez.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si se detecta un click derecho, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                return True
    return False


def right_hold():
    """
    Detecta si el botón derecho del mouse está siendo sostenido.

    Retorna:
        bool: True si el botón derecho está presionado, False en caso contrario.
    """
    return pygame.mouse.get_pressed()[2] == 1


def scroll_up(events):
    """
    Detecta si la rueda del mouse ha sido desplazada hacia arriba.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si se detecta desplazamiento hacia arriba, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                return True
    return False


def scroll_down(events):
    """
    Detecta si la rueda del mouse ha sido desplazada hacia abajo.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si se detecta desplazamiento hacia abajo, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                return True
    return False


# -----------------------------
# Funciones de eventos de teclado
# -----------------------------

def esc_press(events):
    """
    Detecta si la tecla ESC fue presionada.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si ESC fue presionada, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def shift_pressed():
    """
    Detecta si la tecla SHIFT izquierda está siendo sostenida.

    Retorna:
        bool: True si SHIFT izquierda está presionada, False en caso contrario.
    """
    return pygame.key.get_pressed()[pygame.K_LSHIFT]


def r_press(events):
    """
    Detecta si la tecla 'R' fue presionada.

    Parámetros:
        events (list): Lista de eventos de Pygame.

    Retorna:
        bool: True si 'R' fue presionada, False en caso contrario.
    """
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return True
    return False

