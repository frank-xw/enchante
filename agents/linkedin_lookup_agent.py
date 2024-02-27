from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """
    Given the full name {name_of_person}, \
    I want you to get me the link to their Linkedin profile page.
    Your answer should only contain a URL.
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need to\
                get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        tools=tools_for_agent,
        llm=llm,
        prompt=react_prompt,
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    return result["output"]
