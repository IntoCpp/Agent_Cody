from crewai import Agent, Task, Crew, Process
import os

coding_agent = Agent(
    role="Senior Software Engineer",
    goal="Write correct, clean, maintainable code based on instructions",
    backstory="You are an expert software engineer.",
    llm="gpt-4o-mini",   # 👈 IMPORTANT: string, not ChatOpenAI
    verbose=True,
)

review_agent = Agent(
    role="Senior Code Reviewer",
    goal="Find bugs, inefficiencies, and design issues in code",
    backstory="You are extremely strict about correctness and maintainability.",
    llm="gpt-4o-mini",
    verbose=True,
)

# Probably obsolete - it was suggested but never mentioned again following other problems. Then we moved along.
def run_review_task(code: str) -> str:
    task = Task(
        description=f"""
Review the following code:

{code}

Return:
- issues found
- why they are problems
- suggested fixes (as guidance, not rewritten full code)
""",
        expected_output="Review feedback",
        agent=review_agent,
    )

    crew = Crew(
        agents=[review_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()


def run_agent(agent_type: str, prompt: str) -> str:

    if agent_type == "coding":
        agent = coding_agent
        task = Task( description=prompt, expected_output="High quality code", agent=agent )
    elif agent_type == "review":
        agent = review_agent
        task = Task( description=prompt, expected_output="Structured list of review comments", agent=agent )
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


    crew = Crew(
        agents=[agent],  # TODO: Generalize for other tasks (review, design, etc.)  later.
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    # print(Type of result returned: type(result)) # Usually a `crewai.crews.crew_output.CrewOutput`
    return result.raw