# Time Complexity Estimator

A comprehensive system that analyzes code complexity using AI-powered AST parsing with Google's Gemini LLM 1.5 Flash.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Python Backend │    │   Gemini LLM    │
│                 │    │                 │    │                 │
│  - Code Input   │◄──►│  - AST Parser   │◄──►│  - Complexity   │
│  - Results UI   │    │  - Flask API    │    │    Analysis     │
│  - Visualizations│    │  - Data Proc.   │    │  - Explanations │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Components

1. **Frontend (React + Tailwind CSS)**
   - Code input interface
   - Results visualization
   - Real-time analysis display
   - Responsive design

2. **Backend (Python Flask)**
   - AST parsing using Python's built-in `ast` module
   - Gemini LLM integration
   - API endpoints for analysis
   - Error handling and validation

3. **AI Analysis (Gemini 1.5 Flash)**
   - Time and space complexity estimation
   - Detailed analysis explanations
   - Confidence scoring
   - Structured JSON responses

## Features

- **AST-Enhanced Analysis**: Combines structural code analysis with AI intelligence
- **Multiple Complexity Metrics**: Time complexity, space complexity, and detailed explanations
- **Confidence Scoring**: AI provides confidence levels for its analysis
- **Visual Feedback**: Clean, modern interface with intuitive results display
- **Sample Code**: Pre-loaded examples for testing
- **Real-time Analysis**: Instant feedback with loading states

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Lucide React
- **Backend**: Python, Flask, Flask-CORS
- **AI**: Google Gemini 1.5 Flash
- **AST Parsing**: Python's built-in `ast` module
- **Environment**: dotenv for configuration

## Setup Instructions

### Prerequisites

- Node.js (v18+)
- Python (v3.8+)
- Google Gemini API key

### 1. Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start the Flask server
python app.py
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Add it to `backend/.env`:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Sample Prompts and Expected Outputs

### Sample 1: Binary Search
**Input:**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Expected Output:**
```json
{
  "time_complexity": "O(log n)",
  "space_complexity": "O(1)",
  "analysis": "This binary search algorithm has logarithmic time complexity because it eliminates half of the search space in each iteration. The while loop runs at most log₂(n) times, where n is the array size. Space complexity is constant as only a few variables are used regardless of input size.",
  "ast_info": {
    "loops": 1,
    "recursive_calls": 0,
    "nested_depth": 1,
    "functions": ["binary_search"]
  },
  "confidence": 95
}
```

### Sample 2: Bubble Sort
**Input:**
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

**Expected Output:**
```json
{
  "time_complexity": "O(n²)",
  "space_complexity": "O(1)",
  "analysis": "This bubble sort implementation has quadratic time complexity due to nested loops. The outer loop runs n times, and the inner loop runs up to n-1 times, resulting in roughly n² comparisons in the worst case. Space complexity is constant as sorting is done in-place.",
  "ast_info": {
    "loops": 2,
    "recursive_calls": 0,
    "nested_depth": 2,
    "functions": ["bubble_sort"]
  },
  "confidence": 98
}
```

### Sample 3: Recursive Fibonacci
**Input:**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Expected Output:**
```json
{
  "time_complexity": "O(2^n)",
  "space_complexity": "O(n)",
  "analysis": "This naive recursive Fibonacci implementation has exponential time complexity because it recalculates the same values multiple times. Each call branches into two recursive calls, creating a binary tree of depth n. Space complexity is O(n) due to the maximum call stack depth.",
  "ast_info": {
    "loops": 0,
    "recursive_calls": 2,
    "nested_depth": 0,
    "functions": ["fibonacci"]
  },
  "confidence": 90
}
```

## API Endpoints

### POST /analyze
Analyzes code complexity using AST parsing and Gemini LLM.

**Request:**
```json
{
  "code": "def example_function():\n    # your code here"
}
```

**Response:**
```json
{
  "time_complexity": "O(n)",
  "space_complexity": "O(1)",
  "analysis": "Detailed explanation...",
  "ast_info": {
    "loops": 1,
    "recursive_calls": 0,
    "nested_depth": 1,
    "functions": ["example_function"]
  },
  "confidence": 85
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Time Complexity Estimator API is running"
}
```

## How It Works

1. **Code Input**: User enters code in the React frontend
2. **AST Analysis**: Backend parses code using Python's AST module to extract:
   - Number of loops
   - Recursive function calls
   - Nesting depth
   - Function names
3. **Prompt Engineering**: Structured prompt combines code and AST data
4. **AI Analysis**: Gemini LLM analyzes the enhanced prompt
5. **Result Processing**: Backend processes AI response and returns structured data
6. **Visualization**: Frontend displays results with complexity metrics and explanations

## Testing

Use the provided sample codes in `backend/test_samples.py` to test different complexity scenarios:

- Binary Search (O(log n))
- Bubble Sort (O(n²))
- Recursive Factorial (O(n))
- Naive Fibonacci (O(2^n))
- Linear Search (O(n))
- Merge Sort (O(n log n))

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request
