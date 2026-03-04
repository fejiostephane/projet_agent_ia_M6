from collections import Counter


def generate_agent_responses():
	return [
		{
			"agent": "agent_research",
			"answer": "Adopter une approche hybride (LLM + RAG)",
			"score": 0.84,
			"rationale": "Bon équilibre entre coût, précision et mise à l'échelle.",
		},
		{
			"agent": "agent_writer",
			"answer": "Adopter une approche hybride (LLM + RAG)",
			"score": 0.79,
			"rationale": "Réponse la plus complète pour un rapport opérationnel.",
		},
		{
			"agent": "agent_reviewer",
			"answer": "Privilégier un LLM pur",
			"score": 0.67,
			"rationale": "Implémentation plus rapide à court terme.",
		},
		{
			"agent": "agent_finance",
			"answer": "Adopter une approche hybride (LLM + RAG)",
			"score": 0.91,
			"rationale": "Meilleur ratio qualité/coût sur 12 mois.",
		},
	]


def majority_vote(responses):
	answers = [r["answer"] for r in responses]
	final_answer = max(set(answers), key=answers.count)
	votes = Counter(answers)
	return {
		"strategy": "Vote majoritaire",
		"final": final_answer,
		"justification": f"{votes[final_answer]} votes sur {len(answers)}",
	}


def judge_arbitration(responses):
	prompt = f"Analyse ces réponses : {responses}. Choisis la meilleure."

	best = sorted(
		responses,
		key=lambda r: (r["score"], len(r["rationale"])),
		reverse=True,
	)[0]
	return {
		"strategy": "Agent arbitre",
		"final": best["answer"],
		"justification": (
			f"Choix arbitré sur confiance={best['score']:.2f} "
			f"et qualité d'argumentaire ({best['agent']})."
		),
		"judge_prompt": prompt,
	}


def confidence_score_selection(responses):
	weighted = sorted(responses, key=lambda r: r["score"], reverse=True)[0]
	return {
		"strategy": "Score de confiance",
		"final": weighted["answer"],
		"justification": (
			f"Score max retenu: {weighted['score']:.2f} "
			f"({weighted['agent']})."
		),
	}


def print_responses(responses):
	print("=== Réponses initiales des agents ===")
	for r in responses:
		print(f"- {r['agent']}: {r['answer']} | score={r['score']:.2f}")


def print_comparative_table(results):
	print("\n=== Tableau comparatif des stratégies ===")
	header = f"{'Stratégie':<22} | {'Résultat final':<40} | Justification"
	print(header)
	print("-" * len(header))
	for result in results:
		print(
			f"{result['strategy']:<22} | "
			f"{result['final']:<40} | "
			f"{result['justification']}"
		)


def print_mini_analysis(results):
	winners = [r["final"] for r in results]
	consensus = len(set(winners)) == 1

	print("\n=== Mini-analyse ===")
	if consensus:
		print("- Les 3 méthodes convergent vers la même décision.")
		print("- La décision est robuste car validée par popularité et confiance.")
	else:
		print("- Les méthodes divergent: le choix dépend de la gouvernance adoptée.")
		print("- Vote majoritaire favorise la popularité, score favorise la certitude.")
		print("- L'agent arbitre est utile pour trancher en contexte ambigu.")


if __name__ == "__main__":
	responses = generate_agent_responses()
	print_responses(responses)

	vote_result = majority_vote(responses)
	judge_result = judge_arbitration(responses)
	score_result = confidence_score_selection(responses)

	all_results = [vote_result, judge_result, score_result]
	print_comparative_table(all_results)
	print_mini_analysis(all_results)
