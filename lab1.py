def researcher(task):
	return f"Résultats bruts sur {task}"


def writer(data):
	return f"Résumé: {data}"


def reviewer(text):
	return f"Amélioration: {text}"


def run_collaboration(task):
	raw_data = researcher(task)
	summary = writer(raw_data)
	improved_text = reviewer(summary)
	return raw_data, summary, improved_text


if __name__ == "__main__":
	task = "les tendances de l'IA en 2026"
	raw_data, summary, improved_text = run_collaboration(task)

	print("=== Collaboration entre agents ===")
	print(f"Chercheur  -> {raw_data}")
	print(f"Rédacteur  -> {summary}")
	print(f"Relecteur  -> {improved_text}")
