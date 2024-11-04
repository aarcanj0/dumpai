import customtkinter as ctk
from tkinter import messagebox
#powered by Llama 3 LLM https://github.com/Strvm/meta-ai-api
from meta_ai_api import MetaAI
import asyncio
import threading

ai = MetaAI()

async def get_response(user_input):
    response = await asyncio.to_thread(ai.prompt, user_input)
    return response['message']

def show_startup_message():
    messagebox.showinfo("Aviso", "Bem-vindo ao Meka AI - versão de desenvolvimento 0.1\n\nDeveloped by: aarcanj0\nPowered by Llama 3 LLM")

async def send_message_async(user_input):
    output_text.configure(state="normal")
    output_text.insert("end", f"MekaIA está pensando...\n")
    output_text.see("end")
    output_text.configure(state="disabled")
    sendButton.configure(state="disabled")
    mainEntry.configure(state="disabled")
    response = await get_response(user_input)
    output_text.configure(state="normal")
    output_text.insert("end", f"Você: {user_input}\n\n")
    output_text.insert("end", f"Meka AI: {response}\n")
    output_text.see("end")
    output_text.configure(state="disabled")
    sendButton.configure(state="normal")
    mainEntry.configure(state="normal")
    mainEntry.delete(0, "end")

def send_message(event=None):
    user_input = mainEntry.get().strip()
    if user_input:
        threading.Thread(target=lambda: asyncio.run(send_message_async(user_input))).start()
    else:
        messagebox.showwarning("Aviso", "A entrada do usuário não pode estar vazia.")

app = ctk.CTk()
app.geometry("900x550")
app.title("Meka AI - dev version 0.1")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

output_frame = ctk.CTkFrame(app)
output_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

output_text = ctk.CTkTextbox(output_frame, wrap="word")
output_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
output_text.configure(state="disabled")

input_frame = ctk.CTkFrame(app)
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=0)

mainEntry = ctk.CTkEntry(input_frame, placeholder_text='Como posso te ajudar?')
mainEntry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
mainEntry.bind("<Return>", send_message)

sendButton = ctk.CTkButton(input_frame, text='Enviar', command=send_message)
sendButton.grid(row=0, column=1, pady=5)

app.after(0, show_startup_message)
app.mainloop()

