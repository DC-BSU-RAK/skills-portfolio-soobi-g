import tkinter as tk
import random

class JokeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Alexa Joke Teller")
        self.window.geometry("500x400")
        self.window.configure(bg='light blue')
        
        # list of the jokes
        self.jokes = [
            "Why did the chicken cross the road?To get to the other side.",
            "What happens if you boil a clown?You get a laughing stock.",
            "Why did the car get a flat tire?Because there was a fork in the road!",
            "How did the hipster burn his mouth?He ate his pizza before it was cool.",
            "What did the janitor say when he jumped out of the closet?SUPPLIES!!!!",
            "Why does the golfer wear two pants?Because he's afraid he might get a Hole-in-one.",
            "Why should you wear glasses to maths class?Because it helps with division.",
            "Why did the woman go on the date with the mushroom?Because he was a fun-ghi.",
            "Why do bananas never get lonely?Because they hang out in bunches.",
            "What did the buffalo say when his kid went to college?Bison."
        ]
        
        self.current_joke = ""
        self.setup = ""
        self.punchline = ""
        
        self.create_widgets()
        self.hide_punchline()
    
    def create_widgets(self):
        # the Title
        title_label = tk.Label(self.window, text="Alexa Joke Teller", 
                              font=("Arial", 25, "bold"), bg='light Blue')
        title_label.pack(pady=20)
        
        # Joke  display
        self.setup_label = tk.Label(self.window, text="Click the button to hear a joke!", 
                                   font=("Arial", 14), bg='light Blue', wraplength=400)
        self.setup_label.pack(pady=20)
        
        # Punchline display
        self.punchline_label = tk.Label(self.window, text="", 
                                       font=("Arial", 14, "bold"), bg='light Blue', 
                                       fg='dark red', wraplength=400)
        self.punchline_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.window, bg='light Blue')
        button_frame.pack(pady=30)
        
        # button of telling the joke
        self.joke_button = tk.Button(button_frame, text="Alexa tell me a Joke", 
                                    font=("Arial", 13), command=self.tell_joke,
                                    bg='light green', width=15)
        self.joke_button.grid(row=0, column=0, padx=10, pady=5)
        
        # Show punchline button
        self.punchline_button = tk.Button(button_frame, text="Show Punchline", 
                                         font=("Arial", 14), command=self.show_punchline,
                                         bg='yellow', width=15)
        self.punchline_button.grid(row=0, column=1, padx=10, pady=5)
        
        # Next joke button
        self.next_button = tk.Button(button_frame, text="Next Joke", 
                                    font=("Arial", 14), command=self.next_joke,
                                    bg='orange', width=15)
        self.next_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Quit button
        self.quit_button = tk.Button(button_frame, text="Quit", 
                                    font=("Arial", 14), command=self.window.quit,
                                    bg='red', fg='white', width=15)
        self.quit_button.grid(row=1, column=1, padx=10, pady=5)
    
    def get_random_joke(self):
        # Pick a random joke from our list
        return random.choice(self.jokes)
    
    def split_joke(self, joke):
        # Split the joke into setup and punchline
        if '?' in joke:
            parts = joke.split('?', 1)
            setup = parts[0] + "?"
            punchline = parts[1]
        else:
            setup = "Here's the joke!"
            punchline = joke
        return setup, punchline
    
    def tell_joke(self):
        # Get a random joke
        self.current_joke = self.get_random_joke()
        self.setup, self.punchline = self.split_joke(self.current_joke)
        
        # Showing the setup part
        self.setup_label.config(text=self.setup)
        self.punchline_label.config(text="")
        
        # Enable the punchline 
        self.punchline_button.config(state='normal')
    
    def show_punchline(self):
        # Showing the funny part 
        self.punchline_label.config(text=self.punchline)
        self.punchline_button.config(state='disabled')
    
    def next_joke(self):
        # Get a new joke
        self.tell_joke()
    
    def hide_punchline(self):
        # 
        self.punchline_button.config(state='disabled')
    
    def run(self):
        self.window.mainloop()

# Start the app
if __name__ == "__main__":
    print("Starting Alexa Joke Teller...")
    app = JokeApp()
    app.run()
