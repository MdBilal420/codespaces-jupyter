import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
    api_key = my_api_key
)

###CHAINING PROMPTS


# report = """
# Q3 Performance Summary:
# Our customer satisfaction score rose to 92 points this quarter.
# Revenue grew by 45% compared to last year.
# Market share is now at 23% in our primary market.
# Customer churn decreased to 5% from 8%.
# New user acquisition cost is $43 per user.
# Product adoption rate increased to 78%.
# Employee satisfaction is at 87 points.
# Operating margin improved to 34%.
# """

# prompts = [
#     """Extract only the numerical values and their associated metrics from the text.
#     Format each as 'value: metric' on a new line.
#     Example format:
#     92: customer satisfaction
#     45%: revenue growth""",
#     """Convert all numerical values to percentages where possible.
#     If not a percentage or points, convert to decimal (e.g., 92 points -> 92%).
#     Keep one number per line.
#     Example format:
#     92%: customer satisfaction
#     45%: revenue growth""",
#     """Sort all lines in descending order by numerical value.
#     Keep the format 'value: metric' on each line.
#     Example:
#     92%: customer satisfaction
#     87%: employee satisfaction""",
#     """Format the sorted data as a markdown table with columns:
#     | Metric | Value |
#     |:--|--:|
#     | Customer Satisfaction | 92% |""",
# ]

# def chain(report,prompts):
#     for prompt in prompts:
#         response = client.messages.create(
#             model="claude-haiku-4-5-20251001",
#             max_tokens=1000,
#             messages=[
#                 {"role": "user", "content": f"{report} {prompt}"}
#             ]
#         )
#         print(response.content[0].text)

# chain(report,prompts)

# response = client.messages.create(
#     model="claude-haiku-4-5-20251001",
#     max_tokens=1000,
#     messages=[
#         {"role": "user", "content": "Hi there! Please write me a joke about a pet chicken"}
#     ]
# )

# print(response.content[0].text)

### PARALLEL PROMPTS
# from concurrent.futures import ThreadPoolExecutor

# stakeholders = ["marketing team", "sales team", "product team", "customer support team"]

# def parallel(question, stakeholders):
#     with ThreadPoolExecutor() as executor:
#         futures = []
#         for stakeholder in stakeholders:
#             future = executor.submit(
#                 client.messages.create,
#                 model="claude-haiku-4-5-20251001",
#                 max_tokens=1000,
#                 messages=[
#                     {"role": "user", "content": f"{question} from the perspective of the {stakeholder}."}
#                 ]
#             )
#             futures.append(future)
        
#         results = [future.result().content[0].text for future in futures]
    
#     return results

# impact_result = parallel(
#     """What is the impact of new investment coming in Q4 ?""",
#     stakeholders,
# )

# for result in impact_result:
#     print(result)
#     print("-" * 100)

### ROUTING WORKFLOW

teams = ["Technical Support", "Finance Team", "General Inquiries"]

def route(teams, question):
    routing_prompt = f"""You are a helpful assistant that routes customer questions to the appropriate team. 
    The teams you can route to are: {', '.join(teams)}.
<reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>
    """
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"{routing_prompt} Customer question: {question}"}
        ]
    )
    
    return response.content[0].text.strip()

result = route(teams, "I have a question about my recent bill. I think I was overcharged and I want to understand the charges better.")
print(result)