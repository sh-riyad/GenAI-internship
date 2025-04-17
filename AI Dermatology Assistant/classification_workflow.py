from typing import List, Dict, Union, Tuple
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from prompt import HYPOTHESIS_PROMPT, HYPOTHESIS_UPDATE_PROMPT, QUESTION_SELECTOR_PROMPT, RESEARCH_PLAN_PROMPT
from settings import settings
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
pool = ConnectionPool(
    conninfo=settings.DATABASE_URL,
    min_size=1, 
    max_size=10,
    kwargs=connection_kwargs,
)
checkpointer = PostgresSaver(pool)
checkpointer.setup()

llm = ChatOpenAI(model="gpt-4o")
tavily= TavilySearch(max_results=2,topic="general",)


class ClassificationState(BaseModel):
    conversation_history: List[Union[HumanMessage, AIMessage, SystemMessage]]
    current_hypotheses: List[Tuple[str, float]]
    research_findings: Dict[str, str]
    research_queries: List[str]
    user_responses: str
    iteration_count: int
    input_description: str
    confident: bool
    current_question: str
    need_input: bool
    final_ans:str

    class Config:
        arbitrary_types_allowed = True

def input_processor(state: ClassificationState) -> ClassificationState:
    """Processes initial user input if not already provided."""
    # if not state.input_description:
    #     user_input = input("Please describe your skin condition: ")
    #     state.input_description = user_input
    #     state.conversation_history.append(HumanMessage(content=user_input))
    # else:
    # state.conversation_history.append(HumanMessage(content=state.input_description))
    return state

def hypothesis_generator(state: ClassificationState) -> ClassificationState:
    """Generates initial disease hypotheses."""
    prompt = HYPOTHESIS_PROMPT.format(description=state.input_description)
    response = llm.invoke([SystemMessage(content="You are a dermatology assistant."), 
                          HumanMessage(content=prompt)])
    diseases = [d.strip() for d in response.content.split('\n') if d.strip()]
    state.current_hypotheses = [(disease, 1.0 / len(diseases)) for disease in diseases]
    return state


def research_planner(state: ClassificationState) -> ClassificationState:
    """Plans internet research by generating searchable queries based on hypotheses."""
    hypotheses = [disease for disease, _ in state.current_hypotheses]
    queries = []
    for disease in hypotheses:
        queries.append(f"common symptoms of {disease} skin condition")
        # queries.append(f"causes of {disease} dermatology")
        # queries.append(f"diagnostic criteria for {disease} skin disease")
    state.research_queries = queries
    return state

def internet_researcher(state: ClassificationState) -> ClassificationState:
    """Conducts internet research."""
    findings = {}
    for query in state.research_queries:
        results = tavily.invoke({"query": query})
        findings[query] = results['results'][0]['content']
    state.research_findings.update(findings)
    return state

def question_selector(state: ClassificationState) -> ClassificationState:
    """Selects a simple question using AI."""
    state.conversation_history.append(HumanMessage(content=state.input_description))
    history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in state.conversation_history])
    findings_text = "\n".join([f"{q}: {f}" for q, f in state.research_findings.items()])
    prompt = QUESTION_SELECTOR_PROMPT + f"\n\nResearch Findings:\n{findings_text}\n\nConversation History:\n{history_text}"
    response = llm.invoke([SystemMessage(content="You are a dermatology assistant."), 
                          HumanMessage(content=prompt)])
    state.current_question = response.content.strip()
    state.conversation_history.append(AIMessage(content=state.current_question))
    return state


def hypothesis_updater(state: ClassificationState) -> ClassificationState:
    """Updates hypotheses based on history."""
    history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in state.conversation_history])
    prompt = HYPOTHESIS_UPDATE_PROMPT + f"\n\nInitial Description: {state.input_description}\n\nConversation History:\n{history_text}"
    response = llm.invoke([SystemMessage(content="You are a dermatology assistant."), 
                          HumanMessage(content=prompt)])
    lines = response.content.split('\n')
    updated_hypotheses = []
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                disease, prob = parts
                try:
                    updated_hypotheses.append((disease.strip(), float(prob.strip())))
                except ValueError:
                    continue
    state.current_hypotheses = updated_hypotheses if updated_hypotheses else state.current_hypotheses
    return state

def confidence_checker(state: ClassificationState) -> ClassificationState:
    """Checks confidence level."""
    state.iteration_count += 1
    if state.current_hypotheses:
        top_prob = max(prob for _, prob in state.current_hypotheses)
        if top_prob > 0.9 or state.iteration_count >= 3:
            state.confident = True
    return state

def final_output_provider(state: ClassificationState) -> ClassificationState:
    """Provides the final diagnosis."""
    if state.current_hypotheses:
        top_disease, top_prob = max(state.current_hypotheses, key=lambda x: x[1])
        print(f"Diagnosis: {top_disease} with {top_prob*100:.2f}% confidence.")
    else:
        print("Unable to determine a diagnosis.")
    return state




graph = StateGraph(ClassificationState)

graph.add_node("input_processor", input_processor)
graph.add_node("hypothesis_generator", hypothesis_generator)
graph.add_node("research_planner", research_planner)
graph.add_node("internet_researcher", internet_researcher)
graph.add_node("question_selector", question_selector)
graph.add_node("hypothesis_updater", hypothesis_updater)
graph.add_node("confidence_checker", confidence_checker)
graph.add_node("final_output_provider", final_output_provider)

graph.add_edge("input_processor", "hypothesis_generator")
graph.add_edge("hypothesis_generator", "research_planner")
graph.add_edge("research_planner", "internet_researcher")
graph.add_edge("internet_researcher", "question_selector")
graph.add_edge("question_selector", "hypothesis_updater")
graph.add_edge("hypothesis_updater", "confidence_checker")

def route_confidence(state: ClassificationState) -> str:
    return "final_output_provider" if state.confident else "research_planner"

graph.add_conditional_edges("confidence_checker", route_confidence, 
                            {"final_output_provider": "final_output_provider", 
                             "research_planner": "research_planner"})
graph.add_edge("final_output_provider", END)

graph.set_entry_point("input_processor")

ClassificationGraph = graph.compile(checkpointer=checkpointer, interrupt_before=['hypothesis_updater'])
