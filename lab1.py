from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
	task: str
	data: str
	summary: str
	feedback: str
	quality_score: int
	decision: str
	trace: list[str]


def researcher(state: AgentState):
	task = state["task"]
	data = f"Résultats bruts sur {task}"
	trace = state.get("trace", []) + ["researcher -> écrit 'data'"]
	return {"data": data, "trace": trace}


def writer(state: AgentState):
	summary = f"Résumé: {state['data']}"
	trace = state.get("trace", []) + ["writer -> lit 'data', écrit 'summary'"]
	return {"summary": summary, "trace": trace}


def reviewer(state: AgentState):
	summary = state["summary"]
	quality_score = 8 if len(summary) > 25 else 6
	decision = "accepté" if quality_score >= 7 else "à retravailler"
	feedback = f"Amélioration: {summary} | score={quality_score}/10"
	trace = state.get("trace", []) + ["reviewer -> lit 'summary', écrit 'feedback'"]
	return {
		"feedback": feedback,
		"quality_score": quality_score,
		"decision": decision,
		"trace": trace,
	}


def build_graph():
	graph = StateGraph(AgentState)
	graph.add_node("researcher", researcher)
	graph.add_node("writer", writer)
	graph.add_node("reviewer", reviewer)

	graph.add_edge(START, "researcher")
	graph.add_edge("researcher", "writer")
	graph.add_edge("writer", "reviewer")
	graph.add_edge("reviewer", END)

	return graph.compile()


def run_collaboration(task: str):
	workflow = build_graph()
	final_state = workflow.invoke({"task": task, "trace": []})
	return final_state


if __name__ == "__main__":
	task = "les tendances de l'IA en 2026"
	state = run_collaboration(task)

	print("=== Collaboration entre agents (LangGraph) ===")
	print(f"Chercheur  -> {state['data']}")
	print(f"Rédacteur  -> {state['summary']}")
	print(f"Relecteur  -> {state['feedback']}")
	print(f"Décision   -> {state['decision']}")
	print("Trace      ->", " | ".join(state["trace"]))
