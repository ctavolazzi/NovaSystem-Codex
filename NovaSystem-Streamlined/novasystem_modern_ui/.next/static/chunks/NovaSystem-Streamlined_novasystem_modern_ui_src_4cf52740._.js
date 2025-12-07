(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "NAVIGATION_CONFIG",
    ()=>NAVIGATION_CONFIG,
    "NavigationProvider",
    ()=>NavigationProvider,
    "useNavigation",
    ()=>useNavigation
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/navigation.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
'use client';
;
;
const NAVIGATION_CONFIG = {
    main: [
        {
            id: 'home',
            label: 'Home',
            url: '/',
            icon: '🏠'
        },
        {
            id: 'workflow',
            label: 'Workflow',
            url: '/workflow',
            icon: '⚡'
        },
        {
            id: 'analytics',
            label: 'Analytics',
            url: '/analytics',
            icon: '📊'
        },
        {
            id: 'monitor',
            label: 'Monitor',
            url: '/monitor',
            icon: '📈'
        }
    ],
    tools: [
        {
            id: 'settings',
            label: 'Settings',
            url: '/settings',
            icon: '⚙️'
        },
        {
            id: 'help',
            label: 'Help',
            url: '/help',
            icon: '❓'
        },
        {
            id: 'about',
            label: 'About',
            url: '/about',
            icon: 'ℹ️'
        }
    ],
    sessions: [
        {
            id: 'active_sessions',
            label: 'Active Sessions',
            url: '/sessions',
            icon: '🔄'
        },
        {
            id: 'session_history',
            label: 'History',
            url: '/history',
            icon: '📋'
        }
    ]
};
const NavigationContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useNavigation = ()=>{
    _s();
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useContext"])(NavigationContext);
    if (!context) {
        throw new Error('useNavigation must be used within a NavigationProvider');
    }
    return context;
};
_s(useNavigation, "b9L3QQ+jgeyIrH0NfHrJ8nn7VMU=");
const NavigationProvider = (param)=>{
    let { children } = param;
    _s1();
    const pathname = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePathname"])();
    const [isMobile, setIsMobile] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [isTablet, setIsTablet] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [sidebarOpen, setSidebarOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    // Detect current page
    const detectCurrentPage = (path)=>{
        const routeMap = {
            '/': 'home',
            '/workflow': 'workflow',
            '/analytics': 'analytics',
            '/monitor': 'monitor',
            '/settings': 'settings',
            '/help': 'help',
            '/about': 'about',
            '/sessions': 'active_sessions',
            '/history': 'session_history'
        };
        return routeMap[path] || 'home';
    };
    const currentPage = detectCurrentPage(pathname);
    // Navigation helper function
    const navigateToPage = (url)=>{
        if ("TURBOPACK compile-time truthy", 1) {
            window.location.href = url;
        }
    };
    // Handle responsive design with comprehensive breakpoints
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "NavigationProvider.useEffect": ()=>{
            const handleResize = {
                "NavigationProvider.useEffect.handleResize": ()=>{
                    if ("TURBOPACK compile-time truthy", 1) {
                        const width = window.innerWidth;
                        const height = window.innerHeight;
                        // Enhanced breakpoint detection
                        setIsMobile(width <= 767);
                        setIsTablet(width > 767 && width <= 1024);
                        // Add viewport meta tag if on mobile
                        if (width <= 767) {
                            const viewport = document.querySelector('meta[name="viewport"]');
                            if (!viewport) {
                                const meta = document.createElement('meta');
                                meta.name = 'viewport';
                                meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                                document.head.appendChild(meta);
                            }
                        }
                        // Handle orientation changes
                        if (width <= 767) {
                            const isLandscape = width > height;
                            document.body.classList.toggle('landscape', isLandscape);
                            document.body.classList.toggle('portrait', !isLandscape);
                        }
                    }
                }
            }["NavigationProvider.useEffect.handleResize"];
            handleResize();
            window.addEventListener('resize', handleResize);
            window.addEventListener('orientationchange', handleResize);
            return ({
                "NavigationProvider.useEffect": ()=>{
                    window.removeEventListener('resize', handleResize);
                    window.removeEventListener('orientationchange', handleResize);
                }
            })["NavigationProvider.useEffect"];
        }
    }["NavigationProvider.useEffect"], []);
    // Handle orientation change on mobile
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "NavigationProvider.useEffect": ()=>{
            const handleOrientationChange = {
                "NavigationProvider.useEffect.handleOrientationChange": ()=>{
                    setTimeout({
                        "NavigationProvider.useEffect.handleOrientationChange": ()=>{
                            if ("TURBOPACK compile-time truthy", 1) {
                                const width = window.innerWidth;
                                setIsMobile(width <= 768);
                                setIsTablet(width > 768 && width <= 1024);
                            }
                        }
                    }["NavigationProvider.useEffect.handleOrientationChange"], 100);
                }
            }["NavigationProvider.useEffect.handleOrientationChange"];
            window.addEventListener('orientationchange', handleOrientationChange);
            return ({
                "NavigationProvider.useEffect": ()=>window.removeEventListener('orientationchange', handleOrientationChange)
            })["NavigationProvider.useEffect"];
        }
    }["NavigationProvider.useEffect"], []);
    // Keyboard shortcuts
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "NavigationProvider.useEffect": ()=>{
            const handleKeyDown = {
                "NavigationProvider.useEffect.handleKeyDown": (e)=>{
                    if (e.ctrlKey || e.metaKey) {
                        switch(e.key){
                            case '1':
                                e.preventDefault();
                                navigateToPage('/');
                                break;
                            case '2':
                                e.preventDefault();
                                navigateToPage('/workflow');
                                break;
                            case '3':
                                e.preventDefault();
                                navigateToPage('/analytics');
                                break;
                            case '4':
                                e.preventDefault();
                                navigateToPage('/monitor');
                                break;
                        }
                    }
                }
            }["NavigationProvider.useEffect.handleKeyDown"];
            document.addEventListener('keydown', handleKeyDown);
            return ({
                "NavigationProvider.useEffect": ()=>document.removeEventListener('keydown', handleKeyDown)
            })["NavigationProvider.useEffect"];
        }
    }["NavigationProvider.useEffect"], []);
    // Touch gestures for mobile
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "NavigationProvider.useEffect": ()=>{
            if (!isMobile) return;
            let startX = 0;
            let startY = 0;
            const handleTouchStart = {
                "NavigationProvider.useEffect.handleTouchStart": (e)=>{
                    startX = e.touches[0].clientX;
                    startY = e.touches[0].clientY;
                }
            }["NavigationProvider.useEffect.handleTouchStart"];
            const handleTouchEnd = {
                "NavigationProvider.useEffect.handleTouchEnd": (e)=>{
                    const endX = e.changedTouches[0].clientX;
                    const endY = e.changedTouches[0].clientY;
                    const diffX = startX - endX;
                    const diffY = startY - endY;
                    // Check if horizontal swipe
                    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                        const pages = NAVIGATION_CONFIG.main;
                        const currentIndex = pages.findIndex({
                            "NavigationProvider.useEffect.handleTouchEnd.currentIndex": (page)=>page.id === currentPage
                        }["NavigationProvider.useEffect.handleTouchEnd.currentIndex"]);
                        if (diffX > 0 && currentIndex < pages.length - 1) {
                            // Swipe left - next page
                            navigateToPage(pages[currentIndex + 1].url);
                        } else if (diffX < 0 && currentIndex > 0) {
                            // Swipe right - previous page
                            navigateToPage(pages[currentIndex - 1].url);
                        }
                    }
                }
            }["NavigationProvider.useEffect.handleTouchEnd"];
            document.addEventListener('touchstart', handleTouchStart, {
                passive: true
            });
            document.addEventListener('touchend', handleTouchEnd, {
                passive: true
            });
            return ({
                "NavigationProvider.useEffect": ()=>{
                    document.removeEventListener('touchstart', handleTouchStart);
                    document.removeEventListener('touchend', handleTouchEnd);
                }
            })["NavigationProvider.useEffect"];
        }
    }["NavigationProvider.useEffect"], [
        isMobile,
        currentPage
    ]);
    const value = {
        currentPage,
        isMobile,
        isTablet,
        sidebarOpen,
        setSidebarOpen,
        navigationConfig: NAVIGATION_CONFIG,
        navigateToPage
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(NavigationContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx",
        lineNumber: 219,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s1(NavigationProvider, "/4Pan65Ni3Whyq2ulir2n6Uxw4A=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePathname"]
    ];
});
_c = NavigationProvider;
var _c;
__turbopack_context__.k.register(_c, "NavigationProvider");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "StreamingProvider",
    ()=>StreamingProvider,
    "useStreaming",
    ()=>useStreaming
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
'use client';
;
const SimpleStreamingContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useStreaming = ()=>{
    _s();
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useContext"])(SimpleStreamingContext);
    if (!context) {
        // Return a default context to prevent hydration errors
        return {
            responses: [],
            addResponse: ()=>{},
            clearResponses: ()=>{},
            isStreaming: false,
            setIsStreaming: ()=>{},
            connectionStatus: 'disconnected',
            searchFilter: '',
            setSearchFilter: ()=>{}
        };
    }
    return context;
};
_s(useStreaming, "b9L3QQ+jgeyIrH0NfHrJ8nn7VMU=");
const StreamingProvider = (param)=>{
    let { children } = param;
    _s1();
    const [responses, setResponses] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [isStreaming, setIsStreaming] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [connectionStatus, setConnectionStatus] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('connected');
    const [searchFilter, setSearchFilter] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [isClient, setIsClient] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    // Ensure we're on the client side to prevent hydration mismatches
    __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].useEffect({
        "StreamingProvider.useEffect": ()=>{
            setIsClient(true);
        }
    }["StreamingProvider.useEffect"], []);
    const addResponse = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "StreamingProvider.useCallback[addResponse]": (newResponse)=>{
            setResponses({
                "StreamingProvider.useCallback[addResponse]": (prevResponses)=>{
                    const existingIndex = prevResponses.findIndex({
                        "StreamingProvider.useCallback[addResponse].existingIndex": (res)=>res.agentId === newResponse.agentId && res.status === 'streaming'
                    }["StreamingProvider.useCallback[addResponse].existingIndex"]);
                    if (existingIndex !== -1) {
                        const updatedResponses = [
                            ...prevResponses
                        ];
                        updatedResponses[existingIndex] = {
                            ...updatedResponses[existingIndex],
                            content: newResponse.content,
                            timestamp: newResponse.timestamp,
                            status: newResponse.status
                        };
                        return updatedResponses;
                    } else {
                        return [
                            ...prevResponses,
                            newResponse
                        ];
                    }
                }
            }["StreamingProvider.useCallback[addResponse]"]);
        }
    }["StreamingProvider.useCallback[addResponse]"], []);
    const clearResponses = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "StreamingProvider.useCallback[clearResponses]": ()=>{
            setResponses([]);
        }
    }["StreamingProvider.useCallback[clearResponses]"], []);
    const value = {
        responses,
        addResponse,
        clearResponses,
        isStreaming,
        setIsStreaming,
        connectionStatus,
        searchFilter,
        setSearchFilter
    };
    // Don't render streaming context on server side to prevent hydration mismatches
    if (!isClient) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
            children: children
        }, void 0, false);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(SimpleStreamingContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx",
        lineNumber: 95,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s1(StreamingProvider, "4NwOEmPBlQgm/45Mv7EsB2f9U3A=");
_c = StreamingProvider;
var _c;
__turbopack_context__.k.register(_c, "StreamingProvider");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Sidebar",
    ()=>Sidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
const Sidebar = (param)=>{
    let { className, children } = param;
    _s();
    const { currentPage, isMobile, navigationConfig } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"])();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("xp-sidebar xp-scrollbar flex", isMobile ? "w-full h-auto flex-row overflow-x-auto overflow-y-hidden border-b border-r-0 nav-mobile" : "w-50 h-full flex-col border-r", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: cn("border-[var(--border-light)] flex-shrink-0", isMobile ? "min-w-32 max-w-40 p-1 border-r border-b-0" : "w-full p-2 border-b"),
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title sm:hidden lg:block",
                        children: "Navigation"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 31,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: cn(isMobile ? "flex gap-2" : "space-y-1"),
                        children: navigationConfig.main.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: cn("xp-sidebar-item", isMobile ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item" : "px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: cn("bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white", isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"),
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 49,
                                        columnNumber: 19
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: item.label
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 55,
                                        columnNumber: 33
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, item.id, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 38,
                                columnNumber: 17
                            }, ("TURBOPACK compile-time value", void 0)))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 34,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 25,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            !isMobile && [
                'workflow',
                'home',
                'active_sessions',
                'session_history'
            ].includes(currentPage) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-2 border-b border-[var(--border-light)] sm:hidden lg:block",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-xs font-bold text-[var(--text-primary)] mb-2 px-1",
                        children: "Sessions"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 64,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-1",
                        children: navigationConfig.sessions.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: cn("xp-sidebar-item px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "w-5 h-5 bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-xs text-white",
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 77,
                                        columnNumber: 21
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: item.label
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 80,
                                        columnNumber: 21
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, item.id, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 69,
                                columnNumber: 19
                            }, ("TURBOPACK compile-time value", void 0)))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 67,
                        columnNumber: 15
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 63,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: cn("p-2 border-b border-[var(--border-light)]", isMobile ? "min-w-50 border-r border-b-0 mr-2" : "border-b"),
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title sm:hidden lg:block",
                        children: "Tools"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 92,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: cn(isMobile ? "flex gap-2" : "space-y-1"),
                        children: navigationConfig.tools.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: cn("xp-sidebar-item", isMobile ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item" : "px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: cn("bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white", isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"),
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 110,
                                        columnNumber: 19
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: item.label
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 116,
                                        columnNumber: 33
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, item.id, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 99,
                                columnNumber: 17
                            }, ("TURBOPACK compile-time value", void 0)))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 95,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 88,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            children && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 p-2",
                children: children
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 124,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "min-w-50 p-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title",
                        children: "Quick Actions"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 132,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-0.5",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "🔄"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 137,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "Refresh"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 138,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 136,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "⛶"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 141,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "Fullscreen"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 142,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 140,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "⚙️"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 145,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "Settings"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 146,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                lineNumber: 144,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 135,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 131,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
        lineNumber: 17,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(Sidebar, "oxT4Chk1Nfk2/vdjKH4nMNDd17Y=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"]
    ];
});
_c = Sidebar;
var _c;
__turbopack_context__.k.register(_c, "Sidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MenuBar",
    ()=>MenuBar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
const MenuBar = (param)=>{
    let { className } = param;
    _s();
    const { currentPage, navigationConfig } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"])();
    const [activeDropdown, setActiveDropdown] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [hoverTimeout, setHoverTimeout] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const getCurrentPageTitle = ()=>{
        const allItems = [
            ...navigationConfig.main,
            ...navigationConfig.tools,
            ...navigationConfig.sessions
        ];
        const currentItem = allItems.find((item)=>item.id === currentPage);
        return (currentItem === null || currentItem === void 0 ? void 0 : currentItem.label) || 'NovaSystem';
    };
    const handleDropdownToggle = (menuName)=>{
        setActiveDropdown(activeDropdown === menuName ? null : menuName);
    };
    const handleDropdownClose = ()=>{
        setActiveDropdown(null);
    };
    const handleMouseEnter = (menuName)=>{
        // Clear any existing timeout
        if (hoverTimeout) {
            clearTimeout(hoverTimeout);
        }
        // Set a new timeout to open dropdown after 2 seconds
        const timeout = setTimeout(()=>{
            setActiveDropdown(menuName);
        }, 2000);
        setHoverTimeout(timeout);
    };
    const handleMouseLeave = ()=>{
        // Clear timeout when mouse leaves
        if (hoverTimeout) {
            clearTimeout(hoverTimeout);
            setHoverTimeout(null);
        }
    };
    // Close dropdowns when clicking outside
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "MenuBar.useEffect": ()=>{
            const handleClickOutside = {
                "MenuBar.useEffect.handleClickOutside": (event)=>{
                    if (activeDropdown) {
                        const target = event.target;
                        if (!target.closest('.menu-item-container')) {
                            setActiveDropdown(null);
                        }
                    }
                }
            }["MenuBar.useEffect.handleClickOutside"];
            document.addEventListener('mousedown', handleClickOutside);
            return ({
                "MenuBar.useEffect": ()=>document.removeEventListener('mousedown', handleClickOutside)
            })["MenuBar.useEffect"];
        }
    }["MenuBar.useEffect"], [
        activeDropdown
    ]);
    // Cleanup timeout on unmount
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "MenuBar.useEffect": ()=>{
            return ({
                "MenuBar.useEffect": ()=>{
                    if (hoverTimeout) {
                        clearTimeout(hoverTimeout);
                    }
                }
            })["MenuBar.useEffect"];
        }
    }["MenuBar.useEffect"], [
        hoverTimeout
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("xp-menubar", "relative z-[var(--z-index-menubar)]", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('file'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: cn("xp-menu-item", activeDropdown === 'file' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('file'),
                                children: "File"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 93,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("dropdown-menu", activeDropdown === 'file' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "New Session"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 106,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Save Session"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 109,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Export Data"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 112,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 115,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Exit"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 116,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 102,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                        lineNumber: 88,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('edit'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: cn("xp-menu-item", activeDropdown === 'edit' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('edit'),
                                children: "Edit"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 128,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("dropdown-menu", activeDropdown === 'edit' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Undo"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 141,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Redo"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 144,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 147,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Clear"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 148,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 137,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                        lineNumber: 123,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('view'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: cn("xp-menu-item", activeDropdown === 'view' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('view'),
                                children: "View"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 160,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("dropdown-menu", activeDropdown === 'view' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Refresh"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 173,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Full Screen"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 176,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 179,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Zoom In"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 180,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Zoom Out"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 183,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 169,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                        lineNumber: 155,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('tools'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: cn("xp-menu-item", activeDropdown === 'tools' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('tools'),
                                children: "Tools"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 195,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("dropdown-menu", activeDropdown === 'tools' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Session Manager"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 208,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Analytics"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 211,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Monitor"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 214,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 217,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Settings"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 218,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 204,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                        lineNumber: 190,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('help'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: cn("xp-menu-item", activeDropdown === 'help' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('help'),
                                children: "Help"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 230,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("dropdown-menu", activeDropdown === 'help' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Help Topics"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 243,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Keyboard Shortcuts"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 246,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 249,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "About NovaSystem"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 250,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 239,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                        lineNumber: 225,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                lineNumber: 86,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "ml-auto text-[var(--text-primary)] font-bold",
                children: getCurrentPageTitle()
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                lineNumber: 258,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
        lineNumber: 81,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(MenuBar, "5gxhyRegwm+aPQts/2+UNpqrH6M=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"]
    ];
});
_c = MenuBar;
var _c;
__turbopack_context__.k.register(_c, "MenuBar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Taskbar",
    ()=>Taskbar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
const Taskbar = (param)=>{
    let { className } = param;
    _s();
    const { navigationConfig, isMobile } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"])();
    const [currentTime, setCurrentTime] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(new Date());
    const [showStartMenu, setShowStartMenu] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    // Update time every second
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Taskbar.useEffect": ()=>{
            const timer = setInterval({
                "Taskbar.useEffect.timer": ()=>{
                    setCurrentTime(new Date());
                }
            }["Taskbar.useEffect.timer"], 1000);
            return ({
                "Taskbar.useEffect": ()=>clearInterval(timer)
            })["Taskbar.useEffect"];
        }
    }["Taskbar.useEffect"], []);
    // Close start menu when clicking outside
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Taskbar.useEffect": ()=>{
            const handleClickOutside = {
                "Taskbar.useEffect.handleClickOutside": (event)=>{
                    if (showStartMenu) {
                        const target = event.target;
                        if (!target.closest('.start-menu-container')) {
                            setShowStartMenu(false);
                        }
                    }
                }
            }["Taskbar.useEffect.handleClickOutside"];
            document.addEventListener('mousedown', handleClickOutside);
            return ({
                "Taskbar.useEffect": ()=>document.removeEventListener('mousedown', handleClickOutside)
            })["Taskbar.useEffect"];
        }
    }["Taskbar.useEffect"], [
        showStartMenu
    ]);
    const formatTime = (date)=>{
        return date.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    };
    const formatDate = (date)=>{
        return date.toLocaleDateString([], {
            month: 'short',
            day: 'numeric'
        });
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("bg-gradient-to-b from-[var(--bg-secondary)] to-[#d6d3ce] border-t border-[var(--border-3d-dark)] shadow-inner", "flex items-center justify-between px-2", "relative z-[var(--z-index-taskbar)]", isMobile ? "relative h-12 flex-wrap gap-2" : "absolute bottom-0 left-0 right-0 h-10", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "relative start-menu-container",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>setShowStartMenu(!showStartMenu),
                        className: cn("xp-button flex items-center text-[var(--text-primary)] cursor-pointer", "bg-gradient-to-b from-[var(--bg-primary)] to-[var(--bg-secondary)]", "hover:bg-gradient-to-b hover:from-[var(--bg-hover)] hover:to-[var(--bg-secondary)]", showStartMenu && "bg-gradient-to-b from-[var(--primary-blue)] to-[var(--primary-blue-hover)] text-white", isMobile ? "gap-1 px-2 py-1.5 text-[10px] min-h-[32px]" : "gap-1.5 px-3 py-1.5 text-xs min-h-[32px]"),
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: cn("bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm", isMobile ? "w-3 h-3" : "w-4 h-4")
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 79,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Start"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 83,
                                columnNumber: 25
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                        lineNumber: 67,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    showStartMenu && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "absolute bottom-full left-0 mb-2 bg-[var(--bg-primary)] border border-[var(--border-light)] shadow-lg z-[var(--z-index-taskbar-dropdown)] min-w-48 rounded-md",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "p-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-xs font-bold text-[var(--text-primary)] mb-2",
                                    children: "NovaSystem v3.0"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 90,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "space-y-0.5",
                                    children: navigationConfig.main.slice(0, 4).map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = item.url;
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-3 py-2 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-blue)] hover:text-white cursor-pointer flex items-center gap-2 rounded-sm transition-colors",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-sm",
                                                    children: item.icon
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 101,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: item.label
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 102,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0))
                                            ]
                                        }, item.id, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                            lineNumber: 93,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)))
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 91,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "border-t border-[var(--border-inset)] my-1"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 106,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "space-y-0.5",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = '/settings';
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "⚙️"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 115,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "Settings"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 116,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0))
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                            lineNumber: 108,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = '/help';
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "❓"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 125,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "Help"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 126,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0))
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                            lineNumber: 118,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 107,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                            lineNumber: 89,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                        lineNumber: 88,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                lineNumber: 66,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex gap-1 ml-2",
                children: navigationConfig.main.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>window.location.href = item.url,
                        className: "flex items-center gap-1 px-2 py-1 text-xs text-[var(--text-primary)] cursor-pointer bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "text-xs",
                            children: item.icon
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                            lineNumber: 143,
                            columnNumber: 15
                        }, ("TURBOPACK compile-time value", void 0))
                    }, item.id, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                        lineNumber: 138,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)))
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                lineNumber: 136,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-1 ml-auto",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-1 px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-2 h-2 bg-green-500 rounded-full animate-pulse"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 153,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-xs text-[var(--text-primary)]",
                                children: "Ready"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 154,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                        lineNumber: 152,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] text-xs text-[var(--text-primary)] cursor-pointer hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "text-center",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "font-bold",
                                    children: formatTime(currentTime)
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 160,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-[10px]",
                                    children: formatDate(currentTime)
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 161,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                            lineNumber: 159,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                        lineNumber: 158,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                lineNumber: 150,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
        lineNumber: 56,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(Taskbar, "omYehcNFC8T/kbZRzPGF54klclQ=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useNavigation"]
    ];
});
_c = Taskbar;
var _c;
__turbopack_context__.k.register(_c, "Taskbar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Window",
    ()=>Window
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
'use client';
;
;
const Window = (param)=>{
    let { title, icon, children, className, onMinimize, onMaximize, onClose } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("absolute top-2.5 left-2.5 right-2.5 bottom-10", "bg-[var(--bg-window)] border-2 border-[var(--border-3d-dark)]", "shadow-[2px_2px_4px_rgba(0,0,0,0.3)]", "flex flex-col xp-window-open", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "xp-titlebar",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-titlebar-title",
                        children: [
                            icon && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm flex items-center justify-center text-[10px] text-white font-bold",
                                children: "N"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 37,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: title
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 41,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                        lineNumber: 35,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-titlebar-controls",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: onMinimize,
                                className: "xp-window-control",
                                title: "Minimize",
                                children: "_"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 44,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: onMaximize,
                                className: "xp-window-control",
                                title: "Maximize",
                                children: "□"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 51,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: onClose,
                                className: "xp-window-control close",
                                title: "Close",
                                children: "×"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 58,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                        lineNumber: 43,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                lineNumber: 34,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            children
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
        lineNumber: 26,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = Window;
var _c;
__turbopack_context__.k.register(_c, "Window");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ResponsiveTest",
    ()=>ResponsiveTest
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
const PRESET_SIZES = [
    {
        name: 'iPhone SE',
        width: 375,
        height: 667
    },
    {
        name: 'iPhone 12',
        width: 390,
        height: 844
    },
    {
        name: 'iPhone 12 Pro Max',
        width: 428,
        height: 926
    },
    {
        name: 'iPad Mini',
        width: 768,
        height: 1024
    },
    {
        name: 'iPad Air',
        width: 820,
        height: 1180
    },
    {
        name: 'iPad Pro',
        width: 1024,
        height: 1366
    },
    {
        name: 'Desktop Small',
        width: 1280,
        height: 720
    },
    {
        name: 'Desktop Medium',
        width: 1440,
        height: 900
    },
    {
        name: 'Desktop Large',
        width: 1920,
        height: 1080
    },
    {
        name: 'Ultra-wide',
        width: 2560,
        height: 1440
    }
];
const ResponsiveTest = (param)=>{
    let { className } = param;
    _s();
    const [isOpen, setIsOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [currentSize, setCurrentSize] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        width: 0,
        height: 0
    });
    const applySize = (width, height)=>{
        if ("TURBOPACK compile-time truthy", 1) {
            // Apply viewport size for testing
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', "width=".concat(width, ", initial-scale=1.0"));
            }
            // Update document body classes for responsive testing
            document.body.style.width = "".concat(width, "px");
            document.body.style.height = "".concat(height, "px");
            document.body.style.overflow = 'auto';
            setCurrentSize({
                width,
                height
            });
        }
    };
    const resetSize = ()=>{
        if ("TURBOPACK compile-time truthy", 1) {
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0');
            }
            document.body.style.width = '';
            document.body.style.height = '';
            document.body.style.overflow = '';
            setCurrentSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        }
    };
    const getCurrentBreakpoint = ()=>{
        const width = currentSize.width || (("TURBOPACK compile-time truthy", 1) ? window.innerWidth : "TURBOPACK unreachable");
        if (width >= 1920) return 'Ultra-wide (1920px+)';
        if (width >= 1440) return 'Extra Large (1440px+)';
        if (width >= 1200) return 'Large (1200px-1439px)';
        if (width >= 1024) return 'Desktop (1024px-1199px)';
        if (width >= 768) return 'Tablet Landscape (768px-1023px)';
        if (width >= 640) return 'Tablet Portrait (640px-767px)';
        if (width >= 480) return 'Mobile Large (480px-639px)';
        if (width >= 375) return 'Mobile Medium (375px-479px)';
        return 'Mobile Small (320px-374px)';
    };
    if (!isOpen) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
            onClick: ()=>setIsOpen(true),
            className: cn("fixed bottom-20 right-4 z-50 bg-[var(--primary-color)] text-white", "px-3 py-2 text-xs rounded-sm shadow-lg hover:bg-[var(--secondary-color)]", "border border-[var(--border-inset)]", className),
            children: "📱 Test Responsive"
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
            lineNumber: 75,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0));
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "bg-[var(--bg-window)] border border-[var(--border-inset)] rounded-sm max-w-4xl w-full max-h-[80vh] overflow-auto",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-b border-[var(--border-inset)]",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex justify-between items-center",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                className: "text-lg font-bold text-[var(--text-primary)]",
                                children: "📱 Responsive Design Tester"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 95,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>setIsOpen(false),
                                className: "text-gray-500 hover:text-gray-700",
                                children: "✕"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 98,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                        lineNumber: 94,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                    lineNumber: 93,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-b border-[var(--border-inset)]",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-2 gap-4 text-sm",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: "Current Size:"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                        lineNumber: 111,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    " ",
                                    currentSize.width,
                                    " × ",
                                    currentSize.height
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 110,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: "Breakpoint:"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                        lineNumber: 114,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    " ",
                                    getCurrentBreakpoint()
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 113,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: "Device Type:"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                        lineNumber: 117,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    " ",
                                    currentSize.width <= 767 ? 'Mobile' : currentSize.width <= 1024 ? 'Tablet' : 'Desktop'
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 116,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                        children: "Orientation:"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                        lineNumber: 123,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    " ",
                                    currentSize.width > currentSize.height ? 'Landscape' : 'Portrait'
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 122,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                        lineNumber: 109,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                    lineNumber: 108,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                            className: "text-md font-bold text-[var(--text-primary)] mb-4",
                            children: "Device Presets"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 132,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2",
                            children: PRESET_SIZES.map((preset)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>applySize(preset.width, preset.height),
                                    className: "p-2 text-xs text-left bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0]",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "font-medium text-[var(--text-primary)]",
                                            children: preset.name
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 142,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-gray-600",
                                            children: [
                                                preset.width,
                                                " × ",
                                                preset.height
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 143,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, preset.name, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                    lineNumber: 137,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)))
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 135,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                    lineNumber: 131,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-t border-[var(--border-inset)]",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                            className: "text-md font-bold text-[var(--text-primary)] mb-4",
                            children: "Custom Size"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 151,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex gap-4 items-end",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                            className: "block text-xs text-[var(--text-primary)] mb-1",
                                            children: "Width"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 156,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                            type: "number",
                                            placeholder: "Width",
                                            className: "w-20 px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm",
                                            min: "320",
                                            max: "3840"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 157,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                    lineNumber: 155,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                            className: "block text-xs text-[var(--text-primary)] mb-1",
                                            children: "Height"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 166,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                            type: "number",
                                            placeholder: "Height",
                                            className: "w-20 px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm",
                                            min: "240",
                                            max: "2160"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 167,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                    lineNumber: 165,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>{
                                        const widthInput = document.querySelector('input[placeholder="Width"]');
                                        const heightInput = document.querySelector('input[placeholder="Height"]');
                                        if ((widthInput === null || widthInput === void 0 ? void 0 : widthInput.value) && (heightInput === null || heightInput === void 0 ? void 0 : heightInput.value)) {
                                            applySize(parseInt(widthInput.value), parseInt(heightInput.value));
                                        }
                                    },
                                    className: "px-3 py-1 text-xs bg-[var(--accent-color)] text-white border border-[var(--border-inset)] rounded-sm hover:bg-green-600",
                                    children: "Apply"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                    lineNumber: 175,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 154,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                    lineNumber: 150,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-t border-[var(--border-inset)] flex justify-between",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: resetSize,
                            className: "px-4 py-2 text-xs bg-[var(--primary-color)] text-white border border-[var(--border-inset)] rounded-sm hover:bg-[var(--secondary-color)]",
                            children: "🔄 Reset to Actual Size"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 192,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>setIsOpen(false),
                            className: "px-4 py-2 text-xs bg-gray-500 text-white border border-[var(--border-inset)] rounded-sm hover:bg-gray-600",
                            children: "Close"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 198,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                    lineNumber: 191,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
            lineNumber: 91,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
        lineNumber: 90,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(ResponsiveTest, "06gbJgaQNSCsdHy+bjekgUosxck=");
