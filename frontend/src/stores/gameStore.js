import { create } from 'zustand';

export const useGameStore = create((set) => ({
  currentEvent: null,
  currentLevel: null,
  levels: [],
  progress: null,
  progressId: null,

  setCurrentEvent: (event) => set({ currentEvent: event }),
  setLevels: (levels) => set({ levels }),
  setCurrentLevel: (level) => set({ currentLevel: level }),
  setProgress: (progress) => set({ progress }),
  setProgressId: (progressId) => set({ progressId }),
  
  reset: () => set({
    currentEvent: null,
    currentLevel: null,
    levels: [],
    progress: null,
    progressId: null,
  }),
}));
