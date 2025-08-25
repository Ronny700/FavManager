# FavManager
Aplicativo em Tkinter para gerenciar lista de filmes, com importação/exportação em Excel, CSV e JSON


# Gerenciador de Filmes Favoritos

Um aplicativo em Python com interface moderna feita em CustomTkinter, para cadastrar, editar, buscar e organizar seus filmes favoritos.  
Além disso, permite exportar e importar dados em diferentes formatos (JSON, CSV e Excel).



#  Funcionalidades

-  **Adicionar filmes** com título, opinião e nota
-  **Editar** dados de filmes já cadastrados
-  **Remover** filmes da lista
-  **Buscar** por título de forma rápida
-  **Salvar e carregar** dados automaticamente em JSON
-  **Exportar** lista para **CSV, Excel (.xlsx) e JSON**
-  **Importar** dados dessas extensões diretamente para o sistema



## 📤 Exportação e 📥 Importação

- Suporta **CSV, Excel (.xlsx) e JSON**
- Permite importar listas existentes nesses formatos
- Exporta os filmes cadastrados para esses formatos, facilitando backup e compartilhamento


## 📂 Exemplos

Na pasta `exemplos/` você encontra arquivos já exportados pelo sistema, como:

- `filmes_exemplo.json`
- `filmes_exemplo.csv`

Eles servem como referência de como ficam os dados gerados.


## 🛠️ Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pandas](https://pandas.pydata.org/)  
- Tkinter (nativo do Python)


##  Como Rodar o Projeto

1. Clone o repositório:
  
   git clone https://github.com/Ronny700/FavManager.git
   cd FavManager
   
Instale as dependências:
pip install customtkinter pandas openpyxl

Execute o programa:
python FavManager.py

Como usar

1. Abra o programa (FavManager.py).
2. Use os botões da interface para adicionar, editar ou Remover filmes.
3. Salve automaticamente em filmes.json.
4. Use o menu para Exportar ou Importar dados nos formatos suportados.
5. Aproveite sua lista organizada de filmes!


 ## Em Execução
 <img width="1011" height="796" alt="image" src="https://github.com/user-attachments/assets/45ff1e05-9aae-4116-ba81-4311c2126fa8" />

 

# Observações
O programa cria e mantém automaticamente um arquivo filmes.json para salvar seus dados localmente.
Os arquivos na pasta exemplos/ são apenas para demonstração.
# Licença
Este projeto é de uso livre para fins de estudo e aprendizado.
