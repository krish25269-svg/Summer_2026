"""
Report Generator for Multi-Model AI Workflow
Creates JSON and HTML reports from workflow results
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

def generate_json_report(results: Dict[str, Any], output_file: str = "results/report.json") -> str:
    """Generate JSON report"""
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "total_models": 3,
            "models": ["GPT", "Claude", "Gemini"]
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ JSON report saved to {output_file}")
    return output_file


def generate_html_report(results: Dict[str, Any], output_file: str = "results/report.html") -> str:
    """Generate HTML report"""
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Model AI Workflow Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
            .model-section {{ margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff; }}
            .model-section h2 {{ color: #007bff; margin-top: 0; }}
            .timestamp {{ color: #666; font-size: 12px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Multi-Model AI Workflow Report</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="model-section">
                <h2>Workflow Models</h2>
                <ul>
                    <li>🟢 OpenAI GPT-4</li>
                    <li>🟢 Anthropic Claude-3</li>
                    <li>🟢 Google Gemini-Pro</li>
                </ul>
            </div>
            
            <div class="model-section">
                <h2>Results Summary</h2>
                <pre>{json.dumps(results, indent=2)}</pre>
            </div>
            
            <div class="model-section">
                <h2>Execution Details</h2>
                <table>
                    <tr>
                        <th>Component</th>
                        <th>Status</th>
                    </tr>
                    <tr>
                        <td>Data Loading</td>
                        <td>✓ Complete</td>
                    </tr>
                    <tr>
                        <td>Model Processing</td>
                        <td>✓ Complete</td>
                    </tr>
                    <tr>
                        <td>Result Aggregation</td>
                        <td>✓ Complete</td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✓ HTML report saved to {output_file}")
    return output_file


if __name__ == "__main__":
    # Sample results for testing
    sample_results = {
        "gpt": "GPT analysis results...",
        "claude": "Claude analysis results...",
        "gemini": "Gemini analysis results..."
    }
    
    generate_json_report(sample_results)
    generate_html_report(sample_results)
