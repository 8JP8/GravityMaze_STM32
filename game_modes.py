"""
GravityMaze - Definições de Modos de Jogo
Este arquivo contém as configurações e lógica para diferentes modos de jogo
"""

# Configurações dos modos de jogo
GAME_MODES = {
    'normal': {
        'name_pt': 'Normal',
        'name_en': 'Normal',
        'timer_direction': 'up',  # Conta para cima
        'has_lives': True,
        'initial_lives': 3,
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
        'initial_lives': 3,
        'mines_everywhere': True,  # Minas em células aleatórias
        'mine_percentage': 0.15,  # 15% das células têm minas
        'desc_pt': 'Evite as minas invisíveis!',
        'desc_en': 'Avoid the invisible mines!'
    },
    'timeattack': {
        'name_pt': 'Contra-Relógio',
        'name_en': 'Time Attack',
        'timer_direction': 'down',  # Conta para baixo
        'initial_time': 300,  # 5 minutos em segundos
        'has_lives': True,
        'initial_lives': 3,
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
        'initial_lives': 3,
        'desc_pt': 'O tempo diminui! Complete níveis para ganhar mais tempo',
        'desc_en': 'Time is running out! Complete levels to gain more time'
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
