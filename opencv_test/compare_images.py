import ctypes, os, openpyxl, math, datetime
from tkinter import *
from PIL import Image, ImageTk
from random import random, sample

class PairComparisonUI:
    MODE_SELECT_UI = 0
    SIDE_BY_SIDE_MODE = 1
    SWAP_IMAGE_MODE = 2
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"} # list of acceptable image extensions (add if necessary)

    def __init__(self, master):
        self.master = master
        self.mode = None
        self.image_list = []

        self.load_images()
        self.create_mode_select_ui()

    # loads images from the images folder into image_list. If the images folder does not exist, it is created here
    def load_images(self):
        # creates images folder if one does not exist, then moves the CWD to that folder
        if not os.path.exists(os.path.join(os.getcwd(), "output")):
            os.makedirs(os.path.join(os.getcwd(), "output"))
        os.chdir(os.path.join(os.getcwd(), "output"))

        self.image_list.clear()

        # loads images with acceptable extensions into image_list and sorts them alphabetically
        for file in os.listdir(os.getcwd()):
            if any(file.endswith(ext) for ext in self.IMAGE_EXTENSIONS):
                self.image_list.append(file)
        self.image_list.sort()

    # creates the initial UI where the user can choose which mode they would like to use to compare images
    def create_mode_select_ui(self):
        self.mode = self.MODE_SELECT_UI
        self.clear_ui()

        # creates a full-screen, non-resizable window
        self.master.title("Image Comparison")
        self.master.geometry('{}x{}'.format(ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)))
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.state("zoomed")

        # creates the menu bar
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.close_window)

        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Change Mode", command=self.change_mode)
        self.options_menu.add_command(label="Start Over", command=self.start_over)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Instructions", command=self.show_instructions)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(master=self.master, bg="#7C7C7C")
        self.top_frame.grid(row=0, sticky="ew")
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.main_frame = Frame(master=self.master, bg="#7C7C7C")
        self.main_frame.grid(row=1, sticky="ns")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.instructions = Label(self.top_frame, text="Select how you would like to compare images", font=("helvetica", 14), fg="light gray", bg="#7C7C7C")
        self.instructions.grid()

        # creates buttons for the user to pick the comparison mode of choice
        self.side_by_side = Button(self.main_frame, width=int(self.master.winfo_screenwidth() / 2), text="Side-by-side", font=("georgia", 20), fg="black", bg="light gray", command=self.enter_side_by_side_mode)
        self.side_by_side.grid(row=0, column=0, sticky="ns", padx=(20, 10), pady=(0, 20))

        self.swap_image = Button(self.main_frame, width=int(self.master.winfo_screenwidth() / 2), text="Swap Images", font=("georgia", 20), fg="black", bg="light gray", command=self.enter_swap_image_mode)
        self.swap_image.grid(row=0, column=1, sticky="ns", padx=(10, 20), pady=(0, 20))

    # takes the user into side-by-side comparison. This is called when the user makes an image selection in side-by-side mode, in order to ready the next image. It is also called when the user changes modes to side-by-side mode. The parameter comparison_in_progress is False when this function is called from the initial mode select screen, but True otherwise since a comparison is in progress. When it is False, which should only happen once per pair comparison, additional segments of code are carried out.
    def enter_side_by_side_mode(self, comparison_in_progress=False):
        # displays error dialogs if image_list is empty or if image naming convention was not followed
        if len(self.image_list) == 0:
            self.display_empty_images_folder_dialog()
        elif not (self.images_named_properly() or comparison_in_progress):
            self.display_images_named_improperly_dialog()
        else:
            # creates the side-by-side comparison UI. This code only runs if the user has just changed modes from a different UI
            if(self.mode != self.SIDE_BY_SIDE_MODE):
                self.mode = self.SIDE_BY_SIDE_MODE
                self.clear_ui()

                self.master.grid_rowconfigure(0, weight=1)
                self.master.grid_rowconfigure(1, weight=0)
                self.master.grid_columnconfigure(0, weight=1)

                self.main_frame = Frame(master=self.master, bg="#7C7C7C")
                self.main_frame.grid(row=0, sticky="nsew")
                self.main_frame.grid_rowconfigure(0, weight=1)
                self.main_frame.grid_rowconfigure(2, weight=1)
                self.main_frame.grid_columnconfigure(0, weight=1)
                self.main_frame.grid_columnconfigure(1, weight=1)

                self.bottom_frame = Frame(master=self.master, bg="#7C7C7C")
                self.bottom_frame.grid(row=1, sticky="ew")
                self.bottom_frame.grid_columnconfigure(0, weight=1)
                self.bottom_frame.grid_columnconfigure(1, weight=1)

                # creates the buttons that correspond with each image
                self.left_image_button = Button(self.bottom_frame, width=int(self.master.winfo_screenwidth() / 2), text="Image 1", font=("georgia", 20), fg="black", bg="light gray", command=lambda: self.remove_images())
                self.left_image_button.grid(row=0, column=0, padx=(20, 10), pady=20)

                self.right_image_button = Button(self.bottom_frame, width=int(self.master.winfo_screenwidth() / 2), text="Image 2", font=("georgia", 20), fg="black", bg="light gray", command=lambda: self.remove_images())
                self.right_image_button.grid(row=0, column=1, padx=(10, 20), pady=20)
            else:
                # if the user was already in side-by-side comparison mode, then only the previous set of images needs to be replaced
                self.left_image_panel.destroy()
                self.right_image_panel.destroy()

            # loads the next pair of images for comparison
            self.left_image = ImageTk.PhotoImage(Image.open(self.image_list[0]))
            self.left_image_panel = Label(self.main_frame, image=self.left_image)
            self.left_image_panel.grid(row=1, column=0, padx=(20, 10), pady=(20, 0))

            self.right_image = ImageTk.PhotoImage(Image.open(self.image_list[1]))
            self.right_image_panel = Label(self.main_frame, image=self.right_image)
            self.right_image_panel.grid(row=1, column=1, padx=(10, 20), pady=(20, 0))

    # takes the user into swap-image comparison. This is called when the user makes an image selection in swap-image mode, in order to ready the next image. It is also called when the user changes modes to swap-image mode. The parameter comparison_in_progress is False when this function is called from the initial mode select screen, but True otherwise since a comparison is in progress. When it is False, which should only happen once per pair comparison, additional segments of code are carried out.
    def enter_swap_image_mode(self, comparison_in_progress=False):
        # displays error dialogs if image_list is empty or if image naming convention was not followed
        if len(self.image_list) == 0:
            self.display_empty_images_folder_dialog()
        elif not (self.images_named_properly() or comparison_in_progress):
            self.display_images_named_improperly_dialog()
        else:
            # creates the swap-image comparison UI. This code only runs if the user has just changed modes from a different UI
            if(self.mode != self.SWAP_IMAGE_MODE):
                self.mode = self.SWAP_IMAGE_MODE
                self.clear_ui()

                # when this is False, the first image in the image pair is shown. Each time the swap image button is clicked, this boolean swaps between True and False
                self.show_other_image = False

                self.master.grid_rowconfigure(0, weight=1)
                self.master.grid_rowconfigure(1, weight=0)
                self.master.grid_columnconfigure(0, weight=1)

                self.main_frame = Frame(master=self.master, bg="#7C7C7C")
                self.main_frame.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="nsew")
                self.main_frame.grid_rowconfigure(0, weight=1)
                self.main_frame.grid_columnconfigure(0, weight=1)

                self.bottom_frame = Frame(master=self.master, bg="#7C7C7C")
                self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
                self.bottom_frame.grid_columnconfigure(0, weight=1)
                self.bottom_frame.grid_columnconfigure(2, weight=1)

                self.right_frame = Frame(master=self.master, bg="#7C7C7C")
                self.right_frame.grid(row=0, rowspan=2, column=1, sticky="ns")
                self.right_frame.grid_rowconfigure(0, weight=1)
                self.right_frame.grid_rowconfigure(2, weight=1)

                # when clicked, store that the user chose the image currently being shown
                self.choose_image_button = Button(self.bottom_frame, text="Choose this image", font=("georgia", 20), fg="black", bg="light gray", command=lambda: self.remove_images())
                self.choose_image_button.grid(row=0, column=1, padx=20, pady=20)

                # when clicked, swap which image of the current image pair is being shown
                self.swap_image_button = Button(self.right_frame, text="Swap", font=("georgia", 20), fg="black", bg="light gray", command=self.swap_images)
                self.swap_image_button.grid(row=1, column=0, padx=20, pady=20)
            else:
                # if the user was already in swap-image comparison mode, then only the previous shown image needs to be replaced
                self.image_panel.destroy()

            # loads the next shown image
            self.shown_image = ImageTk.PhotoImage(Image.open(self.image_list[1 if self.show_other_image else 0]))
            self.image_panel = Label(self.main_frame, image=self.shown_image)
            self.image_panel.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))

    # clears all widgets in the tkinter UI
    def clear_ui(self):
        for item in self.master.grid_slaves():
            item.destroy()

    # closes the program window
    def close_window(self):
        self.master.destroy()

    # displays a pop-up with instructions on how to load and name images
    def show_instructions(self):
        ctypes.windll.user32.MessageBoxW(None, "Place all images for comparison in the 'output' folder before running the program. Only images using JPEG or PNG file formats may be recognized. Each image must be paired with another image for comparison. Each image pair must share the same root file name (case sensitive), followed by '_A' for the first image and '_B' for the second image (also case sensitive). For example, an image named 'cat_A.png' must be paired with an image named 'cat_B.png'.", "Instructions", 0x00040000 | 0x00000040)

    # displays a error indicating that the images folder is empty
    def display_empty_images_folder_dialog(self):
        ctypes.windll.user32.MessageBoxW(None, "There are no images in the 'output' folder!", "Error", 0x00040000 | 0x00000030)

    # displays an error indicating that one or more images are named improperly
    def display_images_named_improperly_dialog(self):
        ctypes.windll.user32.MessageBoxW(None, "One or more images in the 'output' folder are named improperly!", "Error", 0x00040000 | 0x00000030)

    # returns whether all images are named properly
    def images_named_properly(self):
        for x in range(0, len(self.image_list), 2):
            if x + 1 >= len(self.image_list):
                #makes sure each image has a pair
                return False
            else:
                image_A = os.path.splitext(self.image_list[x])[0]
                image_B = os.path.splitext(self.image_list[x + 1])[0]

                #checks to make sure each image pair ends in "_A" and "_B"
                if not (image_A[:-2] == image_B[:-2] and image_A[-2:] == "_A" and image_B[-2:] == "_B"):
                    return False
        return True

    # swaps the image being shown in swap-image mode
    def swap_images(self):
        self.show_other_image = not self.show_other_image
        self.enter_swap_image_mode(True)

    # pop images from list
    def remove_images(self):
        # the image pair is removed from image_list
        self.image_list.pop(0)
        self.image_list.pop(0)

        # saves all the user's choices to an excel file and returns the user to the mode select screen if there are no images left to compare. Otherwise, the user is shown the next pair of images in whatever mode they were in
        if len(self.image_list) == 0:
            ctypes.windll.user32.MessageBoxW(None, "Pair comparison complete. Returning to mode select screen.", "Notice", 0x00040000)
            self.start_over()
        elif self.mode == self.SIDE_BY_SIDE_MODE:
            self.enter_side_by_side_mode(True)
        elif self.mode == self.SWAP_IMAGE_MODE:
            self.enter_swap_image_mode(True)

    # if the user is in a comparison mode, change to the other comparison mode
    def change_mode(self):
        if self.mode == self.SIDE_BY_SIDE_MODE:
            self.enter_swap_image_mode(True)
        elif self.mode == self.SWAP_IMAGE_MODE:
            self.enter_side_by_side_mode(True)

    # restarts pair comparison
    def start_over(self):
        os.chdir(os.path.dirname(os.getcwd()))
        self.load_images()
        self.create_mode_select_ui()

root = Tk()
ui = PairComparisonUI(root)

root.mainloop()
