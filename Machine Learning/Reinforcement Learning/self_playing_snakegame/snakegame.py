import pygame
import random
import sys
import numpy as np
import os
import pickle
import csv
import matplotlib.pyplot as plt
import pandas as pd

pygame.init()
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Playing Snake with RL")

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.q_values = self.load_model("best_model_by_score.pkl")
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05
        self.episode_count = 0
        self.high_score = 0
        self.max_steps = 0
        self.step_count = 0
        self.score = 0

    def generate_food(self):
        return (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

    def get_q_value(self, state, action):
        return self.q_values.get((state, action), 0)

    def update_q_value(self, state, action, value):
        self.q_values[(state, action)] = value

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        else:
            q_values = [self.get_q_value(state, a) for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']]
            return ['UP', 'DOWN', 'LEFT', 'RIGHT'][np.argmax(q_values)]

    def save_model(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.q_values, f)
        print(f"✅ Model disimpan: {filename}")

    def load_model(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                print(f"📦 Model {filename} berhasil dimuat.")
                return pickle.load(f)
        return {}

    def log_training(self, episode, score, steps):
        log_file = "training_log.csv"
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Episode", "Score", "Steps"])
            writer.writerow([episode, score, steps])

    def plot_progress(self):
        try:
            df = pd.read_csv("training_log.csv")
            plt.figure(figsize=(10, 5))
            plt.plot(df["Episode"], df["Score"], label="Score")
            plt.xlabel("Episode")
            plt.ylabel("Score")
            plt.title("Training Progress")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.savefig("progress_chart.png")
            plt.close()
            print("📈 Grafik progress disimpan di 'progress_chart.png'")
        except Exception as e:
            print("❌ Gagal plot grafik:", e)

    def play(self):
        clock = pygame.time.Clock()
        while True:
            try:
                self.snake = [(200, 200), (220, 200), (240, 200)]
                self.direction = 'RIGHT'
                self.food = self.generate_food()
                self.score = 0
                self.step_count = 0
                self.episode_count += 1
                self.q_values = self.load_model("model/best_model_by_steps.pkl")  # atau best_model_by_score.pkl


                while True:
                    clock.tick(FPS)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    head = self.snake[-1]
                    state = (head[0], head[1], self.direction, self.food[0], self.food[1])
                    action = self.choose_action(state)
                    old_direction = self.direction
                    self.direction = action

                    # Gerakan ular
                    if self.direction == 'RIGHT':
                        new_head = (head[0] + BLOCK_SIZE, head[1])
                    elif self.direction == 'LEFT':
                        new_head = (head[0] - BLOCK_SIZE, head[1])
                    elif self.direction == 'UP':
                        new_head = (head[0], head[1] - BLOCK_SIZE)
                    elif self.direction == 'DOWN':
                        new_head = (head[0], head[1] + BLOCK_SIZE)

                    self.snake.append(new_head)
                    self.step_count += 1

                    reward = -1
                    if self.food == new_head:
                        self.food = self.generate_food()
                        reward = 10
                        self.score += 1
                    else:
                        self.snake.pop(0)

                    if (new_head[0] < 0 or new_head[0] >= WIDTH or
                        new_head[1] < 0 or new_head[1] >= HEIGHT or
                        new_head in self.snake[:-1]):
                        reward = -10
                        break

                    new_state = (new_head[0], new_head[1], self.direction, self.food[0], self.food[1])
                    old_q = self.get_q_value(state, old_direction)
                    future_q = max([self.get_q_value(new_state, a) for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']])
                    new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
                    self.update_q_value(state, old_direction, new_q)

                    win.fill(BLACK)
                    for pos in self.snake:
                        pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(win, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
                    pygame.display.update()

                print(f"🏁 Episode {self.episode_count} selesai. Skor: {self.score} | Langkah: {self.step_count}")
                self.log_training(self.episode_count, self.score, self.step_count)

                if self.step_count > self.max_steps:
                    self.max_steps = self.step_count
                    self.save_model("model/best_model_by_steps.pkl")
                    self.q_values = self.load_model("model/best_model_by_steps.pkl")

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_model("model/best_model_by_score.pkl")
                    self.q_values = self.load_model("model/best_model_by_score.pkl")  # <-- Tambahkan ini


                if self.episode_count % 50 == 0:
                    self.plot_progress()

                # Kurangi epsilon
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay

            except Exception as e:
                print(f"❌ Error terjadi: {e}. Restarting game...")
                continue

if __name__ == "__main__":
    game = SnakeGame()
    game.play()
