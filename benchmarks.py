# benchmarks.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# Define structured output for the benchmark in French as requested
class AIUseCase(BaseModel):
    industry: str = Field(description="Secteur d'activité concerné")
    business_function: str = Field(description="Fonction métier concernée")
    entreprise: Optional[str] = Field(None, description="Entreprise mettant en œuvre ce cas d'utilisation")
    origine_de_la_source: str = Field(description="Origine de l'information (article, étude de cas, etc.)")
    lien: str = Field(description="URL de la source")
    derniere_mise_a_jour: Optional[str] = Field(None, description="Date de dernière mise à jour de l'information")
    processus_impacte: List[str] = Field(description="Processus métier impactés par la solution IA")
    valeur_economique: Optional[str] = Field(None, description="Valeur économique générée (si mentionnée)")
    gains_attendus_realises: List[str] = Field(description="Gains attendus ou réalisés par l'implémentation")
    usage_ia: str = Field(description="Description de l'usage de l'IA dans ce cas")
    technologies_ia_utilisees: List[str] = Field(
        description="Technologies d'IA utilisées (NLP, ML, Computer Vision, etc.)")
    partenaires_impliques: Optional[List[str]] = Field(None, description="Partenaires impliqués dans l'implémentation")


class IndustryAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1
        )
        self.parser = PydanticOutputParser(pydantic_object=AIUseCase)

    def analyze_article_content(self, content, url, industry):
        """Analyze article content to extract structured use case information."""
        # Prompt in French as requested
        prompt = ChatPromptTemplate.from_template("""
        Tu es un analyste spécialisé dans l'identification et l'évaluation des cas d'utilisation de l'IA.

        Analyse le contenu de l'article suivant et extrais les informations sur les cas d'utilisation de l'IA dans l'industrie {industry}.
        Réponds uniquement en français.
        Formate ta réponse selon le format de sortie spécifié.

        Contenu de l'article:
        {content}

        {format_instructions}

        IMPORTANT: Si une information n'est pas disponible, utilise TOUJOURS un tableau vide [] pour les champs de type liste, et "Non mentionné" pour les champs de texte simples.
        Par exemple, si aucun partenaire n'est mentionné, utilise [] et NON "Non mentionné".

        Pour chaque champ:
        - industry: Indique précisément le secteur d'activité (finance, santé, etc.)
        - business_function: Précise la fonction métier (marketing, RH, finance, etc.)
        - processus_impacte: Liste les processus métiers impactés
        - valeur_economique: Chiffre les gains financiers si disponibles
        - gains_attendus_realises: Liste les bénéfices concrets
        - usage_ia: Décris clairement comment l'IA est utilisée
        - technologies_ia_utilisees: Énumère les technologies spécifiques
        - partenaires_impliques: Liste des partenaires ou [] si non mentionnés
        """)

        try:
            chain = prompt | self.llm | self.parser
            result = chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions(),
                "industry": industry
            })

            # Add URL to the output
            if hasattr(result, 'lien'):
                result.lien = url
            else:
                setattr(result, 'lien', url)

            # Add today's date as default last update date if not specified
            if not result.derniere_mise_a_jour:
                result.derniere_mise_a_jour = datetime.now().strftime("%Y-%m-%d")

            return result

        except Exception as e:
            # Try to handle the case where the error is due to "Non mentionné" instead of []
            if "partenaires_impliques" in str(e) and "list_type" in str(e):
                print(f"  Attempting to fix partenaires_impliques format issue...")
                # Try a direct approach with custom parsing
                try:
                    # Process response directly without the parser
                    direct_response = self.llm.invoke(prompt.format(
                        content=content,
                        format_instructions=self.parser.get_format_instructions(),
                        industry=industry
                    ))

                    # Create a default object
                    from pydantic import create_model
                    import json

                    # Manually fix the JSON by replacing "Non mentionné" with [] for list fields
                    text = direct_response.content

                    # Extract JSON part
                    import re
                    json_match = re.search(r'\{.*\}', text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        # Replace "Non mentionné" with [] for list fields
                        list_fields = ["processus_impacte", "gains_attendus_realises",
                                       "technologies_ia_utilisees", "partenaires_impliques"]
                        for field in list_fields:
                            json_str = json_str.replace(f'"{field}": "Non mentionné"', f'"{field}": []')

                        data = json.loads(json_str)

                        # Ensure all list fields are actually lists
                        for field in list_fields:
                            if field in data and not isinstance(data[field], list):
                                if data[field] == "Non mentionné":
                                    data[field] = []
                                else:
                                    # If it's a string but not "Non mentionné", convert to a single-item list
                                    data[field] = [data[field]]

                        # Create a new AIUseCase object from the fixed data
                        result = self.parser.pydantic_object(**data)

                        # Add URL and date
                        result.lien = url
                        if not result.derniere_mise_a_jour:
                            result.derniere_mise_a_jour = datetime.now().strftime("%Y-%m-%d")

                        return result
                except Exception as inner_e:
                    print(f"  Failed to fix format issue: {inner_e}")

            # If we reached here, we couldn't fix the issue
            raise e

    def compare_industry_use_cases(self, use_cases, industry):
        """Compare and benchmark AI use cases within an industry."""
        # Prompt in French as requested
        prompt = ChatPromptTemplate.from_template("""
        Tu es un expert en analyse d'impact de l'IA sur les industries. 

        Analyse les cas d'utilisation suivants de l'IA dans l'industrie {industry} et fournis une analyse comparative.
        Réponds uniquement en français.

        Cas d'utilisation:
        {use_cases}

        Dans ton analyse, inclus:
        1. Les technologies d'IA les plus couramment utilisées dans cette industrie
        2. Les fonctions métiers qui bénéficient le plus de l'IA
        3. Les gains typiques observés (qualitatifs et quantitatifs)
        4. Les défis communs d'implémentation
        5. Les tendances émergentes
        6. Recommandations pour les entreprises souhaitant adopter l'IA dans cette industrie

        Fournis une analyse détaillée et nuancée.
        """)

        result = prompt.invoke({
            "industry": industry,
            "use_cases": "\n\n".join([str(case.dict()) for case in use_cases])
        })

        return self.llm.invoke(result.to_string())