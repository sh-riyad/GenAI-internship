
# from app.core.database import get_db
# from sqlalchemy.orm import Session
# from app.crud.message_crud import store_chat_message
# from app.schemas.chat_history import StoreMessageInput

from classification_workflow import ClassificationState, ClassificationGraph

thread_id = 0
thread = {"configurable": {"thread_id": str(thread_id)}}

input_text = input("input: ")

  

    
state = ClassificationGraph.get_state(thread)




if state.next and state.next[0] == 'hypothesis_updater':
    
    if state.values.get('need_input', False):
        
        ClassificationGraph.update_state(state.config, values={"user_responses": input_text})

        result = ClassificationGraph.invoke(None, thread)
        
        
        # print(result)

        if result.get('final_ans'):
            print(result['final_ans'])
            ClassificationGraph.update_state(state.config, values={"need_input": False})
            exit() 
        else:
            print(result.get('current_question', 'No question available'))
            ClassificationGraph.update_state(state.config, values={"need_input": True})
            exit()
        
        
        # state = ClassificationGraph.get_state(thread)


        # print(state.values['user_responses'])

else:
        
    classification_state = ClassificationState(
        conversation_history= [],
        current_hypotheses= [],
        research_findings= {},
        research_queries= [],
        user_responses= "",
        iteration_count= 0,
        input_description= input_text,
        confident=False,
        current_question="",
        need_input=False,
        final_ans="",
    )    
    
    result = ClassificationGraph.invoke(classification_state, thread)
            
    state = ClassificationGraph.get_state(thread)
            
    if state.next[0] == 'hypothesis_updater':
                
        ClassificationGraph.update_state(state.config, values = {"need_input": True})

        print(result['current_question'])
        
        
        


# state = ClassificationGraph.get_state(thread)


# print("---------------")
# print(state.values['user_responses'])
# print("---------------")

# print(state.values['current_question'])
# print(state.values['iteration_count'])

# print(state.values['conversation_history'])