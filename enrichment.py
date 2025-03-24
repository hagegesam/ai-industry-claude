# enrichment.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


class QualityEnhancer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1
        )

    def filter_relevance(self, content, industry):
        """Evaluates if the content is relevant for AI use case analysis."""
        # Prompt in French as requested
        prompt = ChatPromptTemplate.from_template("""
        Analyse le contenu suivant et détermine s'il contient des informations pertinentes sur un cas d'utilisation d'IA 
        dans l'industrie {industry}.

        Contenu:
        {content}

        Réponds uniquement par "OUI" ou "NON".
        Considère comme pertinent uniquement du contenu qui décrit spécifiquement comment l'IA est utilisée, 
        par quelle entreprise, et idéalement avec quels résultats, dans l'industrie {industry}.
        """)

        result = self.llm.invoke(prompt.format(content=content, industry=industry))
        return "OUI" in result.content.upper()

    def enrich_information(self, use_case, industry):
        """Enriches information about a use case if it's incomplete."""
        if not use_case.entreprise or not use_case.technologies_ia_utilisees:
            # Prompt in French as requested
            prompt = ChatPromptTemplate.from_template("""
            Voici des informations partielles sur un cas d'utilisation de l'IA dans l'industrie {industry}:

            {case_information}

            Sur la base de tes connaissances des pratiques courantes dans l'industrie {industry}, 
            complète les informations manquantes de manière plausible. 

            Indique clairement que ces informations sont des estimations basées sur des cas similaires 
            en préfixant par [ESTIMATION] les informations que tu ajoutes.
            """)

            result = self.llm.invoke(prompt.format(
                case_information=str(use_case.dict()),
                industry=industry
            ))

            # Note: This would ideally be a more structured process to update the use_case object
            # This part would require additional implementation to extract and
            # integrate the enriched information

            return result.content

        return "No enrichment needed."

    def verify_coherence(self, use_case, industry):
        """Verifies the coherence of use case information."""
        # Prompt in French as requested
        prompt = ChatPromptTemplate.from_template("""
        Examine les informations suivantes sur un cas d'utilisation de l'IA dans l'industrie {industry}:

        {case_information}

        Vérifie la cohérence des informations et identifie toute contradiction ou information qui semble improbable.
        Par exemple, vérifie si les technologies mentionnées correspondent bien à l'usage décrit,
        ou si les gains mentionnés semblent réalistes par rapport à l'utilisation décrite.

        Si tu détectes des incohérences, explique-les. Sinon, indique "Informations cohérentes".
        """)

        result = self.llm.invoke(prompt.format(
            case_information=str(use_case.dict()),
            industry=industry
        ))

        return result.content