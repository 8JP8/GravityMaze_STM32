"""
GravityMaze - Jogo de Labirinto com Controlo por Acelerómetro ADXL345
Autor: João Oliveira 1240369 / João Santos 1240368
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
        'total_stats': 'Estatísticas Totais:',
        'levels_completed': 'Níveis Completados',
        'total_time': 'Tempo Total',
        'best_time': 'Melhor Tempo',
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
        'total_stats': 'Total Stats:',
        'levels_completed': 'Levels Completed',
        'total_time': 'Total Time',
        'best_time': 'Best Time',
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

class Config:
    """Gestão de configurações persistentes"""
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.default_config = {
            'sensitivity': 1.0,
            'invert_x': True,
            'invert_y': True,
            'swap_xy': False,
            'language': 'pt'
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
        self.conn.commit()

    def add_score(self, player_name, level, time_taken, score, game_mode='normal'):
        cursor = self.conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO leaderboard (player_name, level, time, score, date, game_mode)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_name, level, time_taken, score, date, game_mode))
        self.conn.commit()

    def get_top_scores(self, limit=10, game_mode=None):
        cursor = self.conn.cursor()
        if game_mode:
            cursor.execute('''
                SELECT player_name, level, time, score, date
                FROM leaderboard
                WHERE game_mode = ?
                ORDER BY score DESC, time ASC
                LIMIT ?
            ''', (game_mode, limit))
        else:
            cursor.execute('''
                SELECT player_name, level, time, score, date
                FROM leaderboard
                ORDER BY score DESC, time ASC
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
            if self.is_hovered:
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

class Ball:
    def __init__(self, x, y, sensitivity=1.0, world_width=DEFAULT_WIDTH, world_height=DEFAULT_HEIGHT):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.sensitivity = sensitivity
        self.world_width = world_width
        self.world_height = world_height

    def update(self, ax, ay, dt, walls):
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

        # Aplicar fricção
        self.vx *= FRICTION
        self.vy *= FRICTION

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
        pygame.draw.circle(screen, (100, 0, 0), (int(self.x) + 3, int(self.y) + 3), self.radius)
        # Bola principal
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)
        # Highlight
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x) - 3, int(self.y) - 3), self.radius // 3)

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
            mines.append((center_x, center_y))
        return mines

    def place_mines_everywhere(self, percentage=0.15):
        """Colocar minas em células aleatórias (para modo minefield)"""
        total_cells = self.rows * self.cols
        mine_count = max(1, int(total_cells * percentage))

        # Criar lista de todas as posições (exceto início e fim)
        all_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if not (r == 0 and c == 0) and not (r == self.rows-1 and c == self.cols-1):
                    all_positions.append((r, c))

        # Selecionar posições aleatórias
        mine_positions = random.sample(all_positions, min(mine_count, len(all_positions)))

        # Converter para coordenadas de pixel
        mines = []
        for row, col in mine_positions:
            center_x = col * self.cell_size + self.cell_size // 2
            center_y = row * self.cell_size + self.cell_size // 2
            mines.append((center_x, center_y))
        return mines

    @staticmethod
    def generate(level, world_width, world_height, game_mode='normal', mine_percentage=0.15):
        """Gerar labirinto baseado no nível"""
        # Ajustar tamanho das células baseado no nível
        # Níveis mais altos = células menores = labirintos mais complexos
        base_cell_size = 80
        cell_size = max(50, base_cell_size - (level - 1) * 4)

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

        # Gerar minas baseado no modo de jogo
        mines = []
        if game_mode == 'minefield':
            # Minas espalhadas aleatoriamente
            mines = generator.place_mines_everywhere(mine_percentage)
        elif game_mode == 'normal':
            # Sem minas no modo normal
            mines = []
        # Outros modos também podem ter minas se necessário

        # Aplicar offset da margem às minas
        mines_with_margin = []
        for mine_x, mine_y in mines:
            mines_with_margin.append((mine_x + MAZE_MARGIN, mine_y + MAZE_MARGIN_TOP))

        return walls_with_margin, mines_with_margin

class Game:
    def __init__(self):
        pygame.init()

        # Dimensões da janela (redimensionável)
        self.window_width = DEFAULT_WIDTH
        self.window_height = DEFAULT_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE
        )
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

        # Base de dados
        self.db = Database()

        # Serial
        self.serial_port = None
        self.serial_connected = False

        # Dados do acelerómetro
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0

        # Aceleração do teclado (para combinar com acelerómetro)
        self.keyboard_accel_x = 0
        self.keyboard_accel_y = 0

        # Configurações (carregar do arquivo)
        self.sensitivity = self.config.get('sensitivity')
        self.invert_x = self.config.get('invert_x')
        self.invert_y = self.config.get('invert_y')
        self.swap_xy = self.config.get('swap_xy')
        self.language = self.config.get('language')

        # Modo de jogo
        self.game_mode = 'normal'  # normal, minefield, timeattack, elimination
        self.game_mode_config = {
            'normal': {
                'timer_direction': 'up',
                'has_lives': True,
                'initial_lives': 3,
                'mines_in_deadends': False,
                'track_precision': True
            },
            'minefield': {
                'timer_direction': 'up',
                'has_lives': True,
                'initial_lives': 3,
                'mines_everywhere': True,
                'mine_percentage': 0.15
            },
            'timeattack': {
                'timer_direction': 'down',
                'initial_time': 300,
                'has_lives': True,
                'initial_lives': 3
            },
            'elimination': {
                'timer_direction': 'down',
                'random_time_on_level': True,
                'random_time_min': 30,
                'random_time_max': 80,
                'initial_time': 60,
                'has_lives': True,
                'initial_lives': 3
            }
        }

        # Sistema de vidas
        self.lives = 3
        self.max_lives = 3
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
        self.state = "MENU"  # MENU, SETTINGS, PLAYING, PAUSED, WIN, LEADERBOARD, MODE_SELECT
        self.running = True
        self.level = 1
        self.timer = 0
        self.player_name = "Player"

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

        # Criar menus
        self.create_menus()

        # Tentar conectar ao serial automaticamente
        self.connect_serial()

        # Inicializar jogo
        self.init_level()

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

    def create_menus(self):
        """Criar botões dos menus estilo Minecraft"""
        button_width = 400
        button_height = 70
        center_x = self.world_width // 2 - button_width // 2

        # Menu principal
        self.main_menu_buttons = [
            Button(center_x, 300, button_width, button_height, "Jogar", DARK_GREEN),
            Button(center_x, 390, button_width, button_height, "Definições", GRAY),
            Button(center_x, 480, button_width, button_height, "Leaderboard", BLUE),
            Button(center_x, 570, button_width, button_height, "Sair", RED),
        ]

        # Menu de definições
        self.settings_buttons = [
            Button(center_x, 600, button_width, button_height, "Voltar", GRAY),
        ]

        # Sliders de configuração
        self.sensitivity_slider = Slider(center_x, 280, button_width, 0.1, 2.0, self.sensitivity, "Sensibilidade")

        # Menu de pausa
        self.pause_menu_buttons = [
            Button(center_x, 280, button_width, button_height, "Continuar", DARK_GREEN),
            Button(center_x, 370, button_width, button_height, "Reiniciar Nível", GOLD),
            Button(center_x, 460, button_width, button_height, "Menu Principal", GRAY),
        ]

        # Menu de vitória
        self.win_menu_buttons = [
            Button(center_x, 480, button_width, button_height, "Próximo Nível", DARK_GREEN),
            Button(center_x, 570, button_width, button_height, "Menu Principal", GRAY),
        ]

        # Leaderboard
        self.leaderboard_buttons = [
            Button(center_x, 630, button_width, button_height, "Voltar", GRAY),
        ]

        # Menu de seleção de modos
        self.mode_select_buttons = [
            Button(center_x, 220, button_width, button_height, "Normal", DARK_GREEN),
            Button(center_x, 310, button_width, button_height, "Campo Minado", RED),
            Button(center_x, 400, button_width, button_height, "Contra-Relógio", GOLD),
            Button(center_x, 490, button_width, button_height, "Eliminação", (255, 100, 0)),
            Button(center_x, 580, button_width, button_height, "Voltar", GRAY),
        ]

        # Menu de Game Over
        self.gameover_buttons = [
            Button(center_x, 400, button_width, button_height, "Tentar Novamente", DARK_GREEN),
            Button(center_x, 490, button_width, button_height, "Menu Principal", GRAY),
        ]

    def connect_serial(self):
        """Conectar à porta série do STM32"""
        ports = serial.tools.list_ports.comports()

        # Lista de identificadores comuns de STM32
        stm32_identifiers = [
            'STM32',
            'STMicroelectronics',
            'VCP',  # Virtual COM Port
            'USB Serial Device',
            'USB-SERIAL CH340',  # Chip conversor comum
            'CP210',  # Silicon Labs
            'FTDI',  # FTDI conversor
        ]

        """
        print("\n=== Portas série disponíveis ===")
        for port in ports:
            print(f"  {port.device}: {port.description}")
            print(f"    Fabricante: {port.manufacturer}")
            print(f"    VID:PID: {port.vid}:{port.pid}")
            print(f"    Serial: {port.serial_number}")
        """

        print("\n=== A procurar STM32... ===")
        for port in ports:
            # Verificar se é um dispositivo STM32 ou conversor USB-Serial conhecido
            is_stm32 = False

            # Verificar descrição
            if port.description:
                for identifier in stm32_identifiers:
                    if identifier.lower() in port.description.lower():
                        is_stm32 = True
                        break

            # Verificar fabricante
            if not is_stm32 and port.manufacturer:
                for identifier in stm32_identifiers:
                    if identifier.lower() in port.manufacturer.lower():
                        is_stm32 = True
                        break

            # VID específico da STMicroelectronics (0x0483)
            if not is_stm32 and port.vid == 0x0483:
                is_stm32 = True

            if is_stm32:
                try:
                    print(f"  A tentar conectar a {port.device}...")
                    self.serial_port = serial.Serial(
                        port.device,
                        baudrate=115200,
                        timeout=0.01
                    )
                    self.serial_connected = True
                    print(f"  [OK] Conectado a: {port.device} ({port.description})")
                    return True
                except Exception as e:
                    print(f"  [X] Erro ao conectar a {port.device}: {e}")
                    continue

        print("\nAVISO: Nenhum STM32 encontrado. A usar teclado para controlo.")
        return False

    def init_level(self):
        """Inicializar um novo nível"""
        # Obter configuração do modo atual
        mode_config = self.game_mode_config.get(self.game_mode, {})
        mine_percentage = mode_config.get('mine_percentage', 0.15)

        # Gerar labirinto com minas
        self.walls, self.mines = MazeGenerator.generate(
            self.level,
            self.world_width,
            self.world_height,
            self.game_mode,
            mine_percentage
        )

        # Posição inicial da bola (com margem segura)
        ball_start_x = MAZE_MARGIN + 60
        ball_start_y = MAZE_MARGIN_TOP + 60
        self.ball = Ball(ball_start_x, ball_start_y, self.sensitivity, self.world_width, self.world_height)

        # Objetivo como círculo/buraco verde (com margem segura e longe de paredes)
        self.goal_radius = 30
        self.goal_pos = (self.world_width - MAZE_MARGIN - 80, self.world_height - MAZE_MARGIN - 80)

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

        # Configurar timer baseado no modo
        if mode_config.get('timer_direction') == 'down':
            if mode_config.get('random_time_on_level', False):
                # Modo eliminação - tempo aleatório
                min_time = mode_config.get('random_time_min', 30)
                max_time = mode_config.get('random_time_max', 80)
                self.timer = random.randint(min_time, max_time)
            else:
                # Modo time attack - tempo fixo
                self.timer = mode_config.get('initial_time', 60)

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

        # Calcular aceleração do teclado (normalizada para ser similar ao acelerómetro)
        # O acelerómetro retorna valores entre -1 e 1 (em g's)
        keyboard_accel_magnitude = 0.5  # Equivalente a 0.5g

        if keys[pygame.K_LEFT]:
            self.keyboard_accel_x -= keyboard_accel_magnitude
        if keys[pygame.K_RIGHT]:
            self.keyboard_accel_x += keyboard_accel_magnitude
        if keys[pygame.K_UP]:
            self.keyboard_accel_y -= keyboard_accel_magnitude
        if keys[pygame.K_DOWN]:
            self.keyboard_accel_y += keyboard_accel_magnitude

        # Normalizar se diagonal (para não ter aceleração maior nas diagonais)
        if self.keyboard_accel_x != 0 and self.keyboard_accel_y != 0:
            diagonal_factor = 1 / math.sqrt(2)
            self.keyboard_accel_x *= diagonal_factor
            self.keyboard_accel_y *= diagonal_factor

        # Reset da aceleração do acelerómetro quando se usa apenas teclado
        if not self.serial_connected:
            # Só resetar se não houver input de teclado
            if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]]):
                self.accel_x = 0
                self.accel_y = 0

    def check_win(self):
        """Verificar se a bola chegou ao objetivo (buraco)"""
        # Evitar verificar se já estamos em estado de vitória
        if self.state != "PLAYING":
            return

        dx = self.ball.x - self.goal_pos[0]
        dy = self.ball.y - self.goal_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < self.goal_radius:
            # Toca o buzzer ao vencer
            self.send_beep_command()

            # Congelar a bola
            self.ball.vx = 0
            self.ball.vy = 0

            # Calcular tempo do nível
            level_time = time.time() - self.level_start_time
            self.total_time += level_time
            self.best_time = min(self.best_time, level_time)
            self.levels_completed += 1

            # Calcular pontuação (baseada no nível e tempo)
            # Incluir precisão se for modo normal
            mode_config = self.game_mode_config.get(self.game_mode, {})
            if mode_config.get('track_precision', False):
                score = int(self.level * 1000 / max(0.1, level_time)) + self.precision_score
            else:
                score = int(self.level * 1000 / max(0.1, level_time))
            self.current_score = score
            self.current_time = level_time

            # Adicionar tempo aleatório no modo eliminação
            if mode_config.get('random_time_on_level', False):
                min_time = mode_config.get('random_time_min', 30)
                max_time = mode_config.get('random_time_max', 80)
                bonus_time = random.randint(min_time, max_time)
                self.timer += bonus_time
                print(f"Bónus de tempo: +{bonus_time}s")

            # Adicionar à leaderboard com proteção contra erros
            try:
                self.db.add_score(self.player_name, self.level, level_time, score, self.game_mode)
            except Exception as e:
                print(f"Erro ao salvar pontuação: {e}")

            # Avançar nível
            self.level += 1

            # Mudar estado por último
            self.state = "WIN"

    def draw_direction_indicator(self):
        """Desenhar indicador de direção no top-center"""
        indicator_size = 40
        center_x = self.world_width // 2
        center_y = 60

        # Combinar aceleração do acelerómetro com aceleração do teclado
        combined_accel_x = self.accel_x + self.keyboard_accel_x
        combined_accel_y = self.accel_y + self.keyboard_accel_y

        # Calcular magnitude da inclinação
        magnitude = math.sqrt(combined_accel_x**2 + combined_accel_y**2)

        if magnitude < 0.15:  # Aceleração nivelada (sem input)
            # Desenhar círculo
            pygame.draw.circle(self.world_surface, BLUE, (center_x, center_y), indicator_size // 2)
            pygame.draw.circle(self.world_surface, WHITE, (center_x, center_y), indicator_size // 2, 3)
        else:
            # Desenhar seta a apontar para a direção combinada
            angle = math.atan2(combined_accel_y, combined_accel_x)

            # Pontos da seta
            arrow_length = indicator_size
            arrow_width = indicator_size // 2

            # Ponta da seta
            tip_x = center_x + arrow_length * math.cos(angle)
            tip_y = center_y + arrow_length * math.sin(angle)

            # Base da seta (triângulo)
            base_angle1 = angle + math.pi * 0.75
            base_angle2 = angle - math.pi * 0.75

            base1_x = center_x + arrow_width * math.cos(base_angle1)
            base1_y = center_y + arrow_width * math.sin(base_angle1)

            base2_x = center_x + arrow_width * math.cos(base_angle2)
            base2_y = center_y + arrow_width * math.sin(base_angle2)

            # Desenhar seta
            points = [(tip_x, tip_y), (base1_x, base1_y), (base2_x, base2_y)]
            pygame.draw.polygon(self.world_surface, BLUE, points)
            pygame.draw.polygon(self.world_surface, WHITE, points, 3)

    def draw_hearts(self):
        """Desenhar corações (vidas) no centro inferior"""
        heart_size = 30
        heart_spacing = 40
        y_pos = self.world_height - 60

        # Calcular posição centralizada
        total_width = self.max_lives * heart_spacing - (heart_spacing - heart_size)
        start_x = (self.world_width - total_width) // 2

        for i in range(self.max_lives):
            x = start_x + i * heart_spacing + heart_size // 2

            # Animação de pulso quando perde vida
            scale = 1.0
            if i >= self.lives and self.life_lost_animation_time > 0:
                time_since_lost = time.time() - self.life_lost_animation_time
                if time_since_lost < 0.5:
                    # Pulsar o coração perdido
                    if int(i) == int(self.lives):
                        scale = 1.0 + 0.3 * math.sin(time_since_lost * 20)

            # Desenhar coração (forma simplificada)
            heart_color = RED if i < self.lives else DARK_GRAY
            size = int(heart_size * scale)

            # Coração como dois círculos e um triângulo
            left_circle_pos = (int(x - size//4), int(y_pos - size//4))
            right_circle_pos = (int(x + size//4), int(y_pos - size//4))

            pygame.draw.circle(self.world_surface, heart_color, left_circle_pos, size//3)
            pygame.draw.circle(self.world_surface, heart_color, right_circle_pos, size//3)

            # Triângulo inferior
            triangle_points = [
                (x, y_pos + size//2),
                (x - size//2, y_pos - size//6),
                (x + size//2, y_pos - size//6)
            ]
            pygame.draw.polygon(self.world_surface, heart_color, triangle_points)

    def draw_menu(self):
        """Desenhar menu principal"""
        self.world_surface.fill(BLACK)

        # Título com efeito
        title = self.title_font.render("GravityMaze", True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 150))

        # Sombra do título
        shadow = self.title_font.render("GravityMaze", True, DARK_GREEN)
        shadow_rect = shadow.get_rect(center=(self.world_width // 2 + 5, 156))
        self.world_surface.blit(shadow, shadow_rect)
        self.world_surface.blit(title, title_rect)

        # Subtítulo
        subtitle = self.small_font.render("Controlo por Aceler\u00f3metro ADXL345", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(self.world_width // 2, 220))
        self.world_surface.blit(subtitle, subtitle_rect)

        # Botões
        for button in self.main_menu_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_settings(self):
        """Desenhar menu de definições"""
        self.world_surface.fill(BLACK)

        # Título
        title = self.font.render("Defini\u00e7\u00f5es", True, WHITE)
        title_rect = title.get_rect(center=(self.world_width // 2, 80))
        self.world_surface.blit(title, title_rect)

        # Slider de sensibilidade
        self.sensitivity_slider.draw(self.world_surface, self.small_font)

        # Opções de inversão
        invert_x_text = f"Inverter X: {'SIM' if self.invert_x else 'N\u00c3O'}"
        invert_y_text = f"Inverter Y: {'SIM' if self.invert_y else 'N\u00c3O'}"
        swap_xy_text = f"Trocar X/Y: {'SIM' if self.swap_xy else 'N\u00c3O'}"

        text_x = self.small_font.render(invert_x_text, True, WHITE)
        text_y = self.small_font.render(invert_y_text, True, WHITE)
        text_swap = self.small_font.render(swap_xy_text, True, WHITE)

        self.world_surface.blit(text_x, (self.world_width // 2 - 150, 360))
        self.world_surface.blit(text_y, (self.world_width // 2 - 150, 410))
        self.world_surface.blit(text_swap, (self.world_width // 2 - 150, 460))

        # Info de conexão serial
        connection_text = "Serial: CONECTADO" if self.serial_connected else "Serial: DESCONECTADO (a usar teclado)"
        conn_color = GREEN if self.serial_connected else RED
        conn_surface = self.small_font.render(connection_text, True, conn_color)
        conn_rect = conn_surface.get_rect(center=(self.world_width // 2, 520))
        self.world_surface.blit(conn_surface, conn_rect)

        # Botões
        for button in self.settings_buttons:
            button.draw(self.world_surface, self.font)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_leaderboard(self):
        """Desenhar leaderboard"""
        self.world_surface.fill(BLACK)

        # Título
        title = self.font.render("Leaderboard", True, GOLD)
        title_rect = title.get_rect(center=(self.world_width // 2, 50))
        self.world_surface.blit(title, title_rect)

        # Cabeçalho
        headers = ["#", "Nome", "N\u00edvel", "Tempo", "Pontua\u00e7\u00e3o", "Data"]
        y_offset = 110
        x_positions = [50, 120, 280, 370, 480, 620]

        for i, header in enumerate(headers):
            text = self.small_font.render(header, True, GRAY)
            self.world_surface.blit(text, (x_positions[i], y_offset))

        # Linha separadora
        pygame.draw.line(self.world_surface, GRAY, (40, y_offset + 30), (self.world_width - 40, y_offset + 30), 2)

        # Scores
        scores = self.db.get_top_scores(10)
        y_offset = 150

        for i, (name, level, time_taken, score, date) in enumerate(scores):
            color = GOLD if i == 0 else (LIGHT_GRAY if i == 1 else (GRAY if i == 2 else WHITE))

            rank = self.small_font.render(str(i + 1), True, color)
            name_text = self.small_font.render(name[:10], True, color)
            level_text = self.small_font.render(str(level), True, color)
            time_text = self.small_font.render(f"{time_taken:.2f}s", True, color)
            score_text = self.small_font.render(str(score), True, color)
            date_text = self.small_font.render(date[5:16], True, color)

            self.world_surface.blit(rank, (x_positions[0], y_offset))
            self.world_surface.blit(name_text, (x_positions[1], y_offset))
            self.world_surface.blit(level_text, (x_positions[2], y_offset))
            self.world_surface.blit(time_text, (x_positions[3], y_offset))
            self.world_surface.blit(score_text, (x_positions[4], y_offset))
            self.world_surface.blit(date_text, (x_positions[5], y_offset))

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

        # Desenhar paredes
        for wall in self.walls:
            # Sombra
            shadow_rect = pygame.Rect(wall[0] + 2, wall[1] + 2, wall[2], wall[3])
            pygame.draw.rect(self.world_surface, DARK_GRAY, shadow_rect)
            # Parede
            pygame.draw.rect(self.world_surface, WALL_COLOR, wall)

        # Desenhar objetivo como buraco verde com efeito
        for i in range(3):
            radius = self.goal_radius - i * 8
            color_intensity = 255 - i * 60
            color = (0, color_intensity, 0)
            pygame.draw.circle(self.world_surface, color, self.goal_pos, radius)

        # Círculo interno escuro (buraco)
        pygame.draw.circle(self.world_surface, DARK_GREEN, self.goal_pos, self.goal_radius // 2)

        # Desenhar bola (com animação de explosão se pisar mina)
        if self.mine_hit_animation_time > 0:
            # Animação de explosão
            animation_progress = (time.time() - self.mine_hit_animation_time) / 0.5
            explosion_radius = int(BALL_RADIUS * (1 + animation_progress * 2))
            explosion_alpha = int(255 * (1 - animation_progress))
            explosion_color = (255, explosion_alpha, 0)
            pygame.draw.circle(self.world_surface, explosion_color, (int(self.ball.x), int(self.ball.y)), explosion_radius, 3)

        self.ball.draw(self.world_surface)

        # Indicador de direção
        self.draw_direction_indicator()

        # HUD
        # Timer
        mode_config = self.game_mode_config.get(self.game_mode, {})
        if mode_config.get('timer_direction') == 'down':
            timer_text = self.font.render(f"Tempo: {int(self.timer)}s", True, YELLOW if self.timer > 10 else RED)
        else:
            timer_text = self.font.render(f"Tempo: {self.timer:.1f}s", True, YELLOW)
        self.world_surface.blit(timer_text, (10, 10))

        # Nível
        level_text = self.font.render(f"Nível: {self.level}", True, WHITE)
        self.world_surface.blit(level_text, (self.world_width - 150, 10))

        # Corações (vidas) no centro inferior
        self.draw_hearts()

        # Dados do acelerómetro + teclado (pequenos)
        combined_x = self.accel_x + self.keyboard_accel_x
        combined_y = self.accel_y + self.keyboard_accel_y
        accel_text = self.small_font.render(
            f"X:{combined_x:.2f} Y:{combined_y:.2f}",
            True, GRAY
        )
        self.world_surface.blit(accel_text, (10, self.world_height - 30))

        # Instruções
        instructions = self.small_font.render("ESC: Pausar | R: Reiniciar", True, GRAY)
        self.world_surface.blit(instructions, (self.world_width - 280, self.world_height - 30))

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

        # Desenhar bola na posição pausada
        self.ball.draw(self.world_surface)

        # Indicador de direção
        self.draw_direction_indicator()

        # HUD
        timer_text = self.font.render(f"Tempo: {self.timer:.1f}s", True, YELLOW)
        self.world_surface.blit(timer_text, (10, 10))

        level_text = self.font.render(f"N\u00edvel: {self.level}", True, WHITE)
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

        # Título
        title = self.font.render("PAUSADO", True, WHITE)
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

        # Título
        title = self.title_font.render("N\u00cdVEL COMPLETO!", True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 80))
        self.world_surface.blit(title, title_rect)

        # Métricas
        metrics = [
            f"N\u00edvel: {self.level}",
            f"Tempo: {self.current_time:.2f}s",
            f"Pontua\u00e7\u00e3o: {self.current_score}",
            "",
            "Estat\u00edsticas Totais:",
            f"N\u00edveis Completados: {self.levels_completed}",
            f"Tempo Total: {self.total_time:.2f}s",
            f"Melhor Tempo: {self.best_time:.2f}s",
        ]

        y_offset = 180
        for metric in metrics:
            if metric:
                color = GOLD if "Pontua\u00e7\u00e3o" in metric else WHITE
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
        """Desenhar menu de seleção de modo de jogo"""
        self.world_surface.fill(BLACK)

        # Título
        title = self.title_font.render("Selecionar Modo", True, GREEN)
        title_rect = title.get_rect(center=(self.world_width // 2, 80))
        self.world_surface.blit(title, title_rect)

        # Descrições dos modos
        mode_descriptions = {
            0: "Sistema de precisão - evite tocar nas paredes",
            1: "Minas invisíveis espalhadas pelo labirinto",
            2: "Complete o máximo de níveis em 5 minutos",
            3: "Timer decrescente - ganhe tempo ao passar níveis"
        }

        # Botões com descrições
        for i, button in enumerate(self.mode_select_buttons):
            button.draw(self.world_surface, self.font)

            # Desenhar descrição pequena abaixo do botão (exceto no botão "Voltar")
            if i < 4:
                desc_text = self.small_font.render(mode_descriptions[i], True, GRAY)
                desc_rect = desc_text.get_rect(center=(self.world_width // 2, button.rect.y + button.rect.height + 15))
                self.world_surface.blit(desc_text, desc_rect)

        # Renderizar na tela
        self.render_world_to_screen()
        pygame.display.flip()

    def draw_gameover(self):
        """Desenhar tela de game over"""
        self.world_surface.fill(BLACK)

        # Título
        title = self.title_font.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(self.world_width // 2, 120))

        # Sombra
        shadow = self.title_font.render("GAME OVER", True, DARK_GRAY)
        shadow_rect = shadow.get_rect(center=(self.world_width // 2 + 5, 126))
        self.world_surface.blit(shadow, shadow_rect)
        self.world_surface.blit(title, title_rect)

        # Estatísticas
        stats = [
            f"Nível Alcançado: {self.level}",
            f"Níveis Completados: {self.levels_completed}",
            f"Tempo Total: {self.total_time:.2f}s",
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

    def handle_menu_events(self, event):
        """Tratar eventos do menu principal"""
        for i, button in enumerate(self.main_menu_buttons):
            if button.handle_event(event):
                if i == 0:  # Jogar - ir para seleção de modo
                    self.state = "MODE_SELECT"
                elif i == 1:  # Definições
                    self.state = "SETTINGS"
                elif i == 2:  # Leaderboard
                    self.state = "LEADERBOARD"
                elif i == 3:  # Sair
                    self.running = False

    def handle_mode_select_events(self, event):
        """Tratar eventos do menu de seleção de modo"""
        for i, button in enumerate(self.mode_select_buttons):
            if button.handle_event(event):
                if i == 0:  # Normal
                    self.game_mode = 'normal'
                    self.start_game()
                elif i == 1:  # Campo Minado
                    self.game_mode = 'minefield'
                    self.start_game()
                elif i == 2:  # Contra-Relógio
                    self.game_mode = 'timeattack'
                    self.start_game()
                elif i == 3:  # Eliminação
                    self.game_mode = 'elimination'
                    self.start_game()
                elif i == 4:  # Voltar
                    self.state = "MENU"

    def handle_gameover_events(self, event):
        """Tratar eventos do menu de game over"""
        for i, button in enumerate(self.gameover_buttons):
            if button.handle_event(event):
                if i == 0:  # Tentar Novamente
                    self.start_game()
                elif i == 1:  # Menu Principal
                    self.state = "MENU"

    def start_game(self):
        """Iniciar jogo com modo selecionado"""
        if not self.serial_connected:
            self.connect_serial()
        self.state = "PLAYING"
        self.level = 1
        self.total_time = 0
        self.levels_completed = 0
        # Resetar vidas baseado no modo
        mode_config = self.game_mode_config.get(self.game_mode, {})
        self.lives = mode_config.get('initial_lives', 3)
        self.max_lives = self.lives
        self.init_level()

    def handle_settings_events(self, event):
        """Tratar eventos do menu de definições"""
        self.sensitivity_slider.handle_event(event)
        old_sensitivity = self.sensitivity
        self.sensitivity = self.sensitivity_slider.value

        # Salvar se mudou
        if old_sensitivity != self.sensitivity:
            self.config.set('sensitivity', self.sensitivity)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Botão inverter X (ajustado para nova posição Y: 360)
            if 340 < mouse_pos[1] < 390 and self.world_width // 2 - 150 < mouse_pos[0] < self.world_width // 2 + 200:
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

        for button in self.settings_buttons:
            if button.handle_event(event):
                self.state = "MENU"

    def handle_leaderboard_events(self, event):
        """Tratar eventos da leaderboard"""
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
                    self.init_level()
                    self.state = "PLAYING"
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
                    self.state = "MENU"

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
                    elif event.key == pygame.K_r and self.state == "PLAYING":
                        self.init_level()
                    elif event.key == pygame.K_F11:
                        # Alternar fullscreen
                        pygame.display.toggle_fullscreen()

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
                elif self.state == "MODE_SELECT":
                    self.handle_mode_select_events(event)
                elif self.state == "SETTINGS":
                    self.handle_settings_events(event)
                elif self.state == "LEADERBOARD":
                    self.handle_leaderboard_events(event)
                elif self.state == "PAUSED":
                    self.handle_pause_events(event)
                elif self.state == "WIN":
                    self.handle_win_events(event)
                elif self.state == "GAME_OVER":
                    self.handle_gameover_events(event)

            # Atualização do jogo
            if self.state == "PLAYING":
                # Ler dados
                self.read_serial()
                self.handle_keyboard()

                # Atualizar sensibilidade da bola
                self.ball.sensitivity = self.sensitivity

                # Combinar aceleração do acelerómetro com teclado
                combined_accel_x = self.accel_x + self.keyboard_accel_x
                combined_accel_y = self.accel_y + self.keyboard_accel_y

                # Atualizar bola com aceleração combinada
                collided = self.ball.update(combined_accel_x, combined_accel_y, dt, self.walls)

                # Sistema de precisão (modo normal)
                mode_config = self.game_mode_config.get(self.game_mode, {})
                if mode_config.get('track_precision', False):
                    current_time = time.time()
                    if collided:
                        # Colidiu com parede
                        self.wall_collisions += 1
                        self.collision_pause_time = current_time + 3.0  # Pausa de 3s
                    elif current_time > self.collision_pause_time:
                        # Incrementar precisão se não estiver em pausa
                        time_delta = current_time - self.last_precision_update
                        self.precision_score += int(time_delta * 10)  # 10 pontos por segundo
                    self.last_precision_update = current_time

                # Verificar colisão com minas
                if len(self.mines) > 0 and self.mine_hit_animation_time == 0:
                    for mine_x, mine_y in self.mines[:]:  # Copiar lista para poder modificar
                        distance = math.sqrt((self.ball.x - mine_x)**2 + (self.ball.y - mine_y)**2)
                        if distance < BALL_RADIUS + 15:  # 15 pixels de raio da mina
                            # Pisar mina!
                            self.mines.remove((mine_x, mine_y))
                            self.send_mine_command()
                            self.lives -= 1
                            self.mine_hit_animation_time = time.time()
                            self.life_lost_animation_time = time.time()

                            # Verificar game over
                            if self.lives <= 0:
                                self.state = "GAME_OVER"
                            else:
                                # Resetar posição da bola
                                self.ball.x = MAZE_MARGIN + 60
                                self.ball.y = MAZE_MARGIN_TOP + 60
                                self.ball.vx = 0
                                self.ball.vy = 0
                            break

                # Atualizar timer baseado no modo
                if mode_config.get('timer_direction') == 'down':
                    # Timer decrescente
                    self.timer -= dt
                    if self.timer <= 0:
                        self.timer = 0
                        self.state = "GAME_OVER"
                else:
                    # Timer crescente (normal)
                    self.timer = time.time() - self.level_start_time

                # Atualizar animações
                if self.mine_hit_animation_time > 0:
                    if time.time() - self.mine_hit_animation_time > 0.5:  # 500ms de animação
                        self.mine_hit_animation_time = 0

                # Verificar vitória
                self.check_win()

            # Desenho
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "MODE_SELECT":
                self.draw_mode_select()
            elif self.state == "SETTINGS":
                self.draw_settings()
            elif self.state == "LEADERBOARD":
                self.draw_leaderboard()
            elif self.state == "PLAYING":
                self.draw_playing()
            elif self.state == "PAUSED":
                self.draw_pause()
            elif self.state == "WIN":
                self.draw_win()
            elif self.state == "GAME_OVER":
                self.draw_gameover()

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