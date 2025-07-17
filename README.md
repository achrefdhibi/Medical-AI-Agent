# 🧠 Medical AI Agent – Powered by LangGraph & LangChain

Ce projet présente un **agent d’intelligence artificielle spécialisé dans le domaine médical**, conçu avec **LangGraph** et **LangChain**.  
Il est capable de dialoguer intelligemment avec les utilisateurs, de comprendre leurs besoins en matière de santé, et de leur fournir des réponses précises, fiables et contextualisées.

## 🚀 Fonctionnalités clés

-  Compréhension du langage naturel (NLP) pour analyser les demandes médicales.
- 🤖 Architecture intelligente de type **ReAct Agent**.
- Intégration d’outils médicaux et de bases de connaissances fiables.
- 💬 Interaction dynamique et contextualisée avec les utilisateurs.
- 🧠 Système de mémoire conversationnelle pour un meilleur suivi personnalisé.

## Objectifs du projet

Ce projet vise à démontrer comment les **agents IA** peuvent être utilisés dans le **secteur médical** pour assister les utilisateurs, améliorer la précision des informations fournies, et offrir un service plus intelligent, accessible et réactif.

## Technologies utilisées

- [LangGraph](https://www.langgraph.dev/)
- [LangChain](https://www.langchain.com/)
- Python 🐍
- LLM 

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


