import anthropic
from dotenv import load_dotenv
import os
import re

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

from util import llm_call, extract_xml

evaluator_prompt = """
Evaluate this following code implementation for:
1. code correctness
2. time complexity
3. style and best practices

You should be evaluating only and not attemping to solve the task.
Only output "PASS" if all criteria are met and you have no further suggestions for improvements.
Output your evaluation concisely in the following format.

<evaluation>PASS, NEEDS_IMPROVEMENT, or FAIL</evaluation>
<feedback>
What needs improvement and why.
</feedback>
"""

generator_prompt = """
Your goal is to complete the task based on <user input>. If there are feedback
from your previous generations, you should reflect on them to improve your solution

Output your answer concisely in the following format:

<thoughts>
[Your understanding of the task and feedback and how you plan to improve]
</thoughts>

<response>
[Your code implementation here]
</response>
"""

task = """
<user input>
Implement a Stack with:
1. push(x)
2. pop()
3. getMin()
All operations should be O(1).
</user input>
"""


client = anthropic.Anthropic(
    api_key = my_api_key
)

def generate(prompt, task, context=""):
    full_prompt = f"Prompt: {prompt}\nTask: {task} {context}" if context else f"Prompt: {prompt}\nTask: {task}"
    print("================GENERATION_START")
    response = llm_call(full_prompt)
    thought = extract_xml(response, "thoughts")
    code = extract_xml(response, "response")
    print("GENERATION_END================")
    return thought, code

def evaluate(prompt, code):
    full_prompt = f"Prompt: {prompt}\nCode: {code}"
    print("===========EVALUATION_START")
    response = llm_call(full_prompt)
    evaluation = extract_xml(response, "evaluation")
    feedback = extract_xml(response, "feedback")
    print("EVALUATION_END================")
    return evaluation, feedback

def loop(task, evaluator_prompt, generator_prompt):
    memory = []
    chain_of_thought = []

    thought, code = generate(generator_prompt,task)
    memory.append(code)
    chain_of_thought.append({"thought": thought, "code": code})
    while True:
        evaluation , feedback = evaluate(evaluator_prompt, code)
        if evaluation == "PASS":
            print("Code implementation passed all criteria!")
            print("Final Code:\n", code)
            return code, chain_of_thought
        else:
            print(f"Evaluation: {evaluation}\nFeedback: {feedback}")
            context = "\n".join(
                ["Previous attempts:", *[f"- {m}" for m in memory], f"\nFeedback: {feedback}"]
            )
            print("Generating new code implementation based on feedback...")
            print("Context for new generation:\n", context)
            thought, code = generate(generator_prompt, task, context=context)

            memory.append(code)
            chain_of_thought.append({"thought": thought, "code": code})

loop(task, evaluator_prompt, generator_prompt)