# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from app.models.message import MessageRequest
from app.agents.communication_agent import CommunicationAgent
from app.agents.intent_detector import IntentDetector
from app.agents.context_builder import ContextBuilder
from app.agents.prompt_router import PromptRouter
from app.services.prompt_renderer import PromptRenderer
from app.services.llm_factory import LLMFactory
from app.services.message_generation_service import MessageGenerationService

# Load environment variables
load_dotenv()

def main():
    print("Initializing components...")
    intent_detector = IntentDetector()
    context_builder = ContextBuilder()
    prompt_router = PromptRouter()
    prompt_renderer = PromptRenderer()
    
    # Initialize the LLM (using GeminiService)
    llm = LLMFactory().get_provider("gemini")
    
    # Initialize generation service
    message_generation_service = MessageGenerationService(
        prompt_router=prompt_router,
        prompt_renderer=prompt_renderer,
        llm=llm
    )
    
    # Initialize main orchestrator
    agent = CommunicationAgent(
        intent_detector=intent_detector,
        context_builder=context_builder,
        message_generation_service=message_generation_service
    )
    
    # Create request (WhatsApp to family, tone apologetic/casual, late purpose)
    request = MessageRequest(
        message="Hey mom, sorry I will be 30 minutes late for dinner because of heavy traffic.",
        platform="whatsapp"
    )
    
    print("\nProcessing request through agent...")
    result = agent.process(request)
    
    print("\n" + "=" * 60)
    print("PIPELINE RESULT")
    print("=" * 60)
    
    # Check if we got a clarification context or final response
    if hasattr(result, "needs_clarification") and result.needs_clarification:
        print(f"Clarification required: {result.question}")
        print(f"Missing fields: {result.missing_fields}")
    else:
        print(f"Original Message: {result.original_message}")
        print(f"Detected Platform: {result.detected_platform}")
        print(f"Detected Relationship: {result.detected_relationship}")
        print(f"Detected Tone: {result.detected_tone}")
        print(f"Detected Language: {result.detected_language}")
        print("\nGenerated Variants:")
        for i, variant in enumerate(result.messages, 1):
            print(f"\n{i}. Style: {variant.style}")
            print(f"   Text: {variant.text}")
            
    print("=" * 60)

if __name__ == "__main__":
    main()
