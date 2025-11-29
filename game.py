"""
GravityMaze - Jogo de Labirinto com Controlo por Acelerómetro ADXL345
Autoria: João Oliveira 1240369 / João Santos 1240368
Data: 19/11/2025
"""

import pygame
import serial
import serial.tools.list_ports
import sys
import math
import random
import time
import sqlite3
import json
import os
from datetime import datetime
import threading
import numpy as np

# Configurações do jogo
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
FPS = 60

# Margens do labirinto
MAZE_MARGIN = 60
MAZE_MARGIN_TOP = 120

# Arquivo de configurações
CONFIG_FILE = "config.json"

# Traduções
TRANSLATIONS = {
    'pt': {
        'title': 'GravityMaze',
        'subtitle': 'Controlo por Acelerómetro ADXL345',
        'play': 'Jogar',
        'settings': 'Definições',
        'leaderboard': 'Leaderboard',
        'exit': 'Sair',
        'continue': 'Continuar',
        'restart_level': 'Reiniciar Nível',
        'main_menu': 'Menu Principal',
        'next_level': 'Próximo Nível',
        'back': 'Voltar',
        'paused': 'PAUSADO',
        'level_complete': 'NÍVEL COMPLETO!',
        'game_over': 'GAME OVER!',
        'lives': 'Vidas',
        'time': 'Tempo',
        'level': 'Nível',
        'score': 'Pontuação',
        'precision': 'Precisão',
        'sensitivity': 'Sensibilidade',
        'volume': 'Volume',
        'invert_x': 'Inverter X',
        'invert_y': 'Inverter Y',
        'swap_xy': 'Trocar X/Y',
        'language': 'Idioma',
        'serial_connected': 'Serial: CONECTADO',
        'serial_disconnected': 'Serial: DESCONECTADO (a usar teclado)',
        'yes': 'SIM',
        'no': 'NÃO',
        'normal_mode': 'Normal',
        'minefield_mode': 'Campo Minado',
        'timeattack_mode': 'Contra-Relógio',
        'elimination_mode': 'Eliminação',
        'select_mode': 'Selecionar Modo de Jogo',
        'total_stats': 'Estatísticas Totais',
        'levels_completed': 'Níveis Completados',
        'total_time': 'Tempo Total',
        'best_time': 'Melhor Tempo',
        'time_bonus': 'Bónus de Tempo',
        'enter_name': 'Insira o seu nome:',
        'save': 'Guardar',
        'discard': 'Descartar',
        'save_score': 'Guardar Pontuação?',
        'filter_mode': 'Filtrar por Modo:',
        'all_modes': 'Todos os Modos',
        'player_profile': 'Perfil do Jogador',
        'total_playtime': 'Tempo Total de Jogo',
        'total_points': 'Pontos Totais',
        'levels_by_mode': 'Níveis por Modo',
        'points_by_mode': 'Pontos por Modo',
        'close': 'Fechar',
        'resume': 'Continuar',
        'restart': 'Reiniciar',
        'menu': 'Menu',
        'try_again': 'Tentar Novamente',
        'level_reached': 'Nível Alcançado',
        'no_data': 'Sem dados disponíveis',
        'rank': '#',
        'name': 'Nome',
        'date': 'Data',
        'mode': 'Modo',
        'save_progress': 'Guardar Progresso',
        'single_player': 'Um Jogador',
        'multi_player': 'Multijogador',
        'select_players': 'Selecionar Jogadores',
        'controls': 'Controlos',
        'show_commands': 'Mostrar Comandos',
        'movement': 'Movimento',
        'player_1': 'Jogador 1',
        'player_2': 'Jogador 2',
        'general': 'Geral',
        'arrows': 'Setas',
        'wasd': 'WASD',
        'pause': 'Pausar',
        'restart': 'Reiniciar',
        'stm32_test': 'Teste STM32',
        'stm32_setup': 'Configuração STM32',
        'beep_1': 'Apitar Placa 1',
        'beep_2': 'Apitar Placa 2',
        'waiting_partner': 'À espera do parceiro...',
        'winner': 'VENCEDOR',
        'eliminated': 'ELIMINADO',
        'both_lost': 'AMBOS PERDERAM',
        'draw': 'EMPATE',
        'p1_wins': 'JOGADOR 1 VENCEU!',
        'p2_wins': 'JOGADOR 2 VENCEU!',
        'play_again': 'Jogar Novamente',
        'select_difficulty': 'Selecionar Dificuldade',
        'difficulty_easy': 'Fácil',
        'difficulty_normal': 'Normal',
        'difficulty_hard': 'Difícil',
        'hud_instructions': 'ESC: Pausar | R: Reiniciar',
        'stm32_detected': 'STM32 Detectados',
    },
    'en': {
        'title': 'GravityMaze',
        'subtitle': 'Accelerometer Control ADXL345',
        'play': 'Play',
        'settings': 'Settings',
        'leaderboard': 'Leaderboard',
        'exit': 'Exit',
        'continue': 'Continue',
        'restart_level': 'Restart Level',
        'main_menu': 'Main Menu',
        'next_level': 'Next Level',
        'back': 'Back',
        'paused': 'PAUSED',
        'level_complete': 'LEVEL COMPLETE!',
        'game_over': 'GAME OVER!',
        'lives': 'Lives',
        'time': 'Time',
        'level': 'Level',
        'score': 'Score',
        'precision': 'Precision',
        'sensitivity': 'Sensitivity',
        'volume': 'Volume',
        'invert_x': 'Invert X',
        'invert_y': 'Invert Y',
        'swap_xy': 'Swap X/Y',
        'language': 'Language',
        'serial_connected': 'Serial: CONNECTED',
        'serial_disconnected': 'Serial: DISCONNECTED (using keyboard)',
        'yes': 'YES',
        'no': 'NO',
        'normal_mode': 'Normal',
        'minefield_mode': 'Minefield',
        'timeattack_mode': 'Time Attack',
        'elimination_mode': 'Elimination',
        'select_mode': 'Select Game Mode',
        'total_stats': 'Total Stats',
        'levels_completed': 'Levels Completed',
        'total_time': 'Total Time',
        'best_time': 'Best Time',
        'time_bonus': 'Time Bonus',
        'enter_name': 'Enter your name:',
        'save': 'Save',
        'discard': 'Discard',
        'save_score': 'Save Score?',
        'filter_mode': 'Filter by Mode:',
        'all_modes': 'All Modes',
        'player_profile': 'Player Profile',
        'total_playtime': 'Total Playtime',
        'total_points': 'Total Points',
        'levels_by_mode': 'Levels by Mode',
        'points_by_mode': 'Points by Mode',
        'close': 'Close',
        'resume': 'Resume',
        'restart': 'Restart',
        'menu': 'Menu',
        'try_again': 'Try Again',
        'level_reached': 'Level Reached',
        'no_data': 'No data available',
        'rank': '#',
        'name': 'Name',
        'date': 'Date',
        'mode': 'Mode',
        'save_progress': 'Save Progress',
        'single_player': 'Single Player',
        'multi_player': 'Multiplayer',
        'select_players': 'Select Players',
        'controls': 'Controls',
        'show_commands': 'Show Commands',
        'movement': 'Movement',
        'player_1': 'Player 1',
        'player_2': 'Player 2',
        'general': 'General',
        'arrows': 'Arrows',
        'wasd': 'WASD',
        'pause': 'Pause',
        'restart': 'Restart',
        'stm32_test': 'STM32 Test',
        'stm32_setup': 'STM32 Setup',
        'beep_1': 'Beep Board 1',
        'beep_2': 'Beep Board 2',
        'waiting_partner': 'Waiting for partner...',
        'winner': 'WINNER',
        'eliminated': 'ELIMINATED',
        'both_lost': 'BOTH LOST',
        'draw': 'DRAW',
        'p1_wins': 'PLAYER 1 WINS!',
        'p2_wins': 'PLAYER 2 WINS!',
        'play_again': 'Play Again',
        'select_difficulty': 'Select Difficulty',
        'difficulty_easy': 'Easy',
        'difficulty_normal': 'Normal',
        'difficulty_hard': 'Hard',
        'hud_instructions': 'ESC: Pause | R: Restart',
        'stm32_detected': 'STM32 Detected',
    }
}

