import pytesseract
from PIL import ImageGrab
import keyboard
import pyautogui
import time
import os
import tkinter as tk
from tkinter import Canvas

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class SnippetTool:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot = None

    def create_overlay(self):
        """Cria uma janela transparente com overlay opaco"""
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.2)  # Opacidade do overlay
        self.root.attributes('-topmost', True) 
        
        # Cria canvas para desenhar a área transparente
        self.canvas = Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Captura screenshot para mostrar por baixo do overlay
        self.screenshot = pyautogui.screenshot()
        self.screenshot.save('temp_screen.png')
        
        # Bind de eventos do mouse
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        self.root.mainloop()

    def on_press(self, event):
        """Quando o usuário clica para iniciar a seleção"""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 
            self.start_x, self.start_y,
            outline='white', 
            width=2,
            )

    def on_drag(self, event):
        """Atualiza o retângulo de seleção enquanto o mouse se move"""
        if self.rect:
            self.canvas.coords(
                self.rect, 
                self.start_x, self.start_y, 
                event.x, event.y)

    def on_release(self, event):
        """Quando o usuário solta o mouse para finalizar a seleção"""
        end_x, end_y = event.x, event.y
        
        # Garante coordenadas corretas independente da direção do arraste
        x1, x2 = sorted([self.start_x, end_x])
        y1, y2 = sorted([self.start_y, end_y])
        
        # Fecha o overlay
        self.root.destroy()
        
        # Captura a região selecionada (convertendo coordenadas da tela)
        screen_shot = ImageGrab.grab(bbox=(
            x1, y1, x2, y2))
        
        # Realiza OCR
        self.perform_ocr(screen_shot)

    def perform_ocr(self, image):
        """Executa OCR na imagem capturada"""
        text = pytesseract.image_to_string(image, lang='por')
        
        # Exibe resultado
        print("\nTexto extraído:")
        print(text)
        
        # Copia para área de transferência
        try:
            import pyperclip
            pyperclip.copy(text)
            print("\nTexto copiado para a área de transferência!")
        except:
            pass
        
        # Remove arquivo temporário
        if os.path.exists('temp_screen.png'):
            os.remove('temp_screen.png')

def main():
    print("Pressione Ctrl+Shift+S para capturar um snippet")
    
    while True:
        if keyboard.is_pressed('ctrl+shift+s'):
            tool = SnippetTool()
            tool.create_overlay()
            time.sleep(1)  # Evita múltiplas ativações
        time.sleep(0.1)

if __name__ == "__main__":
    main()