import asyncio
from collections import deque
import numpy as np
import pygame
import os
import math

class VisualInterface:
    def __init__(self, width=400, height=400, icon_path="icon.png"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Operator")
        self.clock = pygame.time.Clock()

        self.draw_color = (255, 255, 255)  # White

        self.is_active = False
        self.is_assistant_speaking = False

        self.base_radius = 100
        self.current_radius = self.base_radius

        self.energy_queue = deque(maxlen=50)
        self.update_interval = 0.05
        self.max_energy = 1.0

        self.wave_phase = 0.0
        self.transition_factor = 0.0

        self.icon_image = pygame.image.load("assistant_modules/icon.png").convert_alpha()
        self.icon_size = (96, 96)  # Smaller base size
        self.icon_image = pygame.transform.smoothscale(self.icon_image, self.icon_size)

        # Text related
        self.font = pygame.font.SysFont(None, 24)
        self.full_text = ""
        self.displayed_text = ""
        self.text_display_progress = 0
        self.text_animation_speed = 10  # characters per frame
        

    async def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        self.screen.fill((0, 0, 0))

        # Energy smoothing
        normalized_energy = (
            np.mean(self.energy_queue) / (self.max_energy or 1.0)
            if self.energy_queue else 0.0
        )

        # Scale changes
        if self.is_assistant_speaking:
            target_scale = 1.0 + 0.2 * normalized_energy  # Bounce
        else:
            target_scale = 1.0 + 0.05 * normalized_energy  # Gentle pulse

        self.current_scale = getattr(self, "current_scale", 1.0)
        self.current_scale += (target_scale - self.current_scale) * 0.3

        # Scaled icon
        scaled_size = (
            int(self.icon_size[0] * self.current_scale),
            int(self.icon_size[1] * self.current_scale),
        )
        scaled_size = (
            min(scaled_size[0], self.width),
            min(scaled_size[1], self.height),
        )
        scaled_icon = pygame.transform.smoothscale(self.icon_image, scaled_size)
        icon_x = self.width // 2 - scaled_size[0] // 2
        icon_y = self.height // 2 - scaled_size[1] // 2
        self.screen.blit(scaled_icon, (icon_x, icon_y))

        # Pulse effect when not speaking
        if not self.is_assistant_speaking:
            self.pulse_phase = getattr(self, "pulse_phase", 0)
            self.pulse_phase += 1

            pulse_radius = int(self.icon_size[0] * (1.5 + 0.5 * np.sin(self.pulse_phase * 0.2)))
            pulse_alpha = max(0, 180 - self.pulse_phase * 4)

            if pulse_alpha > 0:
                pulse_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.circle(
                    pulse_surface,
                    (255, 255, 255, pulse_alpha),
                    (self.width // 2, self.height // 2),
                    pulse_radius,
                    width=2
                )
                self.screen.blit(pulse_surface, (0, 0))
            else:
                self.pulse_phase = 0  # Restart pulse

        # Text animation (typewriter effect)
        if self.full_text:
            self.text_display_progress += self.text_animation_speed
            chars_to_show = int(self.text_display_progress)
            if chars_to_show > len(self.full_text):
                chars_to_show = len(self.full_text)
            self.displayed_text = self.full_text[:chars_to_show]

            text_surface = self.font.render(self.displayed_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height - 30))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        self.clock.tick(60)
        await asyncio.sleep(self.update_interval)
        return True

    def set_active(self, is_active):
        self.is_active = is_active

    def set_assistant_speaking(self, is_speaking):
        self.is_assistant_speaking = is_speaking

    def update_energy(self, energy):
        if isinstance(energy, np.ndarray):
            energy = np.mean(np.abs(energy))
        self.energy_queue.append(energy)

        current_max = max(self.energy_queue)
        if current_max > self.max_energy:
            self.max_energy = current_max
        elif len(self.energy_queue) == self.energy_queue.maxlen:
            self.max_energy = max(self.energy_queue)

    def process_audio_data(self, audio_data: bytes):
        audio_frame = np.frombuffer(audio_data, dtype=np.int16)
        energy = np.abs(audio_frame).mean()
        self.update_energy(energy)

    def display_text(self, text: str):
        self.full_text = text
        self.displayed_text = ""
        self.text_display_progress = 0



async def run_visual_interface(interface):
    while True:
        if not await interface.update():
            break


async def simulate_state(interface):
    while True:
        interface.set_assistant_speaking(True)
        await asyncio.sleep(3)
        interface.set_assistant_speaking(False)
        await asyncio.sleep(3)


if __name__ == "__main__":
    interface = VisualInterface()

    async def simulate_energy():
        import random

        while True:
            energy = random.randint(0, 5000)
            interface.update_energy(energy)
            await asyncio.sleep(0.05)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            run_visual_interface(interface),
            simulate_state(interface),
            simulate_energy(),
        )
    )
