import json

from agent_cody.crew import run_agent
from agent_cody.dispatcher.prompt_builder import PromptBuilder

#RENDULA  _YEG_
#- Faire les tests - revoir ChatGTP pour les 2 derniere "🚀" -> Optional improvement (later)



class CodingWorkflow:

    # Avoid infinite review loops. A MAX is needed, because a reviewer will never stop giving suggestions.
    MAX_REVIEW_ITERATIONS = 3 # 10 is best, but use lower for testing.

    def __init__(self):
        self.language = None # TODO ? Could stay local with +1 param to build_review_prompt
        self.review_history = []  # TODO ? Could stay local with +1 param to build_review_prompt

    def parse_review(self, review_text: str):
        try:
            return json.loads(review_text)
        except Exception as e:
            raise ValueError(f"Invalid review JSON: {review_text}") from e    

    # TODO: add DOC "Call agent for selected task (param) and loop some review feedback to get better result"
    def run_with_review_loop(self, agent: str, language: str, prompt: str, max_iterations=MAX_REVIEW_ITERATIONS):
        """ Run a task with the received agent, with a loop to refine the task based on review feedback.
            The loop will stop when the reviewer approves the code or when the maximum number of iterations is reached.
        """
        self.language = language # keep for other functions in this class

        # 1. Get code -> first pass
        print("Getting code")
        code = run_agent(agent, prompt)
        print("----- ### DEBUG ### - CODE -----")
        print(code)
        print("----------------------")

        # 2. Refine the code using review agent.
        # FUTURE TODO do not do the review loop if this is a review task.
        self.review_history = []
        self.review_prompt_history = []
        review_prompt = None
        review_approved = False

        for i in range(max_iterations): # Make sure to NEVER loop indefinitely
            print(f"Code review pass {i+1}")

            # First iteration? Create the review prompt, otherwise, append the last review result and new code.
            if review_prompt is None:
                # Build the initial review prompt with the code to review and no history.
                prompt_builder = PromptBuilder()
                review_prompt = prompt_builder.build_review_prompt( language=self.language, code=code )
            else:
                # Not the first pass, just add the latest code and review to the prompt for the next review pass.
                review_prompt += self.get_last_review_and_new_code(review, code, iteration=i+1)


            # Do the code review with the review agent, and get the structured JSON result.
            review_raw = run_agent( "review", review_prompt )
            print("----- ### DEBUG ### - Review raw -----")
            print(review_raw)
            print("----------------------")

            # Extract the JSON from the agent reply
            review = self.parse_review(review_raw)
           
            # 3. Check stop condition
            if self.stop_review(review):
                print("Code approved by reviewer - review done")
                review_approved = True
                break

            # 4. refine the prompt for the next code loop
            print("Refining prompt for next coding pass (post-review)")
            refined_prompt = self.get_refined_prompt(code, review )

            # 5. Do a code refining pass:
            code = run_agent(agent, refined_prompt)
        
        if not review_approved:
            print(f"Max review iterations reached ({max_iterations}) - review done, but may not be perfect.")
        return code

    def stop_review(self, review_json: dict) -> bool:
        """ Returns `False` if reviewer approves the code to stop the review loop, True otherwise. """
        return review_json.get("approved", False) is True


#region Prompt Builders - Keep at the end of file because of the bad text alignment of the f-strings.


    # TODO Rename get_refined_coding_prompt
    def get_refined_prompt(self, code: str, review: str ) -> str:
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

    def get_last_review_and_new_code(self, review: list, code: str, iteration: int ) -> str:
        """
            Append to the initial review prompt the latest code and review, to get a new review from the reviewer.    
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