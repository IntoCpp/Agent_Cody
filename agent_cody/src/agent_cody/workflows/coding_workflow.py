import json

from agent_cody.crew import run_agent
from agent_cody.dispatcher.prompt_builder import PromptBuilder

class CodingWorkflow:
    """ 
    This workflow is used for coding tasks. 
    It runs the coding agent to generate code, then runs the review agent + coding agent in a loop until the code is 
    approved or a maximum number of iterations is reached (to avoid infinite loops).

    The prompts are refined at each loop to add the latest review comments / code.
    """

    # Avoid infinite review loops. A MAX is needed, because a reviewer will never stop giving suggestions.
    MAX_REVIEW_ITERATIONS = 3 # 10 is best, but use lower for testing.

    def __init__(self):
        pass

    def parse_review(self, review_text: str):
        try:
            return json.loads(review_text)
        except Exception as e:
            raise ValueError(f"Invalid review JSON: {review_text}") from e    

    def run_with_review_loop(
        self,
        agent: str,
        task: str,
        prompt: str,
        coding_model: str,
        review_model: str,
        max_iterations=MAX_REVIEW_ITERATIONS,
    ):
        """ Run the coding agent with a loop to refine code based on review feedback.
            The loop will stop when the reviewer approves the code or when the maximum number of iterations is reached.
        """
        # 1. First pass -> Get some code from the agent
        print("Getting code")
        code = run_agent(agent, prompt, model=coding_model)
        print("----- ### DEBUG ### - CODE from agent -----")
        print(code)
        print("----------------------")

        # 2. LOOP to refine the code using review agent.
        review_prompt = None
        review_approved = False

        for i in range(max_iterations): # Make sure to NEVER loop indefinitely
            print(f"Code review pass {i+1}")

            # Build the prompt for the review agent, based on the code to be reviewed, and history of previous reviews.
            #  Create the review prompt, otherwise, 
            if review_prompt is None:
                # First iteration? Build the initial review prompt with the code to review and no history.
                prompt_builder = PromptBuilder()
                review_prompt = prompt_builder.build_review_prompt( task=task, code=code )
            else:
                # Not the first pass, append the last review result and latest code.
                review_prompt += self.get_refined_review_prompt(review, code, iteration=i+1)


            # Do the code review with the review agent, and get the structured JSON result.
            review_raw = run_agent("review", review_prompt, model=review_model)
            print("----- ### DEBUG ### - Review raw -----")
            print(review_raw)
            print("----------------------")

            # Extract the JSON from the agent reply
            review = self.parse_review(review_raw)
           
            # 3. Check stop condition - review approved?
            if self.stop_review(review):
                print("Code approved by reviewer - review done")
                review_approved = True
                break

            # 4. refine the prompt for the next code loop
            print("Refining prompt for next coding pass (post-review)")
            refined_prompt = self.get_refined_coding_prompt(code, review )

            # 5. Do a code refining pass (apply review comments):
            code = run_agent(agent, refined_prompt, model=coding_model)
        
        if not review_approved:
            print(f"Max review iterations reached ({max_iterations}) - review done, but may not be perfect.")
        return code

    def stop_review(self, review_json: dict) -> bool:
        """ Returns `False` if reviewer approves the code to stop the review loop, True otherwise. """
        # TODO - Future enhancement: have a better stop condition based on the severity of the review issues.
        # ex: up to 10 loops if 'critical' is present. 5 if 'major' is present. 3 if 'minor' is present. 1 if 'cosmetic' is present. If 'approved' we are done.
        # all that using class variables with default values but can be changed by user.

        return review_json.get("approved", False) is True
    

#region Prompt Builders - Keep at the end of file because of the bad text alignment of the f-strings.

    def get_refined_coding_prompt(self, code: str, review: str ) -> str:
        """ 
            Build a very simple prompt (simpler than the initial one from "prompt builder") 
            for the coding agent to refine the code based on the review feedback.
        """
        return f"""
You are a coding agent.

Fix the code according to the review.

--- CODE ---
{code}

--- REVIEW ---
{review}

Return ONLY the full corrected code.
"""

    def get_refined_review_prompt(self, review: list, code: str, iteration: int ) -> str:
        """
            Append to the previous review prompt the latest review comments + the new code when sent to the codingagent.
        """
        return f"""
You are reviewing code iteratively. Most recent changes last.
Do NOT repeat previously reported issues unless they still exist.

## Review {iteration}
{review}
## Code fix of review {iteration}
{code}
"""


#endregion Prompt Builders