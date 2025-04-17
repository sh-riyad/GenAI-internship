HYPOTHESIS_PROMPT = "Based on the description: '{description}', list possible 3 skin diseases."

RESEARCH_PLAN_PROMPT = "Generate a research plan to gather information about the following skin diseases: {diseases}. Focus on symptoms, causes, and diagnostic criteria."

QUESTION_SELECTOR_PROMPT = "Based on the research findings and current hypotheses, generate a simple, relevant question to ask the user to refine the diagnosis. Avoid repeating questions from the conversation history."

HYPOTHESIS_UPDATE_PROMPT = "Update the list of possible skin diseases with probabilities (as decimals between 0 and 1) based on the initial description and conversation history."