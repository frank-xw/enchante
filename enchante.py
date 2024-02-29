from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import person_intel_parser, PersonIntel


def enchante(name: str) -> PersonIntel:
    load_dotenv()

    linkedin_profile_url = linkedin_lookup_agent(name=name)

    # with open("prompt_info.txt", "r") as f:
    #     information = f.read()

    print(f"Linkedin Profile URL: {linkedin_profile_url}")

    summary_template = """
    Given the Linkedin information {information} \
    about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    3. A topic may interest them
    4. Two creative icebreakers may to open a conversion with them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": (
                person_intel_parser.get_format_instructions()
            )
        },
    )

    # TODO: try local model, llama cpp
    # temperature: creative level
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url
    )

    res = chain.invoke(input={"information": linkedin_data})

    print(res["text"])
    return person_intel_parser.parse(res["text"])


if __name__ == "__main__":
    print("Hello Langchain")
    result = enchante(name="Andrew Ng")
