"""
Standalone demo — no database, no authentication required.
Shows the core AI capabilities of BurnoutSense.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Minimal settings mock to avoid importing Django
class MockSettings:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

import sys
sys.modules['django.conf'] = type(sys)('django.conf')
sys.modules['django.conf'].settings = MockSettings()

from services import (
    compute_burnout_score,
    chat_with_gemini,
    update_score_from_chat,
    determine_level,
    build_context_prefix,
)


def demo_questionnaire():
    print("\n" + "="*60)
    print("DEMO 1 — Burnout Score from Questionnaire")
    print("="*60)

    # Simulated questionnaire responses
    responses = {
        "Veuillez-indiquer votre niveau de stress": 8,
        "Veuillez-indiquer votre charge de travail": 9,
        "Vous sentez-vous isolez ?": "oui",
        "À quel point vous sentez-vous \"heureux(se)\" ?": "😟",
        "À quel point vous sentez-vous fatigué(e) ?": "😟",
        "À quel point vous sentez-vous déprimé(e) ?": "😕",
        "À quel point vous sentez-vous \"à bout\" ?": "😟",
        "Qu'est-ce qui vous cause le plus de stress au travail ?": 
            "Les réunions interminables et les deadlines impossibles",
    }

    result = compute_burnout_score(responses)
    level  = determine_level(result["score"])

    print(f"\nRisk Score : {result['score']}/100")
    print(f"Risk Level : {level or 'none'}")
    print(f"Signals detected:")
    for reason in result["raisons"]:
        print(f"  • {reason}")

    return result


def demo_chat(initial_result: dict):
    print("\n" + "="*60)
    print("DEMO 2 — Therapeutic Chat with Memory")
    print("="*60)

    history = []

    exchanges = [
        "Je suis complètement épuisé, je n'arrive plus à décrocher le soir.",
        "Mon manager ne nous écoute pas, j'ai l'impression que rien ne changera jamais.",
        "Je ne sais plus si j'ai encore envie de venir travailler.",
    ]

    for user_msg in exchanges:
        print(f"\n[Employee] {user_msg}")

        response = chat_with_gemini(history, user_msg)
        print(f"[PsychoBot] {response}")

        history.append({"role": "user",      "content": user_msg})
        history.append({"role": "assistant", "content": response})

    return history


def demo_score_update(history: list, initial_result: dict):
    print("\n" + "="*60)
    print("DEMO 3 — Score Refinement After Chat")
    print("="*60)

    updated = update_score_from_chat(
        history,
        initial_result["score"],
        initial_result["raisons"]
    )

    print(f"\nInitial score : {initial_result['score']}/100")
    print(f"Refined score : {updated['score']}/100")
    print(f"Updated signals:")
    for reason in updated["raisons"]:
        print(f"  • {reason}")


if __name__ == "__main__":
    print("BurnoutSense — Standalone AI Demo")
    print("Powered by Groq (Llama 3.3-70B)")

    initial = demo_questionnaire()
    history = demo_chat(initial)
    demo_score_update(history, initial)

    print("\n" + "="*60)
    print("Demo complete.")
    