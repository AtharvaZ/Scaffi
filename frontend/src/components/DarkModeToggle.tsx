import { Moon, Sun } from 'lucide-react';
import { Button } from './ui/button';
import { useAppStore } from '../store/useAppStore';

export function DarkModeToggle() {
  const { isDarkMode, toggleDarkMode } = useAppStore();

  return (
    <Button
      variant="ghost"
      size="default"
      onClick={toggleDarkMode}
      className="relative"
      aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDarkMode ? (
        <Sun className="h-6 w-6" />
      ) : (
        <Moon className="h-6 w-6" />
      )}
    </Button>
  );
}

