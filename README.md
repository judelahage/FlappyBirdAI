<h1 align="center">Flappy Bird AI</h1>

<p align="center">
  A Flappy Bird clone where the birds aren't controlled by you — a <b>NEAT</b> neuro-evolution
  algorithm teaches itself to play from scratch.
</p>

---

## Overview

This is the classic Flappy Bird game built in **pygame**, wired up to **NEAT** (NeuroEvolution of Augmenting Topologies) via [`neat-python`](https://neat-python.readthedocs.io/). Instead of a single player, each generation spawns a whole **population of birds**, each driven by its own neural network. Birds that fly farther earn higher fitness; the best are bred and mutated; and over successive generations the flock evolves into expert players.

## How the AI works

Every bird is controlled by a small feed-forward network:

**Inputs (3)**
- The bird's vertical position (`y`)
- Distance to the **top** pipe of the gap
- Distance to the **bottom** pipe of the gap

**Output (1)** — passed through `tanh`; if the value clears **0.5**, the bird flaps.

**Fitness**
- `+0.1` for every frame survived
- `+5` for each pipe cleared
- `−1` for a collision

Networks start fully connected with **0 hidden nodes** and grow in complexity as NEAT mutates weights, biases, and topology across generations.

## NEAT configuration

Tunable in [`config-feedforward.txt`](config-feedforward.txt):

| Setting | Value |
|---|---|
| Population size | 20 |
| Max generations | 50 |
| Fitness threshold | 100 |
| Activation function | `tanh` |
| Inputs / Outputs | 3 / 1 |
| Starting hidden nodes | 0 |

## Run it

```bash
pip install pygame neat-python
python flappy_bird.py
```

A window opens and you watch each generation learn in real time, with the live generation and score drawn on screen. Training ends when a bird reaches the fitness threshold or the generation cap is hit.

## Project layout

| File | Purpose |
|---|---|
| `flappy_bird.py` | The game plus the NEAT training loop |
| `config-feedforward.txt` | NEAT hyperparameters |
| `imgs/` | Bird, pipe, base, and background sprites |
| `notes.txt` | My working notes on how NEAT is set up |

## Credits

Built while learning neuro-evolution, following the well-known `neat-python` Flappy Bird approach — with my own comments throughout the code as I worked through it. Sprites are the classic Flappy Bird art set.
