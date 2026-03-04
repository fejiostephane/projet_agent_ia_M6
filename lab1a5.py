"""
Projet : Spécialisation d'agents + Manager/Worker + Mémoire partagée + Mini CrewAI + Consensus

Exécution :
python projet_agents.py
"""

from dataclasses import dataclass
from typing import Callable, List, Dict, Any


# =========================
# LABO 1 — Spécialisation d’agents
# Objectif : 3 agents avec rôles distincts, fonctions simples, chainage séquentiel.
# =========================

def researcher(task: str) -> str:
    """Agent Chercheur : collecte des données (ici simulées)."""
    return f"Résultats bruts sur {task} : (1) point A (2) point B (3) point C"

def writer(data: str) -> str:
    """Agent Rédacteur : synthétise les données."""
    return f"Résumé: {data} -> Synthèse: A, B, C (version courte et claire)"

def reviewer(text: str) -> str:
    """Agent Relecteur : critique clarté, propose amélioration."""
    return f"Amélioration: {text} -> Suggestion: phrases plus courtes + structure en puces"


def labo1_demo() -> None:
    print("\n" + "="*60)
    print("LABO 1 — Spécialisation d’agents")
    print("="*60)

    task = "les tendances IA 2025"
    raw = researcher(task)
    summary = writer(raw)
    feedback = reviewer(summary)

    print("Tâche:", task)
    print("1) Chercheur ->", raw)
    print("2) Rédacteur ->", summary)
    print("3) Relecteur ->", feedback)

    print("\nLivrable (sortie illustrant la collaboration) : OK")


# =========================
# LABO 2 — Architecture Manager-Worker
# Objectif : un Manager délègue à plusieurs Workers, log mission + résultats.
# =========================

class Manager:
    def __init__(self, workers: List[Callable[[str], str]]):
        self.workers = workers

    def run(self, mission: str) -> None:
        print(f"Mission : {mission}")
        for w in self.workers:
            result = w(mission)
            print("→", result)


def labo2_demo() -> None:
    print("\n" + "="*60)
    print("LABO 2 — Architecture Manager-Worker")
    print("="*60)

    manager = Manager([researcher, writer, reviewer])
    manager.run("les tendances IA 2025")

    print("\nLivrable (log délégation + agrégation) : OK")


# =========================
# LABO 3 — Communication et mémoire partagée
# Objectif : dictionnaire shared_memory, chaque agent lit/écrit dedans.
# =========================

def labo3_demo() -> None:
    print("\n" + "="*60)
    print("LABO 3 — Communication et mémoire partagée")
    print("="*60)

    shared_memory: Dict[str, Any] = {}

    # Les agents écrivent dans la mémoire partagée
    shared_memory["data"] = researcher("énergie verte")
    shared_memory["summary"] = writer(shared_memory["data"])
    shared_memory["feedback"] = reviewer(shared_memory["summary"])

    print("Contenu final de shared_memory :")
    for k, v in shared_memory.items():
        print(f"- {k}: {v}")

    print("\nExplication:")
    print("- 'data' contient la collecte brute du chercheur.")
    print("- 'summary' réutilise 'data' pour produire un résumé.")
    print("- 'feedback' réutilise 'summary' pour proposer des améliorations.")
    print("=> Tout le monde travaille sur le même 'état' partagé.")


# =========================
# LABO 4 — Mini CrewAI : équipe collaborative
# Objectif : utiliser CrewAI (si dispo) avec 3 agents.
# =========================

def labo4_demo() -> None:
    print("\n" + "="*60)
    print("LABO 4 — Mini CrewAI : équipe collaborative")
    print("="*60)

    try:
        from crewai import Agent, Crew  # type: ignore
    except Exception:
        print("CrewAI n'est pas installé (ou import impossible).")
        print("Installe-le avec: pip install crewai")
        print("Livrable : tu peux faire une capture d’écran après installation.")
        return

    researcher_agent = Agent(role="Researcher", goal="Collecter des infos IA 2025")
    writer_agent = Agent(role="Writer", goal="Rédiger un résumé")
    reviewer_agent = Agent(role="Reviewer", goal="Relire et corriger")

    crew = Crew(agents=[researcher_agent, writer_agent, reviewer_agent])

    # Selon versions, kickoff peut varier (prompt/mission).
    # On le tente simplement :
    result = crew.kickoff("Créer un rapport sur les tendances IA 2025")

    print("Résultat CrewAI :")
    print(result)
    print("\nLivrable : capture d’écran du résultat / dialogue")


# =========================
# LABO 5 — Consensus et résolution de conflits
# Objectif : plusieurs réponses, 3 méthodes (vote, juge, score).
# Livrable : tableau comparatif + mini-analyse.
# =========================

@dataclass
class ScoredResponse:
    text: str
    score: float


def majority_vote(responses: List[str]) -> str:
    """Vote majoritaire : prend la réponse la plus fréquente."""
    return max(set(responses), key=responses.count)

def judge_choice(responses: List[str]) -> str:
    """
    Agent arbitre (simulé) : choisit selon une règle simple.
    Ici: la réponse la plus longue (souvent plus détaillée).
    """
    return sorted(responses, key=len, reverse=True)[0]

def confidence_score_pick(responses: List[ScoredResponse]) -> ScoredResponse:
    """Score de confiance : prend le score max."""
    return sorted(responses, key=lambda r: r.score, reverse=True)[0]


def labo5_demo() -> None:
    print("\n" + "="*60)
    print("LABO 5 — Consensus et résolution de conflits")
    print("="*60)

    # 1) Générer plusieurs réponses d’agents (simulé)
    responses_text = [
        "Tendance IA 2025: agents autonomes + copilots partout.",
        "Tendance IA 2025: agents autonomes + copilots partout.",  # volontairement identique
        "Tendance IA 2025: efficacité énergétique + IA embarquée + régulation renforcée.",
    ]

    # 2) Trois méthodes
    final_vote = majority_vote(responses_text)
    final_judge = judge_choice(responses_text)

    scored = [
        ScoredResponse(text=responses_text[0], score=0.72),
        ScoredResponse(text=responses_text[1], score=0.68),
        ScoredResponse(text=responses_text[2], score=0.91),
    ]
    final_scored = confidence_score_pick(scored)

    # 3) Comparer (tableau simple)
    print("\nTableau comparatif des stratégies :")
    rows = [
        ("Vote majoritaire", final_vote, "Choisit la réponse la plus répétée"),
        ("Agent arbitre", final_judge, "Choisit la réponse 'meilleure' selon un critère"),
        ("Score confiance", final_scored.text, f"Choisit le score max ({final_scored.score})"),
    ]

    # Affichage "table" basique
    print("-"*110)
    print(f"{'Méthode':<18} | {'Résultat final':<65} | {'Principe'}")
    print("-"*110)
    for m, r, p in rows:
        print(f"{m:<18} | {r:<65} | {p}")
    print("-"*110)

    print("\nMini-analyse :")
    print("- Vote majoritaire : simple, mais peut ignorer une réponse plus pertinente si elle est minoritaire.")
    print("- Agent arbitre : plus 'intelligent' si le critère est bon, mais dépend fortement des règles.")
    print("- Score confiance : utile si les scores sont fiables, sinon ça peut tromper.")


# =========================
# MAIN : exécuter tous les labos
# =========================

def main():
    labo1_demo()
    labo2_demo()
    labo3_demo()
    labo4_demo()
    labo5_demo()

if __name__ == "__main__":
    main()