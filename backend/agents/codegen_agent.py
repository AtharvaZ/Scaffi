""" Agent 2 for boiler plate code generation tasks.
Generates starter code templates with TODO comments for specific tasks
"""

import logging
from typing import List
from pyd_models.schemas import BoilerPlateCodeSchema, StarterCode
from services import get_anthropic_client
from utils.json_parser import extract_json_from_response

logger = logging.getLogger(__name__)

# Agent responsible for generating boilerplate code templates
class CodegenAgent:

    def __init__(self):
        self.client = get_anthropic_client()
        self.max_retries = 3

    def generate_file_scaffolding(self, filename: str,
                                   tasks: List[BoilerPlateCodeSchema],
                                   class_structure: dict = None,
                                   template_variables: list = None) -> List[StarterCode]:
        """
        Generate scaffolding for ONE complete file.

        Args:
            filename: Name of file to generate
            tasks: List of tasks for this file
            class_structure: Dict of {class_name: [tasks]} or None for single-class
            template_variables: List of variable names from template to preserve, or None

        Returns:
            List of StarterCode objects for this file's tasks
        """

        if not tasks:
            raise ValueError(f"No tasks provided for {filename}")

        # Convert tasks to dict format for prompt
        tasks_dict_list = []
        for task in tasks:
            task_dict = {
                'task_description': task.task_description,
                'programming_language': task.programming_language,
                'concepts': task.concepts,
                'known_language': task.known_language,
                'filename': task.filename,
                'experience_level': getattr(task, 'experience_level', 'intermediate'),
                'class_name': getattr(task, 'class_name', None),
                'template_variables': getattr(task, 'template_variables', None)
            }
            tasks_dict_list.append(task_dict)

        # Get focused prompt for THIS file
        from utils.agent_prompts import get_file_codegen_prompt

        prompt = get_file_codegen_prompt(
            tasks_dict_list,
            filename,
            class_structure=class_structure,
            template_variables=template_variables
        )

        last_error = None
        for attempt in range(self.max_retries):
            try:
                logger.info(f"File codegen for {filename}, attempt {attempt + 1}/{self.max_retries}")

                # Estimate tokens for this file
                estimated_tokens = len(tasks) * 400
                max_tokens = min(estimated_tokens + 1000, 4000)

                response_text = self.client.generate_response(prompt, max_tokens=max_tokens)

                # Log the first 500 chars of response for debugging
                logger.info(f"AI response preview (first 500 chars): {response_text[:500]}")

                data = extract_json_from_response(response_text)

                # Log what keys we got
                logger.info(f"Parsed JSON keys: {list(data.keys())}")

                # Validate response
                if "tasks" not in data:
                    logger.error(f"Response missing 'tasks' field. Got keys: {list(data.keys())}")
                    logger.error(f"Full parsed data: {data}")
                    raise ValueError(f"Response missing 'tasks' field. Got: {list(data.keys())}")

                if not isinstance(data["tasks"], list):
                    raise ValueError("'tasks' must be a list")

                if len(data["tasks"]) != len(tasks):
                    raise ValueError(f"Expected {len(tasks)} tasks, got {len(data['tasks'])}")

                # Convert to StarterCode objects
                results = []
                for i, task_data in enumerate(data["tasks"], 1):
                    if "code_snippet" not in task_data and "code" not in task_data:
                        raise ValueError(f"Task {i} missing 'code_snippet' or 'code' field")
                    if "instructions" not in task_data:
                        raise ValueError(f"Task {i} missing 'instructions' field")
                    if "todos" not in task_data:
                        raise ValueError(f"Task {i} missing 'todos' field")
                    if "filename" not in task_data:
                        task_data["filename"] = filename

                    if "code" in task_data and "code_snippet" not in task_data:
                        task_data["code_snippet"] = task_data["code"]

                    results.append(StarterCode(
                        code_snippet=task_data["code_snippet"],
                        instructions=task_data["instructions"],
                        todos=task_data["todos"],
                        concept_examples=None,
                        filename=task_data["filename"]
                    ))

                logger.info(f"Successfully generated {len(results)} tasks for {filename}")
                return results

            except Exception as e:
                last_error = e
                logger.warning(f"File codegen attempt {attempt + 1} failed: {str(e)}")

                if attempt < self.max_retries - 1:
                    prompt += f"\n\nIMPORTANT: Previous attempt failed. Ensure response is ONLY valid JSON with all {len(tasks)} tasks."
                continue

        logger.error(f"All {self.max_retries} attempts failed for {filename}")
        raise ValueError(f"Failed to generate scaffolding for {filename} after {self.max_retries} attempts: {str(last_error)}")

codegen_agent = None
def get_batch_codegen_agent() -> CodegenAgent:
    global codegen_agent
    if codegen_agent is None:
        codegen_agent = CodegenAgent()
    return codegen_agent