_c = ResponsiveTest;
var _c;
__turbopack_context__.k.register(_c, "ResponsiveTest");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MainLayout",
    ()=>MainLayout
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$MenuBar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Taskbar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$Window$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ResponsiveTest$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
'use client';
;
;
;
;
;
;
;
;
;
const MainLayout = (param)=>{
    let { children, title = 'NovaSystem', icon, sidebarContent, className } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["NavigationProvider"], {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["StreamingProvider"], {
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "h-screen w-screen overflow-hidden bg-[var(--bg-primary)] relative safe-area-all",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$Window$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Window"], {
                        title: title,
                        icon: icon,
                        className: cn("relative responsive-spacing", className),
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex flex-col h-full responsive-padding",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$MenuBar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["MenuBar"], {}, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                    lineNumber: 39,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex flex-1 overflow-hidden responsive-spacing sm:flex-col lg:flex-row",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Sidebar"], {
                                            children: sidebarContent
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                            lineNumber: 44,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex-1 bg-[var(--bg-primary)] overflow-auto responsive-padding container-padding content-mobile",
                                            children: children
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                            lineNumber: 49,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                    lineNumber: 42,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                            lineNumber: 37,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                        lineNumber: 32,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Taskbar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Taskbar"], {}, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                        lineNumber: 57,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ResponsiveTest$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ResponsiveTest"], {}, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                        lineNumber: 60,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                lineNumber: 31,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
            lineNumber: 30,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
        lineNumber: 29,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = MainLayout;
var _c;
__turbopack_context__.k.register(_c, "MainLayout");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPCard",
    ()=>XPCard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
'use client';
;
;
const XPCard = (param)=>{
    let { className, variant = 'outset', children, ...props } = param;
    const variantStyles = {
        default: "bg-[var(--xp-content-bg)] border border-[var(--xp-content-border)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]",
        inset: "bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)]",
        outset: "bg-[var(--xp-content-bg)] border border-[var(--xp-window-border-light)] border-t-[var(--xp-window-border-light)] border-l-[var(--xp-window-border-light)] border-r-[var(--xp-window-border-dark)] border-b-[var(--xp-window-border-dark)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("font-sans text-sm", variantStyles[variant], className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 30,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = XPCard;
const XPCardHeader = (param)=>{
    let { className, children, ...props } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("p-2 border-b border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] font-bold text-black text-sm", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 45,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c1 = XPCardHeader;
const XPCardContent = (param)=>{
    let { className, children, ...props } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("p-3 text-black text-sm", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 59,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c2 = XPCardContent;
const XPCardFooter = (param)=>{
    let { className, children, ...props } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: cn("p-2 border-t border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] text-black text-sm flex justify-end gap-2", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c3 = XPCardFooter;
XPCard.Header = XPCardHeader;
XPCard.Content = XPCardContent;
XPCard.Footer = XPCardFooter;
var _c, _c1, _c2, _c3;
__turbopack_context__.k.register(_c, "XPCard");
__turbopack_context__.k.register(_c1, "XPCardHeader");
__turbopack_context__.k.register(_c2, "XPCardContent");
__turbopack_context__.k.register(_c3, "XPCardFooter");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPButton",
    ()=>XPButton
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
'use client';
;
;
const XPButton = (param)=>{
    let { className, variant = 'default', size = 'md', icon, children, onClick, ...props } = param;
    const handleClick = (e)=>{
        // Add button press animation
        const button = e.currentTarget;
        button.classList.add('xp-button-press');
        setTimeout(()=>{
            button.classList.remove('xp-button-press');
        }, 100);
        if (onClick) {
            onClick(e);
        }
    };
    const baseStyles = "inline-flex items-center justify-center font-sans transition-all duration-150 focus:outline-none disabled:cursor-not-allowed";
    const variantStyles = {
        default: "bg-[var(--xp-button-bg)] text-[var(--xp-button-text)] border border-[var(--xp-button-border-light)] border-t-[var(--xp-button-border-light)] border-l-[var(--xp-button-border-light)] border-r-[var(--xp-button-border-dark)] border-b-[var(--xp-button-border-dark)] shadow-[1px_1px_0px_var(--xp-button-border-light),-1px_-1px_0px_var(--xp-button-border-dark)] hover:bg-[var(--xp-button-bg-light)] active:bg-[var(--xp-button-bg-dark)] active:shadow-[inset_1px_1px_0px_var(--xp-button-border-dark),inset_-1px_-1px_0px_var(--xp-button-border-light)] active:border-t-[var(--xp-button-border-dark)] active:border-l-[var(--xp-button-border-dark)] active:border-r-[var(--xp-button-border-light)] active:border-b-[var(--xp-button-border-light)]",
        primary: "bg-[var(--xp-primary-blue)] text-white border border-[var(--xp-primary-blue-dark)] border-t-[var(--xp-primary-blue-light)] border-l-[var(--xp-primary-blue-light)] border-r-[var(--xp-primary-blue-dark)] border-b-[var(--xp-primary-blue-dark)] shadow-[1px_1px_0px_var(--xp-primary-blue-light),-1px_-1px_0px_var(--xp-primary-blue-dark)] hover:bg-[var(--xp-primary-blue-light)] active:bg-[var(--xp-primary-blue-dark)] active:shadow-[inset_1px_1px_0px_var(--xp-primary-blue-dark),inset_-1px_-1px_0px_var(--xp-primary-blue-light)] active:border-t-[var(--xp-primary-blue-dark)] active:border-l-[var(--xp-primary-blue-dark)] active:border-r-[var(--xp-primary-blue-light)] active:border-b-[var(--xp-primary-blue-light)]",
        success: "bg-[var(--xp-success)] text-white border border-[var(--xp-success)] border-t-[var(--xp-success)] border-l-[var(--xp-success)] border-r-[var(--xp-success)] border-b-[var(--xp-success)] shadow-[1px_1px_0px_var(--xp-success),-1px_-1px_0px_var(--xp-success)] hover:bg-[#8dd066] active:bg-[#4a8b2b] active:shadow-[inset_1px_1px_0px_var(--xp-success),inset_-1px_-1px_0px_var(--xp-success)]",
        warning: "bg-[var(--xp-warning)] text-white border border-[var(--xp-warning)] border-t-[var(--xp-warning)] border-l-[var(--xp-warning)] border-r-[var(--xp-warning)] border-b-[var(--xp-warning)] shadow-[1px_1px_0px_var(--xp-warning),-1px_-1px_0px_var(--xp-warning)] hover:bg-[#ffb84d] active:bg-[#cc8400] active:shadow-[inset_1px_1px_0px_var(--xp-warning),inset_-1px_-1px_0px_var(--xp-warning)]",
        danger: "bg-[var(--xp-error)] text-white border border-[var(--xp-error)] border-t-[var(--xp-error)] border-l-[var(--xp-error)] border-r-[var(--xp-error)] border-b-[var(--xp-error)] shadow-[1px_1px_0px_var(--xp-error),-1px_-1px_0px_var(--xp-error)] hover:bg-[#ff3333] active:bg-[#cc0000] active:shadow-[inset_1px_1px_0px_var(--xp-error),inset_-1px_-1px_0px_var(--xp-error)]"
    };
    const sizeStyles = {
        sm: "h-5 px-2 text-xs min-w-[60px]",
        md: "h-6 px-3 text-sm min-w-[75px]",
        lg: "h-7 px-4 text-base min-w-[90px]"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        className: cn(baseStyles, variantStyles[variant], sizeStyles[size], className),
        onClick: handleClick,
        ...props,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "flex items-center justify-center gap-1",
            children: [
                icon && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                    className: "text-xs",
                    children: icon
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx",
                    lineNumber: 61,
                    columnNumber: 18
                }, ("TURBOPACK compile-time value", void 0)),
                children
            ]
        }, void 0, true, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx",
            lineNumber: 60,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx",
        lineNumber: 50,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = XPButton;
var _c;
__turbopack_context__.k.register(_c, "XPButton");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPInput",
    ()=>XPInput,
    "XPSelect",
    ()=>XPSelect,
    "XPTextArea",
    ()=>XPTextArea
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
'use client';
;
;
const baseInputStyles = "font-sans text-sm text-black bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)] focus:outline-none focus:border-[var(--xp-primary-blue)] focus:ring-1 focus:ring-[var(--xp-primary-blue)] disabled:bg-[var(--xp-button-bg-dark)] disabled:text-[var(--text-disabled)]";
const XPInput = (param)=>{
    let { label, error, helperText, variant = 'inset', size = 'md', className, ...props } = param;
    const sizeStyles = {
        sm: "h-5 px-1 text-xs",
        md: "h-6 px-2 text-sm",
        lg: "h-7 px-3 text-base"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 56,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                className: cn(baseInputStyles, sizeStyles[size], error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 60,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 70,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#666666]",
                children: helperText
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 73,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
        lineNumber: 54,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = XPInput;
const XPTextArea = (param)=>{
    let { label, error, helperText, variant = 'inset', className, ...props } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 90,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                className: cn(baseInputStyles, "px-2 py-1 min-h-[60px] resize-vertical", error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 94,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 104,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#666666]",
                children: helperText
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 107,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
        lineNumber: 88,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c1 = XPTextArea;
const XPSelect = (param)=>{
    let { label, error, helperText, options, variant = 'inset', size = 'md', className, ...props } = param;
    const sizeStyles = {
        sm: "h-5 px-1 text-xs",
        md: "h-6 px-2 text-sm",
        lg: "h-7 px-3 text-base"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 132,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                className: cn(baseInputStyles, sizeStyles[size], error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props,
                children: options.map((option)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: option.value,
                        disabled: option.disabled,
                        children: option.label
                    }, option.value, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                        lineNumber: 146,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)))
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 136,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 156,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#666666]",
                children: helperText
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 159,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
        lineNumber: 130,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c2 = XPSelect;
var _c, _c1, _c2;
__turbopack_context__.k.register(_c, "XPInput");
__turbopack_context__.k.register(_c1, "XPTextArea");
__turbopack_context__.k.register(_c2, "XPSelect");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPAgentResponseStream",
    ()=>XPAgentResponseStream
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
;
const XPAgentResponseStream = (param)=>{
    let { className } = param;
    _s();
    const streamingContext = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useStreaming"])();
    const messagesEndRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    // Handle case where context might not be available during SSR
    if (!streamingContext) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
            className: cn("flex flex-col h-full", className),
            variant: "outset",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-lg",
                                children: "📡"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 24,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "font-bold",
                                children: "Loading..."
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 25,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 23,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                    lineNumber: 22,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                    className: "flex-1 flex items-center justify-center",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-center text-[#666666]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-2xl mb-2",
                                children: "⏳"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 30,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-sm",
                                children: "Initializing streaming..."
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 31,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 29,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                    lineNumber: 28,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
            lineNumber: 21,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0));
    }
    const { responses, clearResponses, isStreaming, connectionStatus, searchFilter, setSearchFilter } = streamingContext;
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "XPAgentResponseStream.useEffect": ()=>{
            var _messagesEndRef_current;
            (_messagesEndRef_current = messagesEndRef.current) === null || _messagesEndRef_current === void 0 ? void 0 : _messagesEndRef_current.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }["XPAgentResponseStream.useEffect"], [
        responses
    ]);
    const filteredResponses = responses.filter((response)=>response.agentId.toLowerCase().includes(searchFilter.toLowerCase()) || response.content.toLowerCase().includes(searchFilter.toLowerCase()));
    const getStatusColor = (status)=>{
        switch(status){
            case 'streaming':
                return 'bg-[#0054e3]';
            case 'complete':
                return 'bg-[#6bbf44]';
            case 'error':
                return 'bg-[#ff4444]';
            default:
                return 'bg-[#808080]';
        }
    };
    const handleExport = ()=>{
        const dataStr = JSON.stringify(responses, null, 2);
        const dataBlob = new Blob([
            dataStr
        ], {
            type: 'application/json'
        });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = "agent_responses_".concat(new Date().toISOString(), ".json");
        link.click();
        URL.revokeObjectURL(url);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
        className: cn("flex flex-col h-full", className),
        variant: "outset",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex justify-between items-center",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-lg",
                                    children: "📡"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 74,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "font-bold",
                                    children: "Live Agent Responses"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 75,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                            lineNumber: 73,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: cn("w-2 h-2 rounded-full", connectionStatus === 'connected' ? 'bg-[#6bbf44]' : 'bg-[#ff4444]')
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 78,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-xs text-black",
                                    children: connectionStatus === 'connected' ? 'Connected' : 'Disconnected'
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 79,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                    variant: "default",
                                    size: "sm",
                                    onClick: clearResponses,
                                    children: "Clear"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 80,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                    variant: "primary",
                                    size: "sm",
                                    onClick: handleExport,
                                    children: "Export"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 83,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                            lineNumber: 77,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                    lineNumber: 72,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                lineNumber: 71,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                className: "flex-1 overflow-y-auto p-2 space-y-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mb-2",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPInput"], {
                            placeholder: "Search responses...",
                            value: searchFilter,
                            onChange: (e)=>setSearchFilter(e.target.value),
                            size: "sm"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                            lineNumber: 91,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 90,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    filteredResponses.length === 0 && !isStreaming && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-center text-[#666666] py-8",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-2xl mb-2",
                                children: "🤖"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 100,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-sm",
                                children: "No responses yet. Start a workflow to see agent activity."
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 101,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 99,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    filteredResponses.map((response, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
                            className: "p-3",
                            variant: "inset",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex items-center justify-between text-xs text-[#666666] mb-2",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: cn("w-3 h-3 rounded-full", getStatusColor(response.status))
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                                    lineNumber: 108,
                                                    columnNumber: 17
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "font-bold text-black text-sm",
                                                    children: response.agentId
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                                    lineNumber: 109,
                                                    columnNumber: 17
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-xs bg-[#e0e0e0] px-2 py-1 rounded border border-[#c0c0c0]",
                                                    children: response.status.toUpperCase()
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                                    lineNumber: 110,
                                                    columnNumber: 17
                                                }, ("TURBOPACK compile-time value", void 0))
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                            lineNumber: 107,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "text-xs font-mono",
                                            children: new Date(response.timestamp).toLocaleTimeString()
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                            lineNumber: 114,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 106,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "bg-white p-2 border border-[#c0c0c0] rounded",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "text-sm text-black leading-relaxed whitespace-pre-wrap font-sans",
                                        children: response.content
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                        lineNumber: 117,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 116,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, index, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                            lineNumber: 105,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))),
                    isStreaming && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2 text-sm text-[#666666]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "animate-spin w-4 h-4 border-2 border-[#0054e3] border-t-transparent rounded-full"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 125,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Streaming..."
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 126,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 124,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        ref: messagesEndRef
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                        lineNumber: 129,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                lineNumber: 89,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(XPAgentResponseStream, "t+4mhU1p1Q+nzT3DRcg05uGPE1Y=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useStreaming"]
    ];
});
_c = XPAgentResponseStream;
var _c;
__turbopack_context__.k.register(_c, "XPAgentResponseStream");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPWorkflowSystem",
    ()=>XPWorkflowSystem
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$XPAgentResponseStream$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-client] (ecmascript)");
(()=>{
    const e = new Error("Cannot find module '@/lib/utils'");
    e.code = 'MODULE_NOT_FOUND';
    throw e;
})();
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
;
;
const MOCK_AGENTS = [
    {
        id: 'agent-1',
        name: 'Problem Solver',
        type: 'problemSolver',
        description: 'Analyzes problems',
        version: '1.2.0',
        status: 'idle',
        icon: '🧠'
    },
    {
        id: 'agent-2',
        name: 'Research Agent',
        type: 'research',
        description: 'Gathers information',
        version: '2.1.0',
        status: 'idle',
        icon: '🔍'
    },
    {
        id: 'agent-3',
        name: 'Data Analyst',
        type: 'analysis',
        description: 'Analyzes data',
        version: '1.8.0',
        status: 'idle',
        icon: '📊'
    },
    {
        id: 'agent-4',
        name: 'Synthesizer',
        type: 'synthesizer',
        description: 'Combines insights',
        version: '1.5.0',
        status: 'idle',
        icon: '🔗'
    },
    {
        id: 'agent-5',
        name: 'Data Processor',
        type: 'data',
        description: 'Handles data',
        version: '2.0.0',
        status: 'idle',
        icon: '📈'
    },
    {
        id: 'agent-6',
        name: 'Optimizer',
        type: 'optimization',
        description: 'Optimizes processes',
        version: '1.3.0',
        status: 'idle',
        icon: '⚡'
    }
];
const XPWorkflowSystem = ()=>{
    _s();
    const [problemStatement, setProblemStatement] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [selectedAgents, setSelectedAgents] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [workflowStatus, setWorkflowStatus] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('idle');
    const [activeTab, setActiveTab] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('status');
    const { addResponse, setIsStreaming, clearResponses } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useStreaming"])();
    const handleAgentToggle = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "XPWorkflowSystem.useCallback[handleAgentToggle]": (agent)=>{
            setSelectedAgents({
                "XPWorkflowSystem.useCallback[handleAgentToggle]": (prev)=>prev.some({
                        "XPWorkflowSystem.useCallback[handleAgentToggle]": (a)=>a.id === agent.id
                    }["XPWorkflowSystem.useCallback[handleAgentToggle]"]) ? prev.filter({
                        "XPWorkflowSystem.useCallback[handleAgentToggle]": (a)=>a.id !== agent.id
                    }["XPWorkflowSystem.useCallback[handleAgentToggle]"]) : [
                        ...prev,
                        agent
                    ]
            }["XPWorkflowSystem.useCallback[handleAgentToggle]"]);
        }
    }["XPWorkflowSystem.useCallback[handleAgentToggle]"], []);
    const startWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "XPWorkflowSystem.useCallback[startWorkflow]": ()=>{
            if (!problemStatement.trim()) {
                alert('Please enter a problem statement.');
                return;
            }
            if (selectedAgents.length === 0) {
                alert('Please select at least one agent.');
                return;
            }
            setWorkflowStatus('running');
            setIsStreaming(true);
            clearResponses();
            setActiveTab('responses');
            let step = 0;
            const totalSteps = selectedAgents.length * 2;
            const interval = setInterval({
                "XPWorkflowSystem.useCallback[startWorkflow].interval": ()=>{
                    if (step >= totalSteps) {
                        clearInterval(interval);
                        setWorkflowStatus('completed');
                        setIsStreaming(false);
                        addResponse({
                            agentId: 'System',
                            content: 'Workflow completed successfully!',
                            timestamp: Date.now(),
                            status: 'complete'
                        });
                        return;
                    }
                    const currentAgentIndex = Math.floor(step / 2);
                    const currentAgent = selectedAgents[currentAgentIndex];
                    if (step % 2 === 0) {
                        const analysisMessages = [
                            '🔍 Analyzing problem statement: "'.concat(problemStatement.substring(0, 50)).concat(problemStatement.length > 50 ? '...' : '', '"'),
                            "📊 Breaking down the problem into key components and identifying potential approaches...",
                            "🧠 Evaluating different solution strategies and their feasibility...",
                            "⚡ Processing requirements and constraints for optimal solution design...",
                            "🎯 Identifying critical success factors and potential challenges...",
                            "💡 Generating initial insights and preliminary analysis..."
                        ];
                        addResponse({
                            agentId: currentAgent.name,
                            content: analysisMessages[Math.floor(Math.random() * analysisMessages.length)],
                            timestamp: Date.now(),
                            status: 'streaming'
                        });
                    } else {
                        const solutionMessages = [
                            "✅ Analysis complete! Generated comprehensive solution framework with ".concat(Math.floor(Math.random() * 5) + 3, " key components."),
                            "🎯 Solution strategy developed: Implemented ".concat(Math.floor(Math.random() * 3) + 2, "-phase approach with clear milestones."),
                            "📈 Delivered actionable recommendations with ".concat(Math.floor(Math.random() * 4) + 2, " implementation steps."),
                            "🔧 Created detailed technical specification with performance metrics and success criteria.",
                            "💼 Business case analysis complete with ROI projections and risk assessment.",
                            "🚀 Solution ready for implementation with comprehensive documentation and next steps."
                        ];
                        addResponse({
                            agentId: currentAgent.name,
                            content: solutionMessages[Math.floor(Math.random() * solutionMessages.length)],
                            timestamp: Date.now(),
                            status: 'complete'
                        });
                    }
                    step++;
                }
            }["XPWorkflowSystem.useCallback[startWorkflow].interval"], 1500);
        }
    }["XPWorkflowSystem.useCallback[startWorkflow]"], [
        problemStatement,
        selectedAgents,
        addResponse,
        clearResponses,
        setIsStreaming
    ]);
    const stopWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "XPWorkflowSystem.useCallback[stopWorkflow]": ()=>{
            setWorkflowStatus('idle');
            setIsStreaming(false);
            addResponse({
                agentId: 'System',
                content: 'Workflow stopped by user.',
                timestamp: Date.now(),
                status: 'complete'
            });
        }
    }["XPWorkflowSystem.useCallback[stopWorkflow]"], [
        addResponse,
        setIsStreaming
    ]);
    const resetWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "XPWorkflowSystem.useCallback[resetWorkflow]": ()=>{
            setProblemStatement('');
            setSelectedAgents([]);
            setWorkflowStatus('idle');
            clearResponses();
            setIsStreaming(false);
        }
    }["XPWorkflowSystem.useCallback[resetWorkflow]"], [
        clearResponses,
        setIsStreaming
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex h-full gap-4 p-4 bg-[#ece9d8]",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
                className: "w-1/3 flex flex-col",
                variant: "outset",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-lg",
                                    children: "⚙️"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 142,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    children: "Workflow Configuration"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 143,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                            lineNumber: 141,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 140,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                        className: "flex-1 overflow-y-auto space-y-4",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPTextArea"], {
                                    label: "Problem Statement",
                                    placeholder: "Describe the problem you want to solve...",
                                    value: problemStatement,
                                    onChange: (e)=>setProblemStatement(e.target.value),
                                    disabled: workflowStatus === 'running',
                                    rows: 4
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 148,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 147,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        className: "text-sm font-bold text-black mb-2",
                                        children: "Select Agents"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 159,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "grid grid-cols-2 gap-2",
                                        children: MOCK_AGENTS.map((agent)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
                                                className: cn("p-2 cursor-pointer transition-all duration-100", selectedAgents.some((a)=>a.id === agent.id) ? "border-[#0054e3] bg-[#e6f2ff]" : "border-[#c0c0c0] hover:bg-[#f0f0f0]"),
                                                variant: "outset",
                                                onClick: ()=>handleAgentToggle(agent),
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-center gap-2 mb-1",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "text-sm",
                                                                children: agent.icon
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 174,
                                                                columnNumber: 21
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "font-medium text-black text-xs",
                                                                children: agent.name
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 175,
                                                                columnNumber: 21
                                                            }, ("TURBOPACK compile-time value", void 0))
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 173,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-xs text-[#666666]",
                                                        children: agent.description
                                                    }, void 0, false, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 177,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0))
                                                ]
                                            }, agent.id, true, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 162,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0)))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 160,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 158,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 146,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Footer, {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "default",
                                onClick: resetWorkflow,
                                disabled: workflowStatus === 'running',
                                children: "Reset"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 184,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            workflowStatus === 'running' ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "danger",
                                onClick: stopWorkflow,
                                children: "Stop Workflow"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 188,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "primary",
                                onClick: startWorkflow,
                                disabled: !problemStatement.trim() || selectedAgents.length === 0,
                                children: "Start Workflow"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 192,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 183,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                lineNumber: 139,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
                className: "w-2/3 flex flex-col",
                variant: "outset",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex justify-between items-center",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex items-center gap-2",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "text-lg",
                                            children: "🔄"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 208,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: "Workflow Execution"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 209,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 207,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex gap-1",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'status' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('status'),
                                            size: "sm",
                                            children: "Status"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 212,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'responses' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('responses'),
                                            size: "sm",
                                            children: "Responses"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 219,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'results' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('results'),
                                            size: "sm",
                                            children: "Results"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 226,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 211,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                            lineNumber: 206,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 205,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                        className: "flex-1 overflow-hidden",
                        children: [
                            activeTab === 'status' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "h-full flex flex-col space-y-4 overflow-y-auto",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center gap-2",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                className: "text-sm font-bold text-black",
                                                children: "Current Status:"
                                            }, void 0, false, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 240,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                className: cn("text-sm font-bold capitalize", workflowStatus === 'running' && "text-[#0054e3]", workflowStatus === 'completed' && "text-[#6bbf44]", workflowStatus === 'error' && "text-[#ff4444]"),
                                                children: workflowStatus
                                            }, void 0, false, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 241,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 239,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "grid grid-cols-2 gap-3",
                                        children: selectedAgents.map((agent)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPCard"], {
                                                className: "p-2",
                                                variant: "inset",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-center gap-2 mb-1",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "text-sm",
                                                                children: agent.icon
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 254,
                                                                columnNumber: 23
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "font-medium text-black text-xs",
                                                                children: agent.name
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 255,
                                                                columnNumber: 23
                                                            }, ("TURBOPACK compile-time value", void 0))
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 253,
                                                        columnNumber: 21
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-xs text-[#666666] mb-2",
                                                        children: agent.description
                                                    }, void 0, false, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 257,
                                                        columnNumber: 21
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-center gap-2",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: cn("w-2 h-2 rounded-full", workflowStatus === 'running' ? "bg-[#0054e3] animate-pulse" : "bg-[#808080]")
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 259,
                                                                columnNumber: 23
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "text-xs text-[#666666]",
                                                                children: workflowStatus === 'running' ? 'Processing...' : 'Idle'
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 263,
                                                                columnNumber: 23
                                                            }, ("TURBOPACK compile-time value", void 0))
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 258,
                                                        columnNumber: 21
                                                    }, ("TURBOPACK compile-time value", void 0))
                                                ]
                                            }, agent.id, true, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 252,
                                                columnNumber: 19
                                            }, ("TURBOPACK compile-time value", void 0)))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 250,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 238,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            activeTab === 'responses' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "h-full",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$XPAgentResponseStream$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPAgentResponseStream"], {
                                    className: "h-full"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 274,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 273,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            activeTab === 'results' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "h-full flex items-center justify-center text-[#666666]",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-center",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-4xl mb-2",
                                            children: "📊"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 280,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-sm",
                                            children: "Workflow results will appear here after completion."
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 281,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 279,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 278,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 236,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                lineNumber: 204,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
        lineNumber: 137,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(XPWorkflowSystem, "0BhXMWFCSWPnCGn9fEfW9pe9wWA=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useStreaming"]
    ];
});
_c = XPWorkflowSystem;
var _c;
__turbopack_context__.k.register(_c, "XPWorkflowSystem");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>WorkflowPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$layout$2f$MainLayout$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$XPWorkflowSystem$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx [app-client] (ecmascript)");
'use client';
;
;
;
function WorkflowPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$layout$2f$MainLayout$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["MainLayout"], {
        title: "Workflow Engine",
        icon: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm"
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx",
            lineNumber: 11,
            columnNumber: 13
        }, void 0),
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$XPWorkflowSystem$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["XPWorkflowSystem"], {}, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx",
            lineNumber: 13,
            columnNumber: 13
        }, this)
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx",
        lineNumber: 9,
        columnNumber: 5
    }, this);
}
_c = WorkflowPage;
var _c;
__turbopack_context__.k.register(_c, "WorkflowPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=NovaSystem-Streamlined_novasystem_modern_ui_src_4cf52740._.js.map