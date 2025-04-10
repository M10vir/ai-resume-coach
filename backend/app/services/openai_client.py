# backend/app/services/openai_client.py

def analyze_resume(resume_text: str) -> str:
    """
    Mock GPT-4 resume analysis until Azure OpenAI access is approved.
    """

    # You could add logic to adjust based on input later
    feedback = f"""
    ✅ **Summary**: This resume shows strong experience in backend development, cloud services, and modern Python frameworks.

    ⚠️ **Areas to Improve**:
    - Consider adding quantifiable metrics (e.g., % improvement, revenue impact).
    - Improve section structure: "Projects" and "Skills" should be clearer.

    💡 **Suggestions**:
    - Include specific achievements in bullet format.
    - Emphasize cloud-related certifications or training.
    - Tailor content for the role (e.g., backend vs. full-stack).

    Keep up the great work!
    """

    return feedback
