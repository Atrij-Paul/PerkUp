import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET

class BoundingBoxAnnotator:
    def __init__(self, root):
        
        self.option_menus = {}  # Dictionary to store OptionMenu widgets
        self.option_labels = {}
        self.id_vars = {}  # Dictionary to store StringVar for ID types
        
        self.root = root
        self.root.title("Text Bounding Box Annotator")
        
        root.resizable(0,0)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas_width = 650
        self.canvas_height = 550

        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill="x")
        
    ############################################## LOAD IMAGE #############################################################    

        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image)
        # self.load_button.pack(side="left")
        
        self.load_button.grid(row=0, column=0)

    ################################################# COLOR ################################################################

        self.color_var = tk.StringVar()
        self.color_var.set("Red")
        self.color_menu = tk.OptionMenu(self.button_frame, self.color_var, "Red", "Green", "Blue", "Yellow", "Purple", "Orange")
        # self.color_menu.pack(side="left")

    ####################################################  QUESTION ##########################################################

        self.question_id_var = tk.StringVar()
        self.question_id_var.set("QuestionID")
        self.last_question_id = None
        # self.question_id_menu = tk.OptionMenu(self.button_frame, self.question_id_var, *["QuestionID"] + list(map(str, range(1, 21))), command=self.set_question_id_text)
        # self.question_id_menu.pack(side="left")
        self.question_id_menu = tk.OptionMenu(self.button_frame, self.question_id_var, *["QuestionID"] + list(map(str, range(1, 21))), command=self.set_question_id_color_and_id)
        # self.question_id_menu.pack(side="left")
        self.option_menus["QuestionID"] = self.question_id_menu  # Store the OptionMenu in the dictionary
        
        # Create and place a label for the Question ID selection
        self.question_id_label = tk.Label(self.button_frame, text=self.question_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["QuestionID"] = self.question_id_label  # Store the label in the dictionary
        
        # self.question_id_label.pack(side="left")
        # self.question_id_menu.pack(side="left")
        
        
        
        #############################################     DIAGRAM         ###########################################
        self.diagram_id_var = tk.StringVar()
        self.diagram_id_var.set("DiagramID")
        # self.diagram_id_menu = tk.OptionMenu(self.button_frame, self.diagram_id_var, *["DiagramID"] + list(map(str, range(1, 21))), command=self.set_diagram_color)
        # self.diagram_id_menu.pack(side="left")
        self.diagram_id_menu = tk.OptionMenu(self.button_frame, self.diagram_id_var, *["DiagramID"] + list(map(str, range(1, 21))), command=self.set_diagram_id_color_and_id)
        # self.diagram_id_menu.pack(side="left")
        self.option_menus["DiagramD"] = self.diagram_id_menu  # Store the OptionMenu in the dictionary
        
        self.diagram_id_label = tk.Label(self.button_frame, text=self.diagram_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["DiagramID"] = self.diagram_id_label  # Store the label in the dictionary
        
        # self.diagram_id_label.pack(side="left")
        # self.diagram_id_menu.pack(side="left")
        
        
        #############################################     MATHEMATICAL         ###########################################
        
        self.math_id_var = tk.StringVar()
        self.math_id_var.set("MathematicalID")
        # self.math_id_menu = tk.OptionMenu(self.button_frame, self.math_id_var, *["MathematicalID"] + list(map(str, range(1, 21))), command=self.set_math_color)
        # self.math_id_menu.pack(side="left")
        self.mathematical_id_menu = tk.OptionMenu(self.button_frame, self.math_id_var, *["MathematicalID"] + list(map(str, range(1, 21))), command=self.set_mathematical_id_color_and_id)
        # self.mathematical_id_menu.pack(side="left")
        self.option_menus["MathematicalID"] = self.mathematical_id_menu  # Store the OptionMenu in the dictionary
        
        self.mathematical_id_label = tk.Label(self.button_frame, text=self.math_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["MathematicalID"] = self.mathematical_id_label  # Store the label in the dictionary
        
        # self.mathematical_id_label.pack(side="left")
        # self.mathematical_id_menu.pack(side="left")
        
        
        #############################################     MATCHING         ###########################################
        
        
        self.matching_id_var = tk.StringVar()
        self.matching_id_var.set("MatchingID")
        # self.matching_id_menu = tk.OptionMenu(self.button_frame, self.matching_id_var, *["MatchingID"] + list(map(str, range(1, 21))), command=self.set_matching_color)
        # self.matching_id_menu.pack(side="left")
        self.matching_id_menu = tk.OptionMenu(self.button_frame, self.matching_id_var, *["MatchingID"] + list(map(str, range(1, 21))), command=self.set_matching_id_color_and_id)
        # self.matching_id_menu.pack(side="left")
        self.option_menus["MatchingID"] = self.matching_id_menu  # Store the OptionMenu in the dictionary
        
        
        self.matching_id_label = tk.Label(self.button_frame, text=self.matching_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["MatchingID"] = self.matching_id_label  # Store the label in the dictionary
        
        # self.matching_id_label.pack(side="left")
        # self.matching_id_menu.pack(side="left")
        
        
        #############################################     ANSWER         ###########################################
        
        self.answer_id_var = tk.StringVar()
        self.answer_id_var.set("AnswerID")
        # self.answer_id_menu = tk.OptionMenu(self.button_frame, self.answer_id_var, *["AnswerID"] + list(map(str, range(1, 21))), command=self.set_answer_color)
        # self.answer_id_menu.pack(side="left")
        self.answer_id_menu = tk.OptionMenu(self.button_frame, self.answer_id_var, *["AnswerID"] + list(map(str, range(1, 21))), command=self.set_answer_id_color_and_id)
        # self.answer_id_menu.pack(side="left")
        self.option_menus["AnswerID"] = self.answer_id_menu  # Store the OptionMenu in the dictionary
        
        
        self.answer_id_label = tk.Label(self.button_frame, text=self.answer_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["AnswerID"] = self.answer_id_label  # Store the label in the dictionary
        
        # self.answer_id_label.pack(side="left")
        # self.answer_id_menu.pack(side="left")
        
        #############################################     OPTION A         ###########################################
        
        self.option_a_id_var = tk.StringVar()
        self.option_a_id_var.set("OptionA")
        # self.option_a_menu = tk.OptionMenu(self.button_frame, self.option_a_id_var, *["OptionA"] + list(map(str, range(1, 21))), command=self.set_option_a_color)
        # self.option_a_menu.pack(side="left")
        self.option_a_menu = tk.OptionMenu(self.button_frame, self.option_a_id_var, *["OptionA"] + list(map(str, range(1, 21))), command=self.set_option_a_color_and_id)
        # self.option_a_menu.pack(side="left")
        self.option_menus["OptionA"] = self.option_a_menu  # Store the OptionMenu in the dictionary
        
        
        self.option_a_label = tk.Label(self.button_frame, text=self.option_a_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["Option A"] = self.option_a_label  # Store the label in the dictionary
        
        # self.option_a_label.pack(side="left")
        # self.option_a_menu.pack(side="left")
        
        
        #############################################     OPTION B        ###########################################
        
        self.option_b_id_var = tk.StringVar()
        self.option_b_id_var.set("OptionB")
        # self.option_b_menu = tk.OptionMenu(self.button_frame, self.option_b_id_var, *["OptionB"] + list(map(str, range(1, 21))), command=self.set_option_b_color)
        # self.option_b_menu.pack(side="left")
        self.option_b_menu = tk.OptionMenu(self.button_frame, self.option_b_id_var, *["OptionB"] + list(map(str, range(1, 21))), command=self.set_option_b_color_and_id)
        # self.option_b_menu.pack(side="left")
        self.option_menus["OptionB"] = self.option_b_menu  # Store the OptionMenu in the dictionary
        
        
        self.option_b_label = tk.Label(self.button_frame, text=self.option_b_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["Option B"] = self.option_b_label  # Store the label in the dictionary
        
        # self.option_b_label.pack(side="left")
        # self.option_b_menu.pack(side="left")
        
        #############################################     OPTION C       ###########################################
        

        self.option_c_id_var = tk.StringVar()
        self.option_c_id_var.set("OptionC")
        # self.option_c_menu = tk.OptionMenu(self.button_frame, self.option_c_id_var, *["OptionC"] + list(map(str, range(1, 21))), command=self.set_option_c_color)
        # self.option_c_menu.pack(side="left")
        self.option_c_menu = tk.OptionMenu(self.button_frame, self.option_c_id_var, *["OptionC"] + list(map(str, range(1, 21))), command=self.set_option_c_color_and_id)
        # self.option_c_menu.pack(side="left") 
        self.option_menus["OptionC"] = self.option_c_menu  # Store the OptionMenu in the dictionary
        
        self.option_c_label = tk.Label(self.button_frame, text=self.option_c_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["Option C"] = self.option_c_label  # Store the label in the dictionary
        
        # self.option_c_label.pack(side="left")
        # self.option_c_menu.pack(side="left")
        
        #############################################     OPTION D      ###########################################
        
        
        self.option_d_id_var = tk.StringVar()
        self.option_d_id_var.set("OptionD")
        # self.option_d_menu = tk.OptionMenu(self.button_frame, self.option_d_id_var, *["OptionD"] + list(map(str, range(1, 21))), command=self.set_option_d_color)
        # self.option_d_menu.pack(side="left")
        self.option_d_menu = tk.OptionMenu(self.button_frame, self.option_d_id_var, *["OptionD"] + list(map(str, range(1, 21))), command=self.set_option_d_color_and_id)
        # self.option_d_menu.pack(side="left")
        self.option_menus["OptionD"] = self.option_d_menu  # Store the OptionMenu in the dictionary
        
        self.option_d_label = tk.Label(self.button_frame, text=self.option_d_id_var.get())
        # self.question_id_label.pack(side="left")
        self.option_labels["Option D"] = self.option_d_label  # Store the label in the dictionary
        
        # self.option_d_label.pack(side="left")
        # self.option_d_menu.pack(side="left")
        
        #############################################     DELETE      ###########################################
        
        self.delete_button = tk.Button(self.button_frame, text="Delete Bounding Box", command=self.delete_bbox)
        # self.delete_button.pack(side="right")
        
        # self.delete_button.grid(row=0, column=0, padx=10, pady=10)
        
        #############################################     SAVE ANNOTATIONS      ###########################################
        
        self.save_button = tk.Button(self.button_frame, text="Save Annotations", command=self.save_annotations)
        # self.save_button.pack(side="right")
        
        self.save_button.grid(row=0, column=0, padx=10, pady=10)
        
        #############################################     ###############      ###########################################
        
        self.bboxes = []  
        self.current_bbox = None
        self.image_path = None
        self.image = None
        self.img_label = None

        self.current_id_type = None
        self.current_id_number = None
        
        self.canvas.bind("<Button-1>", self.start_bbox)
        self.canvas.bind("<B1-Motion>", self.draw_bbox)
        self.canvas.bind("<ButtonRelease-1>", self.end_bbox)
        
        id_types = ["QuestionID", "DiagramID", "MathematicalID", "MatchingID", "AnswerID", "OptionA", "OptionB", "OptionC", "OptionD"]

        # Divide the button_frame into sections for different groups of widgets
        row_offset = 2
        for idx, id_type in enumerate(id_types):
            if idx == 4:  # Start a new column after OptionD
                row_offset = 2
            self.id_vars[id_type] = tk.StringVar(value="Select")
            self.option_menus[id_type] = tk.OptionMenu(self.button_frame, self.id_vars[id_type], *["Select"] + list(map(str, range(1, 21))), command=self.set_id_color_and_id)
            self.option_menus[id_type].grid(row=row_offset + idx % 5, column=(idx // 5) * 2 + 1)

            self.option_labels[id_type] = tk.Label(self.button_frame, text=id_type)
            self.option_labels[id_type].grid(row=row_offset + idx % 5, column=(idx // 5) * 2)
            
        self.delete_button.grid(row = 0 , column = 6)
        
        self.save_button.grid(row = 0 , column = 7)
        

        
    def set_question_id_color_and_id(self, selected_value):
       self.set_question_id_color(selected_value)
       self.set_id_type("QuestionID")
       self.set_id_number(selected_value)  
    #    self.update_option_menu_label("QuestionID", selected_value)  # Update the OptionMenu label   
       self.option_labels["QuestionID"].config(text="QuestionID")  # Update the label text
       
    
    def set_id_color_and_id(self, selected_id):
        if selected_id != "Select":
            self.current_id_type = self.get_selected_id_type()
            self.current_id_number = int(selected_id)
            self.option_labels[self.current_id_type].configure(foreground=self.color_var.get())
            self.update_canvas()
        
    def set_diagram_id_color_and_id(self, selected_value):
       self.set_diagram_id_color(selected_value)
       self.set_id_type("DiagramID")
       self.set_id_number(selected_value)
    #    self.update_option_menu_label("DiagramID", selected_value)  # Update the OptionMenu label   
       self.option_labels["DiagramID"].config(text="DiagramID")  # Update the label text
    
    def set_mathematical_id_color_and_id(self, selected_value):
       self.set_mathematical_id_color(selected_value)
       self.set_id_type("MathematicalID")
       self.set_id_number(selected_value)
    #    self.update_option_menu_label("MathematicalID", selected_value)  # Update the OptionMenu label   
       self.option_labels["MathematicalID"].config(text="MathematicalID")  # Update the label text
    
    
    def set_matching_id_color_and_id(self, selected_value):
       self.set_matching_id_color(selected_value)
       self.set_id_type("MatchingID")
       self.set_id_number(selected_value)
       self.update_option_menu_label("MatchingID", selected_value)  # Update the OptionMenu label   
       self.option_labels["MatchingID"].config(text="MatchingID")  # Update the label text
    
    
    def set_answer_id_color_and_id(self, selected_value):
       self.set_answer_id_color(selected_value)
       self.set_id_type("AnswerID")
       self.set_id_number(selected_value)
       self.update_option_menu_label("AnswerID", selected_value)  # Update the OptionMenu label   
       self.option_labels["AnswerID"].config(text="AnswerID")  # Update the label text
    
    
    def set_option_a_color_and_id(self, selected_value):
       self.set_option_a_color(selected_value)
       self.set_id_type("Option A")
       self.set_id_number(selected_value)
       self.update_option_menu_label("OptionA", selected_value)  # Update the OptionMenu label   
       self.option_labels["Option A"].config(text="Option A")  # Update the label text
     
     
    def set_option_b_color_and_id(self, selected_value):
       self.set_option_b_color(selected_value)
       self.set_id_type("Option B")
       self.set_id_number(selected_value)
       self.update_option_menu_label("OptionB", selected_value)  # Update the OptionMenu label   
       self.option_labels["Option B"].config(text="Option B")  # Update the label text
       
    
    def set_option_c_color_and_id(self, selected_value):
       self.set_option_c_color(selected_value)
       self.set_id_type("Option C")
       self.set_id_number(selected_value)
       self.update_option_menu_label("OptionC", selected_value)  # Update the OptionMenu label   
       self.option_labels["Option C"].config(text="Option C")  # Update the label text
       
        
    def set_option_d_color_and_id(self, selected_value):
       self.set_option_d_color(selected_value)
       self.set_id_type("Option D")
       self.set_id_number(selected_value) 
       self.update_option_menu_label("OptionD", selected_value)  # Update the OptionMenu label   
       self.option_labels["Option D"].config(text="Option D")  # Update the label text
       
       
    def set_id_type(self, selected_value):
     self.current_id_type = selected_value
     if self.current_bbox:
        self.current_bbox[5] = self.current_id_type

    def set_id_number(self, selected_value):
      self.current_id_number = selected_value
      if self.current_bbox:
        self.current_bbox[6] = self.current_id_number

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((self.canvas_width, self.canvas_height))
            self.img_label = ImageTk.PhotoImage(self.image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_label)
            self.bboxes = []

    def start_bbox(self, event):
        if self.image:
            x, y = event.x, event.y
            id_type = self.current_id_type if self.current_id_type else "None"
            id_number = self.current_id_number if self.current_id_number else "None"
            self.current_bbox = [x, y, x, y, self.color_var.get(), id_type, id_number]
        
        
    def draw_bbox(self, event):
        if self.current_bbox:
            x2, y2 = event.x, event.y
            self.canvas.delete("bbox")
            for bbox in self.bboxes:
                self.canvas.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], outline=bbox[4], width=2, tags="bbox")

            self.canvas.create_rectangle(self.current_bbox[0], self.current_bbox[1], x2, y2, outline=self.current_bbox[4], width=2, tags="bbox")

    def end_bbox(self, event):
        if self.current_bbox:
            x2, y2 = event.x, event.y
            self.current_bbox[2] = x2
            self.current_bbox[3] = y2
            self.bboxes.append(tuple(self.current_bbox))
            self.current_bbox = None

    def delete_bbox(self):
        if self.bboxes and self.current_bbox:
            self.bboxes.remove(self.current_bbox)
            self.canvas.delete("bbox")
            for bbox in self.bboxes:
                self.canvas.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], outline=bbox[4], width=2, tags="bbox")
                if bbox[5] != "None":
                    text_x = bbox[0]
                    text_y = bbox[1] - 20
                    self.canvas.create_text(text_x, text_y, text=bbox[5], anchor="sw", fill=bbox[4], font=("Arial", 12, "bold"))
            self.current_bbox = None

    def save_annotations(self):
        if self.bboxes and self.image_path:
            annotation_path = "C:\\Users\\atrij\\OneDrive\\Desktop\\PerkUp\\{BB20.image}" + ".xml"
            root_elem = ET.Element("annotations")
            for bbox in self.bboxes:
                bbox_elem = ET.SubElement(root_elem, "bbox")
                ET.SubElement(bbox_elem, "x1").text = str(bbox[0])
                ET.SubElement(bbox_elem, "y1").text = str(bbox[1])
                ET.SubElement(bbox_elem, "x2").text = str(bbox[2])
                ET.SubElement(bbox_elem, "y2").text = str(bbox[3])
                ET.SubElement(bbox_elem, "color").text = bbox[4]
                ET.SubElement(bbox_elem, "id_type").text = bbox[5]
                ET.SubElement(bbox_elem, "id_number").text = bbox[6]
            tree = ET.ElementTree(root_elem)
            tree.write(annotation_path)
            print("Annotations saved to:", annotation_path)
        else:
            print("No annotations to save.")

        self.bboxes = []


    def set_question_id_color(self, selected_value):
      self.color_var.set("Red")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_diagram_id_color(self, selected_value):
      self.color_var.set("Yellow")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_mathematical_id_color(self, selected_value):
      self.color_var.set("Purple")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_matching_id_color(self, selected_value):
      self.color_var.set("Orange")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_answer_id_color(self, selected_value):
      self.color_var.set("Green")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_option_a_color(self, selected_value):
      self.color_var.set("SkyBlue")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_option_b_color(self, selected_value):
      self.color_var.set("Indigo")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_option_c_color(self, selected_value):
      self.color_var.set("Pink")
      if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()

    def set_option_d_color(self, selected_value):
     self.color_var.set("Seagreen")
     if self.current_bbox:
        self.current_bbox[4] = self.color_var.get()
        
    def update_option_menu_label(self, button_name, selected_value):
        if button_name in self.option_menus:
            option_menu = self.option_menus[button_name]
            option_menu.configure(text=button_name)  # Restore the original button name

if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxAnnotator(root)
    root.mainloop()