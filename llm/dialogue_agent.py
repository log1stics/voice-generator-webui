from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import Tool, AgentOutputParser
from langchain.schema import HumanMessage, SystemMessage

import re
from typing import List, Union

from . import template


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        pattern = r'(.*?)[：:]\s*(.*)'
        llm_output = llm_output.replace('「', '').replace('」', '')
        matches = re.findall(pattern, llm_output)
        dialogues = {}

        # parentheses pattern
        pattern = r"[（\(][^）\)]*[）\)]"

        if matches:
            for n, match in enumerate(matches):
                speaker, dialogue = re.sub(pattern, "", match[0]), re.sub(pattern, "", match[1])
                if speaker not in dialogues:
                    dialogues[speaker] = {}
                dialogues[speaker][n] = dialogue

        else:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")

        return AgentFinish(
            # Return values is generally always a dictionary with a single `output` key
            # It is not recommended to try anything else at the moment :)
            return_values={"output": (dialogues, llm_output)},
            log=llm_output,
        )


class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    # template: str
    template = template.template
    # The list of tools available
    tools: List[Tool]

    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


if __name__ == '__main__':
    output_parser = CustomOutputParser()
    prompt = CustomPromptTemplate(
        tools=tools,
        input_variables=["input", "intermediate_steps", "chat_history"]
    )
