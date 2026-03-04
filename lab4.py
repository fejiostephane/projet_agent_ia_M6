import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def build_crew(topic: str) -> Crew:
	researcher = Agent(
		role="Researcher",
		goal=f"Collecter des infos fiables sur {topic}",
		backstory="Analyste qui identifie tendances, opportunités et risques.",
		verbose=True,
	)

	writer = Agent(
		role="Writer",
		goal="Rédiger un résumé clair, structuré et actionnable",
		backstory="Rédacteur qui transforme des données brutes en rapport lisible.",
		verbose=True,
	)

	reviewer = Agent(
		role="Reviewer",
		goal="Relire, corriger et améliorer la clarté du rapport",
		backstory="Relecteur exigeant sur la précision et la cohérence.",
		verbose=True,
	)

	research_task = Task(
		description=(
			f"Rechercher 5 tendances majeures sur {topic}, avec pour chacune "
			"une opportunité et un risque."
		),
		expected_output="Liste structurée des tendances avec opportunité et risque.",
		agent=researcher,
	)

	writing_task = Task(
		description=(
			"Produire un rapport synthétique (10-15 lignes) basé sur la recherche, "
			"avec sections: Tendances, Opportunités, Risques, Recommandations."
		),
		expected_output="Rapport clair et structuré.",
		agent=writer,
	)

	review_task = Task(
		description=(
			"Relire le rapport final, corriger les ambiguïtés, "
			"et proposer 3 améliorations concrètes."
		),
		expected_output="Version relue + 3 recommandations d'amélioration.",
		agent=reviewer,
	)

	crew = Crew(
		agents=[researcher, writer, reviewer],
		tasks=[research_task, writing_task, review_task],
		process=Process.sequential,
		verbose=True,
	)
	return crew


def run_lab(topic: str = "les tendances IA 2025"):
	if not os.getenv("OPENAI_API_KEY"):
		print("Aucune clé OPENAI_API_KEY détectée.")
		print("Pour lancer CrewAI avec un vrai LLM, exécute:")
		print("  $env:OPENAI_API_KEY='ta_cle'")
		print("Puis relance: python .\\lab4.py")
		print("\nMode démonstration (livrable texte):")
		print(f"- Researcher: collecte des infos sur {topic}")
		print("- Writer: rédige un résumé structuré")
		print("- Reviewer: corrige et propose des améliorations")
		return

	print(f"Mission: Créer un rapport sur {topic}")
	crew = build_crew(topic)
	result = crew.kickoff()

	print("\n=== Résultat final CrewAI ===")
	print(result)


if __name__ == "__main__":
	run_lab("les tendances IA 2025")
