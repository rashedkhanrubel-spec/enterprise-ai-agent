from agent.agent import EnterpriseAgent
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

def main():
    tools = [DuckDuckGoSearchRun()]
    agent = EnterpriseAgent(tools=tools)
    print("Enterprise AI Agent ready!")
    while True:
        user_input = input("
You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print(f"
Agent: {response}")

if __name__ == "__main__":
    main()

