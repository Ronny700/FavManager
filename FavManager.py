import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import json
import os
import pandas as pd

ARQUIVO = "filmes.json"
filmes = []

# ---------------- FUNÇÕES DE DADOS ----------------
def carregar_filmes():
    global filmes
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                filmes = json.load(f)
                for filme in filmes:
                    if "nota" not in filme:
                        filme["nota"] = "—"
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Arquivo de dados corrompido. Começando com lista vazia.")
            filmes = []
    else:
        filmes = []

def salvar_filmes():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(filmes, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar os dados: {e}")

def atualizar_lista(filtro=""):
    for item in lista_filmes.get_children():
        lista_filmes.delete(item)
    for i, filme in enumerate(filmes):
        titulo = filme.get("titulo", "")
        opiniao = filme.get("opiniao", "")
        nota = filme.get("nota", "—")
        if filtro.lower() in titulo.lower():
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            lista_filmes.insert("", "end", iid=i, values=(titulo, opiniao, nota), tags=(tag,))

# ---------------- CRUD ----------------
def adicionar_filme():
    titulo = entry_titulo.get().strip()
    opiniao = entry_opiniao.get().strip()
    nota = entry_nota.get().strip()

    if nota and not nota.isdigit():
        messagebox.showwarning("Atenção", "A nota deve ser um número.")
        return

    if titulo:
        filmes.append({"titulo": titulo, "opiniao": opiniao, "nota": nota if nota else "—"})
        salvar_filmes()
        atualizar_lista()
        entry_titulo.delete(0, "end")
        entry_opiniao.delete(0, "end")
        entry_nota.delete(0, "end")
    else:
        messagebox.showwarning("Atenção", "O título do filme não pode estar vazio.")

def remover_filme():
    selecionado = lista_filmes.selection()
    if selecionado:
        indice = int(selecionado[0])
        filme = filmes.pop(indice)
        salvar_filmes()
        atualizar_lista()
        messagebox.showinfo("Removido", f"Filme '{filme['titulo']}' removido com sucesso.")
    else:
        messagebox.showwarning("Atenção", "Selecione um filme para remover.")

def editar_filme():
    selecionado = lista_filmes.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um filme para editar.")
        return

    indice = int(selecionado[0])
    filme = filmes[indice]

    # Janela de edição
    edit_win = ctk.CTkToplevel()
    edit_win.title("Editar Filme")
    edit_win.geometry("350x200")
    edit_win.resizable(False, False)
    edit_win.grab_set()

    ctk.CTkLabel(edit_win, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_novo_titulo = ctk.CTkEntry(edit_win, width=250, font=("Helvetica", 12))
    entry_novo_titulo.grid(row=0, column=1, padx=5, pady=5)
    entry_novo_titulo.insert(0, filme["titulo"])

    ctk.CTkLabel(edit_win, text="Opinião:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_nova_opiniao = ctk.CTkEntry(edit_win, width=250, font=("Helvetica", 12))
    entry_nova_opiniao.grid(row=1, column=1, padx=5, pady=5)
    entry_nova_opiniao.insert(0, filme["opiniao"])

    ctk.CTkLabel(edit_win, text="Nota:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_nova_nota = ctk.CTkEntry(edit_win, width=100, font=("Helvetica", 12))
    entry_nova_nota.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    entry_nova_nota.insert(0, filme["nota"])

    def salvar_edicao():
        novo_titulo = entry_novo_titulo.get().strip()
        nova_opiniao = entry_nova_opiniao.get().strip()
        nova_nota = entry_nova_nota.get().strip()

        if not novo_titulo:
            messagebox.showwarning("Atenção", "O título não pode ficar vazio.")
            return

        filmes[indice]["titulo"] = novo_titulo
        filmes[indice]["opiniao"] = nova_opiniao
        filmes[indice]["nota"] = nova_nota

        salvar_filmes()
        atualizar_lista()
        edit_win.destroy()

    ctk.CTkButton(edit_win, text="OK", width=80, command=salvar_edicao).grid(row=3, column=0, pady=15)
    ctk.CTkButton(edit_win, text="Cancelar", width=80, command=edit_win.destroy).grid(row=3, column=1, pady=15)

def buscar_filmes():
    termo = entry_busca.get().strip()
    atualizar_lista(termo)

# ---------------- EXPORTAR / IMPORTAR ----------------
def exportar_csv():
    if not filmes:
        messagebox.showwarning("Atenção", "Não há filmes para exportar.")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if caminho:
        df = pd.DataFrame(filmes)
        df.to_csv(caminho, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Sucesso", f"Filmes exportados para {caminho}")

def exportar_excel():
    if not filmes:
        messagebox.showwarning("Atenção", "Não há filmes para exportar.")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
    if caminho:
        df = pd.DataFrame(filmes)
        df.to_excel(caminho, index=False)
        messagebox.showinfo("Sucesso", f"Filmes exportados para {caminho}")

def importar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("CSV/Excel", "*.csv *.xlsx")])
    if caminho:
        try:
            if caminho.endswith(".csv"):
                df = pd.read_csv(caminho)
            else:
                df = pd.read_excel(caminho)

            for _, row in df.iterrows():
                filmes.append({
                    "titulo": str(row.get("titulo", "")),
                    "opiniao": str(row.get("opiniao", "")),
                    "nota": str(row.get("nota", "—"))
                })

            salvar_filmes()
            atualizar_lista()
            messagebox.showinfo("Sucesso", f"Filmes importados de {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar arquivo:\n{e}")

# ---------------- INTERFACE ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("🎬 Meus Filmes Favoritos")
janela.geometry("820x625")
janela.resizable(False, False)

# Frame de entrada
frame_top = ctk.CTkFrame(janela)
frame_top.pack(fill="x", pady=10, padx=10)

ctk.CTkLabel(frame_top, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_titulo = ctk.CTkEntry(frame_top, width=300, font=("Helvetica", 12))
entry_titulo.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_top, text="Opinião:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_opiniao = ctk.CTkEntry(frame_top, width=300, font=("Helvetica", 12))
entry_opiniao.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_top, text="Nota (0-10):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_nota = ctk.CTkEntry(frame_top, width=100, font=("Helvetica", 12))
entry_nota.grid(row=2, column=1, padx=5, pady=5, sticky="w")

ctk.CTkButton(frame_top, text="➕ Adicionar Filme", command=adicionar_filme, font=("Helvetica",12), height=35).grid(row=3, column=0, columnspan=2, pady=10)

# Frame de busca
frame_busca = ctk.CTkFrame(janela)
frame_busca.pack(fill="x", pady=5, padx=10)

ctk.CTkLabel(frame_busca, text="🔎 Buscar:", font=("Helvetica",12)).pack(side="left", padx=5)
entry_busca = ctk.CTkEntry(frame_busca, width=200, font=("Helvetica",12))
entry_busca.pack(side="left", padx=5)
ctk.CTkButton(frame_busca, text="Buscar", width=80, command=buscar_filmes, font=("Helvetica",12), height=30).pack(side="left", padx=5)
ctk.CTkButton(frame_busca, text="Mostrar Todos", width=120, command=lambda: atualizar_lista(), font=("Helvetica",12), height=30).pack(side="left", padx=5)

# Frame de lista de filmes
frame_lista = ctk.CTkFrame(janela, fg_color="#1e1e1e")
frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

# Treeview
colunas = ("Título", "Opinião", "Nota")
lista_filmes = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=12)
for col in colunas:
    lista_filmes.heading(col, text=col)
    lista_filmes.column(col, width=200)
lista_filmes.pack(side="left", fill="both", expand=True)

# Estilo alternado nas linhas
lista_filmes.tag_configure('oddrow', background="#C5C6EB")
lista_filmes.tag_configure('evenrow', background="#9ed4ed")

# Scrollbar
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=lista_filmes.yview)
lista_filmes.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Frame de botões
frame_botoes = ctk.CTkFrame(janela, corner_radius=15)
frame_botoes.pack(fill="x", pady=10, padx=10)

btn_editar = ctk.CTkButton(frame_botoes, text="✏️ Editar", width=150, command=editar_filme, corner_radius=15, hover_color="#2a2a2a", font=("Helvetica",12), height=35)
btn_editar.pack(side="left", padx=5)

btn_remover = ctk.CTkButton(frame_botoes, text="🗑️ Remover", width=150, command=remover_filme, corner_radius=15, hover_color="#2a2a2a", font=("Helvetica",12), height=35)
btn_remover.pack(side="left", padx=5)

btn_exportar_csv = ctk.CTkButton(frame_botoes, text="⬇️ Exportar CSV", width=150, command=exportar_csv, corner_radius=15, hover_color="#2a2a2a", font=("Helvetica",12), height=35)
btn_exportar_csv.pack(side="left", padx=5)

btn_exportar_excel = ctk.CTkButton(frame_botoes, text="⬇️ Exportar Excel", width=150, command=exportar_excel, corner_radius=15, hover_color="#2a2a2a", font=("Helvetica",12), height=35)
btn_exportar_excel.pack(side="left", padx=5)

btn_importar = ctk.CTkButton(frame_botoes, text="⬆️ Importar Arquivo", width=150, command=importar_arquivo, corner_radius=15, hover_color="#2a2a2a", font=("Helvetica",12), height=35)
btn_importar.pack(side="left", padx=5)

# Inicializa
carregar_filmes()
atualizar_lista()
janela.mainloop()

