import React, { useState } from 'react';
import { Code, Brain, Clock, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

interface ComplexityResult {
  time_complexity: string;
  space_complexity: string;
  analysis: string;
  ast_info: {
    loops: number;
    recursive_calls: number;
    nested_depth: number;
    functions: string[];
  };
  confidence: number;
}

function App() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState<ComplexityResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sampleCode = `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1`;

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError('Failed to analyze code. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = () => {
    setCode(sampleCode);
    setError('');
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Brain className="w-12 h-12 text-indigo-600 mr-3" />
              <h1 className="text-4xl font-bold text-gray-900">Time Complexity Estimator</h1>
            </div>
            <p className="text-xl text-gray-600">
              Analyze python code complexity using AI-powered AST parsing with LLM
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-800 flex items-center">
                  <Code className="w-6 h-6 mr-2 text-indigo-600" />
                  Code Input
                </h2>
                <button
                  onClick={loadSample}
                  className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Load Sample
                </button>
              </div>
              
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter your code here..."
                className="w-full h-64 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              />
              
              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center">
                  <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                  <span className="text-red-700">{error}</span>
                </div>
              )}
              
              <button
                onClick={handleAnalyze}
                disabled={loading || !code.trim()}
                className="w-full mt-4 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Brain className="w-5 h-5 mr-2" />
                    Analyze Complexity
                  </>
                )}
              </button>
            </div>

            {/* Results Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
                <Clock className="w-6 h-6 mr-2 text-indigo-600" />
                Analysis Results
              </h2>
              
              {result ? (
                <div className="space-y-6">
                  {/* Complexity Overview */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h3 className="font-semibold text-blue-900 mb-2">Time Complexity</h3>
                      <p className="text-2xl font-bold text-blue-600">{result.time_complexity}</p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h3 className="font-semibold text-green-900 mb-2">Space Complexity</h3>
                      <p className="text-2xl font-bold text-green-600">{result.space_complexity}</p>
                    </div>
                  </div>

                  {/* Confidence Level */}
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-purple-900 mb-2">Confidence Level</h3>
                    <div className="flex items-center">
                      <div className="flex-1 bg-purple-200 rounded-full h-2 mr-3">
                        <div 
                          className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${result.confidence}%` }}
                        ></div>
                      </div>
                      <span className="text-purple-700 font-semibold">{result.confidence}%</span>
                    </div>
                  </div>

                  {/* AST Analysis */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-3">AST Analysis</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Loops:</span>
                        <span className="ml-2 font-semibold">{result.ast_info.loops}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Recursive Calls:</span>
                        <span className="ml-2 font-semibold">{result.ast_info.recursive_calls}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Nested Depth:</span>
                        <span className="ml-2 font-semibold">{result.ast_info.nested_depth}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Functions:</span>
                        <span className="ml-2 font-semibold">{result.ast_info.functions.length}</span>
                      </div>
                    </div>
                    {result.ast_info.functions.length > 0 && (
                      <div className="mt-2">
                        <span className="text-gray-600 text-sm">Function names:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {result.ast_info.functions.map((func, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                              {func}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Detailed Analysis */}
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-yellow-900 mb-2">Detailed Analysis</h3>
                    <p className="text-yellow-800 leading-relaxed">{result.analysis}</p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 text-lg">
                    Enter your code and click "Analyze Complexity" to see results
                  </p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;