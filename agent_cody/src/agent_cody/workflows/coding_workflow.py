from agent_cody.crew import run_agent

class CodingWorkflow:

    MAX_ITERATIONS = 5

    # TODO: add DOC "Call agent for selected task (param) and loop some review feedback to get better result"
    def run_with_review_loop(self, agent: str, prompt: str, max_iterations=MAX_ITERATIONS):
        # 1. Get code -> first pass
        print("Getting code")
        code = run_agent(agent, prompt)

        # 2. Refine the code using review agent.
        for i in range(max_iterations): # Make sure to NEVER loop indefinitely
            print(f"Code review pass {i+1}")
            review = run_agent( "review", code )
            # 3. Check stop condition
            if self.stop_review(review):
                print("Code reviews done")
                break

            # 4. refine the prompt for the next code loop
            print("Refining prompt for next coding pass (post-review)")
            refined_prompt = self.get_refined_prompt(code, review )

            # 5. Do a code refining pass:
            code = run_agent(agent, refined_prompt)
        
        return code

    # TODO: Change later to use structured output.
    def stop_review(self, review_text: str) -> bool:
        text = review_text.lower()

        return (
        "no issues" in text or
        "looks good" in text or
        "approved" in text
    )

    def get_refined_prompt(self, code: str, review: str ) -> str:
        return f"""
You are a coding agent.

Fix the code according to the review.

--- CODE ---
{code}

--- REVIEW ---
{review}

Return ONLY the full corrected code.
"""




        