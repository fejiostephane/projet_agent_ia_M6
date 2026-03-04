from pprint import pprint
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class SharedMemoryState(TypedDict):
	task: str
	data: dict
	summary: str
	feedback: dict
	trace: list[str]


def researcher(state: SharedMemoryState):
	task = state["task"]
	findings = {
		"topic": task,
		"facts": [
			"Le coût du solaire baisse depuis plusieurs années.",
			"L'éolien couvre une part croissante de la production électrique.",
			"Le stockage par batteries améliore la stabilité du réseau.",
		],
		"source_count": 3,
	}
	trace = state.get("trace", []) + ["researcher -> écrit 'data'"]
	return {"data": findings, "trace": trace}


def writer(state: SharedMemoryState):
	data = state["data"]
	summary = (
		f"Sujet: {data['topic']} | "
		f"Faits clés: {len(data['facts'])} | "
		"Conclusion: la transition énergétique est portée par la baisse des coûts "
		"et les progrès du stockage."
	)
	trace = state.get("trace", []) + ["writer -> lit 'data', écrit 'summary'"]
	return {"summary": summary, "trace": trace}


def reviewer(state: SharedMemoryState):
	text = state["summary"]
	feedback = {
		"clarity_score": 8,
		"strengths": ["message clair", "structure concise"],
		"improvements": [
			"ajouter un exemple chiffré",
			"séparer le contexte et la conclusion",
		],
		"final_text": text + " (Version relue)",
	}
	trace = state.get("trace", []) + ["reviewer -> lit 'summary', écrit 'feedback'"]
	return {"feedback": feedback, "trace": trace}


def build_workflow():
	graph = StateGraph(SharedMemoryState)
	graph.add_node("researcher", researcher)
	graph.add_node("writer", writer)
	graph.add_node("reviewer", reviewer)

	graph.add_edge(START, "researcher")
	graph.add_edge("researcher", "writer")
	graph.add_edge("writer", "reviewer")
	graph.add_edge("reviewer", END)

	return graph.compile()


if __name__ == "__main__":
	workflow = build_workflow()
	shared_memory = workflow.invoke({"task": "énergie verte", "trace": []})

	print("=== Mémoire partagée finale (LangGraph) ===")
	pprint(shared_memory, width=100)

	print("\n=== Explication ===")
	print("1) researcher écrit les données brutes dans shared_memory['data']")
	print("2) writer lit 'data' et écrit shared_memory['summary']")
	print("3) reviewer lit 'summary' et écrit shared_memory['feedback']")
	print("4) trace garde l'ordre des échanges entre agents")
