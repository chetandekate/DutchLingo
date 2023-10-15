import os
import time
import pygame
import tkinter as tk
from tkinter import (filedialog, messagebox, StringVar, Entry, PhotoImage)
from tkinter.ttk import Progressbar
from gtts import gTTS
from googletrans import Translator
from tkinter.font import Font
from PIL import Image, ImageTk
from constants import *
from tooltip import ToolTip
from custombutton import CustomButton
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import simpledialog

class DutchPracticeApp:
    """
    A GUI application for practicing Dutch vocabulary. The app allows users to upload a list of Dutch words.
    Users can then listen to the word's pronunciation and provide the English translation. Feedback is given
    based on the correctness of their answer.
    """

    def __init__(self):
        """
        Initialize the main application, set up initial variables and start the GUI.
        """
        pygame.mixer.init()  # Preparing the mixer module for audio playback
        self.words = []  # List of Dutch words uploaded by the user
        self.answers = []  # Corresponding English translations of the Dutch words
        self.translator = Translator()  # Google Translator instance
        self.current_index = 0  # Current word's index being practiced
        self.translation_cache = {}  # To save translations and avoid repeated API calls
        self._init_gui()  # UI setup method call
        self.audio_files = []  # Paths to audio files of Dutch words

    def _init_gui(self):
        """
        Set up the application's main graphical user interface components.
        """
        # Window setup
        self.root = tk.Tk()
        self.root.resizable(False, False)  # Disable resizing
        self.root.title('Dutch Practice')
        self.root.geometry("900x650")
        self.root.configure(bg='white')

        # Load background image and adjust its size
        bg_image = Image.open(os.path.abspath('icons/background.png'))
        bg_image = bg_image.resize((900, 650))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load logo and adjust its size
        logo_image = Image.open(os.path.abspath('icons/logo.png'))
        logo_image = logo_image.resize((400, 100))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.root, image=logo_photo, bg='white')
        logo_label.pack(pady=(20, 0))

        # Main frame for text boxes and buttons
        frame = tk.Frame(self.root, bg='white')
        frame.pack(padx=50, pady=30)

        # Dutch word display (read-only for user)
        self.displayed_word_var = tk.StringVar()
        self.displayed_word_entry = tk.Entry(frame, textvariable=self.displayed_word_var, font=("Arial", 18), width=30,
                                             state="readonly", borderwidth=2, relief="groove")
        self.displayed_word_entry.grid(row=0, column=0, padx=20, pady=10)

        # English translation entry
        self.translation_var = tk.StringVar()
        self.translation_entry = tk.Entry(frame, textvariable=self.translation_var, font=("Arial", 18), width=30,
                                          borderwidth=2, relief="groove")
        self.translation_entry.grid(row=1, column=0, padx=20, pady=10)

        # Buttons Frame
        button_frame = tk.Frame(frame, bg='white')
        button_frame.grid(row=2, column=0, pady=20)

        # Change the Button Color and Design
        gradient_color_top = "#2c3e50"
        gradient_color_bottom = "#3498db"
        button_style = {
            "font": ("Arial", 16),
            "bg": gradient_color_bottom,
            "fg": "white",
            "borderwidth": 1,
            "relief": "solid",
            "height": 1,
            "width": 9,
            "activebackground": gradient_color_top
        }
        small_button_style = {
            "font": ("Arial", 16),
            "bg": gradient_color_bottom,
            "fg": "white",
            "borderwidth": 1,
            "relief": "solid",
            "height": 1,
            "width": 3,
            "activebackground": gradient_color_top
        }

        # Change Typography
        font_style = Font(family="Helvetica", size=16, weight="bold")
        self.upload_button = tk.Button(button_frame, text="Upload", command=self.load_files,
                                       **button_style)
        self.upload_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(button_frame, text="Play", command=self.play_audio,
                                     **button_style)
        self.play_button.grid(row=0, column=1, padx=10)

        self.submit_button = tk.Button(button_frame, text="Submit", command=self.check_answer,
                                       **button_style)
        self.submit_button.grid(row=0, column=2, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_word,
                                     **button_style)
        self.next_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(button_frame, text="Previous", command=self.previous_word,
                                     **button_style)
        self.next_button.grid(row=0, column=4, padx=10)

        self.instructions_button = tk.Button(button_frame, text="?", command=self.show_instructions,
                                             **small_button_style)
        self.instructions_button.grid(row=0, column=5, padx=10)

        # Tooltip for additional information (Part of UX improvement)
        ToolTip(self.upload_button, text="Click to upload Dutch word files")

        self.progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)
        # Add this after setting up your buttons
        self.result_label = tk.Label(self.root, bg='white', font=("Arial", 18))
        self.result_label.pack(pady=20)

        '''# Load footer image and adjust its size
        footer_image = Image.open(os.path.abspath('icons/footer.png'))
        footer_image = footer_image.resize((900, 150))
        footer_photo = ImageTk.PhotoImage(footer_image)
        footer_label = tk.Label(self.root, image=footer_photo)
        footer_label.pack(side=tk.BOTTOM, fill=tk.X)

        # To retain reference to the images
        self.bg_photo = bg_photo
        self.logo_photo = logo_photo
        self.footer_photo = footer_photo'''
        # New footer setup
        footer_frame = tk.Frame(self.root, bg="#4E4E50", height=50)  # Adjust the color as needed
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        app_name_label = tk.Label(footer_frame, text="Dutch Practice", fg="white", bg="#4E4E50", font=("Arial", 10))
        app_name_label.pack(side=tk.LEFT, padx=20)

        copyright_label = tk.Label(footer_frame, text="© " + str(time.localtime().tm_year), fg="white", bg="#4E4E50", font=("Arial", 10))
        copyright_label.pack(side=tk.RIGHT, padx=20)

        self.root.mainloop()

    def show_instructions(self):
        """
        Display an instruction window detailing how the application works.
        """
        instructions = """
                1. Click 'Upload File' to upload a Dutch words file.
                2. Once uploaded, the first word will be played.
                3. Type the English translation and click 'Submit'.
                4. Click 'Next' to move to the next word.
                5. Click 'Play Audio' to hear the Dutch word again.
                """
        response = messagebox.askyesno("Instructions", instructions + "\n\nWas this helpful?")
        if not response:
            feedback = simpledialog.askstring("Feedback", "Please provide your feedback to help us improve:")


    def update_progress(self):
        """
        Update the progress bar based on the number of words practiced.
        """
        if not self.words:
            self.progress["value"] = 0
            return

        progress = (self.current_index / len(self.words)) * 100
        self.progress["value"] = progress

    def check_answer(self):
        """
        Verify user's translation against the correct translation and provide feedback.
        """
        if not self.words:
            return
        user_translation = self.translation_entry.get().strip().lower()
        correct_translation = self.translate_word(self.words[self.current_index]).lower()
        if user_translation == correct_translation:
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Incorrect! It is: {correct_translation}", fg="red")

    def translate_word(self, word):
        """
        Fetch the English translation of a Dutch word. If the translation was previously fetched,
        it is retrieved from the cache.
        """
        try:
            if word in self.translation_cache:
                return self.translation_cache[word]
            translation = self.translator.translate(word, src='nl', dest='en').text
            self.translation_cache[word] = translation
            return translation
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while translating the word: {str(e)}")
            return ""

    def play_audio(self):
        """
        Play the pronunciation of the current Dutch word.
        """
        if not self.words or not self.audio_files:
            return
        # Check if audio file exists for the current word
        if self.current_index < len(self.audio_files):
            pygame.mixer.music.load(self.audio_files[self.current_index])
            pygame.mixer.music.play()
        else:
            messagebox.showerror("Error", "No audio file found for the current word.")

    def previous_word(self):
        """
        Move to the previous word in the list and update the display accordingly.
        """
        # Check if there are words loaded
        if not self.words:
            return
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.words) - 1
        self.displayed_word_var.set(self.words[self.current_index])
        self.translation_var.set("")  # This will clear the input box
        self.result_label.config(text="")
        self.update_progress()

    def next_word(self):
        """
        Move to the next word in the list and update the display accordingly.
        """
        # Check if there are words loaded
        if not self.words:
            return
        self.current_index += 1
        if self.current_index >= len(self.words):
            self.current_index = 0
        self.displayed_word_var.set(self.words[self.current_index])
        self.translation_var.set("")  # This will clear the input box
        self.result_label.config(text="")
        self.update_progress()

    def clean_everything(self):
        """
        Reset all variables and the interface to the initial state.
        """
        """
        Reset everything to the initial state."""
        self.words = []
        self.answers = []
        self.audio_files = []
        self.current_index = 0
        self.displayed_word_var.set("")
        self.translation_var.set("")
        self.progress["value"] = 0

    def load_files(self):
        """
        Allow user to upload a text file containing Dutch words and set up corresponding audio files.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'r') as file:
            self.words = [word.strip() for word in file.readlines()]

        if not self.words:
            messagebox.showerror("Error", "No words found in the uploaded file!")
            return

        # Check for maximum number of lines
        MAX_LINES = 500
        if len(self.words) > MAX_LINES:
            self.clean_everything()
            messagebox.showerror("Error", f"Uploaded file exceeds the maximum allowed lines ({MAX_LINES}).")
            return

        # Check for correct format (one Dutch word per line)
        for word in self.words:
            if " " in word:  # checking for spaces to determine if there's more than one word on a line
                self.clean_everything()
                messagebox.showerror("Error", "Ensure there's only one Dutch word per line!")
                return

        # Show the user that audio files are being generated.
        messagebox.showinfo("Info", "Generating audio files. This may take a few moments...")
        self.answers = [self.translate_word(word) for word in self.words]
        self.generate_audio_files()
        self.current_index = 0
        self.displayed_word_var.set(self.words[self.current_index])
        self.update_progress()
        self.play_audio()

    def generate_audio_files(self):
        """
        Produce audio files for the Dutch words using Google's Text-to-Speech.
        """
        self.audio_files = []
        for word in self.words:
            audio_path = f"audio_cache/{word}.mp3"
            if not os.path.exists(audio_path):
                try:
                    tts = gTTS(text=word, lang='nl')
                    tts.save(audio_path)
                    time.sleep(0.5)  # Adjusted sleep time
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate audio for '{word}': {str(e)}")
                    return
            self.audio_files.append(audio_path)

        if len(self.words) != len(self.audio_files):
            # If this check is true, something went wrong
            messagebox.showerror("Error",
                                 "Mismatch between words and audio files. Please check the words or try again.")

    def run(self):
        """
        Main event loop of the application.
        """
        self.root.mainloop()
        pygame.mixer.quit()
        self.cleanup()

    def cleanup(self):
        """
        Cleanup method that runs when the application closes. It deletes all generated audio files.
        """
        for audio_file in self.audio_files:
            try:
                os.remove(audio_file)
            except Exception:
                pass


if __name__ == "__main__":
    app = DutchPracticeApp()
    app.run()


