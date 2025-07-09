import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Label, Button, Separator, Progressbar
import secrets


def toss_coin():
    # Disable button while animating
    toss_button.config(state="disabled")
    coin_result_label.config(text="Result: Tossing...")

    try:
        num_tosses = int(toss_count_entry.get())
        if num_tosses < 1:
            num_tosses = 1
    except ValueError:
        num_tosses = 1

    def animate_progress(value=0):
        if value <= 100:
            progressbar['value'] = value
            root.after(15, animate_progress, value + 1)  # 30ms * 100 = 3 seconds approx
        else:
            results = [secrets.choice(['●', '○']) for _ in range(num_tosses)]
            if num_tosses == 1:
                coin_result_label.config(text=f"Result: {results[0]}")
                root.geometry("400x480")  # Reset to default height
            else:
                result_text = "Results: " + ", ".join(results)
                coin_result_label.config(text=result_text)
                # Dynamically adjust window height if too many results
                if num_tosses > 20:
                    # Estimate needed height: 480 + 10 * (num_tosses - 20) / 5
                    extra_height = int(10 * ((num_tosses - 20) / 5))
                    new_height = 480 + extra_height
                    root.geometry(f"400x{new_height}")
                else:
                    root.geometry("400x480")  # Reset to default height
            toss_button.config(state="normal")
            progressbar['value'] = 0

    animate_progress()

def generate_number():
    try:
        min_val = int(min_entry.get())
        max_val = int(max_entry.get())

        if min_val > max_val:
            number_result_entry.config(state='normal')
            number_result_entry.delete(0, tk.END)
            number_result_entry.insert(0, "Error: Min > Max")
            number_result_entry.config(state='readonly')
            return

    except ValueError:
        number_result_entry.config(state='normal')
        number_result_entry.delete(0, tk.END)
        number_result_entry.insert(0, "Invalid input")
        number_result_entry.config(state='readonly')
        return

    generate_button.config(state="disabled")
    number_result_entry.config(state='normal')
    number_result_entry.delete(0, tk.END)
    number_result_entry.insert(0, "Generating...")
    number_result_entry.config(state='')
    def animate_rng_progress(value=0):
        if value <= 100:
            rng_progress['value'] = value
            root.after(15, animate_rng_progress, value + 1)
        else:
            result = secrets.randbelow(max_val - min_val + 1) + min_val
            number_result_entry.config(state='normal')
            number_result_entry.delete(0, tk.END)
            number_result_entry.insert(0, str(result))
            generate_button.config(state="normal")
            rng_progress['value'] = 0

    animate_rng_progress()

root = tk.Tk()
root.title("Coin Toss & RNG")
root.geometry("400x480")
root.resizable(False, False)
style = Style(theme="superhero")

rounded_font = ("Noto Sans", 14)

coin_label = Label(root, text="Coin Toss", font=rounded_font)
coin_label.pack(pady=10)

# Add frame for toss count input
toss_count_frame = tk.Frame(root)
toss_count_frame.pack(pady=5)

toss_count_label = Label(toss_count_frame, text="Number of tosses:", font=("Noto Sans", 10))
toss_count_label.grid(row=0, column=0, padx=5)
toss_count_entry = Entry(toss_count_frame, width=5, bootstyle="info", font=("Noto Sans", 8))
toss_count_entry.grid(row=0, column=1, padx=5)
toss_count_entry.insert(0, "1")

toss_button = Button(root, text="Toss Coin", command=toss_coin, bootstyle="success")
toss_button.pack(pady=5)

coin_result_label = Label(root, text="Result: ", font=rounded_font, wraplength=350)
coin_result_label.pack(pady=5)

# Add progressbar under the result label
progressbar = Progressbar(root, length=300, mode='determinate', bootstyle="success-striped")
progressbar.pack(pady=(0, 15))

# Add separator
separator = Separator(root, bootstyle="warning")
separator.pack(fill="x", pady=15)

rng_label = Label(root, text="Random Number Generator", font=rounded_font)
rng_label.pack(pady=10)

range_frame = tk.Frame(root)
range_frame.pack(pady=5)

min_label = Label(range_frame, text="Min:", font=("Noto Sans", 12))
min_label.grid(row=0, column=0, padx=5, pady=5)
min_entry = Entry(range_frame, width=10, bootstyle="info")
min_entry.grid(row=0, column=1, padx=10, pady=5)

max_label = Label(range_frame, text="Max:", font=("Noto Sans", 12))
max_label.grid(row=0, column=2, padx=5, pady=5)
max_entry = Entry(range_frame, width=10, bootstyle="info")
max_entry.grid(row=0, column=3, padx=10, pady=5)

# Add some space before the generate button
generate_button = Button(root, text="Generate Number", command=generate_number, bootstyle="info")
generate_button.pack(pady=10)

rng_progress = Progressbar(root, length=300, mode='determinate', bootstyle="info-striped")
rng_progress.pack(pady=(0, 10))

number_result_entry = Entry(root, width=15, font=("Noto Sans", 12), bootstyle="info", state='readonly')
number_result_entry.pack(pady=5)

root.mainloop()
