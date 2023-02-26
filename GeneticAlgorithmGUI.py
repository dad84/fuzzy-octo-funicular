import random
from tqdm import tqdm
import tkinter as tk

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.title("Genetic Algorithm")

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.text_box = tk.Text(self.root)
        self.text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.running = False

        self.pop_size = 5
        self.num_generations = 50
        self.mutation_rate = 0.2
        self.tournament_size = 2

        self.pop = [random.uniform(-10, 10) for i in range(self.pop_size)]

    def start(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        for i in tqdm(range(self.num_generations)):
            if not self.running:
                break

            # Calculate fitness of each individual
            fitness_values = [fitness(x) for x in self.pop]

            # Select parents for mating (tournament selection)
            parents = []
            while len(parents) < self.pop_size:
                tournament = random.sample(self.pop, self.tournament_size)
                tournament_scalars = [x for x in tournament if not isinstance(x, list)]
                if tournament_scalars:
                    winner = max(tournament_scalars, key=fitness)
                    parents.append(winner)

            # Create offspring via crossover (variable-length crossover)
            offspring = []
            while len(offspring) < self.pop_size:
                parent1, parent2 = random.sample(parents, 2)
                if isinstance(parent1, list) and isinstance(parent2, list):
                    crossover_point = random.randint(1, min(len(parent1), len(parent2))-1)
                    child = parent1[:crossover_point] + parent2[crossover_point:]
                    offspring.append(child[0])
                elif not isinstance(parent1, list) and not isinstance(parent2, list):
                    crossover_point = random.randint(1, 2)
                    if crossover_point == 1:
                        child = [parent1, parent2]
                    else:
                        child = [parent2, parent1]
                    offspring.append(child[0])

            # Mutate offspring (random reset mutation)
            for j in range(len(offspring)):
                if random.random() < self.mutation_rate:
                    offspring[j] = random.uniform(-10, 10)

            # Replace population with offspring
            self.pop = offspring

            # Print best individual in population
            best_ind = max(self.pop, key=fitness)
            self.text_box.insert(tk.END, "Best individual in generation {}: {:.4f} (fitness = {:.4f})\n".format(i+1, best_ind, fitness(best_ind)))
            self.text_box.see(tk.END)

        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop(self):
        self.running = False

def fitness(x):
    return x**2

if __name__ == '__main__':
    gui = GUI()
    gui.root.mainloop()
