import sqlite3
from langchain import GroqCloud, Llama3
from langchain.prompts import ReActPrompt
from langchain.agents import Tool, initialize_agent
import sys

# Initialize GroqCloud and Llama3 with your API key
groq_api_key = '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'
llm = Llama3(api_key=groq_api_key)

# Connect to SQLite database
conn = sqlite3.connect('Northwind_small.sqlite')

# Define a function to execute SQL queries
def execute_sql_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Define a tool to use within the ReAct agent
tools = [
    Tool(
        name="SQLExecutor",
        func=execute_sql_query,
        description="Executes SQL queries on the Northwind database"
    )
]

# Create a ReAct prompt template
react_prompt = ReActPrompt.from_template("""
Question: {input}
Let's think step-by-step to solve this problem. What do I need to know or do to get the answer?
""")

# Initialize the agent with the ReAct prompt
agent = initialize_agent(llm, tools, prompt=react_prompt)

# Build the command-line interface
def main():
    print("Welcome to the AI SQL Agent. Type your question and press Enter.")
    while True:
        user_input = input("Question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Use the agent to process the input and generate a response
        response = agent(user_input)
        print(f"Answer: {response}")

if __name__ == "__main__":
    main()
