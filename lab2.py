from typing import TypedDict

from langgraph.graph import END, START, StateGraph


TREND_DATA = [
	{
		"trend": "Copilotes IA métiers",
		"adoption": "élevée",
		"impact": 9,
		"risk": "dépendance fournisseur",
	},
	{
		"trend": "Agents autonomes multi-étapes",
		"adoption": "moyenne",
		"impact": 8,
		"risk": "hallucinations et supervision",
	},
	{
		"trend": "IA embarquée sur device (edge)",
		"adoption": "moyenne",
		"impact": 7,
		"risk": "capacité matérielle limitée",
	},
	{
		"trend": "Gouvernance IA et conformité",
		"adoption": "élevée",
		"impact": 8,
		"risk": "coût de mise en conformité",
	},
]


class WorkflowState(TypedDict):
	mission: str
	researcher: dict
	writer: dict
	reviewer: dict
	aggregated: dict
	delegation_log: list[str]


def manager_node(state: WorkflowState):
	mission = state["mission"]
	print(f"Mission : {mission}")
	log = state.get("delegation_log", []) + [
		"manager -> délègue à researcher",
		"manager -> délègue à writer",
		"manager -> délègue à reviewer",
	]
	return {"delegation_log": log}


def researcher_node(state: WorkflowState):
	mission = state["mission"]
	ranked = sorted(TREND_DATA, key=lambda item: item["impact"], reverse=True)
	top_trends = ranked[:3]
	result = {
		"mission": mission,
		"top_trends": top_trends,
		"insight": "Les usages à ROI court terme restent les plus adoptés.",
		"sources_count": 4,
	}
	print("→ researcher terminé")
	return {"researcher": result}


def writer_node(state: WorkflowState):
	research = state["researcher"]
	trend_lines = []
	for item in research["top_trends"]:
		trend_lines.append(
			f"- {item['trend']} (impact={item['impact']}, adoption={item['adoption']})"
		)

	draft = (
		f"Mission: {research['mission']}\n"
		"Tendances prioritaires:\n"
		+ "\n".join(trend_lines)
		+ "\nSynthèse: "
		+ research["insight"]
	)
	result = {
		"draft": draft,
		"angle": "business + risques",
		"target_audience": "direction produit",
	}
	print("→ writer terminé")
	return {"writer": result}


def reviewer_node(state: WorkflowState):
	text = state["writer"]["draft"]
	contains_risk = "risque" in text.lower() or "risk" in text.lower()
	recommendations = []

	if not contains_risk:
		recommendations.append("Ajouter explicitement une section risques par tendance.")
	recommendations.append("Conclure avec 2 priorités actionnables à 90 jours.")

	clarity_score = 8 if contains_risk else 6
	result = {
		"clarity_score": clarity_score,
		"recommendations": recommendations,
		"final_note": "Texte clair, améliorer la partie exécution.",
	}
	print("→ reviewer terminé")
	return {"reviewer": result}


def aggregate_node(state: WorkflowState):
	aggregated = {
		"mission": state["mission"],
		"trends_selected": [
			trend["trend"] for trend in state["researcher"]["top_trends"]
		],
		"draft_length": len(state["writer"]["draft"]),
		"clarity_score": state["reviewer"]["clarity_score"],
		"next_actions": state["reviewer"]["recommendations"],
	}
	return {"aggregated": aggregated}


def build_workflow():
	graph = StateGraph(WorkflowState)
	graph.add_node("manager", manager_node)
	graph.add_node("researcher", researcher_node)
	graph.add_node("writer", writer_node)
	graph.add_node("reviewer", reviewer_node)
	graph.add_node("aggregate", aggregate_node)

	graph.add_edge(START, "manager")
	graph.add_edge("manager", "researcher")
	graph.add_edge("researcher", "writer")
	graph.add_edge("writer", "reviewer")
	graph.add_edge("reviewer", "aggregate")
	graph.add_edge("aggregate", END)

	return graph.compile()


class Manager:
	def __init__(self):
		self.workflow = build_workflow()

	def run(self, mission):
		final_state = self.workflow.invoke({"mission": mission, "delegation_log": []})

		print("\n=== Log de délégation ===")
		for line in final_state["delegation_log"]:
			print(line)
		print("researcher ->", final_state["researcher"])
		print("writer ->", final_state["writer"])
		print("reviewer ->", final_state["reviewer"])

		print("\n=== Résultat agrégé ===")
		print(final_state["aggregated"])
		return final_state["aggregated"]


if __name__ == "__main__":
	manager = Manager()
	manager.run("les tendances IA 2025")
