import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

if __name__ == "__main__":
    load_dotenv()
    print("Hello Langchain")
    print(os.environ["OPENAI_API_KEY"])

    summary_template = """
    Given the information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                             template=summary_template)

    # TODO: try local model, llama cpp
    # temperature: creative level
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
