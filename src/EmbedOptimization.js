// SyllaFlow Embed Optimization for elv48.me Integration
// Optimized for WordPress/WooCommerce with 48AXIOM aesthetic

import React, { useState, useEffect, useRef, useCallback } from 'react';

/**
 * EmbedOptimization Component
 * Handles responsive embedding, performance optimization, and WordPress integration
 */
const EmbedOptimization = ({ 
  children, 
  config = {}, 
  onResize = null,
  onVisibilityChange = null,
  onPerformanceMetric = null
}) => {
  const containerRef = useRef(null);
  const [embedState, setEmbedState] = useState({
    isVisible: false,
    isIntersecting: false,
    containerSize: { width: 0, height: 0 },
    deviceType: 'desktop',
    connectionType: 'unknown',
    performanceMetrics: {},
    wordPressContext: null
  });

  // Device detection
  const detectDevice = useCallback(() => {
    const width = window.innerWidth;
    if (width < 480) return 'mobile';
    if (width < 768) return 'tablet';
    return 'desktop';
  }, []);

  // Connection quality detection
  const detectConnection = useCallback(() => {
    if ('connection' in navigator) {
      const connection = navigator.connection;
      return {
        effectiveType: connection.effectiveType,
        downlink: connection.downlink,
        rtt: connection.rtt,
        saveData: connection.saveData
      };
    }
    return { effectiveType: 'unknown' };
  }, []);

  // WordPress context detection
  const detectWordPressContext = useCallback(() => {
    // Check for WordPress-specific globals and elements
    const wpContext = {
      isWordPress: typeof window.wp !== 'undefined',
      isAdmin: document.body.classList.contains('wp-admin'),
      isCustomizer: window.parent !== window && window.name === 'customize-preview',
      theme: document.body.className.match(/theme-([^\s]+)/)?.[1] || 'unknown',
      postId: document.querySelector('meta[property="article:id"]')?.content || null,
      userId: window.syllaflowData?.userId || null,
      nonce: window.syllaflowData?.nonce || null,
      restUrl: window.syllaflowData?.restUrl || '/wp-json/syllaflow/v1/',
      ajaxUrl: window.syllaflowData?.ajaxUrl || '/wp-admin/admin-ajax.php'
    };

    // Check for AlignFlow journal integration
    wpContext.alignFlowActive = document.querySelector('.alignflow-journal') !== null;
    wpContext.wooCommerceActive = typeof window.wc_add_to_cart_params !== 'undefined';

    return wpContext;
  }, []);

  // Performance monitoring
  const measurePerformance = useCallback(() => {
    if ('performance' in window) {
      const navigation = performance.getEntriesByType('navigation')[0];
      const paint = performance.getEntriesByType('paint');
      
      const metrics = {
        domContentLoaded: navigation?.domContentLoadedEventEnd - navigation?.domContentLoadedEventStart,
        loadComplete: navigation?.loadEventEnd - navigation?.loadEventStart,
        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime,
        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
        memoryUsage: performance.memory ? {
          used: performance.memory.usedJSHeapSize,
          total: performance.memory.totalJSHeapSize,
          limit: performance.memory.jsHeapSizeLimit
        } : null
      };

      setEmbedState(prev => ({ ...prev, performanceMetrics: metrics }));
      onPerformanceMetric?.(metrics);
    }
  }, [onPerformanceMetric]);

  // Intersection Observer for visibility tracking
  useEffect(() => {
    if (!containerRef.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        const isIntersecting = entry.isIntersecting;
        
        setEmbedState(prev => ({ 
          ...prev, 
          isVisible: isIntersecting,
          isIntersecting 
        }));
        
        onVisibilityChange?.(isIntersecting);

        // Lazy load resources when visible
        if (isIntersecting && !embedState.isVisible) {
          measurePerformance();
        }
      },
      { 
        threshold: [0, 0.25, 0.5, 0.75, 1],
        rootMargin: '50px'
      }
    );

    observer.observe(containerRef.current);

    return () => observer.disconnect();
  }, [embedState.isVisible, measurePerformance, onVisibilityChange]);

  // Resize Observer for responsive updates
  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0];
      const { width, height } = entry.contentRect;
      
      setEmbedState(prev => ({
        ...prev,
        containerSize: { width, height },
        deviceType: detectDevice()
      }));
      
      onResize?.({ width, height, deviceType: detectDevice() });
    });

    resizeObserver.observe(containerRef.current);

    return () => resizeObserver.disconnect();
  }, [detectDevice, onResize]);

  // Initialize embed state
  useEffect(() => {
    setEmbedState(prev => ({
      ...prev,
      deviceType: detectDevice(),
      connectionType: detectConnection(),
      wordPressContext: detectWordPressContext()
    }));

    // Listen for WordPress events
    if (window.wp?.hooks) {
      const handleWordPressEvent = (data) => {
        setEmbedState(prev => ({
          ...prev,
          wordPressContext: { ...prev.wordPressContext, ...data }
        }));
      };

      window.wp.hooks.addAction('syllaflow.contextUpdate', 'syllaflow/embed', handleWordPressEvent);
      
      return () => {
        window.wp.hooks.removeAction('syllaflow.contextUpdate', 'syllaflow/embed');
      };
    }
  }, [detectDevice, detectConnection, detectWordPressContext]);

  // Connection change listener
  useEffect(() => {
    if ('connection' in navigator) {
      const handleConnectionChange = () => {
        setEmbedState(prev => ({
          ...prev,
          connectionType: detectConnection()
        }));
      };

      navigator.connection.addEventListener('change', handleConnectionChange);
      
      return () => {
        navigator.connection.removeEventListener('change', handleConnectionChange);
      };
    }
  }, [detectConnection]);

  // Optimize rendering based on device and connection
  const shouldReduceAnimations = embedState.connectionType.saveData || 
                                 embedState.connectionType.effectiveType === 'slow-2g' ||
                                 embedState.connectionType.effectiveType === '2g';

  const shouldLazyLoad = !embedState.isIntersecting && embedState.deviceType === 'mobile';

  // CSS classes for optimization
  const optimizationClasses = [
    'syllaflow-embed-optimized',
    `device-${embedState.deviceType}`,
    `connection-${embedState.connectionType.effectiveType}`,
    shouldReduceAnimations ? 'reduce-animations' : '',
    shouldLazyLoad ? 'lazy-load' : '',
    embedState.isVisible ? 'visible' : 'hidden',
    embedState.wordPressContext?.isWordPress ? 'wordpress-context' : '',
    embedState.wordPressContext?.alignFlowActive ? 'alignflow-active' : ''
  ].filter(Boolean).join(' ');

  // Inline styles for responsive optimization
  const optimizationStyles = {
    '--container-width': `${embedState.containerSize.width}px`,
    '--container-height': `${embedState.containerSize.height}px`,
    '--device-type': embedState.deviceType,
    '--connection-speed': embedState.connectionType.effectiveType,
    '--animation-duration': shouldReduceAnimations ? '0.1s' : '0.3s',
    '--transition-duration': shouldReduceAnimations ? '0.05s' : '0.15s'
  };

  return (
    <div
      ref={containerRef}
      className={optimizationClasses}
      style={optimizationStyles}
      data-embed-config={JSON.stringify(config)}
      data-performance-metrics={JSON.stringify(embedState.performanceMetrics)}
      data-wordpress-context={JSON.stringify(embedState.wordPressContext)}
    >
      {/* Performance monitoring overlay (development only) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="syllaflow-debug-overlay">
          <div className="debug-info">
            <div>Device: {embedState.deviceType}</div>
            <div>Connection: {embedState.connectionType.effectiveType}</div>
            <div>Size: {embedState.containerSize.width}x{embedState.containerSize.height}</div>
            <div>Visible: {embedState.isVisible ? 'Yes' : 'No'}</div>
            <div>WordPress: {embedState.wordPressContext?.isWordPress ? 'Yes' : 'No'}</div>
          </div>
        </div>
      )}

      {/* Lazy loading placeholder */}
      {shouldLazyLoad ? (
        <div className="syllaflow-lazy-placeholder">
          <div className="lazy-loading-indicator">
            <div className="loading-spinner"></div>
            <p>Loading SyllaFlow...</p>
          </div>
        </div>
      ) : (
        children
      )}
    </div>
  );
};

