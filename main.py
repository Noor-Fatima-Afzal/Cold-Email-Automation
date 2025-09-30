from workflows.agent_workflow import EmailCampaignAgent
from workflows.sequential_workflow import SequentialEmailWorkflow

def run_langchain_agent():
    agent_workflow = EmailCampaignAgent()
    return agent_workflow.execute_campaign()

def run_langchain_sequential():
    sequential_workflow = SequentialEmailWorkflow()
    return sequential_workflow.execute_workflow()

if __name__ == "__main__":
    print("Choose workflow type:")
    print("1. LangChain Agent-based (more autonomous)")
    print("2. LangChain Sequential (more controlled)")
    print("3. Run both")

    choice = input("Enter choice (1, 2, or 3): ").strip()

    if choice == "1":
        run_langchain_agent()
    elif choice == "2":
        run_langchain_sequential()
    elif choice == "3":
        print("\n" + "="*60)
        print("RUNNING AGENT-BASED WORKFLOW FIRST")
        print("="*60)
        run_langchain_agent()

        print("\n" + "="*60)
        print("RUNNING SEQUENTIAL WORKFLOW SECOND")
        print("="*60)
        run_langchain_sequential()
    else:
        print("Invalid choice. Running sequential workflow by default.")
        run_langchain_sequential()
