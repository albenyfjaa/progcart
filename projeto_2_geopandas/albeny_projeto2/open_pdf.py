import os
import webbrowser

class PDFOpener:
    def __init__(self, plugin_dir, nome_pdf="SirgasCon_info.pdf"):
        self.plugin_dir = plugin_dir
        self.nome_pdf = nome_pdf

    def abrir(self):
        caminho_pdf = os.path.join(self.plugin_dir, self.nome_pdf)
        if os.path.exists(caminho_pdf):
            webbrowser.open(f'file:///{caminho_pdf}')
        else:
            print(f"PDF file not found: {caminho_pdf}")