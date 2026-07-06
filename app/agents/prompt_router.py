import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PromptRouter:
    """
    Routes a given context to the appropriate Markdown prompt template.
    Uses the inferred platform, relationship, and tone to find the best match.
    """

    def __init__(self, prompts_dir: str | Path = "app/prompts"):
        """
        Initializes the PromptRouter.
        
        Args:
            prompts_dir: Base directory containing the Markdown prompt files.
        """
        self.prompts_dir = Path(prompts_dir)

    def _get_platform_default(self, platform: str) -> str:
        """
        Returns the sensible default filename for a given platform.
        """
        defaults = {
            "gmail": "formal",
            "instagram": "caption",
            "linkedin": "professional",
            "sms": "default",
            "whatsapp": "default"
        }
        return defaults.get(platform, "default")

    def get_prompt(self, context: dict) -> str:
        """
        Determines the correct prompt template based on context and loads it.
        Gracefully falls back through a hierarchy of templates if specific ones
        are missing.
        
        Args:
            context (dict): The resolved context dictionary.
            
        Returns:
            str: The loaded markdown prompt template.
        """
        platform = str(context.get("platform", "default")).lower()
        relationship = str(context.get("relationship", "default")).lower()
        tone = str(context.get("tone", "default")).lower()

        platform_dir = self.prompts_dir / platform
        platform_default = self._get_platform_default(platform)

        # Build fallback hierarchy
        candidates = [
            platform_dir / f"{relationship}.md",   # e.g., whatsapp/family.md
            platform_dir / f"{tone}.md",           # e.g., whatsapp/professional.md
            platform_dir / f"{platform_default}.md", # e.g., instagram/caption.md
            platform_dir / "default.md",           # e.g., sms/default.md
            self.prompts_dir / "default.md"        # Global fallback
        ]

        # Attempt to read files in order of precedence
        for file_path in candidates:
            if file_path.is_file():
                try:
                    logger.info("Prompt selected: %s", file_path.name)
                    return file_path.read_text(encoding="utf-8")
                except OSError as e:
                    logger.warning(
                        "Failed to read prompt file %s: %s",
                        file_path,
                        e,
                    )
        # Ultimate hardcoded fallback if absolutely no templates exist
        logger.warning("No prompt templates found. Using generic hardcoded fallback.")
        return (
            "You are an expert AI communication agent.\n\n"
            "Draft a well-crafted message matching the user's intent, "
            "adhering strictly to the requested platform conventions and tone."
        )