/**
 * WordPress Integration Hook
 * Provides WordPress-specific functionality and data synchronization
 */
export const useWordPressIntegration = () => {
  const [wpData, setWpData] = useState({
    isConnected: false,
    user: null,
    nonce: null,
    restUrl: null,
    ajaxUrl: null
  });

  useEffect(() => {
    // Initialize WordPress connection
    if (typeof window.syllaflowData !== 'undefined') {
      setWpData({
        isConnected: true,
        user: {
          id: window.syllaflowData.userId,
          isLoggedIn: window.syllaflowData.isLoggedIn
        },
        nonce: window.syllaflowData.nonce,
        restUrl: window.syllaflowData.restUrl,
        ajaxUrl: window.syllaflowData.ajaxUrl
      });
    }
  }, []);

  const makeRestRequest = useCallback(async (endpoint, options = {}) => {
    if (!wpData.isConnected) {
      throw new Error('WordPress integration not available');
    }

    const url = `${wpData.restUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      'X-WP-Nonce': wpData.nonce,
      ...options.headers
    };

    const response = await fetch(url, {
      ...options,
      headers
    });

    if (!response.ok) {
      throw new Error(`WordPress API request failed: ${response.statusText}`);
    }

    return response.json();
  }, [wpData]);

  const makeAjaxRequest = useCallback(async (action, data = {}) => {
    if (!wpData.isConnected) {
      throw new Error('WordPress integration not available');
    }

    const formData = new FormData();
    formData.append('action', action);
    formData.append('nonce', wpData.nonce);
    
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, typeof value === 'object' ? JSON.stringify(value) : value);
    });

    const response = await fetch(wpData.ajaxUrl, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`WordPress AJAX request failed: ${response.statusText}`);
    }

    return response.json();
  }, [wpData]);

  return {
    isConnected: wpData.isConnected,
    user: wpData.user,
    makeRestRequest,
    makeAjaxRequest
  };
};

/**
 * Performance Optimization Hook
 * Monitors and optimizes performance based on device capabilities
 */
export const usePerformanceOptimization = () => {
  const [optimization, setOptimization] = useState({
    shouldReduceAnimations: false,
    shouldLazyLoad: false,
    shouldPreloadAssets: true,
    maxConcurrentRequests: 6,
    imageQuality: 'high'
  });

  useEffect(() => {
    // Detect device capabilities
    const detectCapabilities = () => {
      const connection = navigator.connection;
      const memory = navigator.deviceMemory;
      const cores = navigator.hardwareConcurrency;

      const isLowEnd = memory && memory < 4;
      const isSlowConnection = connection && 
        (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g');
      const isSaveData = connection && connection.saveData;

      setOptimization({
        shouldReduceAnimations: isLowEnd || isSlowConnection || isSaveData,
        shouldLazyLoad: isLowEnd || isSlowConnection,
        shouldPreloadAssets: !isSlowConnection && !isSaveData,
        maxConcurrentRequests: isLowEnd ? 2 : isSlowConnection ? 3 : 6,
        imageQuality: isSlowConnection || isSaveData ? 'low' : 'high'
      });
    };

    detectCapabilities();

    // Listen for connection changes
    if (navigator.connection) {
      navigator.connection.addEventListener('change', detectCapabilities);
      return () => navigator.connection.removeEventListener('change', detectCapabilities);
    }
  }, []);

  return optimization;
};

/**
 * Responsive Design Hook
 * Handles responsive behavior and breakpoint management
 */
export const useResponsiveDesign = () => {
  const [responsive, setResponsive] = useState({
    breakpoint: 'desktop',
    orientation: 'landscape',
    viewportSize: { width: 0, height: 0 },
    isTouch: false,
    pixelRatio: 1
  });

  useEffect(() => {
    const updateResponsive = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      let breakpoint = 'desktop';
      if (width < 480) breakpoint = 'mobile';
      else if (width < 768) breakpoint = 'tablet';
      else if (width < 1024) breakpoint = 'laptop';

      setResponsive({
        breakpoint,
        orientation: width > height ? 'landscape' : 'portrait',
        viewportSize: { width, height },
        isTouch: 'ontouchstart' in window,
        pixelRatio: window.devicePixelRatio || 1
      });
    };

    updateResponsive();
    window.addEventListener('resize', updateResponsive);
    window.addEventListener('orientationchange', updateResponsive);

    return () => {
      window.removeEventListener('resize', updateResponsive);
      window.removeEventListener('orientationchange', updateResponsive);
    };
  }, []);

  return responsive;
};

export default EmbedOptimization;
