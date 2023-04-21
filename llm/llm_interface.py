from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.utilities import WikipediaAPIWrapper

import description_agent


def set_executor(temperature, prompt, tools, output_parser):
    llm = ChatOpenAI(temperature=temperature, model_name='gpt-3.5-turbo')

    # LLM chain consisting of the LLM and a prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    tool_names = [tool.name for tool in tools]

    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names,
        verbose=True,
    )
    agent.llm_chain.verbose = True

    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True,)


def set_description_agent():
    tools = [
        Tool(
            name="Wikipedia",
            func=WikipediaAPIWrapper().run,
            description="useful for when you need to answer questions about current events"
        )
    ]

    output_parser = description_agent.CustomOutputParser()
    prompt = description_agent.CustomPromptTemplate(
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )
    return set_executor(0, prompt, tools, output_parser)


def parse(llm_output):
    output_parser = description_agent.CustomOutputParser()

    return output_parser.parse(llm_output)




if __name__ == '__main__':
    llm_exe = set_description_agent()
    out = llm_exe.run("戦争")
    print(out)
