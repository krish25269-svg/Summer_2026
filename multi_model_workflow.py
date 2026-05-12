"""
Multi-Model AI Workflow
Orchestrates multiple AI models (GPT, Claude, Gemini) for the Myntra dataset
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any
from dotenv import load_dotenv
import asyncio
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model APIs
try:
    from openai import OpenAI  # GPT
    gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    logger.warning("OpenAI library not installed")

try:
    import anthropic  # Claude
    claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except ImportError:
    logger.warning("Anthropic library not installed")

try:
    import google.generativeai as genai  # Gemini
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except ImportError:
    logger.warning("Google Generative AI library not installed")


class MultiModelWorkflow:
    """Orchestrates multiple AI models for processing and analysis"""
    
    def __init__(self):
        self.results = {}
        self.dataset = None
    
    # ============ DATA LOADING ============
    def load_myntra_dataset(self, csv_path: str) -> pd.DataFrame:
        """Load Myntra dataset from CSV"""
        try:
            self.dataset = pd.read_csv(csv_path)
            logger.info(f"✓ Dataset loaded: {len(self.dataset)} products")
            return self.dataset
        except FileNotFoundError:
            logger.error(f"Dataset not found at {csv_path}")
            return None
    
    # ============ GPT MODEL ============
    async def process_with_gpt(self, prompt: str, model: str = "gpt-4") -> str:
        """Process data using OpenAI GPT"""
        try:
            response = gpt_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            result = response.choices[0].message.content
            logger.info(f"✓ GPT processed successfully")
            return result
        except Exception as e:
            logger.error(f"✗ GPT error: {str(e)}")
            return None
    
    # ============ CLAUDE MODEL ============
    async def process_with_claude(self, prompt: str, model: str = "claude-3-sonnet-20240229") -> str:
        """Process data using Anthropic Claude"""
        try:
            message = claude_client.messages.create(
                model=model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            result = message.content[0].text
            logger.info(f"✓ Claude processed successfully")
            return result
        except Exception as e:
            logger.error(f"✗ Claude error: {str(e)}")
            return None
    
    # ============ GEMINI MODEL ============
    async def process_with_gemini(self, prompt: str, model: str = "gemini-pro") -> str:
        """Process data using Google Gemini"""
        try:
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(prompt)
            result = response.text
            logger.info(f"✓ Gemini processed successfully")
            return result
        except Exception as e:
            logger.error(f"✗ Gemini error: {str(e)}")
            return None
    
    # ============ PARALLEL EXECUTION ============
    async def run_all_models_parallel(self, prompt: str) -> Dict[str, str]:
        """Run all models in parallel"""
        logger.info("🔄 Running all models in parallel...")
        
        tasks = [
            self.process_with_gpt(prompt),
            self.process_with_claude(prompt),
            self.process_with_gemini(prompt)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "gpt": results[0],
            "claude": results[1],
            "gemini": results[2]
        }
    
    # ============ SEQUENTIAL EXECUTION ============
    async def run_models_sequential(self, initial_prompt: str) -> Dict[str, Any]:
        """Run models sequentially (output of one feeds into next)"""
        logger.info("⏭️  Running models sequentially...")
        
        # Step 1: GPT analyzes data
        gpt_analysis = await self.process_with_gpt(initial_prompt)
        
        # Step 2: Claude refines GPT output
        claude_prompt = f"Refine and improve this analysis:\n{gpt_analysis}"
        claude_refinement = await self.process_with_claude(claude_prompt)
        
        # Step 3: Gemini validates and summarizes
        gemini_prompt = f"Validate and summarize this analysis:\n{claude_refinement}"
        gemini_summary = await self.process_with_gemini(gemini_prompt)
        
        return {
            "step_1_gpt": gpt_analysis,
            "step_2_claude": claude_refinement,
            "step_3_gemini": gemini_summary
        }
    
    # ============ ENSEMBLE VOTING ============
    async def ensemble_voting(self, prompt: str) -> Dict[str, Any]:
        """Get responses from all models and aggregate"""
        logger.info("🗳️  Running ensemble voting...")
        
        results = await self.run_all_models_parallel(prompt)
        
        ensemble_result = {
            "individual_responses": results,
            "consensus": self._aggregate_responses(results),
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        return ensemble_result
    
    # ============ RESPONSE AGGREGATION ============
    def _aggregate_responses(self, responses: Dict[str, str]) -> str:
        """Aggregate responses from multiple models"""
        aggregation_prompt = f"""
        Based on these three AI model responses, provide a unified conclusion:
        
        GPT: {responses['gpt']}
        Claude: {responses['claude']}
        Gemini: {responses['gemini']}
        
        Identify common themes and create a single best response.
        """
        return aggregation_prompt
    
    # ============ PRODUCT ANALYSIS ============
    async def analyze_product_recommendations(self, product_data: Dict) -> Dict[str, Any]:
        """Use multi-model workflow for product recommendations"""
        prompt = f"""
        Analyze this product from Myntra dataset and provide recommendations:
        Product Name: {product_data.get('ProductName', 'N/A')}
        Brand: {product_data.get('Brand', 'N/A')}
        Price: {product_data.get('Price', 'N/A')}
        Category: {product_data.get('Category', 'N/A')}
        
        Provide: 1) Market analysis 2) Price positioning 3) Target audience
        """
        
        results = await self.run_all_models_parallel(prompt)
        
        return {
            "product": product_data.get('ProductName'),
            "gpt_recommendation": results['gpt'],
            "claude_recommendation": results['claude'],
            "gemini_recommendation": results['gemini']
        }
    
    # ============ SAVE RESULTS ============
    def save_results(self, results: Dict, output_file: str = "workflow_results.json"):
        """Save workflow results to JSON"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"✓ Results saved to {output_file}")


# ============ MAIN EXECUTION ============
async def main():
    """Main workflow execution"""
    workflow = MultiModelWorkflow()
    
    # Example: Analyze a product
    sample_product = {
        "ProductName": "Women's Cotton T-Shirt",
        "Brand": "Nike",
        "Price": 999,
        "Category": "Apparel"
    }
    
    # Run ensemble analysis
    results = await workflow.ensemble_voting(
        f"Analyze this Myntra product: {json.dumps(sample_product)}"
    )
    
    workflow.save_results(results)
    logger.info("✓ Workflow completed!")


if __name__ == "__main__":
    asyncio.run(main())
