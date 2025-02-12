import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar
import re
import time

# Chatbot Patterns
patterns = [
    (r"Where is the library\?", "The library is located on the semi-floor. You can find it on the left of the stairs.", ["what is located on the semi-floor", "library location", "location of the library"]),
    (r"What are the opening hours of the library\?", "From Monday to Friday: 08.00 AM - 20.00 PM and on Saturday: 09.00 AM - 15.00 PM", ["opening hours of the library", "library timetable", "library opening hours"]),
    (r"What are the opening hours of the university\?", "From Monday to Friday: 08.00 M - 22.00 PM and on Saturday: 09.00 AM - 18.00 PM", ["opening hours of the university", "university opening hours"]),
    (r"Where is University of Macedonia located\?", "Egnatia 156, Thessaloniki", ["location of the university", "address", "name of the street", "where is the university"]),
    (r"Can I study abroad during my time at the university\?", "Yes, the university offers study abroad programs and exchange opportunities for students who wish to explore different cultures and academic experiences. You can learn more about study abroad options through our international programs office.", ["study abroad", "abroad", "international", "ability to study abroad", "erasmus"]),
    (r"What transportation options are available for students\?", "Students can use public transportation such as buses.", ["transportation", "bus", "public"]),
    (r"What support services are available for students with disabilities\?", "The university provides support services for students with disabilities, including accommodations, assistive technology, and accessibility resources.", ["disabilities", "support services", "accommodations"]),
    (r"Is there a health center on campus\?", "Yes, the university has a health center on campus staffed with healthcare professionals. It provides medical services, counseling, and wellness programs to support student health and well-being.", ["health center", "medical", "wellness"]),
    (r"What extracurricular activities are available for students\?", "The university offers a wide range of extracurricular activities, including clubs, sports teams, volunteer opportunities, and cultural events. You can explore these options through our student organizations.", ["extracurricular activities", "clubs", "sports"]),
    (r"Where is the University restaurant\?", "The restaurant is located on the base floor. You can find it on the left of the central entrance.", ["restaurant", "dining", "food", "location of the restaurant"])
]

greetings_patterns = [
    (r"hello|hi|hey", "Hello! How can I assist you today?"),
    (r"goodbye|bye", "Goodbye! Have a great day!"),
]

compiled_patterns = [(re.compile(pattern, re.IGNORECASE), response, [kw.lower() for kw in flexible_keywords]) for pattern, response, flexible_keywords in patterns]
compiled_greetings = [(re.compile(pattern, re.IGNORECASE), response) for pattern, response in greetings_patterns]

def get_response(question):
    matched_pattern = None
    for pattern, response, keywords in compiled_patterns:
        if pattern.match(question):
            matched_pattern = (pattern, response)
            break
        for keyword in keywords:
            if keyword in question.lower():
                matched_pattern = (pattern, response)
                break
    if matched_pattern:
        pattern, response = matched_pattern
        return response
    else:
        for pattern, response in compiled_greetings:
            if pattern.match(question):
                return response
        return "I'm sorry, I don't understand that. Can you rephrase that please?"

def send_message():
    question = input_box.get("1.0", 'end-1c').strip()
    if question:
        add_message(question, "user")
        response = get_response(question)
        root.after(500, lambda: add_message(response, "bot"))  # Delay for a natural typing feel
    input_box.delete("1.0", tk.END)

def add_message(message, sender):
    bubble_frame = tk.Frame(chat_canvas, bg="#ffffff", padx=10, pady=5)
    if sender == "user":
        bubble_label = tk.Label(bubble_frame, text=message, bg="#0078d7", fg="#ffffff", font=("Arial", 12), wraplength=400, justify="left", padx=10, pady=5)
        bubble_frame.pack(anchor="e", padx=10, pady=5)
    else:
        bubble_label = tk.Label(bubble_frame, text=message, bg="#eeeeee", fg="#333333", font=("Arial", 12), wraplength=400, justify="left", padx=10, pady=5)
        bubble_frame.pack(anchor="w", padx=10, pady=5)
    
    bubble_label.pack()
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)  # Scroll to the bottom

# Main Application Window
root = tk.Tk()
root.title("UoM ChatBot")
root.geometry("500x700")
root.configure(bg="#f2f2f2")

# Chat Display Area with Scrollable Canvas
chat_frame = Frame(root, bg="#f2f2f2")
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_canvas = Canvas(chat_frame, bg="#f2f2f2", highlightthickness=0)
chat_scroll = Scrollbar(chat_frame, orient=tk.VERTICAL, command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=chat_scroll.set)

scrollable_frame = Frame(chat_canvas, bg="#f2f2f2")
scrollable_window = chat_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def configure_scrollable_frame(event):
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollable_frame)
chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Input Frame
input_frame = tk.Frame(root, bg="#ffffff", height=50)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Text Box for Input
input_box = tk.Text(input_frame, height=2, font=("Arial", 12), bg="#ffffff", fg="#333333", relief="flat", highlightthickness=1, highlightbackground="#cccccc", padx=10, pady=5)
input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Send Button
send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#0078d7", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat", padx=20)
send_button.pack(side=tk.RIGHT)

# Add Welcome Message
add_message("Hello! How can I assist you today?", "bot")

root.mainloop()