# Função helper para tradução
def t(key, lang='pt'):
    """Traduzir uma chave para o idioma especificado"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
GOLD = (255, 215, 0)
ORANGE = (255, 100, 0)

# Configurações da bola
BALL_RADIUS = 10
BALL_COLOR = RED
FRICTION = 0.98

# Aceleração gravitacional real em pixels/s² (9.8 m/s² convertido)
# 1g = 9.8 m/s² -> assumindo que 1m = 100 pixels no jogo
REAL_GRAVITY = 980  # pixels/s²

# Configurações do labirinto
WALL_COLOR = WHITE
WALL_THICKNESS = 10

# =============================================================================
# Sound Generation Functions
# =============================================================================

def generate_8bit_sound(frequency, duration, sample_rate=22050):
    """Generate a simple 8-bit style sound wave"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)
    # Convert to 8-bit style by quantizing
    wave = np.round(wave * 127) / 127
    # Convert to 16-bit for pygame
    wave = np.int16(wave * 32767)
    # Stereo
    stereo_wave = np.repeat(wave.reshape(-1, 1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo_wave)

def generate_level_complete_sound():
    """Generate upward arpeggio for level complete - C major chord"""
    sample_rate = 22050
    duration = 0.1
    notes = [523, 659, 784, 1047]  # C5, E5, G5, C6

    sounds = []
    for freq in notes:
        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = np.sin(2 * np.pi * freq * t)
        # Apply envelope for smooth sound
        envelope = np.exp(-3 * t / duration)
        wave = wave * envelope
        # 8-bit style
        wave = np.round(wave * 127) / 127
        wave = np.int16(wave * 32767)
        sounds.append(wave)

    # Concatenate all notes
    full_wave = np.concatenate(sounds)
    stereo_wave = np.repeat(full_wave.reshape(-1, 1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo_wave)

def generate_mine_hit_sound():
    """Generate explosion sound for mine hit"""
    sample_rate = 22050
    duration = 0.3

    t = np.linspace(0, duration, int(sample_rate * duration))
    # Start with high frequency noise, drop to low rumble
    freq = 800 * np.exp(-8 * t / duration) + 60
    wave = np.sin(2 * np.pi * freq * t)
    # Add noise for explosion effect
    noise = np.random.uniform(-0.3, 0.3, len(t))
    wave = wave * 0.7 + noise * 0.3
    # Apply envelope
    envelope = np.exp(-4 * t / duration)
    wave = wave * envelope
    # 8-bit style
    wave = np.round(wave * 127) / 127
    wave = np.int16(wave * 32767)

    stereo_wave = np.repeat(wave.reshape(-1, 1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo_wave)

def generate_game_over_sound():
    """Generate dramatic descending arpeggio for game over"""
    sample_rate = 22050
    duration = 0.25
    # Dramatic descending minor chord progression
    notes = [523, 392, 349, 294, 262, 220]  # C5, G4, F4, D4, C4, A3 (descending arpeggio)

    sounds = []
    for i, freq in enumerate(notes):
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Sine wave with slight vibrato for dramatic effect
        vibrato = 1 + 0.02 * np.sin(2 * np.pi * 5 * t)
        wave = np.sin(2 * np.pi * freq * vibrato * t)
        # Strong decay envelope for dramatic effect
        envelope = np.exp(-3 * t / duration)
        wave = wave * envelope
        # 8-bit style
        wave = np.round(wave * 127) / 127
        wave = np.int16(wave * 32767)
        sounds.append(wave)

    # Concatenate all notes
    full_wave = np.concatenate(sounds)
    stereo_wave = np.repeat(full_wave.reshape(-1, 1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo_wave)

def generate_wall_collision_sound():
    """Generate short impact sound for wall collisions"""
    sample_rate = 22050
    duration = 0.08  # Very short impact

    t = np.linspace(0, duration, int(sample_rate * duration))
    # Mix of frequencies for impact effect
    wave = (np.sin(2 * np.pi * 200 * t) +
            0.5 * np.sin(2 * np.pi * 150 * t) +
            0.3 * np.random.randn(len(t)))  # Add noise for impact

    # Sharp attack, quick decay
    envelope = np.exp(-30 * t / duration)
    wave = wave * envelope

    # 8-bit style and normalize
    wave = np.round(wave * 127) / 127
    wave = np.int16(wave * 32767 * 0.3)  # Lower volume (30%)

    stereo_wave = np.repeat(wave.reshape(-1, 1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo_wave)

# =============================================================================
# MODOS DE JOGO
# =============================================================================

GAME_MODES = {
    'normal': {
        'name_pt': 'Normal',
        'name_en': 'Normal',
        'timer_direction': 'up',  # Conta para cima
        'has_lives': True,
        'initial_lives': 5,
        'mines_in_deadends': False,
        'track_precision': True,  # Sistema de precisão ativo
        'desc_pt': 'Modo clássico com sistema de precisão',
        'desc_en': 'Classic mode with precision system'
    },
    'minefield': {
        'name_pt': 'Campo Minado',
        'name_en': 'Minefield',
        'timer_direction': 'up',
        'has_lives': True,
        'initial_lives': 5,
        'mines_everywhere': True,  # Minas em células aleatórias
        'mine_percentage': 0.15,  # 15% das células têm minas
        'track_precision': True,
        'desc_pt': 'Evite as minas invisíveis!',
        'desc_en': 'Avoid the invisible mines!'
    },
    'timeattack': {
        'name_pt': 'Contra-Relógio',
        'name_en': 'Time Attack',
        'timer_direction': 'down',  # Conta para baixo
        'initial_time': 300,  # 5 minutos em segundos
        'has_lives': True,
        'initial_lives': 5,
        'track_precision': True,
        'desc_pt': 'Complete o máximo de níveis em 5 minutos',
        'desc_en': 'Complete as many levels as possible in 5 minutes'
    },
    'elimination': {
        'name_pt': 'Eliminação',
        'name_en': 'Elimination',
        'timer_direction': 'down',
        'random_time_on_level': True,  # Adiciona tempo random ao passar nível
        'random_time_min': 30,
        'random_time_max': 80,
        'initial_time': 60,  # Começa com 60s
        'has_lives': True,
        'initial_lives': 5,
        'track_precision': True,
        'desc_pt': 'Complete níveis para ganhar mais tempo',
        'desc_en': 'Complete levels to gain more time'
    }
}


class GameMode:
    """Classe para gerenciar o modo de jogo atual"""

    def __init__(self, mode_name='normal'):
        self.mode_name = mode_name
        self.config = GAME_MODES.get(mode_name, GAME_MODES['normal'])

    def get_name(self, language='pt'):
        """Retorna o nome do modo no idioma especificado"""
        key = f'name_{language}'
        return self.config.get(key, self.config['name_pt'])

    def get_description(self, language='pt'):
        """Retorna a descrição do modo no idioma especificado"""
        key = f'desc_{language}'
        return self.config.get(key, self.config['desc_pt'])

    def has_timer(self):
        """Verifica se o modo tem timer"""
        return 'initial_time' in self.config

    def get_initial_time(self):
        """Retorna tempo inicial se houver"""
        return self.config.get('initial_time', 0)

    def should_add_random_time(self):
        """Verifica se deve adicionar tempo aleatório ao passar nível"""
        return self.config.get('random_time_on_level', False)

    def get_random_time_range(self):
        """Retorna range de tempo aleatório"""
        min_time = self.config.get('random_time_min', 30)
        max_time = self.config.get('random_time_max', 80)
        return (min_time, max_time)

    def has_lives(self):
        """Verifica se o modo tem sistema de vidas"""
        return self.config.get('has_lives', True)

    def get_initial_lives(self):
        """Retorna número inicial de vidas"""
        return self.config.get('initial_lives', 3)

    def has_mines_in_deadends(self):
        """Verifica se tem minas em dead-ends"""
        return self.config.get('mines_in_deadends', False)

    def has_mines_everywhere(self):
        """Verifica se tem minas espalhadas"""
        return self.config.get('mines_everywhere', False)

    def get_mine_percentage(self):
        """Retorna percentagem de minas"""
        return self.config.get('mine_percentage', 0.15)

    def tracks_precision(self):
        """Verifica se rastreia precisão"""
        return self.config.get('track_precision', False)

    def timer_counts_down(self):
        """Verifica se timer conta para baixo"""
        return self.config.get('timer_direction', 'up') == 'down'


# =============================================================================
# CLASSES DE CONFIGURAÇÃO E DADOS
# =============================================================================

class Config:
    """Gestão de configurações persistentes"""
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.default_config = {
            'sensitivity': 1.0,
            'invert_x': True,
            'invert_y': True,
            'swap_xy': False,
            'language': 'pt',
            'game_volume': 0.7
        }
        self.config = self.load()

    def load(self):
        """Carregar configurações do arquivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**self.default_config, **json.load(f)}
            except:
                return self.default_config.copy()
        return self.default_config.copy()

    def save(self):
        """Salvar configurações no arquivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def get(self, key):
        """Obter valor de configuração"""
        return self.config.get(key, self.default_config.get(key))

    def set(self, key, value):
        """Definir valor de configuração"""
        self.config[key] = value
        self.save()

class Database:
    """Gestão da base de dados SQLite para leaderboard"""
    def __init__(self):
        self.conn = sqlite3.connect('gravitymaze.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                level INTEGER NOT NULL,
                time REAL NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL,
                game_mode TEXT DEFAULT 'normal'
            )
        ''')

        # Migrate old database - add game_mode column if it doesn't exist
        try:
            cursor.execute("SELECT game_mode FROM leaderboard LIMIT 1")
        except sqlite3.OperationalError:
            print("Migrando base de dados antiga - adicionando coluna game_mode...")
            cursor.execute("ALTER TABLE leaderboard ADD COLUMN game_mode TEXT DEFAULT 'normal'")
            self.conn.commit()

        # Create player_stats table for player profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                player_name TEXT PRIMARY KEY,
                total_playtime REAL DEFAULT 0,
                levels_normal INTEGER DEFAULT 0,
                levels_minefield INTEGER DEFAULT 0,
                levels_timeattack INTEGER DEFAULT 0,
                levels_elimination INTEGER DEFAULT 0,
                points_normal INTEGER DEFAULT 0,
                points_minefield INTEGER DEFAULT 0,
                points_timeattack INTEGER DEFAULT 0,
                points_elimination INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_score(self, player_name, level, time_taken, score, game_mode='normal'):
        cursor = self.conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO leaderboard (player_name, level, time, score, date, game_mode)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_name, level, time_taken, score, date, game_mode))

        # Update player stats
        self.update_player_stats(player_name, level, time_taken, score, game_mode)

        self.conn.commit()

    def update_player_stats(self, player_name, level, time_taken, score, game_mode='normal'):
        """Update player statistics in player_stats table"""
        cursor = self.conn.cursor()

        # Check if player exists
        cursor.execute('SELECT player_name FROM player_stats WHERE player_name = ?', (player_name,))
        exists = cursor.fetchone()

        if not exists:
            # Create new player entry
            cursor.execute('''
                INSERT INTO player_stats (player_name, total_playtime)
                VALUES (?, ?)
            ''', (player_name, time_taken))
        else:
            # Update playtime
            cursor.execute('''
                UPDATE player_stats
                SET total_playtime = total_playtime + ?
                WHERE player_name = ?
            ''', (time_taken, player_name))

        # Update level count for specific mode
        levels_col = f'levels_{game_mode}'
        cursor.execute(f'''
            UPDATE player_stats
            SET {levels_col} = {levels_col} + 1
            WHERE player_name = ?
        ''', (player_name,))

        # Update points for specific mode
        points_col = f'points_{game_mode}'
        cursor.execute(f'''
            UPDATE player_stats
            SET {points_col} = {points_col} + ?
            WHERE player_name = ?
        ''', (score, player_name))

        self.conn.commit()

    def get_player_stats(self, player_name):
        """Get statistics for a specific player"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT total_playtime,
                   levels_normal, levels_minefield, levels_timeattack, levels_elimination,
                   points_normal, points_minefield, points_timeattack, points_elimination
            FROM player_stats
            WHERE player_name = ?
        ''', (player_name,))
        return cursor.fetchone()

    def get_top_scores(self, limit=10, game_mode=None):
        cursor = self.conn.cursor()
        if game_mode:
            cursor.execute('''
                SELECT player_name, level, time, score, date, game_mode
                FROM leaderboard
                WHERE game_mode = ?
                ORDER BY level DESC, score DESC, time ASC
                LIMIT ?
            ''', (game_mode, limit))
        else:
            cursor.execute('''
                SELECT player_name, level, time, score, date, game_mode
                FROM leaderboard
                ORDER BY level DESC, score DESC, time ASC
                LIMIT ?
            ''', (limit,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()

class Button:
    """Botão estilo Minecraft minimalista"""
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = LIGHT_GRAY
        self.is_hovered = False

    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color

        # Desenhar botão com efeito 3D
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Efeito de sombra
        if not self.is_hovered:
            shadow_rect = self.rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, DARK_GRAY, shadow_rect)
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Texto centralizado
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                return True
        return False

class Slider:
    """Slider para configurações"""
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.handle_radius = 8

    def draw(self, screen, font):
        # Desenhar linha
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Desenhar handle
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(screen, LIGHT_GRAY, (int(handle_x), self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, WHITE, (int(handle_x), self.rect.centery), self.handle_radius, 2)

        # Desenhar label
        label_text = font.render(f"{self.label}: {self.value:.2f}", True, WHITE)
        screen.blit(label_text, (self.rect.x, self.rect.y - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            mouse_pos = event.pos
            distance = math.sqrt((mouse_pos[0] - handle_x)**2 + (mouse_pos[1] - self.rect.centery)**2)
            if distance <= self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x = event.pos[0]
                relative_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
                self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)

class ModeCard:
    """Card for game mode selection"""
    def __init__(self, x, y, width, height, mode_name, title, description, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.mode_name = mode_name
        self.title = title
        self.description = description
        self.color = color
        self.hover_color = LIGHT_GRAY
        self.is_hovered = False

    def draw(self, screen, title_font, desc_font):
        color = self.hover_color if self.is_hovered else self.color

        # Draw card background with shadow
        if not self.is_hovered:
            shadow_rect = self.rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(screen, DARK_GRAY, shadow_rect)

        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Draw title
        title_surface = title_font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.y + 40))
        screen.blit(title_surface, title_rect)

        # Draw description (wrap text if needed)
        desc_lines = self.wrap_text(self.description, desc_font, self.rect.width - 20)
        y_offset = self.rect.y + 80
        for line in desc_lines:
            desc_surface = desc_font.render(line, True, WHITE)
            desc_rect = desc_surface.get_rect(center=(self.rect.centerx, y_offset))
            screen.blit(desc_surface, desc_rect)
            y_offset += 25

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, WHITE)
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class TextInput:
    """Simple text input field"""
    def __init__(self, x, y, width, height, max_length=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.max_length = max_length
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, screen, font):
        # Draw input box
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        pygame.draw.rect(screen, DARK_GRAY, self.rect)

        # Draw text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)

        # Draw cursor (blinking)
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer > 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            if self.cursor_visible:
                cursor_x = text_rect.right + 2
                cursor_y1 = self.rect.centery - 10
                cursor_y2 = self.rect.centery + 10
                pygame.draw.line(screen, WHITE, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return 'submit'
            elif len(self.text) < self.max_length:
                if event.unicode.isprintable():
                    self.text += event.unicode
        return None

class Ball:
    def __init__(self, x, y, sensitivity=1.0, world_width=DEFAULT_WIDTH, world_height=DEFAULT_HEIGHT, color=BALL_COLOR):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.sensitivity = sensitivity
        self.world_width = world_width
        self.world_height = world_height
        self.color = color
        self.base_friction = FRICTION # Store original friction

    def update(self, ax, ay, dt, walls, friction_factor=None):
        if friction_factor is None:
            friction_factor = self.base_friction

        # Aplicar curva suave para transição mais natural
        # Usar função quadrática para amplificar pequenas inclinações
        # e suavizar grandes inclinações
        def smooth_curve(value):
            """Curva suave para transição natural"""
            sign = 1 if value >= 0 else -1
            abs_val = abs(value)
            # Curva quadrática suavizada
            if abs_val < 0.3:
                # Amplificar pequenas inclinações (mais responsivo)
                smoothed = abs_val * 1.5
            else:
                # Suavizar grandes inclinações (menos radical)
                smoothed = 0.45 + (abs_val - 0.3) * 0.8
            return sign * smoothed

        # Aplicar curva suave
        ax_smooth = smooth_curve(ax)
        ay_smooth = smooth_curve(ay)

        # Aplicar aceleração com sensibilidade ajustável e gravidade real
        self.vx += ax_smooth * REAL_GRAVITY * self.sensitivity * dt
        self.vy += ay_smooth * REAL_GRAVITY * self.sensitivity * dt

        # Aplicar fricção (usando o fator ajustado para sub-stepping)
        self.vx *= friction_factor
        self.vy *= friction_factor

        # Calcular nova posição
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        # Verificar colisões com paredes usando detecção circular
        collision_occurred = False
        for wall in walls:
            if self.check_collision_circle(new_x, new_y, wall):
                # Encontrar o ponto mais próximo da parede
                closest_x = max(wall[0], min(new_x, wall[0] + wall[2]))
                closest_y = max(wall[1], min(new_y, wall[1] + wall[3]))

                # Calcular distância
                dx = new_x - closest_x
                dy = new_y - closest_y
                distance = math.sqrt(dx*dx + dy*dy)

                if distance < self.radius:
                    # Normalizar e empurrar para fora
                    if distance > 0:
                        nx = dx / distance
                        ny = dy / distance
                    else:
                        nx = 1
                        ny = 0

                    # Reposicionar bola
                    new_x = closest_x + nx * self.radius
                    new_y = closest_y + ny * self.radius

                    # Calcular velocidade refletida (atrito reduzido)
                    dot = self.vx * nx + self.vy * ny
                    self.vx = (self.vx - 2 * dot * nx) * 0.9
                    self.vy = (self.vy - 2 * dot * ny) * 0.9

                    collision_occurred = True

        # Limites da janela
        if new_x - self.radius < 0:
            new_x = self.radius
            self.vx = -self.vx * 0.5
        if new_x + self.radius > self.world_width:
            new_x = self.world_width - self.radius
            self.vx = -self.vx * 0.5
        if new_y - self.radius < 0:
            new_y = self.radius
            self.vy = -self.vy * 0.5
        if new_y + self.radius > self.world_height:
            new_y = self.world_height - self.radius
            self.vy = -self.vy * 0.5

        self.x = new_x
        self.y = new_y

        return collision_occurred

    def check_collision_circle(self, x, y, wall):
        """Detecção de colisão circular melhorada para evitar bugs nos cantos"""
        # Encontrar o ponto mais próximo na parede
        closest_x = max(wall[0], min(x, wall[0] + wall[2]))
        closest_y = max(wall[1], min(y, wall[1] + wall[3]))

        # Calcular distância ao ponto mais próximo
        dx = x - closest_x
        dy = y - closest_y
        distance = math.sqrt(dx*dx + dy*dy)

        return distance < self.radius

    def draw(self, screen):
        # Sombra
        shadow_color = (int(self.color[0] * 0.4), int(self.color[1] * 0.4), int(self.color[2] * 0.4))
        pygame.draw.circle(screen, shadow_color, (int(self.x) + 3, int(self.y) + 3), self.radius)
        # Bola principal
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Highlight
        # Make highlight also use the ball's color
        highlight_color = (min(255, int(self.color[0] * 1.5)), min(255, int(self.color[1] * 1.5)), min(255, int(self.color[2] * 1.5)))
        pygame.draw.circle(screen, highlight_color, (int(self.x) - 3, int(self.y) - 3), self.radius // 3)

class Mine:
    def __init__(self, x, y, size=3):
        self.x = x
        self.y = y
        self.size = size
        self.animation_time = random.randint(0, 60) # Start animation at a random time

    def draw(self, screen):
        self.animation_time = (self.animation_time + 1) % 60
        
        # Cor base da mina
        mine_color = (40, 40, 40)
        
        # Desenhar corpo da mina
        pygame.draw.circle(screen, mine_color, (int(self.x), int(self.y)), self.size)
        
        # Desenhar espinhos
        for i in range(8):
            angle = math.pi * 2 * i / 8
            start_pos = (self.x + self.size * 0.8 * math.cos(angle), self.y + self.size * 0.8 * math.sin(angle))
            end_pos = (self.x + self.size * 1.5 * math.cos(angle), self.y + self.size * 1.5 * math.sin(angle))
            pygame.draw.line(screen, mine_color, start_pos, end_pos, 2)
            
        # Animação de piscar para perigo
        if self.animation_time < 20:
            # Piscar um ponto vermelho no centro
            blink_color = RED
            pygame.draw.circle(screen, blink_color, (int(self.x), int(self.y)), self.size // 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class MazeGenerator:
    """Gerador de labirintos usando Recursive Backtracking (DFS)"""

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size

        # Grid de células - cada célula tem 4 paredes [top, right, bottom, left]
        self.grid = []
        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                grid_row.append({
                    'visited': False,
                    'walls': [True, True, True, True]  # [top, right, bottom, left]
                })
            self.grid.append(grid_row)

    def get_neighbors(self, row, col):
        """Obter vizinhos não visitados de uma célula"""
        neighbors = []

        # Top
        if row > 0 and not self.grid[row - 1][col]['visited']:
            neighbors.append((row - 1, col, 0))  # 0 = direção top

        # Right
        if col < self.cols - 1 and not self.grid[row][col + 1]['visited']:
            neighbors.append((row, col + 1, 1))  # 1 = direção right

        # Bottom
        if row < self.rows - 1 and not self.grid[row + 1][col]['visited']:
            neighbors.append((row + 1, col, 2))  # 2 = direção bottom

        # Left
        if col > 0 and not self.grid[row][col - 1]['visited']:
            neighbors.append((row, col - 1, 3))  # 3 = direção left

        return neighbors

    def remove_walls(self, current_row, current_col, next_row, next_col, direction):
        """Remover paredes entre duas células"""
        if direction == 0:  # Top
            self.grid[current_row][current_col]['walls'][0] = False
            self.grid[next_row][next_col]['walls'][2] = False
        elif direction == 1:  # Right
            self.grid[current_row][current_col]['walls'][1] = False
            self.grid[next_row][next_col]['walls'][3] = False
        elif direction == 2:  # Bottom
            self.grid[current_row][current_col]['walls'][2] = False
            self.grid[next_row][next_col]['walls'][0] = False
        elif direction == 3:  # Left
            self.grid[current_row][current_col]['walls'][3] = False
            self.grid[next_row][next_col]['walls'][1] = False

    def generate_maze_recursive(self, row, col):
        """Algoritmo Recursive Backtracking (DFS)"""
        self.grid[row][col]['visited'] = True

        neighbors = self.get_neighbors(row, col)
        random.shuffle(neighbors)

        for next_row, next_col, direction in neighbors:
            if not self.grid[next_row][next_col]['visited']:
                self.remove_walls(row, col, next_row, next_col, direction)
                self.generate_maze_recursive(next_row, next_col)

    def ensure_fully_connected(self):
        """Garantir que todas as células estejam conectadas removendo paredes adicionais se necessário"""
        # Verificar células não visitadas e conectá-las
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col]['visited']:
                    # Encontrar célula vizinha visitada e remover parede
                    if row > 0 and self.grid[row-1][col]['visited']:
                        self.remove_walls(row, col, row-1, col, 0)
                        self.grid[row][col]['visited'] = True
                    elif col > 0 and self.grid[row][col-1]['visited']:
                        self.remove_walls(row, col, row, col-1, 3)
                        self.grid[row][col]['visited'] = True
                    elif row < self.rows-1 and self.grid[row+1][col]['visited']:
                        self.remove_walls(row, col, row+1, col, 2)
                        self.grid[row][col]['visited'] = True
                    elif col < self.cols-1 and self.grid[row][col+1]['visited']:
                        self.remove_walls(row, col, row, col+1, 1)
                        self.grid[row][col]['visited'] = True

    def grid_to_walls(self):
        """Converte a grade do labirinto em uma lista de retângulos de parede para renderização.
        Usa um conjunto para garantir que não haja paredes duplicadas, evitando sobreposições e artefatos."""
        walls = set()
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                # Adiciona a parede superior se existir
                if self.grid[r][c]['walls'][0]:
                    walls.add((x, y, self.cell_size, WALL_THICKNESS))
                # Adiciona a parede direita se existir
                if self.grid[r][c]['walls'][1]:
                    walls.add((x + self.cell_size, y, WALL_THICKNESS, self.cell_size))
                # Adiciona a parede inferior se existir
                if self.grid[r][c]['walls'][2]:
                    walls.add((x, y + self.cell_size, self.cell_size, WALL_THICKNESS))
                # Adiciona a parede esquerda se existir
                if self.grid[r][c]['walls'][3]:
                    walls.add((x, y, WALL_THICKNESS, self.cell_size))
        return list(walls)

    def detect_deadends(self):
        """Detectar células dead-end (com 3 paredes)"""
        deadends = []
        for r in range(self.rows):
            for c in range(self.cols):
                wall_count = sum(self.grid[r][c]['walls'])
                if wall_count == 3:  # Dead-end tem 3 paredes
                    # Evitar colocar mina na posição inicial (0,0) e final (última célula)
                    if not (r == 0 and c == 0) and not (r == self.rows-1 and c == self.cols-1):
                        deadends.append((r, c))
        return deadends

    def place_mines_in_deadends(self):
        """Colocar minas em 50% dos dead-ends"""
        deadends = self.detect_deadends()
        mine_count = max(1, len(deadends) // 2)  # 50% dos dead-ends
        mine_positions = random.sample(deadends, min(mine_count, len(deadends)))

        # Converter posições de grid para coordenadas de pixel (centro da célula)
        mines = []
        for row, col in mine_positions:
            center_x = col * self.cell_size + self.cell_size // 2
            center_y = row * self.cell_size + self.cell_size // 2
            mines.append(Mine(center_x, center_y))
        return mines

    def place_mines_everywhere(self, percentage=0.15):
        """Colocar minas em células aleatórias (para modo minefield), garantindo espaçamento."""
        total_cells = self.rows * self.cols
        mine_count = max(1, int(total_cells * percentage))

        # Criar lista de todas as posições possíveis para minas
        available_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                # Excluir a célula inicial e final
                if not (r == 0 and c == 0) and not (r == self.rows - 1 and c == self.cols - 1):
                    available_positions.append((r, c))

        random.shuffle(available_positions)

        mines = []
        occupied_cells = set()

        for r, c in available_positions:
            if len(mines) >= mine_count:
                break

            # Verificar se a célula ou suas vizinhas já estão ocupadas
            is_valid_position = True
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if (r + dr, c + dc) in occupied_cells:
                        is_valid_position = False
                        break
                if not is_valid_position:
                    break
            
            if is_valid_position:
                center_x = c * self.cell_size + self.cell_size // 2
                center_y = r * self.cell_size + self.cell_size // 2
                mines.append(Mine(center_x, center_y))
                occupied_cells.add((r,c))

        return mines

    @staticmethod
    def generate(level, world_width, world_height, game_mode='normal', mine_percentage=0.15, difficulty='normal'):
        """Gerar labirinto baseado no nível e dificuldade"""
        # Ajustar tamanho das células baseado no nível e dificuldade
        # Easy = maior, Hard = menor
        base_cell_size = 80
        if difficulty == 'easy':
            base_cell_size = 100
        elif difficulty == 'hard':
            base_cell_size = 60

        # Níveis mais altos diminuem um pouco o tamanho, mas respeitando a dificuldade
        cell_size = max(40, base_cell_size - (level - 1) * 2)

        # Criar gerador com margens, ajustando a altura para a nova margem superior
        maze_width_available = world_width - (MAZE_MARGIN * 2)
        maze_height_available = world_height - (MAZE_MARGIN_TOP + MAZE_MARGIN)

        # Ajusta a largura e altura do labirinto para serem múltiplos do tamanho da célula,
        # e evita áreas não utilizadas nas bordas direita e inferior.
        maze_width = (maze_width_available // cell_size) * cell_size
        maze_height = (maze_height_available // cell_size) * cell_size
        
        generator = MazeGenerator(maze_width, maze_height, cell_size)

        # CORREÇÃO: Começar sempre do canto superior esquerdo (0, 0)
        # Isto garante que o algoritmo visite todas as células conectadas
        generator.generate_maze_recursive(0, 0)

        # Garantir que todas as células estejam conectadas
        generator.ensure_fully_connected()

        # Converter para paredes e adicionar offset da margem
        walls = generator.grid_to_walls()

        # Aplicar offset da margem a todas as paredes, usando a margem superior nova
        walls_with_margin = []
        for wall in walls:
            x, y, width, height = wall
            walls_with_margin.append((x + MAZE_MARGIN, y + MAZE_MARGIN_TOP, width, height))

        # Gerar minas baseado no modo de jogo e dificuldade
        # Ajustar percentagem baseada na dificuldade
        adjusted_percentage = mine_percentage
        if difficulty == 'easy':
            adjusted_percentage *= 0.6
        elif difficulty == 'hard':
            adjusted_percentage *= 1.4
            
        mines = []
        if game_mode == 'minefield':
            # Minas espalhadas aleatoriamente
            mines = generator.place_mines_everywhere(adjusted_percentage)
        elif game_mode == 'normal':
            # Sem minas no modo normal
            mines = []
        # Outros modos também podem ter minas se necessário

        # Aplicar offset da margem às minas
        for mine in mines:
            mine.x += MAZE_MARGIN
            mine.y += MAZE_MARGIN_TOP

        # Calculate Goal Position (Center of last cell)
        # Last cell is at (maze_width - cell_size, maze_height - cell_size) relative to maze origin
        # Plus margins and half cell size for center
        goal_x = MAZE_MARGIN + maze_width - (cell_size // 2)
        goal_y = MAZE_MARGIN_TOP + maze_height - (cell_size // 2)

        return walls_with_margin, mines, (goal_x, goal_y), cell_size

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # Set window icon BEFORE set_mode to avoid SetProp errors
        try:
            # Prefer PNG for Pygame compatibility
            icon_path = "icon.png"
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(sys._MEIPASS, 'icon.png')
            
            # Fallback to ICO if PNG not found
            if not os.path.exists(icon_path):
                icon_path = "icon.ico"
                if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')

            if os.path.exists(icon_path):
                icon_surface = pygame.image.load(icon_path)
                # Scale to 32x32 to prevent potential memory errors with large icons
                icon_surface = pygame.transform.scale(icon_surface, (32, 32))
                pygame.display.set_icon(icon_surface)
        except Exception as e:
            print(f"Warning: Could not set window icon: {e}")

        # Dimensões da janela (redimensionável)
        self.window_width = DEFAULT_WIDTH
        self.window_height = DEFAULT_HEIGHT
        
        # Try to set mode, fallback if SetProp fails (common on Windows)
        try:
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
        except pygame.error as e:
            print(f"Warning: Failed to set RESIZABLE mode ({e}). Retrying without it.")
            try:
                self.screen = pygame.display.set_mode(
                    (self.window_width, self.window_height)
                )
            except pygame.error as e2:
                print(f"Critical Error: Failed to set video mode: {e2}")
                raise e2

        pygame.display.set_caption("GravityMaze - Controlo ADXL345")

        self.clock = pygame.time.Clock()

        # Dimensões virtuais do mundo do jogo (fixas)
        self.world_width = DEFAULT_WIDTH
        self.world_height = DEFAULT_HEIGHT

        # Surface virtual para renderizar o jogo
        self.world_surface = pygame.Surface((self.world_width, self.world_height))

        # Fontes (ajustadas para resolução maior)
        self.title_font = pygame.font.Font(None, 96)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        # Configurações persistentes
        self.config = Config()

        # Volume control (0.0 to 1.0)
        self.game_volume = self.config.get('game_volume')

        # Generate game sounds
        try:
            self.sound_level_complete = generate_level_complete_sound()
            self.sound_mine_hit = generate_mine_hit_sound()
            self.sound_game_over = generate_game_over_sound()
            self.sound_wall_collision = generate_wall_collision_sound()

            # Set initial volumes
            self.sound_level_complete.set_volume(self.game_volume)
            self.sound_mine_hit.set_volume(self.game_volume)
            self.sound_game_over.set_volume(self.game_volume)
            self.sound_wall_collision.set_volume(self.game_volume * 0.3)  # Wall collision is quieter
        except Exception as e:
            print(f"Warning: Could not generate sounds: {e}")
            self.sound_level_complete = None
            self.sound_mine_hit = None
            self.sound_game_over = None
            self.sound_wall_collision = None

        # Base de dados
        self.db = Database()

        # Serial
        self.serial_port = None
        self.serial_connected = False

        # Dados do acelerómetro
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        
        self.accel2_x = 0
        self.accel2_y = 0

        # Aceleração do teclado (para combinar com acelerómetro)
        self.keyboard_accel_x = 0
        self.keyboard_accel_y = 0
        
        self.keyboard2_accel_x = 0
        self.keyboard2_accel_y = 0

        # Configurações (carregar do arquivo)
        self.sensitivity = self.config.get('sensitivity')
        self.invert_x = self.config.get('invert_x')
        self.invert_y = self.config.get('invert_y')
        self.swap_xy = self.config.get('swap_xy')
        self.language = self.config.get('language')

        # Modo de jogo
        self.game_mode = 'normal'  # normal, minefield, timeattack, elimination
        self.difficulty = 'normal' # easy, normal, hard
        self.num_players = 1 # 1 or 2
        self.ball2 = None
        self.player1_finished = False
        self.player2_finished = False
        self.player1_time = 0
        self.player2_time = 0
        self.player1_score = 0
        self.player2_score = 0
        self.player1_lives = 0
        self.player2_lives = 0
        self.winner = None # "Player 1", "Player 2" or None
        self.stm32_ports = [] # List of connected STM32 ports
        self.p1_port_index = -1
        self.p2_port_index = -1


        # Sistema de vidas
        self.lives = 5
        self.max_lives = 5
        self.life_lost_animation_time = 0
        self.mine_hit_animation_time = 0

        # Sistema de precisão (modo normal)
        self.precision_score = 0
        self.wall_collisions = 0
        self.collision_pause_time = 0
        self.last_precision_update = 0

        # Lista de minas no labirinto atual
        self.mines = []

        # Estado do jogo
        self.state = "MENU"  # MENU, SETTINGS, PLAYING, PAUSED, WIN, LEADERBOARD, MODE_SELECT, NAME_INPUT, GAME_OVER, PLAYER_PROFILE, DIFFICULTY_SELECT, STM32_SETUP, CONTROLS
        self.running = True
        self.pending_score_data = None  # Store score data until name is entered
        self.selected_player_name = None  # For player profile view
        self.level = 1
        self.timer = 0
        self.player_name = "Player"

        # Leaderboard filter
        self.leaderboard_filter = None  # None = all modes

        # Estatísticas
        self.total_time = 0
        self.best_time = float('inf')
        self.levels_completed = 0

        # Controlo de input para prevenir múltiplas alternâncias
        self.last_esc_time = 0
        self.esc_cooldown = 0.3  # segundos

        # Controlo de beeps para colisões
        self.last_beep_time = 0

        # Armazenar velocidade da bola quando pausado
        self.paused_vx = 0
        self.paused_vy = 0

        # Controlo de redesenho do menu de pausa
        self.pause_menu_dirty = True
        
        # Cursor state
        self.cursor_hand_active = False

        # Criar menus
        self.create_menus()

        # Tentar conectar ao serial automaticamente
        self.connect_serial()
        
        # Iniciar thread de scan em background
        self.scan_thread = threading.Thread(target=self.serial_scan_loop, daemon=True)
        self.scan_thread.start()

        # Inicializar jogo
        self.init_level()

    def serial_scan_loop(self):
        """Background thread to scan for STM32 ports continuously"""
        while self.running:
            try:
                ports = self.scan_stm32_ports()
                self.stm32_ports = ports
            except Exception as e:
                print(f"Error in scan thread: {e}")
            time.sleep(2) # Scan every 2 seconds

    def send_beep_command(self):
        """Enviar comando 'B' para o STM32 fazer beep de forma assíncrona."""
        def beep_async():
            try:
                if self.serial_port and self.serial_port.is_open:
                    # Configurar timeout temporário para não bloquear
                    old_timeout = self.serial_port.timeout
                    self.serial_port.timeout = 0.1  # 100ms timeout
                    self.serial_port.write(b'B')
                    self.serial_port.flush()  # Garantir que o comando é enviado
                    self.serial_port.timeout = old_timeout
            except Exception as e:
                print(f"Erro ao enviar comando beep: {e}")

        # Executar em thread separada para não bloquear o jogo
        beep_thread = threading.Thread(target=beep_async, daemon=True)
        beep_thread.start()

    def send_mine_command(self):
        """Enviar comando 'L' para o STM32 quando pisar mina de forma assíncrona."""
        def mine_async():
            try:
                if self.serial_port and self.serial_port.is_open:
                    # Configurar timeout temporário para não bloquear
                    old_timeout = self.serial_port.timeout
                    self.serial_port.timeout = 0.1  # 100ms timeout
                    self.serial_port.write(b'L')
                    self.serial_port.flush()  # Garantir que o comando é enviado
                    self.serial_port.timeout = old_timeout
            except Exception as e:
                print(f"Erro ao enviar comando mina: {e}")

        # Executar em thread separada para não bloquear o jogo
        mine_thread = threading.Thread(target=mine_async, daemon=True)
        mine_thread.start()

    def create_stm32_setup_buttons(self):
        """Criar botões para configuração STM32"""
        center_x = self.world_width // 2
        button_width = 400
        button_height = 60
        
        self.stm32_setup_buttons = [
            Button(center_x - button_width // 2, 400, button_width, button_height, t('beep_1', self.language), BLUE),
            Button(center_x - button_width // 2, 480, button_width, button_height, t('beep_2', self.language), RED),
            Button(center_x - button_width // 2, 600, button_width, button_height, t('continue', self.language), DARK_GREEN),
            Button(center_x - button_width // 2, 670, button_width, button_height, t('back', self.language), GRAY),
        ]

    def draw_stm32_setup(self):
        """Desenhar tela de configuração STM32"""
        self.world_surface.fill(BLACK)
        
        # Update texts
        self.stm32_setup_buttons[0].text = t('beep_1', self.language)
        self.stm32_setup_buttons[1].text = t('beep_2', self.language)
        self.stm32_setup_buttons[2].text = t('continue', self.language)
        self.stm32_setup_buttons[3].text = t('back', self.language)
        
        # Title
        title = self.font.render(t('stm32_setup', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 80))
        self.world_surface.blit(title, title_rect)
        
        # Info
        info_text = "Detectados: " + ", ".join(self.stm32_ports)
        info = self.small_font.render(info_text, True, GRAY)
        info_rect = info.get_rect(center=(self.world_width // 2, 150))
        self.world_surface.blit(info, info_rect)
        
        # Instructions
        instr = self.small_font.render("Teste qual placa é qual para posicionar corretamente.", True, WHITE)
        instr_rect = instr.get_rect(center=(self.world_width // 2, 200))
        self.world_surface.blit(instr, instr_rect)
        
        # Player Assignments
        p1_txt = f"{t('player_1', self.language)}: {self.stm32_ports[0] if len(self.stm32_ports) > 0 else 'N/A'} (Setas)"
        p2_txt = f"{t('player_2', self.language)}: {self.stm32_ports[1] if len(self.stm32_ports) > 1 else 'N/A'} (WASD)"
        
        p1_surf = self.font.render(p1_txt, True, RED) # Player 1 is Red
        p2_surf = self.font.render(p2_txt, True, GREEN) # Player 2 is Green
        
        self.world_surface.blit(p1_surf, p1_surf.get_rect(center=(self.world_width // 2, 280)))
        self.world_surface.blit(p2_surf, p2_surf.get_rect(center=(self.world_width // 2, 330)))

        for button in self.stm32_setup_buttons:
            button.draw(self.world_surface, self.font)
            
        self.render_world_to_screen()
        pygame.display.flip()

    def send_beep_to_port(self, port_name):
        """Enviar beep para uma porta específica"""
        def beep_async():
            try:
                with serial.Serial(port_name, 115200, timeout=0.1) as ser:
                    ser.write(b'B')
            except Exception as e:
                print(f"Erro beep {port_name}: {e}")
        threading.Thread(target=beep_async, daemon=True).start()

    def handle_stm32_setup_events(self, event):
        """Eventos configuração STM32"""
        for i, button in enumerate(self.stm32_setup_buttons):
            if button.handle_event(event):
                if i == 0: # Beep 1
                    if len(self.stm32_ports) > 0:
                        self.send_beep_to_port(self.stm32_ports[0])
                elif i == 1: # Beep 2
                    if len(self.stm32_ports) > 1:
                        self.send_beep_to_port(self.stm32_ports[1])
                elif i == 2: # Continue
                    # Connect to ports
                    try:
                        if self.serial_port:
                            self.serial_port.close()
                        
                        # Connect P1
                        if len(self.stm32_ports) > 0:
                            self.serial_port = serial.Serial(self.stm32_ports[0], 115200, timeout=0.01)
                            self.serial_connected = True
                        
                        # P2 handled separately? 
                        # Currently self.serial_port is only one.
                        # I need to handle 2 serial ports in the game loop.
                        # For now, let's assume I need to change `read_serial` to read from multiple.
                        pass 
                    except:
                        pass
                    self.state = "MODE_SELECT"
                elif i == 3: # Back
                    self.state = "PLAYER_SELECT"

    def create_difficulty_buttons(self):
        """Criar botões de seleção de dificuldade"""
        button_width = 400
        button_height = 70
        center_x = self.world_width // 2 - button_width // 2
        
        # Consistent layout: Options start at 300, Back at 600
        self.difficulty_buttons = [
            Button(center_x, 300, button_width, button_height, "Easy", DARK_GREEN),
            Button(center_x, 390, button_width, button_height, "Normal", ORANGE),
            Button(center_x, 480, button_width, button_height, "Hard", RED),
            Button(center_x, 600, button_width, button_height, "Back", GRAY)
        ]

    def draw_difficulty_select(self):
        """Desenhar menu de seleção de dificuldade"""
        self.world_surface.fill(BLACK)
        
        # Update texts
        self.difficulty_buttons[0].text = t('difficulty_easy', self.language)
        self.difficulty_buttons[1].text = t('difficulty_normal', self.language)
        self.difficulty_buttons[2].text = t('difficulty_hard', self.language)
        self.difficulty_buttons[3].text = t('back', self.language)
        
        # Title
        title = self.font.render(t('select_difficulty', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))
        self.world_surface.blit(title, title_rect)
        
        for button in self.difficulty_buttons:
            button.draw(self.world_surface, self.font)
            
        self.render_world_to_screen()
        pygame.display.flip()
        
    def handle_difficulty_select_events(self, event):
        """Handle difficulty selection events"""
        for i, button in enumerate(self.difficulty_buttons):
            if button.handle_event(event):
                if i == 0:
                    self.difficulty = 'easy'
                    self.state = "PLAYER_SELECT"
                elif i == 1:
                    self.difficulty = 'normal'
                    self.state = "PLAYER_SELECT"
                elif i == 2:
                    self.difficulty = 'hard'
                    self.state = "PLAYER_SELECT"
                elif i == 3:
                    self.state = "MENU"

    def create_menus(self):
        """Criar botões dos menus estilo Minecraft"""
        button_width = 400
        button_height = 70
        center_x = self.world_width // 2 - button_width // 2
        
        # Create difficulty buttons
        self.create_difficulty_buttons()

        # Menu principal (will use translations when drawing)
        # Consistent layout: Options start at 300
        self.main_menu_buttons = [
            Button(center_x, 300, button_width, button_height, t('play', self.language), DARK_GREEN),
            Button(center_x, 390, button_width, button_height, t('settings', self.language), BLUE),
            Button(center_x, 480, button_width, button_height, t('leaderboard', self.language), ORANGE),
            Button(center_x, 570, button_width, button_height, t('exit', self.language), RED),
        ]

        # Menu de definições
        self.settings_buttons = [
            Button(center_x, 600, button_width, button_height, t('back', self.language), GRAY),
        ]

        # Language toggle button in settings - small, centered below title
        lang_button_width = 80
        lang_button_height = 40
        self.language_button = Button(self.world_width // 2 - lang_button_width // 2, 90,
                                       lang_button_width, lang_button_height,
                                       "PT" if self.language == 'pt' else "EN", BLUE)

        # Sliders de configuração
        self.volume_slider = Slider(center_x, 180, button_width, 0.0, 1.0, self.game_volume, "Volume")
        self.sensitivity_slider = Slider(center_x, 280, button_width, 0.1, 2.0, self.sensitivity, "Sensibilidade")

        # Menu de pausa
        self.pause_menu_buttons = [
            Button(center_x, 280, button_width, button_height, "Continuar", DARK_GREEN),
            Button(center_x, 370, button_width, button_height, "Reiniciar Nível", GOLD),
            Button(center_x, 460, button_width, button_height, "Menu Principal", GRAY),
        ]

        # Menu de vitória (lowered by 60px)
        self.win_menu_buttons = [
            Button(center_x, 540, button_width, button_height, "Próximo Nível", DARK_GREEN),
            Button(center_x, 630, button_width, button_height, "Menu Principal", GRAY),
        ]

        # Leaderboard with filter buttons
        filter_button_width = 180
        filter_button_height = 40
        filter_y = 80
        filter_spacing = 10
        total_filter_width = filter_button_width * 5 + filter_spacing * 4
        filter_start_x = (self.world_width - total_filter_width) // 2

        self.leaderboard_filter_buttons = [
            Button(filter_start_x, filter_y, filter_button_width, filter_button_height, "Todos", BLUE),
            Button(filter_start_x + (filter_button_width + filter_spacing), filter_y, filter_button_width, filter_button_height, "Normal", DARK_GREEN),
            Button(filter_start_x + (filter_button_width + filter_spacing) * 2, filter_y, filter_button_width, filter_button_height, "Minefield", RED),
            Button(filter_start_x + (filter_button_width + filter_spacing) * 3, filter_y, filter_button_width, filter_button_height, "Time Attack", GOLD),
            Button(filter_start_x + (filter_button_width + filter_spacing) * 4, filter_y, filter_button_width, filter_button_height, "Elimination", (255, 100, 0)),
        ]

        self.leaderboard_buttons = [
            Button(center_x, 600, button_width, button_height, "Voltar", GRAY),
        ]

        # Menu de seleção de modos - usar cards verticais
        card_width = 600
        card_height = 105
        card_x = self.world_width // 2 - card_width // 2
        start_y = 100
        card_spacing = 8

        self.mode_cards = [
            ModeCard(card_x, start_y, card_width, card_height,
                    'normal', 'Normal',
                    GAME_MODES['normal']['desc_pt'], DARK_GREEN),
            ModeCard(card_x, start_y + card_height + card_spacing, card_width, card_height,
                    'minefield', 'Campo Minado',
                    GAME_MODES['minefield']['desc_pt'], RED),
            ModeCard(card_x, start_y + (card_height + card_spacing) * 2, card_width, card_height,
                    'timeattack', 'Contra-Relógio',
                    GAME_MODES['timeattack']['desc_pt'], GOLD),
            ModeCard(card_x, start_y + (card_height + card_spacing) * 3, card_width, card_height,
                    'elimination', 'Eliminação',
                    GAME_MODES['elimination']['desc_pt'], (255, 100, 0)),
        ]

        # Botão voltar abaixo dos cards
        self.mode_select_back_button = Button(center_x, start_y + (card_height + card_spacing) * 4 + 20,
                                               button_width, button_height, "Voltar", GRAY)

        # Menu de seleção de jogadores
        self.player_select_buttons = [
            Button(center_x, 300, button_width, button_height, t('single_player', self.language), BLUE),
            Button(center_x, 390, button_width, button_height, t('multi_player', self.language), RED),
            Button(center_x, 600, button_width, button_height, t('back', self.language), GRAY),
        ]

        # Menu de Game Over
        self.gameover_buttons = [
            Button(center_x, 400, button_width, button_height, "Tentar Novamente", DARK_GREEN),
            Button(center_x, 490, button_width, button_height, "Menu Principal", GRAY),
        ]
        
        # Menu de Vitória Multiplayer
        self.mp_win_buttons = [
            Button(center_x, 400, button_width, button_height, t('play_again', self.language), DARK_GREEN),
            Button(center_x, 490, button_width, button_height, "Menu Principal", GRAY),
        ]

        # Name input dialog
        input_width = 400
        input_height = 50
        self.name_input = TextInput(self.world_width // 2 - input_width // 2, 320, input_width, input_height)

        # Center-aligned buttons with spacing - match textbox width
        button_spacing = 20
        button_width_each = (input_width - button_spacing) // 2  # 190px each to match 400px textbox
        buttons_start_x = center_x - input_width // 2
        self.name_input_buttons = [
            Button(buttons_start_x, 420, button_width_each, button_height, "Guardar", DARK_GREEN),
            Button(buttons_start_x + button_width_each + button_spacing, 420, button_width_each, button_height, "Descartar", GRAY),
        ]

    def connect_serial(self):
        """Conectar à porta série do STM32"""
        ports = self.scan_stm32_ports()
        self.stm32_ports = ports  # Update cached list
        
        if ports:
            try:
                print(f"  A tentar conectar a {ports[0]}...")
                self.serial_port = serial.Serial(
                    ports[0],
                    baudrate=115200,
                    timeout=0.01
                )
                self.serial_connected = True
                print(f"  [OK] Conectado a: {ports[0]}")
                return True
            except Exception as e:
                print(f"  [X] Erro ao conectar a {ports[0]}: {e}")
        
        print("\nAVISO: Nenhum STM32 encontrado. A usar teclado para controlo.")
        return False

    def scan_stm32_ports(self):
        """Procurar por portas STM32 disponíveis"""
        ports = serial.tools.list_ports.comports()
        stm32_identifiers = [
            'STM32', 'STMicroelectronics', 'VCP', 'USB Serial Device',
            'USB-SERIAL CH340', 'CP210', 'FTDI'
        ]
        
        found_ports = []
        for port in ports:
            is_stm32 = False
            if port.description:
                for identifier in stm32_identifiers:
                    if identifier.lower() in port.description.lower():
                        is_stm32 = True
                        break
            if not is_stm32 and port.manufacturer:
                for identifier in stm32_identifiers:
                    if identifier.lower() in port.manufacturer.lower():
                        is_stm32 = True
                        break
            if not is_stm32 and port.vid == 0x0483:
                is_stm32 = True

            if is_stm32:
                found_ports.append(port.device)
        
        return found_ports

    def init_level(self):
        """Inicializar um novo nível"""
        # Obter configuração do modo atual
        mode_config = GAME_MODES.get(self.game_mode, {})
        mine_percentage = mode_config.get('mine_percentage', 0.15)

        # Gerar labirinto com minas (usando dificuldade)
        self.walls, self.mines, self.goal_pos, current_cell_size = MazeGenerator.generate(
            self.level,
            self.world_width,
            self.world_height,
            self.game_mode,
            mine_percentage,
            self.difficulty
        )

        # Adjust goal radius to fit in cell (max 30, or 40% of cell size to avoid touching walls)
        self.goal_radius = min(30, int(current_cell_size * 0.4))

        # Posição inicial da bola (com margem segura)
        ball_start_x = MAZE_MARGIN + 60
        ball_start_y = MAZE_MARGIN_TOP + 60
        self.ball = Ball(ball_start_x, ball_start_y, self.sensitivity, self.world_width, self.world_height)
        
        # Setup Multiplayer
        if self.num_players == 2:
            # Balls placed equidistant from the top-left corner (0,0) of the cell
            # This forms a triangle with the corner wall, ensuring fairness.
            
            # Distances within the cell
            dist_far = current_cell_size * 0.75
            dist_close = current_cell_size * 0.25
            
            start_x = MAZE_MARGIN
            start_y = MAZE_MARGIN_TOP
            
            # P1 (Red): Further Right, Closer to Top
            self.ball.x = start_x + dist_far
            self.ball.y = start_y + dist_close
            
            # P2 (Green): Further Down, Closer to Left
            self.ball2 = Ball(start_x + dist_close, start_y + dist_far, self.sensitivity, self.world_width, self.world_height, color=GREEN)
            
            self.player1_finished = False
            self.player2_finished = False
            
            # Store starting distances for score calculation
            self.p1_start_dist = math.sqrt((self.ball.x - self.goal_pos[0])**2 + (self.ball.y - self.goal_pos[1])**2)
            self.p2_start_dist = math.sqrt((self.ball2.x - self.goal_pos[0])**2 + (self.ball2.y - self.goal_pos[1])**2)
        else:
            self.ball2 = None

        # Resetar variáveis do nível
        self.timer = 0
        self.level_start_time = time.time()
        self.mine_hit_animation_time = 0

        # Resetar sistema de precisão
        if mode_config.get('track_precision', False):
            self.wall_collisions = 0
            self.precision_score = 0
            self.collision_pause_time = 0
            self.last_precision_update = time.time()

        # Configurar timer baseado no modo e dificuldade
        if mode_config.get('timer_direction') == 'down':
            if self.game_mode == 'elimination':
                 # Random time adjustments based on difficulty
                 base_min, base_max = 30, 80
                 if self.difficulty == 'easy':
                     base_min, base_max = 45, 100
                 elif self.difficulty == 'hard':
                     base_min, base_max = 35, 75
                 
                 self.timer = random.randint(base_min, base_max)
            elif mode_config.get('random_time_on_level', False):
                # Fallback logic
                min_time = mode_config.get('random_time_min', 30)
                max_time = mode_config.get('random_time_max', 80)
                self.timer = random.randint(min_time, max_time)
            else:
                # Modo time attack - tempo fixo adjusted by difficulty
                base_time = mode_config.get('initial_time', 60)
                if self.difficulty == 'easy':
                    self.timer = base_time + 60 # +1 min
                elif self.difficulty == 'hard':
                    self.timer = max(30, base_time - 60) # -1 min
                else:
                    self.timer = base_time

    def get_scale_and_offset(self):
        """Calcular escala e offset para manter proporções ao redimensionar"""
        # Calcular razão de aspecto
        window_ratio = self.window_width / self.window_height
        world_ratio = self.world_width / self.world_height

        if window_ratio > world_ratio:
            # Janela mais larga - escalar por altura
            scale = self.window_height / self.world_height
            scaled_width = self.world_width * scale
            offset_x = (self.window_width - scaled_width) / 2
            offset_y = 0
        else:
            # Janela mais alta - escalar por largura
            scale = self.window_width / self.world_width
            scaled_height = self.world_height * scale
            offset_x = 0
            offset_y = (self.window_height - scaled_height) / 2

        return scale, offset_x, offset_y

    def screen_to_world(self, screen_x, screen_y):
        """Converter coordenadas da tela para coordenadas do mundo"""
        scale, offset_x, offset_y = self.get_scale_and_offset()
        world_x = (screen_x - offset_x) / scale
        world_y = (screen_y - offset_y) / scale
        return world_x, world_y

    def render_world_to_screen(self):
        """Renderizar surface do mundo na tela com escala correta"""
        scale, offset_x, offset_y = self.get_scale_and_offset()

        # Escalar a surface do mundo
        scaled_width = int(self.world_width * scale)
        scaled_height = int(self.world_height * scale)
        scaled_surface = pygame.transform.scale(self.world_surface, (scaled_width, scaled_height))

        # Limpar tela com preto (barras laterais)
        self.screen.fill(BLACK)

        # Desenhar surface escalada
        self.screen.blit(scaled_surface, (offset_x, offset_y))

    def read_serial(self):
        """Ler dados do acelerómetro via série"""
        if self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:
                    line = self.serial_port.readline().decode('utf-8').strip().replace("g","")
                    # Parse: "X:1.23,Y:-0.45,Z:0.98"
                    if line.startswith('X:'):
                        parts = line.split(',')
                        raw_x = 0
                        raw_y = 0
                        raw_z = 0

                        for part in parts:
                            if part.startswith('X:'):
                                raw_x = float(part[2:])
                            elif part.startswith('Y:'):
                                raw_y = float(part[2:])
                            elif part.startswith('Z:'):
                                raw_z = float(part[2:])

                        # Trocar X e Y se configurado (para diferentes orientações do STM32)
                        if self.swap_xy:
                            raw_x, raw_y = raw_y, raw_x

                        # Aplicar inversões
                        self.accel_x = -raw_x if self.invert_x else raw_x
                        self.accel_y = -raw_y if self.invert_y else raw_y
                        self.accel_z = raw_z
            except Exception:
                pass

    def handle_keyboard(self):
        """Controlo por teclado (fallback) - movimento direto sem gravidade"""
        keys = pygame.key.get_pressed()

        # Resetar aceleração do teclado
        self.keyboard_accel_x = 0
        self.keyboard_accel_y = 0
        self.keyboard2_accel_x = 0
        self.keyboard2_accel_y = 0

        # Calcular aceleração do teclado (normalizada para ser similar ao acelerómetro)
        # O acelerómetro retorna valores entre -1 e 1 (em g's)
        keyboard_accel_magnitude = 0.5  # Equivalente a 0.5g

        # Player 1 (Arrows)
        if keys[pygame.K_LEFT]:
            self.keyboard_accel_x -= keyboard_accel_magnitude
        if keys[pygame.K_RIGHT]:
            self.keyboard_accel_x += keyboard_accel_magnitude
        if keys[pygame.K_UP]:
            self.keyboard_accel_y -= keyboard_accel_magnitude
        if keys[pygame.K_DOWN]:
            self.keyboard_accel_y += keyboard_accel_magnitude
            
        # Player 2 (WASD)
        if self.num_players == 2:
            if keys[pygame.K_a]:
                self.keyboard2_accel_x -= keyboard_accel_magnitude
            if keys[pygame.K_d]:
                self.keyboard2_accel_x += keyboard_accel_magnitude
            if keys[pygame.K_w]:
                self.keyboard2_accel_y -= keyboard_accel_magnitude
            if keys[pygame.K_s]:
                self.keyboard2_accel_y += keyboard_accel_magnitude

        # Normalizar se diagonal (para não ter aceleração maior nas diagonais)
        if self.keyboard_accel_x != 0 and self.keyboard_accel_y != 0:
            diagonal_factor = 1 / math.sqrt(2)
            self.keyboard_accel_x *= diagonal_factor
            self.keyboard_accel_y *= diagonal_factor
            
        if self.keyboard2_accel_x != 0 and self.keyboard2_accel_y != 0:
            diagonal_factor = 1 / math.sqrt(2)
            self.keyboard2_accel_x *= diagonal_factor
            self.keyboard2_accel_y *= diagonal_factor

        # Reset da aceleração do acelerómetro quando se usa apenas teclado
        if not self.serial_connected:
            # Só resetar se não houver input de teclado
            if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]):
                self.accel_x = 0
                self.accel_y = 0
            if not any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]):
                self.accel2_x = 0
                self.accel2_y = 0

    def check_win(self):
        """Verificar se a bola chegou ao objetivo (buraco)"""
        # Evitar verificar se já estamos em estado de vitória
        if self.state != "PLAYING":
            return

        # Helper for single player win logic (reuse existing code logic)
        def process_level_complete(time_taken):
            # Toca o buzzer ao vencer
            self.send_beep_command()

            # Congelar a bola
            self.ball.vx = 0
            self.ball.vy = 0

            # Calcular tempo do nível
            self.total_time += time_taken
            self.best_time = min(self.best_time, time_taken)
            self.levels_completed += 1

            # Calcular pontuação
            mode_config = GAME_MODES.get(self.game_mode, {})
            if mode_config.get('track_precision', False):
                score = int(self.level * 1000 / max(0.1, time_taken)) + self.precision_score
            else:
                score = int(self.level * 1000 / max(0.1, time_taken))
            
            self.current_score = score
            self.total_score += score
            self.current_time = time_taken

            # Adicionar tempo aleatório no modo eliminação
            self.last_bonus_time = 0
            if mode_config.get('random_time_on_level', False):
                min_time = mode_config.get('random_time_min', 30)
                max_time = mode_config.get('random_time_max', 80)
                bonus_time = random.randint(min_time, max_time)
                self.timer += bonus_time
                self.last_bonus_time = bonus_time

            # Adicionar vida se alguma foi perdida
            if self.lives < self.max_lives:
                self.lives += 1

            # Store data for name input
            self.pending_score_data = {
                'level': self.level,
                'time': time_taken,
                'score': self.total_score,
                'game_mode': self.game_mode
            }

            # Avançar nível (Single Player Normal Mode is Infinite in existing code)
            # But multiplayer Normal is 1 level.
            if self.num_players == 2 and self.game_mode == 'normal':
                self.state = "WIN" # End after 1 level
            else:
                self.level += 1
                if self.sound_level_complete:
                    self.sound_level_complete.play()
                self.state = "WIN"

        if self.num_players == 1:
            dx = self.ball.x - self.goal_pos[0]
            dy = self.ball.y - self.goal_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)

            if distance < self.goal_radius:
                process_level_complete(time.time() - self.level_start_time)
        else:
            # Multiplayer
            current_time = time.time() - self.level_start_time
            
            # Check P1
            if not self.player1_finished:
                dist1 = math.sqrt((self.ball.x - self.goal_pos[0])**2 + (self.ball.y - self.goal_pos[1])**2)
                if dist1 < self.goal_radius:
                    self.player1_finished = True
                    self.player1_time = current_time
                    # Calculate P1 score
                    score = int(self.level * 1000 / max(0.1, current_time))
                    self.player1_score += score
                    
                    self.send_beep_command()
                    # Freeze ball
                    self.ball.vx = 0
                    self.ball.vy = 0
                    self.ball.x = -1000 # Move off screen
                    if self.sound_level_complete:
                        self.sound_level_complete.play()

            # Check P2
            if not self.player2_finished:
                dist2 = math.sqrt((self.ball2.x - self.goal_pos[0])**2 + (self.ball2.y - self.goal_pos[1])**2)
                if dist2 < self.goal_radius:
                    self.player2_finished = True
                    self.player2_time = current_time
                    # Calculate P2 score
                    score = int(self.level * 1000 / max(0.1, current_time))
                    self.player2_score += score
                    
                    self.send_beep_command()
                    # Freeze ball
                    self.ball2.vx = 0
                    self.ball2.vy = 0
                    self.ball2.x = -1000 # Move off screen
                    if self.sound_level_complete:
                        self.sound_level_complete.play()
            
            # Check conditions
            if self.player1_finished and self.player2_finished:
                # Both finished
                if self.game_mode == 'normal':
                    # Set current stats for WIN screen
                    self.current_time = max(self.player1_time, self.player2_time)
                    
                    # Determine Winner based on time
                    if self.player1_time < self.player2_time:
                        self.winner = "Player 1"
                    elif self.player2_time < self.player1_time:
                        self.winner = "Player 2"
                    else:
                        self.winner = "Draw"
                        
                    # Score calculation for MP (basic implementation)
                    mode_config = GAME_MODES.get(self.game_mode, {})
                    score = int(self.level * 1000 / max(0.1, self.current_time))
                    self.current_score = score
                    self.total_score += score
                    self.levels_completed += 1
                    self.total_time += self.current_time
                    
                    self.state = "MP_WIN" # End Game on special screen
                else:
                    # Minefield / Elimination - Continue to next level
                    self.level += 1
                    
                    # Add bonus time or Reset Time
                    mode_config = GAME_MODES.get(self.game_mode, {})
                    if self.game_mode == 'elimination':
                        # Reset to random time
                        self.timer = random.randint(30, 80)
                    elif mode_config.get('random_time_on_level', False):
                         bonus = random.randint(30, 80)
                         self.timer += bonus
                         
                    self.init_level()
                    # Reset finished flags
                    self.player1_finished = False
                    self.player2_finished = False

    def draw_direction_indicator(self):
        """Desenhar indicador de direção no top-center"""
        indicator_size = 40
        center_x = self.world_width // 2
        center_y = 60

        def draw_arrow(x, y, ax, ay, color):
            magnitude = math.sqrt(ax**2 + ay**2)
            if magnitude < 0.15:
                pygame.draw.circle(self.world_surface, color, (x, y), indicator_size // 2)
                pygame.draw.circle(self.world_surface, WHITE, (x, y), indicator_size // 2, 3)
            else:
                angle = math.atan2(ay, ax)
                arrow_length = indicator_size
                arrow_width = indicator_size // 2
                
                tip_x = x + arrow_length * math.cos(angle)
                tip_y = y + arrow_length * math.sin(angle)
                
                base_angle1 = angle + math.pi * 0.75
                base_angle2 = angle - math.pi * 0.75
                
                base1_x = x + arrow_width * math.cos(base_angle1)
                base1_y = y + arrow_width * math.sin(base_angle1)
                
                base2_x = x + arrow_width * math.cos(base_angle2)
                base2_y = y + arrow_width * math.sin(base_angle2)
                
                points = [(tip_x, tip_y), (base1_x, base1_y), (base2_x, base2_y)]
                pygame.draw.polygon(self.world_surface, color, points)
                pygame.draw.polygon(self.world_surface, WHITE, points, 3)

        if self.num_players == 2:
            # Player 1 (Red)
            combined_x1 = self.accel_x + self.keyboard_accel_x
            combined_y1 = self.accel_y + self.keyboard_accel_y
            draw_arrow(center_x - 30, center_y, combined_x1, combined_y1, RED)
            
            # Player 2 (Green)
            combined_x2 = self.accel2_x + self.keyboard2_accel_x
            combined_y2 = self.accel2_y + self.keyboard2_accel_y
            draw_arrow(center_x + 30, center_y, combined_x2, combined_y2, GREEN)
        else:
            # Single Player (Blue)
            combined_accel_x = self.accel_x + self.keyboard_accel_x
            combined_accel_y = self.accel_y + self.keyboard_accel_y
            draw_arrow(center_x, center_y, combined_accel_x, combined_accel_y, BLUE)

    def draw_hearts(self):
        """Desenhar corações (vidas) no centro inferior"""
        heart_size = 30
        heart_spacing = 40
        y_pos = self.world_height - 25

        # Calcular posição centralizada
        total_width = self.max_lives * heart_spacing - (heart_spacing - heart_size)
        start_x = (self.world_width - total_width) // 2

        for i in range(self.max_lives):
            x = start_x + i * heart_spacing + heart_size // 2

            # Animação de pulso quando perde vida
            scale = 1.0
            if self.life_lost_animation_time > 0:
                time_since_lost = time.time() - self.life_lost_animation_time
                if time_since_lost < 0.5:
                    # Check which heart to pulse based on who lost life
                    # If P1 lost and i == current_lives, pulse
                    # For shared/single player:
                    if self.num_players == 1 and int(i) == int(self.lives):
                         scale = 1.0 + 0.3 * math.sin(time_since_lost * 20)
                    # For MP, we could pulse specific half, but simpler to pulse whole heart if either lost
                    elif self.num_players == 2:
                         if (int(i) == int(self.player1_lives)) or (int(i) == int(self.player2_lives)):
                             scale = 1.0 + 0.3 * math.sin(time_since_lost * 20)

            size = int(heart_size * scale)
            
            # Shapes logic
            left_circle_pos = (int(x - size//4), int(y_pos - size//4))
            right_circle_pos = (int(x + size//4), int(y_pos - size//4))
            
            # Triangle points
            # Tip is at (x, y_pos + size//2)
            # Top Left is (x - size//2, y_pos - size//6)
            # Top Right is (x + size//2, y_pos - size//6)
            # Top Center is (x, y_pos - size//6)
            
            triangle_tip = (x, y_pos + size//2)
            triangle_top_left = (x - size//2, y_pos - size//6)
            triangle_top_right = (x + size//2, y_pos - size//6)
            triangle_top_center = (x, y_pos - size//6)

            if self.num_players == 2:
                # --- Multiplayer: Split Heart ---
                
                # Save current clip
                original_clip = self.world_surface.get_clip()
                
                # 1. Draw Left Half (Player 1 - RED)
                # Set clip to the left side of the heart's center x
                self.world_surface.set_clip(pygame.Rect(0, 0, x, self.world_height))
                
                color_p1 = RED if i < self.player1_lives else DARK_GRAY
                
                pygame.draw.circle(self.world_surface, color_p1, left_circle_pos, size//3)
                poly_p1 = [triangle_tip, triangle_top_left, triangle_top_center]
                pygame.draw.polygon(self.world_surface, color_p1, poly_p1)
                
                # 2. Draw Right Half (Player 2 - GREEN)
                # Set clip to the right side of the heart's center x
                self.world_surface.set_clip(pygame.Rect(x, 0, self.world_width - x, self.world_height))
                
                color_p2 = GREEN if i < self.player2_lives else DARK_GRAY
                
                pygame.draw.circle(self.world_surface, color_p2, right_circle_pos, size//3)
                poly_p2 = [triangle_tip, triangle_top_right, triangle_top_center]
                pygame.draw.polygon(self.world_surface, color_p2, poly_p2)
                
                # Reset Clip
                self.world_surface.set_clip(original_clip)
                
                # Draw a thin black line in the middle to separate
                # Extend line higher up to split circles visually
                line_top_y = y_pos - size//2
                pygame.draw.line(self.world_surface, BLACK, (x, line_top_y), triangle_tip, 2)
                
            else:
                # --- Single Player: Full Heart ---
                heart_color = RED if i < self.lives else DARK_GRAY
                
                # Draw both circles
                pygame.draw.circle(self.world_surface, heart_color, left_circle_pos, size//3)
                pygame.draw.circle(self.world_surface, heart_color, right_circle_pos, size//3)

                # Full Triangle
                triangle_points = [triangle_tip, triangle_top_left, triangle_top_right]
                pygame.draw.polygon(self.world_surface, heart_color, triangle_points)

    def draw_mines(self):
        """Desenhar minas no labirinto"""
        for mine in self.mines:
            mine.draw(self.world_surface)

    def draw_menu(self):
        """Desenhar menu principal"""
        self.world_surface.fill(BLACK)

        # Update button texts
        button_keys = ['play', 'settings', 'leaderboard', 'exit']
        for i, button in enumerate(self.main_menu_buttons):
            button.text = t(button_keys[i], self.language)

        # Título com efeito
        title = self.title_font.render(t('title', self.language), True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))

        # Sombra do título
        shadow = self.title_font.render(t('title', self.language), True, DARK_GREEN)
        shadow_rect = shadow.get_rect(center=(self.world_width // 2 + 5, 156))
        self.world_surface.blit(shadow, shadow_rect)
        self.world_surface.blit(title, title_rect)

        # Subtítulo
        subtitle = self.small_font.render(t('subtitle', self.language), True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(self.world_width // 2, 220))
        self.world_surface.blit(subtitle, subtitle_rect)

        # Botões
        for button in self.main_menu_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_player_select(self):
        """Desenhar menu de seleção de jogadores"""
        self.world_surface.fill(BLACK)

        # Update button texts
        self.player_select_buttons[0].text = t('single_player', self.language)
        self.player_select_buttons[1].text = t('multi_player', self.language)
        self.player_select_buttons[2].text = t('back', self.language)

        # Título
        title = self.font.render(t('select_players', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))
        self.world_surface.blit(title, title_rect)

        # Botões
        for button in self.player_select_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_settings(self):
        """Desenhar menu de definições"""
        self.world_surface.fill(BLACK)

        # Update button texts
        self.settings_buttons[0].text = t('back', self.language)

        # Título
        title = self.font.render(t('settings', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 50))
        self.world_surface.blit(title, title_rect)

        # Language selector as clickable text (below title, before sliders)
        lang_text = f"{t('language', self.language)}: {'PT' if self.language == 'pt' else 'EN'}"
        lang_surface = self.small_font.render(lang_text, True, WHITE)
        lang_rect = lang_surface.get_rect(center=(self.world_width // 2, 120))
        self.world_surface.blit(lang_surface, lang_rect)
        # Store rect for click detection
        self.language_text_rect = lang_rect

        # Volume slider
        self.volume_slider.label = t('volume', self.language)
        self.volume_slider.draw(self.world_surface, self.small_font)

        # Slider de sensibilidade
        self.sensitivity_slider.label = t('sensitivity', self.language)
        self.sensitivity_slider.draw(self.world_surface, self.small_font)

        # Opções de inversão
        yes_no = t('yes', self.language) if self.invert_x else t('no', self.language)
        invert_x_text = f"{t('invert_x', self.language)}: {yes_no}"
        yes_no = t('yes', self.language) if self.invert_y else t('no', self.language)
        invert_y_text = f"{t('invert_y', self.language)}: {yes_no}"
        yes_no = t('yes', self.language) if self.swap_xy else t('no', self.language)
        swap_xy_text = f"{t('swap_xy', self.language)}: {yes_no}"

        text_x = self.small_font.render(invert_x_text, True, WHITE)
        text_y = self.small_font.render(invert_y_text, True, WHITE)
        text_swap = self.small_font.render(swap_xy_text, True, WHITE)

        # Center-align the text blocks
        self.text_x_rect = text_x.get_rect(center=(self.world_width // 2, 360))
        self.text_y_rect = text_y.get_rect(center=(self.world_width // 2, 410))
        self.text_swap_rect = text_swap.get_rect(center=(self.world_width // 2, 460))

        self.world_surface.blit(text_x, self.text_x_rect)
        self.world_surface.blit(text_y, self.text_y_rect)
        self.world_surface.blit(text_swap, self.text_swap_rect)

        # Info de conexão serial - DETAILED
        # Use cached list from self.stm32_ports instead of scanning every frame
        num_detected = len(self.stm32_ports)
        
        if num_detected > 0:
            connection_text = f"{t('stm32_detected', self.language)}: {num_detected}"
            conn_color = GREEN
        else:
            connection_text = f"{t('stm32_detected', self.language)}: 0"
            conn_color = RED

        # Check for hover on the connection text to indicate clickability
        mouse_pos = pygame.mouse.get_pos()
        # We need to calculate the rect first to check hover, or use a pre-calculated position
        # Let's calculate rect, check hover, then draw with potential color change
        conn_surface_temp = self.small_font.render(connection_text, True, conn_color)
        conn_rect = conn_surface_temp.get_rect(center=(self.world_width // 2, 520))
        
        # Convert mouse pos for collision check
        scale, offset_x, offset_y = self.get_scale_and_offset()
        world_mouse_x = (mouse_pos[0] - offset_x) / scale
        world_mouse_y = (mouse_pos[1] - offset_y) / scale
        
        if conn_rect.collidepoint(world_mouse_x, world_mouse_y):
            conn_color = WHITE  # Highlight on hover
            
        conn_surface = self.small_font.render(connection_text, True, conn_color)
        self.world_surface.blit(conn_surface, conn_rect)
        self.connection_text_rect = conn_rect
        
        # Show Controls as Clickable Blue Text
        show_controls_text = t('show_commands', self.language)
        
        # Check hover for Show Controls
        show_c_surf_temp = self.small_font.render(show_controls_text, True, BLUE)
        show_controls_rect = show_c_surf_temp.get_rect(center=(self.world_width // 2, 560))
        
        show_c_color = BLUE
        if show_controls_rect.collidepoint(world_mouse_x, world_mouse_y):
            show_c_color = YELLOW
            
        show_controls_surface = self.small_font.render(show_controls_text, True, show_c_color)
        self.world_surface.blit(show_controls_surface, show_controls_rect)
        self.show_controls_text_rect = show_controls_rect

        # Botões
        for button in self.settings_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_controls(self):
        """Desenhar menu de comandos"""
        self.world_surface.fill(BLACK)
        
        # Title
        title = self.font.render(t('controls', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 50))
        self.world_surface.blit(title, title_rect)
        
        # Categories
        categories = [
            (t('general', self.language), ["ESC: " + t('pause', self.language), "R: " + t('restart', self.language)]),
            (t('movement', self.language), [t('single_player', self.language) + ": Acelerómetro / " + t('arrows', self.language)]),
            (t('multi_player', self.language), [
                t('player_1', self.language) + ": " + t('arrows', self.language) + " / STM32 (ID 1)",
                t('player_2', self.language) + ": " + t('wasd', self.language) + " / STM32 (ID 2)"
            ])
        ]
        
        y_offset = 120
        for cat_name, cmds in categories:
            # Category Title
            cat_surf = self.font.render(cat_name, True, GOLD)
            cat_rect = cat_surf.get_rect(center=(self.world_width // 2, y_offset))
            self.world_surface.blit(cat_surf, cat_rect)
            y_offset += 40
            
            # Commands
            for cmd in cmds:
                cmd_surf = self.small_font.render(cmd, True, WHITE)
                cmd_rect = cmd_surf.get_rect(center=(self.world_width // 2, y_offset))
                self.world_surface.blit(cmd_surf, cmd_rect)
                y_offset += 30
            y_offset += 20
            
        # Back Button
        if not hasattr(self, 'controls_back_button'):
            self.controls_back_button = Button(self.world_width // 2 - 200, 600, 400, 70, t('back', self.language), GRAY)
        
        # Update button position (in case it was created with old coordinates)
        self.controls_back_button.rect.y = 600
        self.controls_back_button.text = t('back', self.language)
        self.controls_back_button.draw(self.world_surface, self.font)
        
        self.render_world_to_screen()
        pygame.display.flip()

    def handle_controls_events(self, event):
        """Eventos do menu de comandos"""
        if hasattr(self, 'controls_back_button') and self.controls_back_button.handle_event(event):
            self.state = "SETTINGS"

    def draw_leaderboard(self):
        """Desenhar leaderboard com filtro de modo"""
        self.world_surface.fill(BLACK)

        # Update button texts
        self.leaderboard_buttons[0].text = t('back', self.language)

        # Título
        title = self.font.render(t('leaderboard', self.language), True, GOLD)
        title_rect = title.get_rect(center=(self.world_width // 2, 40))
        self.world_surface.blit(title, title_rect)

        # Filter buttons with colored outline for selection
        for i, button in enumerate(self.leaderboard_filter_buttons):
            # Update button text based on language
            button_texts = [
                t('all_modes', self.language),
                t('normal_mode', self.language),
                t('minefield_mode', self.language),
                t('timeattack_mode', self.language),
                t('elimination_mode', self.language)
            ]
            button.text = button_texts[i]

            # Draw button
            button.draw(self.world_surface, self.small_font)

            # Highlight selected filter with colored outline
            filter_mode = None if i == 0 else ['normal', 'minefield', 'timeattack', 'elimination'][i-1]
            if filter_mode == self.leaderboard_filter:
                # Draw thick outline in button's color
                outline_rect = pygame.Rect(button.rect.x - 4, button.rect.y - 4,
                                          button.rect.width + 8, button.rect.height + 8)
                pygame.draw.rect(self.world_surface, button.color, outline_rect, 4)

        # Cabeçalho - conditional based on filter
        show_mode = self.leaderboard_filter is None  # Show mode column when "All Modes" is selected

        if show_mode:
            # Order: #, Name, Date, Level, Time, Score, Mode
            headers = [
                t('rank', self.language),
                t('name', self.language),
                t('date', self.language),
                t('level', self.language),
                t('time', self.language),
                t('score', self.language),
                t('mode', self.language)
            ]
            # Column widths: # (50), Name (150), Date (150), Level (70), Time (90), Score (150), Mode (200)
            x_positions = [35, 90, 250, 410, 490, 590, 750]
        else:
            # Order: #, Name, Date, Level, Time, Score
            headers = [
                t('rank', self.language),
                t('name', self.language),
                t('date', self.language),
                t('level', self.language),
                t('time', self.language),
                t('score', self.language)
            ]
            # Column widths: # (50), Name (150), Date (150), Level (70), Time (90), Score (150)
            x_positions = [35, 90, 250, 410, 490, 590]

        y_offset = 135

        for i, header in enumerate(headers):
            text = self.small_font.render(header, True, GRAY)
            self.world_surface.blit(text, (x_positions[i], y_offset))

        # Linha separadora
        pygame.draw.line(self.world_surface, GRAY, (40, y_offset + 30), (self.world_width - 40, y_offset + 30), 2)

        # Scores - with filter (store rects for clickability)
        scores = self.db.get_top_scores(10, self.leaderboard_filter)
        y_offset = 175
        self.leaderboard_entry_rects = []  # Store entry positions for click detection

        for i, score_data in enumerate(scores):
            # Unpack data - now includes game_mode
            name, level, time_taken, score, date, game_mode = score_data
            color = GOLD if i == 0 else (LIGHT_GRAY if i == 1 else (GRAY if i == 2 else WHITE))

            # Create clickable rect for this entry
            entry_rect = pygame.Rect(40, y_offset - 5, self.world_width - 80, 30)
            self.leaderboard_entry_rects.append((entry_rect, name))

            # Highlight on hover (will be handled in event handler)
            # Draw hover background if mouse is over
            mouse_pos = pygame.mouse.get_pos()
            # Convert to world coordinates
            scale, offset_x, offset_y = self.get_scale_and_offset()
            world_mouse_x = (mouse_pos[0] - offset_x) / scale
            world_mouse_y = (mouse_pos[1] - offset_y) / scale
            if entry_rect.collidepoint(world_mouse_x, world_mouse_y):
                pygame.draw.rect(self.world_surface, (40, 40, 40), entry_rect)

            # Render each field with overflow handling
            rank = self.small_font.render(str(i + 1), True, color)
            # Limit name to 12 characters for overflow
            name_text = self.small_font.render(name[:12], True, color)
            level_text = self.small_font.render(str(level), True, color)
            time_text = self.small_font.render(f"{time_taken:.2f}s", True, color)
            score_text = self.small_font.render(str(score), True, color)
            # Date format: MM-DD HH:MM
            date_text = self.small_font.render(date[5:16], True, color)

            if show_mode:
                # Translate game mode name and limit to fit
                mode_key = f"{game_mode}_mode"
                mode_name = t(mode_key, self.language)
                # Limit mode name to fit the wider column
                if len(mode_name) > 20:
                    mode_name = mode_name[:17] + "..."
                mode_text = self.small_font.render(mode_name, True, color)

                # Order: #, Name, Date, Level, Time, Score, Mode
                self.world_surface.blit(rank, (x_positions[0], y_offset))
                self.world_surface.blit(name_text, (x_positions[1], y_offset))
                self.world_surface.blit(date_text, (x_positions[2], y_offset))
                self.world_surface.blit(level_text, (x_positions[3], y_offset))
                self.world_surface.blit(time_text, (x_positions[4], y_offset))
                self.world_surface.blit(score_text, (x_positions[5], y_offset))
                self.world_surface.blit(mode_text, (x_positions[6], y_offset))
            else:
                # Order: #, Name, Date, Level, Time, Score
                self.world_surface.blit(rank, (x_positions[0], y_offset))
                self.world_surface.blit(name_text, (x_positions[1], y_offset))
                self.world_surface.blit(date_text, (x_positions[2], y_offset))
                self.world_surface.blit(level_text, (x_positions[3], y_offset))
                self.world_surface.blit(time_text, (x_positions[4], y_offset))
                self.world_surface.blit(score_text, (x_positions[5], y_offset))

            y_offset += 35

        # Botões
        for button in self.leaderboard_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_playing(self):
        """Desenhar o jogo em andamento"""
        self.world_surface.fill(BLACK)

        # Desenhar paredes - Inflate by 1px to fix seams
        for wall in self.walls:
            # Create rect from tuple
            wall_rect = pygame.Rect(wall)
            
            # Sombra
            shadow_rect = pygame.Rect(wall[0] + 2, wall[1] + 2, wall[2], wall[3])
            pygame.draw.rect(self.world_surface, DARK_GRAY, shadow_rect)
            
            # Parede - Inflate to fix seams
            pygame.draw.rect(self.world_surface, WALL_COLOR, wall_rect.inflate(1, 1))

        # Desenhar objetivo como buraco verde com efeito
        for i in range(3):
            radius = self.goal_radius - i * 8
            color_intensity = 255 - i * 60
            color = (0, color_intensity, 0)
            pygame.draw.circle(self.world_surface, color, self.goal_pos, radius)

        # Círculo interno escuro (buraco)
        pygame.draw.circle(self.world_surface, DARK_GREEN, self.goal_pos, self.goal_radius // 2)

        # Desenhar minas
        self.draw_mines()

        # Desenhar bola (com animação de explosão se pisar mina)
        if self.mine_hit_animation_time > 0:
            # Animação de explosão
            animation_progress = (time.time() - self.mine_hit_animation_time) / 0.5
            explosion_radius = int(BALL_RADIUS * (1 + animation_progress * 2))
            explosion_alpha = int(255 * (1 - animation_progress))
            explosion_color = (255, explosion_alpha, 0)
            pygame.draw.circle(self.world_surface, explosion_color, (int(self.ball.x), int(self.ball.y)), explosion_radius, 3)

        self.ball.draw(self.world_surface)
        
        if self.ball2:
            self.ball2.draw(self.world_surface)

        # Indicador de direção
        self.draw_direction_indicator()

        # HUD
        # Timer
        mode_config = GAME_MODES.get(self.game_mode, {})
        if mode_config.get('timer_direction') == 'down':
            timer_text = self.font.render(f"{t('time', self.language)}: {self.timer:.1f}s", True, YELLOW if self.timer > 10 else RED)
        else:
            timer_text = self.font.render(f"{t('time', self.language)}: {self.timer:.1f}s", True, YELLOW)
        self.world_surface.blit(timer_text, (10, 10))

        # Nível (Hide in MP Normal Mode)
        if not (self.num_players == 2 and self.game_mode == 'normal'):
            level_text = self.font.render(f"{t('level', self.language)}: {self.level}", True, WHITE)
            # Right align with 10px margin
            level_rect = level_text.get_rect(topright=(self.world_width - 10, 10))
            self.world_surface.blit(level_text, level_rect)

        # MP Normal Mode: Early End Text
        if self.num_players == 2 and self.game_mode == 'normal' and (self.player1_finished or self.player2_finished):
             end_text_str = "Pressione 'T' para terminar" if self.language == 'pt' else "Press 'T' to end"
             end_text = self.small_font.render(end_text_str, True, WHITE)
             # Right align top (replaces Level text)
             end_rect = end_text.get_rect(topright=(self.world_width - 10, 10))
             self.world_surface.blit(end_text, end_rect)

        # Corações (vidas) no centro inferior - apenas no modo minefield
        if self.game_mode == 'minefield':
            self.draw_hearts()

        # Dados do acelerómetro + teclado (pequenos)
        combined_x = self.accel_x + self.keyboard_accel_x
        combined_y = self.accel_y + self.keyboard_accel_y
        accel_text = self.small_font.render(
            f"X:{combined_x:.2f} Y:{combined_y:.2f}",
            True, GRAY
        )
        self.world_surface.blit(accel_text, (10, self.world_height - 30))

        # Instruções - Right align with 10px margin
        instructions = self.small_font.render(t('hud_instructions', self.language), True, GRAY)
        inst_rect = instructions.get_rect(topright=(self.world_width - 10, self.world_height - 30))
        self.world_surface.blit(instructions, inst_rect)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_pause(self):
        """Desenhar menu de pausa"""
        # Só redesenhar se necessário (evita blinking)
        if not self.pause_menu_dirty:
            return

        # Desenhar jogo atrás com overlay escuro
        self.world_surface.fill(BLACK)

        # Desenhar paredes
        for wall in self.walls:
            # Sombra
            shadow_rect = pygame.Rect(wall[0] + 2, wall[1] + 2, wall[2], wall[3])
            pygame.draw.rect(self.world_surface, DARK_GRAY, shadow_rect)
            # Parede
            pygame.draw.rect(self.world_surface, WALL_COLOR, wall)

        # Desenhar objetivo
        for i in range(3):
            radius = self.goal_radius - i * 8
            color_intensity = 255 - i * 60
            color = (0, color_intensity, 0)
            pygame.draw.circle(self.world_surface, color, self.goal_pos, radius)

        pygame.draw.circle(self.world_surface, DARK_GREEN, self.goal_pos, self.goal_radius // 2)

        # Desenhar minas
        self.draw_mines()

        # Desenhar bola na posição pausada
        self.ball.draw(self.world_surface)
        if self.ball2:
            self.ball2.draw(self.world_surface)

        # Indicador de direção
        self.draw_direction_indicator()

        # HUD
        timer_text = self.font.render(f"{t('time', self.language)}: {self.timer:.1f}s", True, YELLOW)
        self.world_surface.blit(timer_text, (10, 10))

        level_text = self.font.render(f"{t('level', self.language)}: {self.level}", True, WHITE)
        self.world_surface.blit(level_text, (self.world_width - 150, 10))

        combined_x = self.accel_x + self.keyboard_accel_x
        combined_y = self.accel_y + self.keyboard_accel_y
        accel_text = self.small_font.render(
            f"X:{combined_x:.2f} Y:{combined_y:.2f}",
            True, GRAY
        )
        self.world_surface.blit(accel_text, (10, self.world_height - 30))

        instructions = self.small_font.render("ESC: Pausar | R: Reiniciar", True, GRAY)
        self.world_surface.blit(instructions, (self.world_width - 280, self.world_height - 30))

        # Overlay escuro
        overlay = pygame.Surface((self.world_width, self.world_height))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.world_surface.blit(overlay, (0, 0))

        # Update button texts
        button_keys = ['resume', 'restart', 'menu']
        for i, button in enumerate(self.pause_menu_buttons):
            button.text = t(button_keys[i], self.language)

        # Título
        title = self.font.render(t('paused', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))
        self.world_surface.blit(title, title_rect)

        # Botões
        for button in self.pause_menu_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

        # Marcar como limpo
        self.pause_menu_dirty = False

    def draw_win(self):
        """Desenhar tela de vitória com métricas"""
        self.world_surface.fill(BLACK)

        # Update button texts
        button_keys = ['next_level', 'menu']
        for i, button in enumerate(self.win_menu_buttons):
            button.text = t(button_keys[i], self.language)

        # Título
        title = self.title_font.render(t('level_complete', self.language), True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 80))
        self.world_surface.blit(title, title_rect)

        # Métricas
        metrics = [
            f"{t('level', self.language)}: {self.level}",
            f"{t('time', self.language)}: {self.current_time:.2f}s",
            f"{t('score', self.language)}: {self.current_score}",
        ]

        # Add time bonus for elimination mode
        if hasattr(self, 'last_bonus_time') and self.last_bonus_time > 0:
            metrics.append(f"{t('time_bonus', self.language)}: +{self.last_bonus_time}s")

        metrics.extend([
            "",
            f"{t('total_stats', self.language)}:",
            f"{t('levels_completed', self.language)}: {self.levels_completed}",
            f"{t('total_time', self.language)}: {self.total_time:.2f}s",
            f"{t('best_time', self.language)}: {self.best_time:.2f}s",
        ])

        y_offset = 180
        for metric in metrics:
            if metric:
                # Check for score or bonus in translation-agnostic way
                if t('score', self.language) in metric:
                    color = GOLD
                elif t('time_bonus', self.language) in metric:
                    color = GREEN
                else:
                    color = WHITE
                text = self.font.render(metric, True, color)
                text_rect = text.get_rect(center=(self.world_width // 2, y_offset))
                self.world_surface.blit(text, text_rect)
            y_offset += 40

        # Botões
        for button in self.win_menu_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_mode_select(self):
        """Desenhar menu de seleção de modo de jogo com cards verticais"""
        self.world_surface.fill(BLACK)

        # Update button texts and card descriptions
        self.mode_select_back_button.text = t('back', self.language)
        
        # Filter available modes
        mode_keys = ['normal', 'minefield', 'timeattack', 'elimination']
        if self.num_players == 2:
             mode_keys = ['normal', 'minefield', 'elimination']
             
        active_cards = []
        for i, key in enumerate(['normal', 'minefield', 'timeattack', 'elimination']):
            if key in mode_keys:
                active_cards.append(self.mode_cards[i])

        for card in active_cards:
            card.title = GAME_MODES[card.mode_name][f'name_{self.language}']
            card.description = GAME_MODES[card.mode_name][f'desc_{self.language}']

        # Título
        title = self.font.render(t('select_mode', self.language), True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 55))
        self.world_surface.blit(title, title_rect)

        # Draw mode cards with adjusted positions
        start_y = 150 # Increased space from title
        card_height = 105
        card_spacing = 8
        
        for i, card in enumerate(active_cards):
            card.rect.y = start_y + i * (card_height + card_spacing)
            card.draw(self.world_surface, self.font, self.small_font)

        # Draw back button (adjust position based on number of cards)
        self.mode_select_back_button.rect.y = start_y + len(active_cards) * (card_height + card_spacing) + 70 # Increased space before back button

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_name_input(self):
        """Desenhar tela de input de nome"""
        self.world_surface.fill(BLACK)

        # Update button texts
        self.name_input_buttons[0].text = t('save', self.language)
        self.name_input_buttons[1].text = t('discard', self.language)

        # Título
        title_text = t('save_progress', self.language)
        title = self.title_font.render(title_text, True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 100))
        self.world_surface.blit(title, title_rect)

        # Prompt
        prompt = self.font.render(t('enter_name', self.language), True, WHITE)
        prompt_rect = prompt.get_rect(center=(self.world_width // 2, 250))
        self.world_surface.blit(prompt, prompt_rect)

        # Text input field
        self.name_input.draw(self.world_surface, self.font)

        # Recalculate button positions to ensure they're centered
        # This ensures buttons are always centered even if screen size changes
        textbox_width = 400
        button_spacing = 20
        button_width_each = (textbox_width - button_spacing) // 2  # 190px each

        # Center the button group
        total_button_width = button_width_each * 2 + button_spacing  # 400px total
        buttons_start_x = (self.world_width // 2) - (total_button_width // 2)

        # Update button positions
        self.name_input_buttons[0].rect.x = buttons_start_x
        self.name_input_buttons[1].rect.x = buttons_start_x + button_width_each + button_spacing

        # Draw buttons
        for button in self.name_input_buttons:
            button.draw(self.world_surface, self.font)

        # Info text
        info = self.small_font.render("ENTER = " + t('save', self.language) + " | ESC = " + t('discard', self.language), True, GRAY)
        info_rect = info.get_rect(center=(self.world_width // 2, 520))
        self.world_surface.blit(info, info_rect)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_mp_win(self):
        """Desenhar tela de vitória multiplayer"""
        self.world_surface.fill(BLACK)
        
        # Update button texts
        self.mp_win_buttons[0].text = t('play_again', self.language)
        self.mp_win_buttons[1].text = t('menu', self.language)
        
        # Determine Title based on winner
        winner_text = t('draw', self.language)
        winner_color = WHITE
        
        # Check if it was a timeout draw or a normal win
        if self.winner == "Draw" or self.winner is None:
             if self.game_mode == 'elimination' and self.timer <= 0:
                 winner_text = t('game_over', self.language)
                 winner_color = RED
             else:
                 winner_text = t('draw', self.language)
        elif self.winner == "Player 1":
            winner_text = t('p1_wins', self.language)
            winner_color = RED
        elif self.winner == "Player 2":
            winner_text = t('p2_wins', self.language)
            winner_color = GREEN
            
        # Title
        title = self.title_font.render(winner_text, True, winner_color)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))
        self.world_surface.blit(title, title_rect)
        
        # Stats - Show P1 vs P2 Scores clearly
        score_text = f"P1: {self.player1_score}   VS   P2: {self.player2_score}"
        score_surf = self.font.render(score_text, True, GOLD)
        score_rect = score_surf.get_rect(center=(self.world_width // 2, 250))
        self.world_surface.blit(score_surf, score_rect)
        
        # Mode info
        if self.game_mode == 'elimination' and self.timer <= 0:
             pass # Already handled in title

        # Buttons
        for button in self.mp_win_buttons:
            button.draw(self.world_surface, self.font)
            
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_gameover(self):
        """Desenhar tela de game over"""
        self.world_surface.fill(BLACK)

        # Update button texts
        button_keys = ['try_again', 'menu']
        for i, button in enumerate(self.gameover_buttons):
            button.text = t(button_keys[i], self.language)

        # Título
        title = self.title_font.render(t('game_over', self.language), True, RED)
        title_rect = title.get_rect(center=(self.world_width // 2, 120))

        # Sombra
        shadow = self.title_font.render(t('game_over', self.language), True, DARK_GRAY)
        shadow_rect = shadow.get_rect(center=(self.world_width // 2 + 5, 126))
        self.world_surface.blit(shadow, shadow_rect)
        self.world_surface.blit(title, title_rect)

        # Estatísticas
        if self.num_players == 2:
            # Multiplayer - show both player scores
            stats = [
                f"{t('level_reached', self.language)}: {self.level}",
                "",
                f"Player 1: {self.player1_score}",
                f"Player 2: {self.player2_score}",
            ]
            
            y_offset = 240
            for i, stat in enumerate(stats):
                if stat:
                    # Color P1 red, P2 green
                    if "Player 1" in stat:
                        color = RED
                    elif "Player 2" in stat:
                        color = GREEN
                    else:
                        color = WHITE
                    text = self.font.render(stat, True, color)
                    text_rect = text.get_rect(center=(self.world_width // 2, y_offset))
                    self.world_surface.blit(text, text_rect)
                y_offset += 50
        else:
            # Single player
            current_score = self.total_score if self.levels_completed > 0 else self.precision_score
            stats = [
                f"{t('level_reached', self.language)}: {self.level}",
                f"{t('levels_completed', self.language)}: {self.levels_completed}",
                f"{t('total_time', self.language)}: {self.total_time:.2f}s",
                f"{t('score', self.language)}: {current_score}",
            ]

            y_offset = 240
            for stat in stats:
                text = self.font.render(stat, True, WHITE)
                text_rect = text.get_rect(center=(self.world_width // 2, y_offset))
                self.world_surface.blit(text, text_rect)
                y_offset += 50

        # Botões
        for button in self.gameover_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_player_profile(self):
        """Desenhar perfil do jogador"""
        self.world_surface.fill(BLACK)

        # Título - smaller font
        title = self.font.render(t('player_profile', self.language), True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 50))
        self.world_surface.blit(title, title_rect)

        # Player name - larger font
        name_text = self.title_font.render(self.selected_player_name, True, GOLD)
        name_rect = name_text.get_rect(center=(self.world_width // 2, 130))
        self.world_surface.blit(name_text, name_rect)

        # Get player stats
        stats = self.db.get_player_stats(self.selected_player_name)

        if stats:
            total_playtime, lvl_n, lvl_m, lvl_t, lvl_e, pts_n, pts_m, pts_t, pts_e = stats

            # Display stats
            y_offset = 200
            info_items = [
                f"{t('total_playtime', self.language)}: {total_playtime:.1f}s",
                "",
                f"{t('levels_by_mode', self.language)}:",
                f"  {t('normal_mode', self.language)}: {lvl_n}",
                f"  {t('minefield_mode', self.language)}: {lvl_m}",
                f"  {t('timeattack_mode', self.language)}: {lvl_t}",
                f"  {t('elimination_mode', self.language)}: {lvl_e}",
                "",
                f"{t('points_by_mode', self.language)}:",
                f"  {t('normal_mode', self.language)}: {pts_n}",
                f"  {t('minefield_mode', self.language)}: {pts_m}",
                f"  {t('timeattack_mode', self.language)}: {pts_t}",
                f"  {t('elimination_mode', self.language)}: {pts_e}",
            ]

            for item in info_items:
                if item:
                    text = self.small_font.render(item, True, WHITE)
                    text_rect = text.get_rect(center=(self.world_width // 2, y_offset))
                    self.world_surface.blit(text, text_rect)
                y_offset += 30
        else:
            no_data = self.font.render(t('no_data', self.language), True, GRAY)
            no_data_rect = no_data.get_rect(center=(self.world_width // 2, 300))
            self.world_surface.blit(no_data, no_data_rect)

        # Back button - create once if doesn't exist, update text each frame
        if not hasattr(self, 'player_profile_back_button'):
            self.player_profile_back_button = Button(self.world_width // 2 - 200, 600, 400, 70, t('back', self.language), GRAY)

        # Update button text for language
        self.player_profile_back_button.text = t('back', self.language)
        self.player_profile_back_button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def handle_player_profile_events(self, event):
        """Tratar eventos do perfil do jogador"""
        if hasattr(self, 'player_profile_back_button') and self.player_profile_back_button.handle_event(event):
            self.state = "LEADERBOARD"

    def handle_menu_events(self, event):
        """Tratar eventos do menu principal"""
        for i, button in enumerate(self.main_menu_buttons):
            if button.handle_event(event):
                if i == 0:  # Jogar - ir para seleção de dificuldade
                    self.state = "DIFFICULTY_SELECT"
                elif i == 1:  # Definições
                    self.state = "SETTINGS"
                elif i == 2:  # Leaderboard
                    self.state = "LEADERBOARD"
                elif i == 3:  # Sair
                    self.running = False

    def handle_player_select_events(self, event):
        """Tratar eventos do menu de seleção de jogadores"""
        for i, button in enumerate(self.player_select_buttons):
            if button.handle_event(event):
                if i == 0:  # Um Jogador
                    self.num_players = 1
                    self.state = "MODE_SELECT"
                elif i == 1:  # Multijogador
                    self.num_players = 2
                    # Verificar STM32 conectados
                    connected_ports = self.scan_stm32_ports()
                    if connected_ports:
                        self.state = "STM32_SETUP"
                        # Initialize setup
                        self.stm32_ports = connected_ports
                        self.p1_port_index = 0 if len(connected_ports) > 0 else -1
                        self.p2_port_index = 1 if len(connected_ports) > 1 else -1
                        # Create buttons for STM32 setup if they don't exist
                        self.create_stm32_setup_buttons()
                    else:
                        # No STM32, fallback to keyboard
                        self.state = "MODE_SELECT"
                elif i == 2:  # Voltar
                    self.state = "DIFFICULTY_SELECT"

    def handle_mode_select_events(self, event):
        """Tratar eventos do menu de seleção de modo"""
        # Filter available modes
        mode_keys = ['normal', 'minefield', 'timeattack', 'elimination']
        if self.num_players == 2:
             mode_keys = ['normal', 'minefield', 'elimination']
             
        active_cards = []
        for i, key in enumerate(['normal', 'minefield', 'timeattack', 'elimination']):
            if key in mode_keys:
                active_cards.append(self.mode_cards[i])

        # Handle mode cards
        for card in active_cards:
            if card.handle_event(event):
                self.game_mode = card.mode_name
                self.start_game()
                return

        # Handle back button
        if self.mode_select_back_button.handle_event(event):
            if self.num_players == 2:
                self.state = "PLAYER_SELECT" # Go back to player select if MP
            else:
                self.state = "PLAYER_SELECT" # Always go back to player select now


    def handle_mp_win_events(self, event):
        """Eventos da tela de vitória multiplayer"""
        for i, button in enumerate(self.mp_win_buttons):
            if button.handle_event(event):
                if i == 0: # Play Again
                    self.start_game()
                elif i == 1: # Menu (Skip Save)
                    self.state = "MENU"

    def handle_gameover_events(self, event):
        """Tratar eventos do menu de game over"""
        for i, button in enumerate(self.gameover_buttons):
            if button.handle_event(event):
                # Show name input screen if there's pending score data
                if self.pending_score_data:
                    self.name_input.text = self.player_name
                    self.state = "NAME_INPUT"
                else:
                    # No pending data, go directly
                    if i == 0:  # Tentar Novamente
                        # Reset everything for a fresh start
                        self.start_game()
                    elif i == 1:  # Menu Principal
                        self.state = "MENU"

    def handle_name_input_events(self, event):
        """Tratar eventos da tela de input de nome"""
        # Handle text input
        result = self.name_input.handle_event(event)

        if result == 'submit' or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            # Save score
            self.save_pending_score()
            return

        # Handle ESC to discard
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.discard_pending_score()
            return

        # Handle buttons
        for i, button in enumerate(self.name_input_buttons):
            if button.handle_event(event):
                if i == 0:  # Save
                    self.save_pending_score()
                elif i == 1:  # Discard
                    self.discard_pending_score()

    def save_pending_score(self):
        """Save the pending score to database"""
        if self.pending_score_data and self.name_input.text.strip():
            self.player_name = self.name_input.text.strip()
            try:
                self.db.add_score(
                    self.player_name,
                    self.pending_score_data['level'],
                    self.pending_score_data['time'],
                    self.pending_score_data['score'],
                    self.pending_score_data['game_mode']
                )
            except Exception as e:
                print(f"Erro ao salvar pontuação: {e}")

        # Go to menu
        self.pending_score_data = None
        self.state = "MENU"

    def discard_pending_score(self):
        """Discard the pending score without saving"""
        # Go to menu without saving
        self.pending_score_data = None
        self.state = "MENU"

    def start_game(self):
        """Iniciar jogo com modo selecionado"""
        if not self.serial_connected:
            self.connect_serial()
        self.state = "PLAYING"
        self.level = 1
        self.total_time = 0
        self.levels_completed = 0
        self.total_score = 0
        self.current_score = 0
        self.current_time = 0
        self.winner = None
        self.player1_score = 0
        self.player2_score = 0
        # Resetar vidas baseado no modo
        mode_config = GAME_MODES.get(self.game_mode, {})
        self.lives = mode_config.get('initial_lives', 5)
        self.max_lives = self.lives
        self.player1_lives = self.lives
        self.player2_lives = self.lives
        self.init_level()

    def handle_settings_events(self, event):
        """Tratar eventos do menu de definições"""
        # Volume slider
        self.volume_slider.handle_event(event)
        old_volume = self.game_volume
        self.game_volume = self.volume_slider.value
        if old_volume != self.game_volume:
            self.config.set('game_volume', self.game_volume)
            # Update sound volumes
            if self.sound_level_complete:
                self.sound_level_complete.set_volume(self.game_volume)
            if self.sound_mine_hit:
                self.sound_mine_hit.set_volume(self.game_volume)
            if self.sound_game_over:
                self.sound_game_over.set_volume(self.game_volume)
            if self.sound_wall_collision:
                self.sound_wall_collision.set_volume(self.game_volume * 0.3)  # Keep wall collision quieter

        # Sensitivity slider
        self.sensitivity_slider.handle_event(event)
        old_sensitivity = self.sensitivity
        self.sensitivity = self.sensitivity_slider.value

        # Salvar se mudou
        if old_sensitivity != self.sensitivity:
            self.config.set('sensitivity', self.sensitivity)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Language text click (Y: 260)
            if hasattr(self, 'language_text_rect') and self.language_text_rect.collidepoint(mouse_pos):
                self.language = 'en' if self.language == 'pt' else 'pt'
                self.config.set('language', self.language)
            # Botão inverter X (ajustado para nova posição Y: 360)
            elif 340 < mouse_pos[1] < 390 and self.world_width // 2 - 150 < mouse_pos[0] < self.world_width // 2 + 200:
                self.invert_x = not self.invert_x
                self.config.set('invert_x', self.invert_x)
            # Botão inverter Y (ajustado para nova posição Y: 410)
            elif 390 < mouse_pos[1] < 440 and self.world_width // 2 - 150 < mouse_pos[0] < self.world_width // 2 + 200:
                self.invert_y = not self.invert_y
                self.config.set('invert_y', self.invert_y)
            # Botão trocar X/Y (nova posição Y: 460)
            elif 440 < mouse_pos[1] < 490 and self.world_width // 2 - 150 < mouse_pos[0] < self.world_width // 2 + 200:
                self.swap_xy = not self.swap_xy
                self.config.set('swap_xy', self.swap_xy)
            # Show Controls Text Click
            elif hasattr(self, 'show_controls_text_rect') and self.show_controls_text_rect.collidepoint(mouse_pos):
                self.state = "CONTROLS"
            # Connection Text Click (Rescan)
            elif hasattr(self, 'connection_text_rect') and self.connection_text_rect.collidepoint(mouse_pos):
                # Rescan and attempt connection
                print("Manual rescan requested...")
                self.connect_serial()

        for i, button in enumerate(self.settings_buttons):
            if button.handle_event(event):
                if i == 0: # Back
                    self.state = "MENU"

    def handle_leaderboard_events(self, event):
        """Tratar eventos da leaderboard"""
        # Handle filter buttons
        for i, button in enumerate(self.leaderboard_filter_buttons):
            if button.handle_event(event):
                if i == 0:
                    self.leaderboard_filter = None  # All modes
                elif i == 1:
                    self.leaderboard_filter = 'normal'
                elif i == 2:
                    self.leaderboard_filter = 'minefield'
                elif i == 3:
                    self.leaderboard_filter = 'timeattack'
                elif i == 4:
                    self.leaderboard_filter = 'elimination'
                return

        # Handle clicks on leaderboard entries
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(self, 'leaderboard_entry_rects'):
            for entry_rect, player_name in self.leaderboard_entry_rects:
                if entry_rect.collidepoint(event.pos):
                    self.selected_player_name = player_name
                    self.state = "PLAYER_PROFILE"
                    return

        # Handle back button
        for button in self.leaderboard_buttons:
            if button.handle_event(event):
                self.state = "MENU"

    def handle_pause_events(self, event):
        """Tratar eventos do menu de pausa"""
        # Marcar menu como dirty quando há eventos de mouse
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            self.pause_menu_dirty = True

        for i, button in enumerate(self.pause_menu_buttons):
            if button.handle_event(event):
                if i == 0:  # Continuar
                    # Restaurar velocidade da bola
                    self.ball.vx = self.paused_vx
                    self.ball.vy = self.paused_vy
                    self.state = "PLAYING"
                    self.level_start_time = time.time() - self.timer
                elif i == 1:  # Reiniciar
                    self.start_game()
                elif i == 2:  # Menu
                    self.state = "MENU"

    def handle_win_events(self, event):
        """Tratar eventos do menu de vitória"""
        for i, button in enumerate(self.win_menu_buttons):
            if button.handle_event(event):
                if i == 0:  # Próximo nível
                    try:
                        # Nível já foi incrementado em check_win
                        self.init_level()
                        self.state = "PLAYING"
                    except Exception as e:
                        print(f"Erro ao iniciar próximo nível: {e}")
                        self.state = "MENU"
                elif i == 1:  # Menu
                    # Only show name input if at least one level was completed
                    if self.levels_completed > 0:
                        self.state = "NAME_INPUT"
                        self.name_input.text = self.player_name  # Pre-fill with current name
                    else:
                        self.state = "MENU"

    def update_cursor(self):
        """Update mouse cursor based on hover state"""
        should_be_hand = False
        
        # Check active buttons based on state
        active_buttons = []
        if self.state == "MENU":
            active_buttons = self.main_menu_buttons
        elif self.state == "SETTINGS":
            active_buttons = self.settings_buttons
            # Check sliders
            if self.volume_slider.rect.collidepoint(pygame.mouse.get_pos()) or \
               self.sensitivity_slider.rect.collidepoint(pygame.mouse.get_pos()):
                should_be_hand = True
            # Check texts
            mouse_pos = pygame.mouse.get_pos()
            scale, offset_x, offset_y = self.get_scale_and_offset()
            world_mouse_x = (mouse_pos[0] - offset_x) / scale
            world_mouse_y = (mouse_pos[1] - offset_y) / scale
            
            if hasattr(self, 'language_text_rect') and self.language_text_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
            if hasattr(self, 'connection_text_rect') and self.connection_text_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
            if hasattr(self, 'show_controls_text_rect') and self.show_controls_text_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
            if hasattr(self, 'text_x_rect') and self.text_x_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
            if hasattr(self, 'text_y_rect') and self.text_y_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
            if hasattr(self, 'text_swap_rect') and self.text_swap_rect.collidepoint(world_mouse_x, world_mouse_y):
                should_be_hand = True
                
        elif self.state == "LEADERBOARD":
            active_buttons = self.leaderboard_buttons + self.leaderboard_filter_buttons
            # Check entries
            if hasattr(self, 'leaderboard_entry_rects'):
                mouse_pos = pygame.mouse.get_pos()
                scale, offset_x, offset_y = self.get_scale_and_offset()
                world_mouse_x = (mouse_pos[0] - offset_x) / scale
                world_mouse_y = (mouse_pos[1] - offset_y) / scale
                for entry_rect, _ in self.leaderboard_entry_rects:
                    if entry_rect.collidepoint(world_mouse_x, world_mouse_y):
                        should_be_hand = True
                        break
        elif self.state == "PAUSED":
            active_buttons = self.pause_menu_buttons
        elif self.state == "WIN":
            active_buttons = self.win_menu_buttons
        elif self.state == "MP_WIN":
            active_buttons = self.mp_win_buttons
        elif self.state == "GAME_OVER":
            active_buttons = self.gameover_buttons
        elif self.state == "MODE_SELECT":
            active_buttons = [self.mode_select_back_button]
            # Check cards
            for card in self.mode_cards:
                # Need to check against active cards only? Or check all, hidden ones wont trigger
                # Card is_hovered is updated in handle_event, let's check rect directly
                mouse_pos = pygame.mouse.get_pos()
                scale, offset_x, offset_y = self.get_scale_and_offset()
                world_mouse_x = (mouse_pos[0] - offset_x) / scale
                world_mouse_y = (mouse_pos[1] - offset_y) / scale
                if card.rect.collidepoint(world_mouse_x, world_mouse_y):
                    should_be_hand = True
        elif self.state == "PLAYER_SELECT":
            active_buttons = self.player_select_buttons
        elif self.state == "DIFFICULTY_SELECT":
            if hasattr(self, 'difficulty_buttons'):
                active_buttons = self.difficulty_buttons
        elif self.state == "STM32_SETUP":
            if hasattr(self, 'stm32_setup_buttons'):
                active_buttons = self.stm32_setup_buttons
        elif self.state == "CONTROLS":
            if hasattr(self, 'controls_back_button'):
                active_buttons = [self.controls_back_button]
        elif self.state == "PLAYER_PROFILE":
            if hasattr(self, 'player_profile_back_button'):
                active_buttons = [self.player_profile_back_button]
        elif self.state == "NAME_INPUT":
            active_buttons = self.name_input_buttons

        # Check buttons
        if not should_be_hand:
            for button in active_buttons:
                # Button hover is already handled? No, let's check logic
                # Button.rect is world coords
                mouse_pos = pygame.mouse.get_pos()
                scale, offset_x, offset_y = self.get_scale_and_offset()
                world_mouse_x = (mouse_pos[0] - offset_x) / scale
                world_mouse_y = (mouse_pos[1] - offset_y) / scale
                if button.rect.collidepoint(world_mouse_x, world_mouse_y):
                    should_be_hand = True
                    break
        
        # Update cursor only if changed
        if should_be_hand != self.cursor_hand_active:
            self.cursor_hand_active = should_be_hand
            if should_be_hand:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def force_finish_mp_game(self):
        """Force finish the MP game if one player is waiting"""
        current_time = time.time() - self.level_start_time
        
        if self.player1_finished and not self.player2_finished:
            self.player2_finished = True
            self.player2_time = current_time + 10 # Penalty
            # Stop ball
            if self.ball2:
                self.ball2.vx = 0
                self.ball2.vy = 0
            
        elif self.player2_finished and not self.player1_finished:
            self.player1_finished = True
            self.player1_time = current_time + 10
            # Stop ball
            self.ball.vx = 0
            self.ball.vy = 0
            
        # The main loop will check 'if p1_finished and p2_finished' in the next frame and trigger win

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Redimensionamento da janela
                    self.window_width = event.w
                    self.window_height = event.h
                    self.screen = pygame.display.set_mode(
                        (self.window_width, self.window_height),
                        pygame.RESIZABLE
                    )
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Verificar cooldown para prevenir múltiplas alternâncias
                        current_time = time.time()
                        if current_time - self.last_esc_time > self.esc_cooldown:
                            self.last_esc_time = current_time
                            if self.state == "PLAYING":
                                # Salvar velocidade da bola antes de pausar
                                self.paused_vx = self.ball.vx
                                self.paused_vy = self.ball.vy
                                # Congelar a bola
                                self.ball.vx = 0
                                self.ball.vy = 0
                                self.state = "PAUSED"
                                self.pause_menu_dirty = True
                            elif self.state == "PAUSED":
                                # Restaurar velocidade da bola
                                self.ball.vx = self.paused_vx
                                self.ball.vy = self.paused_vy
                                self.state = "PLAYING"
                                self.level_start_time = time.time() - self.timer
                            
                            # Menu Navigation Back Logic
                            elif self.state == "SETTINGS":
                                self.state = "MENU"
                            elif self.state == "CONTROLS":
                                self.state = "SETTINGS"
                            elif self.state == "LEADERBOARD":
                                self.state = "MENU"
                            elif self.state == "PLAYER_PROFILE":
                                self.state = "LEADERBOARD"
                            elif self.state == "DIFFICULTY_SELECT":
                                self.state = "MENU"
                            elif self.state == "PLAYER_SELECT":
                                self.state = "DIFFICULTY_SELECT"
                            elif self.state == "MODE_SELECT":
                                self.state = "PLAYER_SELECT"
                            elif self.state == "STM32_SETUP":
                                self.state = "PLAYER_SELECT"
                            elif self.state == "NAME_INPUT":
                                self.discard_pending_score()
                            elif self.state in ["GAME_OVER", "WIN", "MP_WIN"]:
                                self.state = "MENU"

                    elif event.key == pygame.K_r and self.state == "PLAYING":
                        self.init_level()
                    elif event.key == pygame.K_F11:
                        # Alternar fullscreen
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_t:
                         # Force Finish in MP Normal Mode
                         if self.state == "PLAYING" and self.num_players == 2 and self.game_mode == 'normal':
                             if self.player1_finished or self.player2_finished:
                                 self.force_finish_mp_game()

                # Converter coordenadas do mouse para coordenadas do mundo
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(event, 'pos'):
                        world_pos = self.screen_to_world(event.pos[0], event.pos[1])
                        # Criar novo evento com coordenadas do mundo
                        event_dict = event.__dict__.copy()
                        event_dict['pos'] = (int(world_pos[0]), int(world_pos[1]))
                        event = type(event)(event.type, event_dict)

                # Eventos específicos do estado
                if self.state == "MENU":
                    self.handle_menu_events(event)
                elif self.state == "PLAYER_SELECT":
                    self.handle_player_select_events(event)
                elif self.state == "STM32_SETUP":
                    self.handle_stm32_setup_events(event)
                elif self.state == "MODE_SELECT":
                    self.handle_mode_select_events(event)
                elif self.state == "SETTINGS":
                    self.handle_settings_events(event)
                elif self.state == "CONTROLS":
                    self.handle_controls_events(event)
                elif self.state == "LEADERBOARD":
                    self.handle_leaderboard_events(event)
                elif self.state == "PLAYER_PROFILE":
                    self.handle_player_profile_events(event)
                elif self.state == "PAUSED":
                    self.handle_pause_events(event)
                elif self.state == "WIN":
                    self.handle_win_events(event)
                elif self.state == "MP_WIN":
                    self.handle_mp_win_events(event)
                elif self.state == "NAME_INPUT":
                    self.handle_name_input_events(event)
                elif self.state == "GAME_OVER":
                    self.handle_gameover_events(event)
                elif self.state == "DIFFICULTY_SELECT":
                    self.handle_difficulty_select_events(event)
            
            # Update Cursor State
            self.update_cursor()

            # Atualização do jogo
            if self.state == "PLAYING":
                # Ler dados
                self.read_serial()
                self.handle_keyboard()

                # Atualizar sensibilidade da bola
                self.ball.sensitivity = self.sensitivity
                if self.ball2:
                    self.ball2.sensitivity = self.sensitivity

                # PHYSICS SUB-STEPPING (Fix collision bugs)
                physics_steps = 4
                dt_step = dt / physics_steps
                
                # Calculate friction per sub-step to preserve original friction feel
                friction_per_substep = FRICTION**(1/physics_steps)
                
                for _ in range(physics_steps):
                    # Player 1 Update
                    if not self.player1_finished:
                        combined_accel_x = self.accel_x + self.keyboard_accel_x
                        combined_accel_y = self.accel_y + self.keyboard_accel_y
                        collided1 = self.ball.update(combined_accel_x, combined_accel_y, dt_step, self.walls, friction_per_substep)
                        if collided1 and self.sound_wall_collision:
                            # Limit sound frequency
                            if time.time() - self.last_beep_time > 0.1:
                                self.sound_wall_collision.play()
                                self.last_beep_time = time.time()
                        
                        # Check mines P1
                        if len(self.mines) > 0:
                            for mine in self.mines[:]:
                                distance = math.sqrt((self.ball.x - mine.x)**2 + (self.ball.y - mine.y)**2)
                                if distance < BALL_RADIUS + mine.size:
                                    self.mines.remove(mine)
                                    self.send_mine_command()
                                    
                                    if self.num_players == 2:
                                        self.player1_lives -= 1
                                        if self.player1_lives <= 0:
                                            self.winner = "Player 2"
                                            self.lives = 0 
                                    else:
                                        self.lives -= 1
                                        
                                    self.mine_hit_animation_time = time.time()
                                    if self.sound_mine_hit:
                                        self.sound_mine_hit.play()
                                    # Reset P1 pos
                                    offset = BALL_RADIUS + 2
                                    self.ball.x = MAZE_MARGIN + 60 
                                    self.ball.y = MAZE_MARGIN_TOP + 60
                                    self.ball.vx = 0
                                    self.ball.vy = 0
                                    break

                    # Player 2 Update
                    if self.num_players == 2 and self.ball2 and not self.player2_finished:
                        combined_accel2_x = self.accel2_x + self.keyboard2_accel_x
                        combined_accel2_y = self.accel2_y + self.keyboard2_accel_y
                        collided2 = self.ball2.update(combined_accel2_x, combined_accel2_y, dt_step, self.walls, friction_per_substep)
                        if collided2 and self.sound_wall_collision:
                             if time.time() - self.last_beep_time > 0.1:
                                self.sound_wall_collision.play()
                                self.last_beep_time = time.time()

                        # Check mines P2
                        if len(self.mines) > 0:
                            for mine in self.mines[:]:
                                distance = math.sqrt((self.ball2.x - mine.x)**2 + (self.ball2.y - mine.y)**2)
                                if distance < BALL_RADIUS + mine.size:
                                    self.mines.remove(mine)
                                    self.send_mine_command()
                                    
                                    self.player2_lives -= 1
                                    if self.player2_lives <= 0:
                                        self.winner = "Player 1"
                                        self.lives = 0
                                    
                                    self.mine_hit_animation_time = time.time()
                                    if self.sound_mine_hit:
                                        self.sound_mine_hit.play()
                                    # Reset P2 pos
                                    offset_y = BALL_RADIUS * 2 + 10
                                    self.ball2.x = MAZE_MARGIN + 60
                                    self.ball2.y = MAZE_MARGIN_TOP + 60 + offset_y
                                    self.ball2.vx = 0
                                    self.ball2.vy = 0
                                    break

                # Game Over Condition
                if self.lives <= 0 or (self.num_players == 2 and (self.player1_lives <= 0 or self.player2_lives <= 0)):
                    if self.sound_game_over:
                        self.sound_game_over.play()
                    
                    # Calculate final scores for multiplayer based on progress
                    if self.num_players == 2 and self.game_mode == 'elimination':
                        dist1 = math.sqrt((self.ball.x - self.goal_pos[0])**2 + (self.ball.y - self.goal_pos[1])**2)
                        dist2 = math.sqrt((self.ball2.x - self.goal_pos[0])**2 + (self.ball2.y - self.goal_pos[1])**2)
                        
                        # Add progress scores if not already finished
                        if not self.player1_finished and hasattr(self, 'p1_start_dist') and self.p1_start_dist > 0:
                            if dist1 < self.p1_start_dist:
                                p1_partial = int(1000 * (self.p1_start_dist - dist1) / self.p1_start_dist)
                                self.player1_score += p1_partial
                        
                        if not self.player2_finished and hasattr(self, 'p2_start_dist') and self.p2_start_dist > 0:
                            if dist2 < self.p2_start_dist:
                                p2_partial = int(1000 * (self.p2_start_dist - dist2) / self.p2_start_dist)
                                self.player2_score += p2_partial
                    
                    # Determine score to save
                    if self.num_players == 2:
                        if self.winner == "Player 1":
                            score_to_save = self.player1_score
                        elif self.winner == "Player 2":
                            score_to_save = self.player2_score
                        else:
                            score_to_save = max(self.player1_score, self.player2_score)
                    else:
                        score_to_save = self.total_score if self.levels_completed > 0 else self.precision_score
                        
                    self.pending_score_data = {
                        'level': self.level,
                        'time': self.total_time,
                        'score': score_to_save,
                        'game_mode': self.game_mode,
                        'is_game_over': True
                    }
                    self.state = "GAME_OVER"

                # Timer Update
                mode_config = GAME_MODES.get(self.game_mode, {})
                if mode_config.get('timer_direction') == 'down':
                    self.timer -= dt
                    if self.timer <= 0:
                        self.timer = 0
                        if self.sound_game_over:
                            self.sound_game_over.play()
                        
                        # Elimination Mode Logic: Time Out
                        if self.game_mode == 'elimination' and self.num_players == 2:
                            # If time runs out, whoever didn't finish loses.
                            # If both didn't finish, the one furthest from goal loses (closest wins).
                            
                            # Calculate current distances
                            dist1 = math.sqrt((self.ball.x - self.goal_pos[0])**2 + (self.ball.y - self.goal_pos[1])**2)
                            dist2 = math.sqrt((self.ball2.x - self.goal_pos[0])**2 + (self.ball2.y - self.goal_pos[1])**2)
                            
                            # Calculate partial scores based on progress from start
                            if not self.player1_finished:
                                if hasattr(self, 'p1_start_dist') and self.p1_start_dist > 0 and dist1 < self.p1_start_dist:
                                    # Score based on % distance covered
                                    p1_partial = int(1000 * (self.p1_start_dist - dist1) / self.p1_start_dist)
                                    self.player1_score += p1_partial
                                
                            if not self.player2_finished:
                                if hasattr(self, 'p2_start_dist') and self.p2_start_dist > 0 and dist2 < self.p2_start_dist:
                                    p2_partial = int(1000 * (self.p2_start_dist - dist2) / self.p2_start_dist)
                                    self.player2_score += p2_partial
                            
                            # Determine Winner based on scores (not just distance)
                            if self.player1_finished and not self.player2_finished:
                                self.winner = "Player 1"
                            elif self.player2_finished and not self.player1_finished:
                                self.winner = "Player 2"
                            else:
                                # Both failed to finish - winner is who has more points
                                if self.player1_score > self.player2_score:
                                    self.winner = "Player 1"
                                elif self.player2_score > self.player1_score:
                                    self.winner = "Player 2"
                                else:
                                    self.winner = "Draw"
                            
                            self.state = "MP_WIN"
                        else:
                            # Standard Game Over
                            score_to_save = self.total_score if self.levels_completed > 0 else self.precision_score
                            self.pending_score_data = {
                                'level': self.level,
                                'time': self.total_time,
                                'score': score_to_save,
                                'game_mode': self.game_mode,
                                'is_game_over': True
                            }
                            self.state = "GAME_OVER"
                else:
                    self.timer = time.time() - self.level_start_time

                # Atualizar animações
                if self.mine_hit_animation_time > 0:
                    if time.time() - self.mine_hit_animation_time > 0.5:
                        self.mine_hit_animation_time = 0

                # Verificar vitória
                self.check_win()

            # Desenho
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "PLAYER_SELECT":
                self.draw_player_select()
            elif self.state == "STM32_SETUP":
                self.draw_stm32_setup()
            elif self.state == "MODE_SELECT":
                self.draw_mode_select()
            elif self.state == "SETTINGS":
                self.draw_settings()
            elif self.state == "CONTROLS":
                self.draw_controls()
            elif self.state == "LEADERBOARD":
                self.draw_leaderboard()
            elif self.state == "PLAYER_PROFILE":
                self.draw_player_profile()
            elif self.state == "PLAYING":
                self.draw_playing()
            elif self.state == "PAUSED":
                self.draw_pause()
            elif self.state == "WIN":
                self.draw_win()
            elif self.state == "MP_WIN":
                self.draw_mp_win()
            elif self.state == "NAME_INPUT":
                self.draw_name_input()
            elif self.state == "GAME_OVER":
                self.draw_gameover()
            elif self.state == "DIFFICULTY_SELECT":
                self.draw_difficulty_select()

        # Fechar
        if self.serial_port:
            self.serial_port.close()
        self.db.close()
        pygame.quit()

def main():
    print("=" * 60)
    print("  GravityMaze - Jogo de Labirinto com Acelerómetro")
    print("=" * 60)
    print("\nControlos:")
    print("  - Inclinar o acelerómetro para mover a bola")
    print("  - Setas do teclado (modo teste)")
    print("  - ESC: Pausar/Retomar")
    print("  - R: Reiniciar nível")
    print("\nObjetivo: Levar a bola até ao buraco verde!")
    print("=" * 60)

    game = Game()
    game.run()

if __name__ == "__main__":
    main()