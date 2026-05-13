// Performance monitoring utilities
export const performanceMonitor = {
  startTiming: (label) => {
    if (typeof performance !== 'undefined') {
      performance.mark(`${label}-start`);
    }
  },

  endTiming: (label) => {
    if (typeof performance !== 'undefined') {
      performance.mark(`${label}-end`);
      performance.measure(label, `${label}-start`, `${label}-end`);

      const entries = performance.getEntriesByName(label);
      if (entries.length > 0) {
        console.log(`${label}: ${entries[0].duration}ms`);
      }
    }
  },

  measureComponentRender: (componentName, renderFunction) => {
    performanceMonitor.startTiming(`render-${componentName}`);
    const result = renderFunction();
    performanceMonitor.endTiming(`render-${componentName}`);
    return result;
  }
};

// Bundle size optimization tracking
export const bundleAnalyzer = {
  logBundleInfo: () => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Bundle analysis available in development mode');
    }
  }
};
