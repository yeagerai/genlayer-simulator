import { setActivePinia, createPinia } from 'pinia';
import { describe, it, expect, beforeEach, vi, type Mock } from 'vitest';
import { useUIStore } from '@/stores';

describe('UI Store', () => {
  let uiStore: ReturnType<typeof useUIStore>;

  beforeEach(() => {
    setActivePinia(createPinia());
    uiStore = useUIStore();

    vi.stubGlobal('localStorage', {
      getItem: vi.fn(),
      setItem: vi.fn(),
    });

    vi.spyOn(document.documentElement, 'setAttribute');
  });

  it('should initialize with correct mode from localStorage', () => {
    (localStorage.getItem as Mock).mockReturnValue('light');
    const store = useUIStore();
    expect(store.mode).toBe('light');
  });

  it('should toggle mode from light to dark', () => {
    uiStore.mode = 'light';
    uiStore.toggleMode();
    expect(uiStore.mode).toBe('dark');
    expect(localStorage.setItem).toHaveBeenCalledWith(
      'genLayer.ui-mode',
      'dark',
    );
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith(
      'data-mode',
      'dark',
    );
  });

  it('should toggle mode from dark to light', () => {
    uiStore.mode = 'dark';
    uiStore.toggleMode();
    expect(uiStore.mode).toBe('light');
    expect(localStorage.setItem).toHaveBeenCalledWith(
      'genLayer.ui-mode',
      'light',
    );
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith(
      'data-mode',
      'light',
    );
  });

  it('should run the tutorial', () => {
    uiStore.runTutorial();
    expect(uiStore.showTutorial).toBe(true);
  });

  it('should initialize the store correctly', () => {
    uiStore.mode = 'dark';
    uiStore.initialize();
    expect(localStorage.setItem).toHaveBeenCalledWith(
      'genLayer.ui-mode',
      'dark',
    );
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith(
      'data-mode',
      'dark',
    );
  });
});
