import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tqdm import tqdm

# Fitness function (to be optimized)
def fitness(x):
    return x**2

# Genetic algorithm parameters
pop_size = 5
num_generations = 50
mutation_rate = 0.2

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Genetic Algorithm")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create input fields
        self.num_generations_label = tk.Label(self, text="Number of generations:")
        self.num_generations_label.pack()
        self.num_generations_entry = tk.Entry(self)
        self.num_generations_entry.pack()
        self.pop_size_label = tk.Label(self, text="Population size:")
        self.pop_size_label.pack()
        self.pop_size_entry = tk.Entry(self)
        self.pop_size_entry.pack()
        self.mutation_rate_label = tk.Label(self, text="Mutation rate:")
        self.mutation_rate_label.pack()
        self.mutation_rate_entry = tk.Entry(self)
        self.mutation_rate_entry.pack()

        # Create start button
        self.start_button = tk.Button(self, text="Start", command=self.start_evolution)
        self.start_button.pack()
        
        # Create output field
        self.output_field = tk.Text(self, width=50, height=10)
        self.output_field.pack()


    def start_evolution(self):
        # Read input values from GUI
        try:
            num_generations = int(self.num_generations_entry.get())
            pop_size = int(self.pop_size_entry.get())
            mutation_rate = float(self.mutation_rate_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid input values.")
            return
        
        # Generate initial population
        pop = [random.uniform(-10, 10) for i in range(pop_size)]

        # Write initial population to output field
        self.output_field.insert(tk.END, "Initial population:\n")
        for ind in pop:
            self.output_field.insert(tk.END, str(ind) + "\n")

        # Evolution loop
        self.output_field.insert(tk.END, "Starting evolution...\n")
        for i in tqdm(range(num_generations)):
            # Calculate fitness of each individual
            fitness_values = [fitness(x) for x in pop]

            # Select parents for mating (roulette wheel selection)
            total_fitness = sum(fitness_values)
            parent_probs = [f/total_fitness for f in fitness_values]
            parents = [pop[i] for i in range(pop_size) if random.random() < parent_probs[i] and type(pop[i]) == list]

            # Create offspring via crossover (single-point crossover)
            offspring = []
            while len(offspring) < pop_size - len(parents):
                if len(parents) >= 2:
                    parent1, parent2 = random.sample(parents, 2)
                    crossover_point = random.randint(1, len(parent1)-1)
                    offspring.append(parent1[:crossover_point] + parent2[crossover_point:])

            # Add parents to offspring
            offspring += parents

            # Mutate offspring (random reset mutation)
            for j in range(len(offspring)):
                if random.random() < mutation_rate:
                    if type(offspring[j]) == list:
                        offspring[j] = [random.uniform(-10, 10)]
                    else:
                        offspring[j] = random.uniform(-10, 10)

            # Replace population with offspring
            pop = offspring
            
              # Print best individual in population
            best_ind = max(pop, key=fitness)
            self.output_field.insert(tk.END, "Best individual in generation {}: {:.4f} (fitness = {:.4f})\n".format(i+1, best_ind, fitness(best_ind)))

            # Update progress bar
            self.progress_bar["value"] = (i+1) / num_generations * 100
            self.master.update_idletasks()

        # Print final population
        self.output_field.insert(tk.END, "Final population:\n")
        for ind in pop:
            self.output_field.insert(tk.END, str(ind) + "\n")

    def create_progress_bar(self):
        # Create progress bar
        self.progress_bar = tk.ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

root = tk.Tk()
app = Application(master=root)
app.create_progress_bar()
app.mainloop()
