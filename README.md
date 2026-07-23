# Psychobot AI: PsychoBot Core Engine

This repository contains the **standalone AI and Natural Language Processing engine** for *Zenwork*, a well-being application initially developed as a full-stack group project (React/Django/Supabase). 

To specifically showcase my contributions to the project, I have extracted the core AI logic I engineered and packaged it into an independent, lightweight Flask API and CLI environment. This eliminates database and frontend dependencies, allowing you to test the AI capabilities instantly.

## Purpose of this Repository
In the original group project, I was responsible for the AI integration, prompt engineering, and algorithmic risk assessment. This repository isolates that work to demonstrate:
* **LLM Orchestration:** Handling context windows, system prompts, and memory arrays.
* **JSON Enforcement:** Forcing the LLM to return strictly structured JSON for deterministic frontend parsing.
* **Dynamic Refinement:** Updating user states based on conversational context without storing identifiable personal data.

## AI Features

* ** Automated Burnout Scoring (`/analyze`):** Ingests raw questionnaire data (including emojis and free text), normalizes it, and queries the LLM to output a precise risk score (0-100) and structured, anonymized signals.
* ** Therapeutic Chat (`/chat`):** A customized conversational agent ("PsychoBot") with memory tracking. It uses empathy-driven system prompts to act as a supportive listener while secretly keeping track of the user's emotional state.
* ** Post-Chat Score Refinement (`/session/close`):** After a conversation ends, the AI analyzes the entire chat history to adjust the initial burnout score based on conversational cues (e.g., detecting hidden distress or reassuring signals).
* ** Resource Triggering:** Automatically analyzes recent chat history to detect urgent needs (e.g., sleep, stress management) and triggers appropriate internal resources or emergency redirects.

## Technology Stack

* **Language:** Python 3
* **Framework:** Flask (Lightweight API for demo purposes)
* **AI Provider:** Groq API
* **Model:** LLaMA 3.3 (70B Versatile) for ultra-fast, high-reasoning responses.
