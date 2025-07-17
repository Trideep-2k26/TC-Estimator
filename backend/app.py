from flask import Flask, request, jsonify
from flask_cors import CORS
import ast
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

class ComplexityAnalyzer:
    def __init__(self):
        self.loop_count = 0
        self.recursive_calls = 0
        self.nested_depth = 0
        self.current_depth = 0
        self.max_depth = 0
        self.functions = []
        
    def analyze_ast(self, code):
        """Parse code and extract structural information using AST"""
        try:
            tree = ast.parse(code)
            self.visit_node(tree)
            
            return {
                'loops': self.loop_count,
                'recursive_calls': self.recursive_calls,
                'nested_depth': self.max_depth,
                'functions': self.functions
            }
        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing code: {str(e)}")
    
    def visit_node(self, node):
        """Recursively visit AST nodes to extract complexity indicators"""
        if isinstance(node, (ast.For, ast.While)):
            self.loop_count += 1
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)
            
        elif isinstance(node, ast.FunctionDef):
            self.functions.append(node.name)
            # Check for recursion by looking for calls to the same function
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        self.recursive_calls += 1
        
        # Visit all child nodes
        for child in ast.iter_child_nodes(node):
            self.visit_node(child)
            
        # Decrease depth when leaving loop nodes
        if isinstance(node, (ast.For, ast.While)):
            self.current_depth -= 1

def create_analysis_prompt(code, ast_info):
    """Create structured prompt for Gemini LLM"""
    prompt = f"""
You are an expert computer science algorithm analyst. Analyze the following code and provide a comprehensive time and space complexity analysis.

CODE TO ANALYZE:
```python
{code}
```

AST ANALYSIS DATA:
- Number of loops: {ast_info['loops']}
- Recursive function calls: {ast_info['recursive_calls']}
- Maximum nesting depth: {ast_info['nested_depth']}
- Functions found: {ast_info['functions']}

Please provide your analysis in the following JSON format:
{{
    "time_complexity": "O(n)", // Big O notation for time complexity
    "space_complexity": "O(1)", // Big O notation for space complexity
    "analysis": "Detailed explanation of the complexity analysis, including reasoning about loops, recursion, and data structures used",
    "confidence": 85 // Confidence level (0-100) in your analysis
}}

Consider the following factors:
1. Loop structures and their nesting levels
2. Recursive calls and their depth
3. Data structure operations (if any)
4. Input size dependencies
5. Best, average, and worst-case scenarios

Provide only the JSON response without any additional text or formatting.
"""
    return prompt

@app.route('/analyze', methods=['POST'])
def analyze_complexity():
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Initialize analyzer and extract AST information
        analyzer = ComplexityAnalyzer()
        ast_info = analyzer.analyze_ast(code)
        
        # Create prompt for Gemini
        prompt = create_analysis_prompt(code, ast_info)
        
        # Get analysis from Gemini
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        try:
            # Clean the response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            analysis_result = json.loads(response_text)
            
            # Add AST info to result
            analysis_result['ast_info'] = ast_info
            
            return jsonify(analysis_result)
            
        except json.JSONDecodeError:
            # Fallback parsing if JSON is malformed
            return jsonify({
                'error': 'Failed to parse LLM response',
                'raw_response': response.text
            }), 500
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Time Complexity Estimator API is running'})

if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('GEMINI_API_KEY'):
        print("WARNING: GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
    
    app.run(debug=True, host='0.0.0.0', port=5000)