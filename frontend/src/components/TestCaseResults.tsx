import { useState } from 'react';
import { Check, X, ChevronDown, ChevronRight, Edit2 } from 'lucide-react';
import { Button } from './ui/button';
import type { TestResult } from '../types';

interface TestCaseResultsProps {
  testResults?: TestResult[];
  testsPassedCount?: number;
  testsFailedCount?: number;
  onEditTests?: () => void;
}

export function TestCaseResults({ testResults, testsPassedCount, testsFailedCount, onEditTests }: TestCaseResultsProps) {
  const [expandedTest, setExpandedTest] = useState<string | null>(null);

  if (!testResults || testResults.length === 0) {
    return null;
  }

  const totalTests = testResults.length;

  return (
    <div className="h-full flex flex-col bg-white dark:bg-black border-t border-gray-200/60 dark:border-gray-800/60">
      {/* Header */}
      <div className="flex-shrink-0 p-4 border-b border-gray-200/60 dark:border-gray-800/60">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-base font-semibold text-black dark:text-white">
            Test Results
          </h3>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm">
              <span className={`flex items-center gap-1 ${testsPassedCount === totalTests ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'}`}>
                <Check className="h-4 w-4" />
                {testsPassedCount || 0} passed
              </span>
              <span className="text-gray-400">|</span>
              <span className={`flex items-center gap-1 ${(testsFailedCount || 0) > 0 ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'}`}>
                <X className="h-4 w-4" />
                {testsFailedCount || 0} failed
              </span>
            </div>
            {onEditTests && (
              <Button
                onClick={onEditTests}
                size="sm"
                variant="outline"
                className="h-7 px-2 text-xs border-gray-200 dark:border-gray-800"
              >
                <Edit2 className="h-3 w-3 mr-1" />
                Edit Tests
              </Button>
            )}
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-full h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-300 ${
              testsPassedCount === totalTests
                ? 'bg-green-500'
                : (testsFailedCount || 0) > 0
                ? 'bg-red-500'
                : 'bg-gray-400'
            }`}
            style={{ width: `${((testsPassedCount || 0) / totalTests) * 100}%` }}
          />
        </div>
      </div>

      {/* Test Cases List */}
      <div className="flex-1 overflow-y-auto">
        {testResults.map((test, index) => (
          <div
            key={index}
            className="border-b border-gray-200/60 dark:border-gray-800/60 last:border-b-0"
          >
            {/* Test case header */}
            <button
              onClick={() => setExpandedTest(expandedTest === test.test_name ? null : test.test_name)}
              className="w-full flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors text-left"
            >
              {/* Pass/Fail Icon */}
              <div className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center ${
                test.passed
                  ? 'bg-green-100 dark:bg-green-900/30'
                  : 'bg-red-100 dark:bg-red-900/30'
              }`}>
                {test.passed ? (
                  <Check className="h-3 w-3 text-green-600 dark:text-green-400" />
                ) : (
                  <X className="h-3 w-3 text-red-600 dark:text-red-400" />
                )}
              </div>

              {/* Test name */}
              <span className={`flex-1 text-base font-medium ${
                test.passed
                  ? 'text-black dark:text-white'
                  : 'text-red-600 dark:text-red-400'
              }`}>
                {test.test_name}
              </span>

              {/* Expand/Collapse icon */}
              {expandedTest === test.test_name ? (
                <ChevronDown className="h-4 w-4 text-gray-400" />
              ) : (
                <ChevronRight className="h-4 w-4 text-gray-400" />
              )}
            </button>

            {/* Expanded test details */}
            {expandedTest === test.test_name && (
              <div className="px-3 pb-3 space-y-3 bg-gray-50/50 dark:bg-gray-900/30">
                {/* Input */}
                <div>
                  <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                    Input:
                  </div>
                  <code className="block text-sm bg-white dark:bg-black px-2 py-1 rounded border border-gray-200 dark:border-gray-800 text-gray-800 dark:text-gray-300 font-mono">
                    {test.input_data}
                  </code>
                </div>

                {/* Expected Output */}
                <div>
                  <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                    Expected:
                  </div>
                  <code className="block text-sm bg-white dark:bg-black px-2 py-1 rounded border border-gray-200 dark:border-gray-800 text-gray-800 dark:text-gray-300 font-mono">
                    {test.expected_output}
                  </code>
                </div>

                {/* Actual Output */}
                <div>
                  <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                    Actual:
                  </div>
                  <code className={`block text-sm px-2 py-1 rounded border font-mono ${
                    test.passed
                      ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-300'
                      : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300'
                  }`}>
                    {test.actual_output || '(empty)'}
                  </code>
                </div>

                {/* Error if present */}
                {test.error && (
                  <div>
                    <div className="text-sm font-medium text-red-600 dark:text-red-400 mb-1">
                      Error:
                    </div>
                    <code className="block text-sm bg-red-50 dark:bg-red-900/20 px-2 py-1 rounded border border-red-200 dark:border-red-800 text-red-800 dark:text-red-300 font-mono whitespace-pre-wrap">
                      {test.error}
                    </code>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
