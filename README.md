
# 🤖 AI Agent using LangGraph & LangChain

Ce projet est un **AI Agent intelligent** construit avec [LangGraph](https://github.com/langchain-ai/langgraph) et [LangChain](https://github.com/langchain-ai/langchain), conçu pour interagir dynamiquement avec les utilisateurs en utilisant des outils puissants et une architecture de type agent.

---


---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/nom-du-repo.git
cd nom-du-repo
````

### 2. Créer un environnement virtuel 

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration de l'API Key

Tu dois créer un fichier `.env` à la racine du projet et y ajouter ta clé API Groq :

```
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Remplace `sk-xxxxxxxx...` par ta clé réelle.

---

## 🚀 Lancer le projet

Pour exécuter le projet, lance simplement :

```bash
python main.py
```

L'agent sera alors prêt à répondre, utiliser des outils et exécuter les instructions dynamiquement à travers LangGraph.

---

## 🛠️ Technologies utilisées

* **LangGraph** : Orchestration des agents AI avec des graphes d’état
* **LangChain** : Intégration avec LLMs, outils et chaînes
* **Python 3.10+**
* **Groq API** (ou tout autre LLM compatible)


