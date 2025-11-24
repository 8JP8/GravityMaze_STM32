# GravityMaze 🎮

Jogo de labirinto com controlo por acelerómetro ADXL345, desenvolvido em Python com Pygame.

**Resolução**: 1280x720 (HD) | **Janela Redimensionável** | **Suporte Fullscreen**

## 🌟 Funcionalidades

### 🎯 Gameplay
- **Labirintos Procedurais**: Geração automática usando algoritmo Recursive Backtracking (DFS)
- **Física Realista**: Aceleração gravitacional de 9.8 m/s² (980 pixels/s²)
- **Progressão de Dificuldade**: Cada nível aumenta a complexidade do labirinto
- **Timer e Pontuação**: Sistema de scoring baseado em tempo e nível
- **Leaderboard Local**: Top 10 pontuações armazenadas em SQLite

### 🖥️ Interface Redimensionável
- **Resolução HD**: 1280x720 pixels para gráficos nítidos e detalhados
- **Janela Flexível**: Redimensiona mantendo proporções corretas
- **Fullscreen**: Pressione F11 para alternar
- **Viewport Escalável**: Sistema de câmara que adapta o jogo a qualquer resolução
- **Proporções Mantidas**: Barras laterais pretas para manter aspect ratio 16:9
- **Margens Elegantes**: Labirinto com 40px de margem em todos os lados
- **Autoconexão Serial**: Conecta automaticamente ao STM32 ao iniciar

### 🎨 Menus
- **Menu Principal** estilo Minecraft minimalista
- **Definições**: Ajustar sensibilidade (0.1x - 2.0x) e inversão de eixos
- **Leaderboard**: Visualizar top pontuações com ranking visual
- **Menu de Pausa**: Acesso rápido durante o jogo (ESC)

### 🎮 Controlos

#### Acelerómetro ADXL345
- Inclinar para mover a bola
- Eixos X e Y invertidos por padrão (configurável)
- Sensibilidade ajustável

#### Teclado (Fallback)
- **Setas**: Mover a bola
- **ESC**: Pausar/Retomar
- **R**: Reiniciar nível
- **F11**: Fullscreen

#### Mouse
- Navegação nos menus e definições

## 🔧 Requisitos

```bash
pip install pygame pyserial
```

## 🚀 Como Jogar

```bash
python game.py
```

### Primeira Execução
1. O jogo tentará conectar-se automaticamente ao STM32 via serial
2. Se não houver conexão, usará o teclado como controlo
3. Uma base de dados `gravitymaze.db` será criada automaticamente

### Objetivo
Leva a bola vermelha até ao buraco verde no canto inferior direito o mais rápido possível!

## 📊 Sistema de Pontuação

```
Pontuação = Nível × 1000 ÷ Tempo
```

- Quanto mais rápido completares, maior a pontuação
- Níveis superiores valem mais pontos
- As melhores pontuações são guardadas automaticamente

## 🏗️ Arquitetura Técnica

### Algoritmo de Geração de Labirintos
- **Recursive Backtracking (DFS)**
- Garante labirintos perfeitos (sem ciclos)
- Sempre existe um caminho entre quaisquer dois pontos
- Complexidade aumenta com o nível (células mais pequenas)

### Sistema de Física
- Aceleração gravitacional realista (9.8 m/s²)
- Detecção de colisão circular (sem bugs nos cantos)
- Fricção aplicada (0.98)
- Reflexão de velocidade nas colisões

### Redimensionamento
- **Viewport Virtual**: Renderização em surface 800x600 fixa
- **Scaling Inteligente**: Escala mantendo aspect ratio
- **Conversão de Coordenadas**: Mouse/toque mapeados para mundo virtual
- **Offset Automático**: Centralização com letterboxing

## 📁 Estrutura de Ficheiros

```
Trabalho1/
├── game.py             # Código principal
├── gravitymaze.db      # Base de dados SQLite (criada automaticamente)
└── README.md           # Este ficheiro
```

## 🛠️ Configurações Serial

- **Baudrate**: 115200
- **Formato de dados**: `X:1.23,Y:-0.45,Z:0.98`
- **Timeout**: 0.01s
- **Autodetecção**: Tenta todas as portas disponíveis

## 🎯 Níveis de Dificuldade

| Nível | Tamanho da Célula | Complexidade |
|-------|-------------------|--------------|
| 1     | 80x80 px          | Básico       |
| 2     | 76x76 px          | Fácil        |
| 5     | 64x64 px          | Médio        |
| 10    | 50x50 px          | Difícil      |
| 15+   | 50x50 px          | Muito Difícil|

## 📝 Base de Dados

### Tabela: `leaderboard`
```sql
CREATE TABLE leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    level INTEGER NOT NULL,
    time REAL NOT NULL,
    score INTEGER NOT NULL,
    date TEXT NOT NULL
);
```

## 🎨 Paleta de Cores

- **Fundo**: Preto (#000000)
- **Paredes**: Branco (#FFFFFF)
- **Bola**: Vermelho (#FF0000)
- **Objetivo**: Verde (#00FF00)
- **HUD**: Amarelo (#FFFF00)
- **Ouro**: #FFD700 (Leaderboard)

## 👤 Autor

João Santos - ISEP 2025

## 📄 Licença

Projeto académico - SISTR