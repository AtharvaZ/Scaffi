import type { ProgressProps } from '../types';

export function ProgressIndicator({ totalTasks, completedTasks, currentTask }: ProgressProps) {
  const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
  const isComplete = totalTasks > 0 && completedTasks === totalTasks;

  return (
    <div className="w-full border-b border-gray-200/60 dark:border-gray-800/60 pb-6 mb-6">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-gray-900 dark:text-gray-100">Progress</span>
          <span className="text-base font-semibold text-gray-700 dark:text-gray-300">
            {completedTasks} / {totalTasks} tasks complete
          </span>
        </div>
        <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-800">
          <div
            className={`h-full transition-all duration-300 ease-out ${
              isComplete
                ? "bg-green-600 dark:bg-green-500"
                : "bg-blue-600 dark:bg-blue-500"
            }`}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </div>
  );
}

