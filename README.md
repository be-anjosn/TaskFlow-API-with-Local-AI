# TaskFlow API with Local AI

<p align="center">
  <b>[ <a href="#-português">Português</a> ] | [ <a href="#-english">English</a> ]</b>
</p>

---

## 🇧🇷 Português

### Sobre o Projeto
O **TaskFlow API** é um backend moderno construído com **FastAPI** e validado com **Pydantic**, projetado para gerenciar tarefas de forma inteligente. O diferencial desta aplicação é a integração com **Inteligência Artificial local (Ollama / Llama 3.2)**, capaz de processar descrições e e-mails em texto livre, extraindo automaticamente títulos estruturados, prioridades, status e prazos de vencimento (`due_date`), persistindo os dados de forma segura em arquivos CSV.

### Arquitetura do Projeto
O projeto segue uma arquitetura modular limpa e organizada por responsabilidades:

```text
taskflow-api/
├── app/
│   ├── __init__.py
│   ├── main.py        # Ponto de entrada e configuração do Uvicorn
│   ├── routes.py      # Definição e agrupamento de endpoints (APIRouter)
│   ├── schemas.py     # Modelos de validação e tipagem com Pydantic
│   └── services.py    # Lógica de negócio, integração com IA e persistência CSV
├── data/
│   ├── input_tasks.csv    # Log bruto de entradas de texto para serem usadas como exemplo
│   └── output_feedback.csv  # Base estruturada final das tarefas
├── requirements.txt
└── README.md
```

### Endpoints Disponíveis

| Método | Endpoint | Objetivo |
| :--- | :--- | :--- |
| **GET** | `/tasks` | Lista todas as tarefas (suporta filtros por `status` e `priority`) |
| **GET** | `/tasks/{task_id}` | Consulta uma tarefa específica pelo ID |
| **GET** | `/tasks/overdue` | Consulta todas as tarefas vencidas e pendentes |
| **GET** | `/tasks/summary` | Retorna um resumo estatístico agrupado por status e prioridade |
| **GET** | `/health` | Simulação de verificação de saúde e disponibilidade da API (`/health`) |
| **PUT** | `/tasks/{task_id}` | Substitui/atualiza todos os dados editáveis de uma tarefa |
| **POST** | `/tasks` | Cria uma nova tarefa processando texto livre via IA |
| **PATCH** | `/tasks/{task_id}/status` | Atualiza pontualmente o status de uma tarefa |
| **PATCH** | `/tasks/{task_id}/complete` | Marca uma tarefa diretamente como concluída (`completed`) |
| **DELETE** | `/tasks/{task_id}` | Exclui uma tarefa do sistema por ID |


### Instalação e Execução

1. **Clone o repositório e acesse a pasta raiz:**
   ```bash
   cd Project-2
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Certifique-se de que o Ollama está rodando localmente** com o modelo configurado (`llama3.2:1b`).

5. **Execute a aplicação a partir da pasta `app`:**
   ```bash
   cd app
   python main.py
   ```
   *A API estará acessível em `http://localhost:8000`. A documentação interativa automática (Swagger UI) pode ser consultada em `http://localhost:8000/docs`.*

---

---

## 🇺🇸 English

### About the Project
The **TaskFlow API** is a modern backend built with **FastAPI** and validated with **Pydantic**, designed to manage tasks intelligently. The distinguishing feature of this application is its integration with **Local Artificial Intelligence (Ollama / Llama 3.2)**, capable of processing free-text descriptions and emails, automatically extracting structured titles, priorities, statuses, and due dates (`due_date`), while securely persisting the data in CSV files.

### Project Architecture
The project follows a clean, modular architecture organized by responsibilities:

```text
taskflow-api/
├── app/
│   ├── __init__.py
│   ├── main.py        # Entry point and Uvicorn configuration
│   ├── routes.py      # Endpoint definitions and grouping (APIRouter)
│   ├── schemas.py     # Pydantic validation models and typing
│   └── services.py    # Business logic, AI integration, and CSV persistence
├── data/
│   ├── input_tasks.csv    # Raw log of text inputs to be used as examples
│   └── output_feedback.csv  # Final structured database of tasks
├── requirements.txt
└── README.md
```

### Available Endpoints

| Method | Endpoint | Objective |
| :--- | :--- | :--- |
| **GET** | `/tasks` | Lists all tasks (supports filtering by `status` and `priority`) |
| **GET** | `/tasks/{task_id}` | Retrieves a specific task by ID |
| **GET** | `/tasks/overdue` | Retrieves all overdue and pending tasks |
| **GET** | `/tasks/summary` | Returns a statistical summary grouped by status and priority |
| **GET** | `/health` | Simulation of health check and API availability (`/health`) |
| **PUT** | `/tasks/{task_id}` | Replaces/updates all editable data of a task |
| **POST** | `/tasks` | Creates a new task by processing free text via AI |
| **PATCH** | `/tasks/{task_id}/status` | Updates a task's status punctually |
| **PATCH** | `/tasks/{task_id}/complete` | Directly marks a task as completed (`completed`) |
| **DELETE** | `/tasks/{task_id}` | Deletes a task from the system by ID |


### Installation and Execution

1. **Clone the repository and navigate to the root folder:**

   ```bash
   cd Project-2
   ```


2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/macOS:
   source .venv/bin/activate
   ```
   

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt


4. **Make sure Ollama is running locally** with the configured model (`llama3.2:1b`).

5. **Run the application from the `app` folder:**
   ```bash
   cd app
   python main.py

 
   *The API will be accessible at `http://localhost:8000`. The automatic interactive documentation (Swagger UI) can be accessed at `http://localhost:8000/docs`.*
