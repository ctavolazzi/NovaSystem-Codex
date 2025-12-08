module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/action-async-storage.external.js [external] (next/dist/server/app-render/action-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/action-async-storage.external.js", () => require("next/dist/server/app-render/action-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "NAVIGATION_CONFIG",
    ()=>NAVIGATION_CONFIG,
    "NavigationProvider",
    ()=>NavigationProvider,
    "useNavigation",
    ()=>useNavigation
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/navigation.js [app-ssr] (ecmascript)");
'use client';
;
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
const NavigationContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useNavigation = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(NavigationContext);
    if (!context) {
        throw new Error('useNavigation must be used within a NavigationProvider');
    }
    return context;
};
const NavigationProvider = ({ children })=>{
    const pathname = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["usePathname"])();
    const [isMobile, setIsMobile] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [isTablet, setIsTablet] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [sidebarOpen, setSidebarOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
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
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    };
    // Handle responsive design with comprehensive breakpoints
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleResize = ()=>{
            if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
            ;
        };
        handleResize();
        window.addEventListener('resize', handleResize);
        window.addEventListener('orientationchange', handleResize);
        return ()=>{
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('orientationchange', handleResize);
        };
    }, []);
    // Handle orientation change on mobile
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleOrientationChange = ()=>{
            setTimeout(()=>{
                if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
                ;
            }, 100);
        };
        window.addEventListener('orientationchange', handleOrientationChange);
        return ()=>window.removeEventListener('orientationchange', handleOrientationChange);
    }, []);
    // Keyboard shortcuts
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleKeyDown = (e)=>{
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
        };
        document.addEventListener('keydown', handleKeyDown);
        return ()=>document.removeEventListener('keydown', handleKeyDown);
    }, []);
    // Touch gestures for mobile
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!isMobile) return;
        let startX = 0;
        let startY = 0;
        const handleTouchStart = (e)=>{
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        };
        const handleTouchEnd = (e)=>{
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;
            // Check if horizontal swipe
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                const pages = NAVIGATION_CONFIG.main;
                const currentIndex = pages.findIndex((page)=>page.id === currentPage);
                if (diffX > 0 && currentIndex < pages.length - 1) {
                    // Swipe left - next page
                    navigateToPage(pages[currentIndex + 1].url);
                } else if (diffX < 0 && currentIndex > 0) {
                    // Swipe right - previous page
                    navigateToPage(pages[currentIndex - 1].url);
                }
            }
        };
        document.addEventListener('touchstart', handleTouchStart, {
            passive: true
        });
        document.addEventListener('touchend', handleTouchEnd, {
            passive: true
        });
        return ()=>{
            document.removeEventListener('touchstart', handleTouchStart);
            document.removeEventListener('touchend', handleTouchEnd);
        };
    }, [
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
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(NavigationContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx",
        lineNumber: 219,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "StreamingProvider",
    ()=>StreamingProvider,
    "useStreaming",
    ()=>useStreaming
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
'use client';
;
;
const SimpleStreamingContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useStreaming = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(SimpleStreamingContext);
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
const StreamingProvider = ({ children })=>{
    const [responses, setResponses] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [isStreaming, setIsStreaming] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [connectionStatus, setConnectionStatus] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('connected');
    const [searchFilter, setSearchFilter] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('');
    const [isClient, setIsClient] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    // Ensure we're on the client side to prevent hydration mismatches
    __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].useEffect(()=>{
        setIsClient(true);
    }, []);
    const addResponse = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((newResponse)=>{
        setResponses((prevResponses)=>{
            const existingIndex = prevResponses.findIndex((res)=>res.agentId === newResponse.agentId && res.status === 'streaming');
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
        });
    }, []);
    const clearResponses = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setResponses([]);
    }, []);
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
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: children
        }, void 0, false);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(SimpleStreamingContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx",
        lineNumber: 95,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "cn",
    ()=>cn
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/clsx/dist/clsx.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$tailwind$2d$merge$2f$dist$2f$bundle$2d$mjs$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/tailwind-merge/dist/bundle-mjs.mjs [app-ssr] (ecmascript)");
;
;
function cn(...inputs) {
    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$tailwind$2d$merge$2f$dist$2f$bundle$2d$mjs$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["twMerge"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$clsx$2f$dist$2f$clsx$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["clsx"])(inputs));
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Sidebar",
    ()=>Sidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/client/app-dir/link.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
;
const Sidebar = ({ className, children })=>{
    const { currentPage, isMobile, navigationConfig } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useNavigation"])();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-sidebar xp-scrollbar flex", isMobile ? "w-full h-auto flex-row overflow-x-auto overflow-y-hidden border-b border-r-0 nav-mobile" : "w-50 h-full flex-col border-r", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("border-[var(--border-light)] flex-shrink-0", isMobile ? "min-w-32 max-w-40 p-1 border-r border-b-0" : "w-full p-2 border-b"),
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title sm:hidden lg:block",
                        children: "Navigation"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 31,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(isMobile ? "flex gap-2" : "space-y-1"),
                        children: navigationConfig.main.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-sidebar-item", isMobile ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item" : "px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white", isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"),
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 49,
                                        columnNumber: 19
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
            ].includes(currentPage) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-2 border-b border-[var(--border-light)] sm:hidden lg:block",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-xs font-bold text-[var(--text-primary)] mb-2 px-1",
                        children: "Sessions"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 64,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-1",
                        children: navigationConfig.sessions.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-sidebar-item px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "w-5 h-5 bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-xs text-white",
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 77,
                                        columnNumber: 21
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("p-2 border-b border-[var(--border-light)]", isMobile ? "min-w-50 border-r border-b-0 mr-2" : "border-b"),
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title sm:hidden lg:block",
                        children: "Tools"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 92,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(isMobile ? "flex gap-2" : "space-y-1"),
                        children: navigationConfig.tools.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                                href: item.url,
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-sidebar-item", isMobile ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item" : "px-3 py-2 text-xs gap-2", currentPage === item.id && "active"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white", isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"),
                                        children: item.icon
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 110,
                                        columnNumber: 19
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
            children && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 p-2",
                children: children
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                lineNumber: 124,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "min-w-50 p-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-sidebar-section-title",
                        children: "Quick Actions"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                        lineNumber: 132,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-0.5",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "🔄"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 137,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "⛶"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 141,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "xp-button w-full justify-start",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "⚙️"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx",
                                        lineNumber: 145,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MenuBar",
    ()=>MenuBar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
;
const MenuBar = ({ className })=>{
    const { currentPage, navigationConfig } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useNavigation"])();
    const [activeDropdown, setActiveDropdown] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [hoverTimeout, setHoverTimeout] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const getCurrentPageTitle = ()=>{
        const allItems = [
            ...navigationConfig.main,
            ...navigationConfig.tools,
            ...navigationConfig.sessions
        ];
        const currentItem = allItems.find((item)=>item.id === currentPage);
        return currentItem?.label || 'NovaSystem';
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
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleClickOutside = (event)=>{
            if (activeDropdown) {
                const target = event.target;
                if (!target.closest('.menu-item-container')) {
                    setActiveDropdown(null);
                }
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return ()=>document.removeEventListener('mousedown', handleClickOutside);
    }, [
        activeDropdown
    ]);
    // Cleanup timeout on unmount
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        return ()=>{
            if (hoverTimeout) {
                clearTimeout(hoverTimeout);
            }
        };
    }, [
        hoverTimeout
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menubar", "relative z-[var(--z-index-menubar)]", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('file'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menu-item", activeDropdown === 'file' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('file'),
                                children: "File"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 93,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("dropdown-menu", activeDropdown === 'file' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "New Session"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 106,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Save Session"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 109,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Export Data"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 112,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 115,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('edit'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menu-item", activeDropdown === 'edit' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('edit'),
                                children: "Edit"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 128,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("dropdown-menu", activeDropdown === 'edit' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Undo"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 141,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Redo"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 144,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 147,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('view'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menu-item", activeDropdown === 'view' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('view'),
                                children: "View"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 160,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("dropdown-menu", activeDropdown === 'view' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Refresh"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 173,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Full Screen"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 176,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 179,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Zoom In"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 180,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('tools'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menu-item", activeDropdown === 'tools' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('tools'),
                                children: "Tools"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 195,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("dropdown-menu", activeDropdown === 'tools' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Session Manager"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 208,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Analytics"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 211,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Monitor"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 214,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 217,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "relative menu-item-container",
                        onMouseEnter: ()=>handleMouseEnter('help'),
                        onMouseLeave: handleMouseLeave,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-menu-item", activeDropdown === 'help' && "bg-[var(--primary-blue)] text-white"),
                                onClick: ()=>handleDropdownToggle('help'),
                                children: "Help"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                lineNumber: 230,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("dropdown-menu", activeDropdown === 'help' && "open"),
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Help Topics"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 243,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "dropdown-item",
                                        children: "Keyboard Shortcuts"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 246,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "dropdown-divider"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx",
                                        lineNumber: 249,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Taskbar",
    ()=>Taskbar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
;
const Taskbar = ({ className })=>{
    const { navigationConfig, isMobile } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useNavigation"])();
    const [currentTime, setCurrentTime] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(new Date());
    const [showStartMenu, setShowStartMenu] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    // Update time every second
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const timer = setInterval(()=>{
            setCurrentTime(new Date());
        }, 1000);
        return ()=>clearInterval(timer);
    }, []);
    // Close start menu when clicking outside
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleClickOutside = (event)=>{
            if (showStartMenu) {
                const target = event.target;
                if (!target.closest('.start-menu-container')) {
                    setShowStartMenu(false);
                }
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return ()=>document.removeEventListener('mousedown', handleClickOutside);
    }, [
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
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("bg-gradient-to-b from-[var(--bg-secondary)] to-[#d6d3ce] border-t border-[var(--border-3d-dark)] shadow-inner", "flex items-center justify-between px-2", "relative z-[var(--z-index-taskbar)]", isMobile ? "relative h-12 flex-wrap gap-2" : "absolute bottom-0 left-0 right-0 h-10", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "relative start-menu-container",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>setShowStartMenu(!showStartMenu),
                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("xp-button flex items-center text-[var(--text-primary)] cursor-pointer", "bg-gradient-to-b from-[var(--bg-primary)] to-[var(--bg-secondary)]", "hover:bg-gradient-to-b hover:from-[var(--bg-hover)] hover:to-[var(--bg-secondary)]", showStartMenu && "bg-gradient-to-b from-[var(--primary-blue)] to-[var(--primary-blue-hover)] text-white", isMobile ? "gap-1 px-2 py-1.5 text-[10px] min-h-[32px]" : "gap-1.5 px-3 py-1.5 text-xs min-h-[32px]"),
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm", isMobile ? "w-3 h-3" : "w-4 h-4")
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 79,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            !isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                    showStartMenu && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "absolute bottom-full left-0 mb-2 bg-[var(--bg-primary)] border border-[var(--border-light)] shadow-lg z-[var(--z-index-taskbar-dropdown)] min-w-48 rounded-md",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "p-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "text-xs font-bold text-[var(--text-primary)] mb-2",
                                    children: "NovaSystem v3.0"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 90,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "space-y-0.5",
                                    children: navigationConfig.main.slice(0, 4).map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = item.url;
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-3 py-2 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-blue)] hover:text-white cursor-pointer flex items-center gap-2 rounded-sm transition-colors",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-sm",
                                                    children: item.icon
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 101,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "border-t border-[var(--border-inset)] my-1"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 106,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "space-y-0.5",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = '/settings';
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "⚙️"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 115,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>{
                                                window.location.href = '/help';
                                                setShowStartMenu(false);
                                            },
                                            className: "w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "❓"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                                    lineNumber: 125,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
            isMobile && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex gap-1 ml-2",
                children: navigationConfig.main.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>window.location.href = item.url,
                        className: "flex items-center gap-1 px-2 py-1 text-xs text-[var(--text-primary)] cursor-pointer bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-1 ml-auto",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-1 px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-2 h-2 bg-green-500 rounded-full animate-pulse"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                lineNumber: 153,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] text-xs text-[var(--text-primary)] cursor-pointer hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "text-center",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "font-bold",
                                    children: formatTime(currentTime)
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx",
                                    lineNumber: 160,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Window",
    ()=>Window
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
const Window = ({ title, icon, children, className, onMinimize, onMaximize, onClose })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("absolute top-2.5 left-2.5 right-2.5 bottom-10", "bg-[var(--bg-window)] border-2 border-[var(--border-3d-dark)]", "shadow-[2px_2px_4px_rgba(0,0,0,0.3)]", "flex flex-col xp-window-open", className),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "xp-titlebar",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-titlebar-title",
                        children: [
                            icon && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm flex items-center justify-center text-[10px] text-white font-bold",
                                children: "N"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 37,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "xp-titlebar-controls",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: onMinimize,
                                className: "xp-window-control",
                                title: "Minimize",
                                children: "_"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 44,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: onMaximize,
                                className: "xp-window-control",
                                title: "Maximize",
                                children: "□"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx",
                                lineNumber: 51,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ResponsiveTest",
    ()=>ResponsiveTest
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
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
const ResponsiveTest = ({ className })=>{
    const [isOpen, setIsOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [currentSize, setCurrentSize] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        width: 0,
        height: 0
    });
    const applySize = (width, height)=>{
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    };
    const resetSize = ()=>{
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
    };
    const getCurrentBreakpoint = ()=>{
        const width = currentSize.width || (("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : 0);
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
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
            onClick: ()=>setIsOpen(true),
            className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("fixed bottom-20 right-4 z-50 bg-[var(--primary-color)] text-white", "px-3 py-2 text-xs rounded-sm shadow-lg hover:bg-[var(--secondary-color)]", "border border-[var(--border-inset)]", className),
            children: "📱 Test Responsive"
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
            lineNumber: 75,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0));
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "bg-[var(--bg-window)] border border-[var(--border-inset)] rounded-sm max-w-4xl w-full max-h-[80vh] overflow-auto",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-b border-[var(--border-inset)]",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex justify-between items-center",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                className: "text-lg font-bold text-[var(--text-primary)]",
                                children: "📱 Responsive Design Tester"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                lineNumber: 95,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-b border-[var(--border-inset)]",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "grid grid-cols-2 gap-4 text-sm",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
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
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
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
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
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
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
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
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                            className: "text-md font-bold text-[var(--text-primary)] mb-4",
                            children: "Device Presets"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 132,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2",
                            children: PRESET_SIZES.map((preset)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>applySize(preset.width, preset.height),
                                    className: "p-2 text-xs text-left bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0]",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "font-medium text-[var(--text-primary)]",
                                            children: preset.name
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 142,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-t border-[var(--border-inset)]",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                            className: "text-md font-bold text-[var(--text-primary)] mb-4",
                            children: "Custom Size"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 151,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex gap-4 items-end",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                            className: "block text-xs text-[var(--text-primary)] mb-1",
                                            children: "Width"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 156,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
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
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                            className: "block text-xs text-[var(--text-primary)] mb-1",
                                            children: "Height"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                                            lineNumber: 166,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
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
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>{
                                        const widthInput = document.querySelector('input[placeholder="Width"]');
                                        const heightInput = document.querySelector('input[placeholder="Height"]');
                                        if (widthInput?.value && heightInput?.value) {
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
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "p-4 border-t border-[var(--border-inset)] flex justify-between",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: resetSize,
                            className: "px-4 py-2 text-xs bg-[var(--primary-color)] text-white border border-[var(--border-inset)] rounded-sm hover:bg-[var(--secondary-color)]",
                            children: "🔄 Reset to Actual Size"
                        }, void 0, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx",
                            lineNumber: 192,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "MainLayout",
    ()=>MainLayout
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/NavigationProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Sidebar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Sidebar.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$MenuBar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/MenuBar.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Taskbar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/navigation/Taskbar.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$Window$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/Window.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ResponsiveTest$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ResponsiveTest.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
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
const MainLayout = ({ children, title = 'NovaSystem', icon, sidebarContent, className })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$NavigationProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["NavigationProvider"], {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["StreamingProvider"], {
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "h-screen w-screen overflow-hidden bg-[var(--bg-primary)] relative safe-area-all",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$Window$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Window"], {
                        title: title,
                        icon: icon,
                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("relative responsive-spacing", className),
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex flex-col h-full responsive-padding",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$MenuBar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MenuBar"], {}, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                    lineNumber: 39,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex flex-1 overflow-hidden responsive-spacing sm:flex-col lg:flex-row",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Sidebar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Sidebar"], {
                                            children: sidebarContent
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                                            lineNumber: 44,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$navigation$2f$Taskbar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Taskbar"], {}, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx",
                        lineNumber: 57,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ResponsiveTest$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ResponsiveTest"], {}, void 0, false, {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPCard",
    ()=>XPCard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
const XPCard = ({ className, variant = 'outset', children, ...props })=>{
    const variantStyles = {
        default: "bg-[var(--xp-content-bg)] border border-[var(--xp-content-border)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]",
        inset: "bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)]",
        outset: "bg-[var(--xp-content-bg)] border border-[var(--xp-window-border-light)] border-t-[var(--xp-window-border-light)] border-l-[var(--xp-window-border-light)] border-r-[var(--xp-window-border-dark)] border-b-[var(--xp-window-border-dark)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("font-sans text-sm", variantStyles[variant], className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 30,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const XPCardHeader = ({ className, children, ...props })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("p-2 border-b border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] font-bold text-black text-sm", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 45,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const XPCardContent = ({ className, children, ...props })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("p-3 text-black text-sm", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 59,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const XPCardFooter = ({ className, children, ...props })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("p-2 border-t border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] text-black text-sm flex justify-end gap-2", className),
        ...props,
        children: children
    }, void 0, false, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
XPCard.Header = XPCardHeader;
XPCard.Content = XPCardContent;
XPCard.Footer = XPCardFooter;
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPButton",
    ()=>XPButton
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
const XPButton = ({ className, variant = 'default', size = 'md', icon, children, onClick, ...props })=>{
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
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(baseStyles, variantStyles[variant], sizeStyles[size], className),
        onClick: handleClick,
        ...props,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "flex items-center justify-center gap-1",
            children: [
                icon && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPInput",
    ()=>XPInput,
    "XPSelect",
    ()=>XPSelect,
    "XPTextArea",
    ()=>XPTextArea
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
'use client';
;
;
const baseInputStyles = "font-sans text-sm text-black bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)] focus:outline-none focus:border-[var(--xp-primary-blue)] focus:ring-1 focus:ring-[var(--xp-primary-blue)] disabled:bg-[var(--xp-button-bg-dark)] disabled:text-[var(--text-disabled)]";
const XPInput = ({ label, error, helperText, variant = 'inset', size = 'md', className, ...props })=>{
    const sizeStyles = {
        sm: "h-5 px-1 text-xs",
        md: "h-6 px-2 text-sm",
        lg: "h-7 px-3 text-base"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 56,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(baseInputStyles, sizeStyles[size], error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 60,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 70,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
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
const XPTextArea = ({ label, error, helperText, variant = 'inset', className, ...props })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 90,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(baseInputStyles, "px-2 py-1 min-h-[60px] resize-vertical", error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 94,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 104,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
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
const XPSelect = ({ label, error, helperText, options, variant = 'inset', size = 'md', className, ...props })=>{
    const sizeStyles = {
        sm: "h-5 px-1 text-xs",
        md: "h-6 px-2 text-sm",
        lg: "h-7 px-3 text-base"
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-1",
        children: [
            label && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                className: "block text-sm font-medium text-black",
                children: label
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 132,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])(baseInputStyles, sizeStyles[size], error && "border-[#ff0000] focus:border-[#ff0000]", className),
                ...props,
                children: options.map((option)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
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
            error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-xs text-[#ff0000]",
                children: error
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx",
                lineNumber: 156,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)),
            helperText && !error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPAgentResponseStream",
    ()=>XPAgentResponseStream
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
;
;
;
;
const XPAgentResponseStream = ({ className })=>{
    const streamingContext = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useStreaming"])();
    const messagesEndRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    // Handle case where context might not be available during SSR
    if (!streamingContext) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
            className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("flex flex-col h-full", className),
            variant: "outset",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-lg",
                                children: "📡"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 24,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                    className: "flex-1 flex items-center justify-center",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-center text-[#666666]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-2xl mb-2",
                                children: "⏳"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 30,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        messagesEndRef.current?.scrollIntoView({
            behavior: 'smooth'
        });
    }, [
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
        link.download = `agent_responses_${new Date().toISOString()}.json`;
        link.click();
        URL.revokeObjectURL(url);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("flex flex-col h-full", className),
        variant: "outset",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex justify-between items-center",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-lg",
                                    children: "📡"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 74,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("w-2 h-2 rounded-full", connectionStatus === 'connected' ? 'bg-[#6bbf44]' : 'bg-[#ff4444]')
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 78,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-xs text-black",
                                    children: connectionStatus === 'connected' ? 'Connected' : 'Disconnected'
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 79,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                    variant: "default",
                                    size: "sm",
                                    onClick: clearResponses,
                                    children: "Clear"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                    lineNumber: 80,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
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
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                className: "flex-1 overflow-y-auto p-2 space-y-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mb-2",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPInput"], {
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
                    filteredResponses.length === 0 && !isStreaming && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-center text-[#666666] py-8",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-2xl mb-2",
                                children: "🤖"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 100,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
                    filteredResponses.map((response, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
                            className: "p-3",
                            variant: "inset",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex items-center justify-between text-xs text-[#666666] mb-2",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-center gap-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("w-3 h-3 rounded-full", getStatusColor(response.status))
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                                    lineNumber: 108,
                                                    columnNumber: 17
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "font-bold text-black text-sm",
                                                    children: response.agentId
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                                    lineNumber: 109,
                                                    columnNumber: 17
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "bg-white p-2 border border-[#c0c0c0] rounded",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
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
                    isStreaming && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-2 text-sm text-[#666666]",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "animate-spin w-4 h-4 border-2 border-[#0054e3] border-t-transparent rounded-full"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx",
                                lineNumber: 125,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
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
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.module.css [app-ssr] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
});
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "WorkflowNode",
    ()=>WorkflowNode,
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.module.css [app-ssr] (css module)");
'use client';
;
;
;
const WorkflowNode = ({ node, variant = 'default', selected = false, draggable = true, onSelect, onPositionChange, onConnect, className = '' })=>{
    const [isDragging, setIsDragging] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [dragStart, setDragStart] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        x: 0,
        y: 0
    });
    const [isConnecting, setIsConnecting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [connectingPort, setConnectingPort] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const nodeRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const handleClick = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        event.stopPropagation();
        if (onSelect) {
            onSelect(node);
        }
    }, [
        node,
        onSelect
    ]);
    const handleMouseDown = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        if (!draggable) return;
        event.preventDefault();
        setIsDragging(true);
        setDragStart({
            x: event.clientX - node.position.x,
            y: event.clientY - node.position.y
        });
    }, [
        draggable,
        node.position
    ]);
    const handleMouseMove = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        if (!isDragging || !onPositionChange) return;
        const newPosition = {
            x: event.clientX - dragStart.x,
            y: event.clientY - dragStart.y
        };
        onPositionChange(node.id, newPosition);
    }, [
        isDragging,
        dragStart,
        node.id,
        onPositionChange
    ]);
    const handleMouseUp = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setIsDragging(false);
    }, []);
    __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].useEffect(()=>{
        if (isDragging) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            return ()=>{
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [
        isDragging,
        handleMouseMove,
        handleMouseUp
    ]);
    const handlePortClick = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((portId, event)=>{
        event.stopPropagation();
        if (isConnecting && connectingPort && onConnect) {
            // Complete connection
            const [fromNodeId, fromPort] = connectingPort.split(':');
            const [toNodeId, toPort] = portId.split(':');
            if (fromNodeId !== toNodeId) {
                onConnect(fromNodeId, toNodeId, fromPort, toPort);
            }
            setIsConnecting(false);
            setConnectingPort(null);
        } else {
            // Start connection
            setIsConnecting(true);
            setConnectingPort(`${node.id}:${portId}`);
        }
    }, [
        isConnecting,
        connectingPort,
        node.id,
        onConnect
    ]);
    const handleKeyDown = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            handleClick(event);
        } else if (event.key === 'Delete' || event.key === 'Backspace') {
            event.preventDefault();
        // Handle node deletion
        }
    }, [
        handleClick
    ]);
    const getStatusIndicator = ()=>{
        switch(node.status){
            case 'processing':
                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeStatus} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].processing}`,
                    "aria-label": "Processing"
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 125,
                    columnNumber: 16
                }, ("TURBOPACK compile-time value", void 0));
            case 'complete':
                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeStatus} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].complete}`,
                    "aria-label": "Complete"
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 127,
                    columnNumber: 16
                }, ("TURBOPACK compile-time value", void 0));
            case 'error':
                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeStatus} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].error}`,
                    "aria-label": "Error"
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 129,
                    columnNumber: 16
                }, ("TURBOPACK compile-time value", void 0));
            default:
                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeStatus} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].idle}`,
                    "aria-label": "Idle"
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 131,
                    columnNumber: 16
                }, ("TURBOPACK compile-time value", void 0));
        }
    };
    const getNodeIcon = ()=>{
        switch(node.type){
            case 'problemSolver':
                return '🧠';
            case 'research':
                return '🔍';
            case 'analysis':
                return '📊';
            case 'synthesizer':
                return '🔗';
            case 'data':
                return '📈';
            case 'optimization':
                return '⚡';
            default:
                return '⚙️';
        }
    };
    const nodeClasses = [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].workflowNode,
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"][node.status],
        variant !== 'default' && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"][variant],
        selected && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].selected,
        isDragging && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].dragging,
        className
    ].filter(Boolean).join(' ');
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        ref: nodeRef,
        className: nodeClasses,
        style: {
            left: node.position.x,
            top: node.position.y,
            transform: isDragging ? 'rotate(2deg)' : 'none'
        },
        role: "button",
        tabIndex: 0,
        "aria-label": `${node.name} node - ${node.description}`,
        "aria-pressed": selected,
        onClick: handleClick,
        onKeyDown: handleKeyDown,
        onMouseDown: handleMouseDown,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodePorts,
                children: [
                    node.inputs.map((input, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionPort} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].input}`,
                            style: {
                                top: index === 0 ? '50%' : index === 1 ? '30%' : '70%'
                            },
                            "data-port": `${node.id}:${input}`,
                            onClick: (e)=>handlePortClick(`${node.id}:${input}`, e),
                            title: `Input: ${input}`,
                            "aria-label": `Input port: ${input}`
                        }, `input-${input}`, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                            lineNumber: 184,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))),
                    node.outputs.map((output, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionPort} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].output}`,
                            style: {
                                top: index === 0 ? '50%' : index === 1 ? '30%' : '70%'
                            },
                            "data-port": `${node.id}:${output}`,
                            onClick: (e)=>handlePortClick(`${node.id}:${output}`, e),
                            title: `Output: ${output}`,
                            "aria-label": `Output port: ${output}`
                        }, `output-${output}`, false, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                            lineNumber: 199,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                lineNumber: 181,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeHeader,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeIcon,
                        children: getNodeIcon()
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                        lineNumber: 215,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeTitle,
                        children: node.name
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                        lineNumber: 218,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    getStatusIndicator()
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                lineNumber: 214,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeContent,
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeDescription,
                    children: node.description
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 226,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                lineNumber: 225,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            isConnecting && connectingPort && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectingIndicator,
                "aria-hidden": "true",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectingDot
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                    lineNumber: 234,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            }, void 0, false, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
                lineNumber: 233,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx",
        lineNumber: 164,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const __TURBOPACK__default__export__ = WorkflowNode;
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.module.css [app-ssr] (css module)", ((__turbopack_context__) => {

__turbopack_context__.v({
});
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "WorkflowCanvas",
    ()=>WorkflowCanvas,
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowNode/WorkflowNode.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.module.css [app-ssr] (css module)");
'use client';
;
;
;
;
const WorkflowCanvas = ({ nodes, connections, selectedNodes = [], zoom = 1, pan = {
    x: 0,
    y: 0
}, onNodeSelect, onNodePositionChange, onConnectionCreate, onConnectionDelete, onZoomChange, onPanChange, onCanvasClick, className = '' })=>{
    const [isPanning, setIsPanning] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [panStart, setPanStart] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        x: 0,
        y: 0
    });
    const [isSelecting, setIsSelecting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [selectionStart, setSelectionStart] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        x: 0,
        y: 0
    });
    const [selectionEnd, setSelectionEnd] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        x: 0,
        y: 0
    });
    const [isConnecting, setIsConnecting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [connectingFrom, setConnectingFrom] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [mousePosition, setMousePosition] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({
        x: 0,
        y: 0
    });
    const canvasRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const svgRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    // Handle canvas mouse events
    const handleMouseDown = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        if (event.target === canvasRef.current) {
            if (event.ctrlKey || event.metaKey) {
                // Start selection
                setIsSelecting(true);
                const rect = canvasRef.current.getBoundingClientRect();
                setSelectionStart({
                    x: event.clientX - rect.left,
                    y: event.clientY - rect.top
                });
                setSelectionEnd({
                    x: event.clientX - rect.left,
                    y: event.clientY - rect.top
                });
            } else {
                // Start panning
                setIsPanning(true);
                setPanStart({
                    x: event.clientX - pan.x,
                    y: event.clientY - pan.y
                });
            }
        }
    }, [
        pan
    ]);
    const handleMouseMove = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        const rect = canvasRef.current?.getBoundingClientRect();
        if (!rect) return;
        const mousePos = {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
        setMousePosition(mousePos);
        if (isPanning && onPanChange) {
            const newPan = {
                x: event.clientX - panStart.x,
                y: event.clientY - panStart.y
            };
            onPanChange(newPan);
        }
        if (isSelecting) {
            setSelectionEnd(mousePos);
        }
    }, [
        isPanning,
        panStart,
        isSelecting,
        onPanChange
    ]);
    const handleMouseUp = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setIsPanning(false);
        setIsSelecting(false);
    }, []);
    // Handle zoom
    const handleZoom = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((delta, center)=>{
        if (!onZoomChange) return;
        const newZoom = Math.max(0.1, Math.min(3, zoom + delta));
        onZoomChange(newZoom);
        if (center && onPanChange) {
            // Zoom towards mouse position
            const zoomFactor = newZoom / zoom;
            const newPan = {
                x: center.x - (center.x - pan.x) * zoomFactor,
                y: center.y - (center.y - pan.y) * zoomFactor
            };
            onPanChange(newPan);
        }
    }, [
        zoom,
        pan,
        onZoomChange,
        onPanChange
    ]);
    // Handle wheel zoom
    const handleWheel = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        event.preventDefault();
        const delta = event.deltaY > 0 ? -0.1 : 0.1;
        handleZoom(delta, mousePosition);
    }, [
        handleZoom,
        mousePosition
    ]);
    // Handle canvas click
    const handleCanvasClick = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((event)=>{
        if (event.target === canvasRef.current && onCanvasClick) {
            const rect = canvasRef.current.getBoundingClientRect();
            onCanvasClick({
                x: event.clientX - rect.left,
                y: event.clientY - rect.top
            });
        }
    }, [
        onCanvasClick
    ]);
    // Render connection path
    const renderConnection = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((connection)=>{
        const fromNode = nodes.find((n)=>n.id === connection.fromNodeId);
        const toNode = nodes.find((n)=>n.id === connection.toNodeId);
        if (!fromNode || !toNode) return null;
        const fromX = fromNode.position.x + 180; // Node width
        const fromY = fromNode.position.y + 40; // Node height / 2
        const toX = toNode.position.x;
        const toY = toNode.position.y + 40;
        // Create curved path
        const controlPoint1X = fromX + 50;
        const controlPoint1Y = fromY;
        const controlPoint2X = toX - 50;
        const controlPoint2Y = toY;
        const pathData = `M ${fromX} ${fromY} C ${controlPoint1X} ${controlPoint1Y}, ${controlPoint2X} ${controlPoint2Y}, ${toX} ${toY}`;
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("g", {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                    d: pathData,
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionPath} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"][connection.status]}`,
                    strokeWidth: connection.status === 'active' ? 3 : 2,
                    onClick: ()=>onConnectionDelete?.(connection.id)
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                    lineNumber: 170,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("polygon", {
                    points: `${toX - 10},${toY - 5} ${toX},${toY} ${toX - 10},${toY + 5}`,
                    className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionArrow} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"][connection.status]}`
                }, void 0, false, {
                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                    lineNumber: 177,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, connection.id, true, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
            lineNumber: 169,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0));
    }, [
        nodes,
        onConnectionDelete
    ]);
    // Render temporary connection line while connecting
    const renderTemporaryConnection = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        if (!isConnecting || !connectingFrom) return null;
        const fromNode = nodes.find((n)=>n.id === connectingFrom);
        if (!fromNode) return null;
        const fromX = fromNode.position.x + 180;
        const fromY = fromNode.position.y + 40;
        const toX = mousePosition.x;
        const toY = mousePosition.y;
        const controlPoint1X = fromX + 50;
        const controlPoint1Y = fromY;
        const controlPoint2X = toX - 50;
        const controlPoint2Y = toY;
        const pathData = `M ${fromX} ${fromY} C ${controlPoint1X} ${controlPoint1Y}, ${controlPoint2X} ${controlPoint2Y}, ${toX} ${toY}`;
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: pathData,
            className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionPath} ${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].active}`,
            strokeDasharray: "5,5",
            strokeWidth: 2
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
            lineNumber: 205,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0));
    }, [
        isConnecting,
        connectingFrom,
        nodes,
        mousePosition
    ]);
    // Event listeners
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (isPanning || isSelecting) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            return ()=>{
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [
        isPanning,
        isSelecting,
        handleMouseMove,
        handleMouseUp
    ]);
    const canvasClasses = [
        __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].workflowCanvas,
        isPanning && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].panning,
        isSelecting && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].selecting,
        isConnecting && __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connecting,
        className
    ].filter(Boolean).join(' ');
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: canvasClasses,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                ref: canvasRef,
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].canvasViewport,
                onMouseDown: handleMouseDown,
                onWheel: handleWheel,
                onClick: handleCanvasClick,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].canvasContent,
                        style: {
                            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionLayer,
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                    ref: svgRef,
                                    className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].connectionSvg,
                                    style: {
                                        width: '100%',
                                        height: '100%'
                                    },
                                    children: [
                                        connections.map(renderConnection),
                                        renderTemporaryConnection()
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                    lineNumber: 252,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                lineNumber: 251,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].nodeLayer,
                                children: nodes.map((node)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowNode$2f$WorkflowNode$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["WorkflowNode"], {
                                        node: node,
                                        selected: selectedNodes.includes(node.id),
                                        onSelect: onNodeSelect,
                                        onPositionChange: onNodePositionChange,
                                        onConnect: onConnectionCreate,
                                        onDisconnect: onConnectionDelete
                                    }, node.id, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                        lineNumber: 268,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                lineNumber: 266,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 244,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    isSelecting && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].selectionRectangle,
                        style: {
                            left: Math.min(selectionStart.x, selectionEnd.x),
                            top: Math.min(selectionStart.y, selectionEnd.y),
                            width: Math.abs(selectionEnd.x - selectionStart.x),
                            height: Math.abs(selectionEnd.y - selectionStart.y)
                        }
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 283,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                lineNumber: 237,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].canvasControls,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].zoomControls,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].zoomControl,
                                onClick: ()=>handleZoom(0.1),
                                title: "Zoom In",
                                children: "+"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                lineNumber: 298,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].zoomControl,
                                onClick: ()=>handleZoom(-0.1),
                                title: "Zoom Out",
                                children: "−"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                                lineNumber: 305,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 297,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].canvasControl,
                        onClick: ()=>onPanChange?.({
                                x: 0,
                                y: 0
                            }),
                        title: "Reset View",
                        children: "🎯"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 313,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                lineNumber: 296,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].zoomIndicator,
                children: [
                    Math.round(zoom * 100),
                    "%"
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                lineNumber: 323,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].canvasToolbar,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: `${__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].toolbarButton} ${isConnecting ? __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].active : ''}`,
                        onClick: ()=>{
                            setIsConnecting(!isConnecting);
                            setConnectingFrom(null);
                        },
                        title: "Connection Mode",
                        children: "🔗 Connect"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 329,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].toolbarButton,
                        onClick: ()=>{
                            // Auto-layout nodes
                            const cols = Math.ceil(Math.sqrt(nodes.length));
                            nodes.forEach((node, index)=>{
                                const x = index % cols * 220;
                                const y = Math.floor(index / cols) * 120;
                                onNodePositionChange?.(node.id, {
                                    x,
                                    y
                                });
                            });
                        },
                        title: "Auto Layout",
                        children: "📐 Layout"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 339,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].toolbarButton,
                        onClick: ()=>{
                            // Clear all connections
                            connections.forEach((conn)=>onConnectionDelete?.(conn.id));
                        },
                        title: "Clear Connections",
                        children: "🗑️ Clear"
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                        lineNumber: 354,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
                lineNumber: 328,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx",
        lineNumber: 236,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const __TURBOPACK__default__export__ = WorkflowCanvas;
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/services/workflowApi.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * Workflow API Service
 *
 * Communicates with the Flask backend for workflow execution and status polling.
 */ // Backend API base URL - defaults to Flask dev server
__turbopack_context__.s([
    "executeWorkflow",
    ()=>executeWorkflow,
    "getWorkflowStatus",
    ()=>getWorkflowStatus
]);
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
async function executeWorkflow(nodes, connections) {
    const response = await fetch(`${API_BASE_URL}/api/workflow/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nodes,
            connections
        })
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    return response.json();
}
async function getWorkflowStatus(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/status`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    return response.json();
}
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/hooks/useWorkflowPolling.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__,
    "useWorkflowPolling",
    ()=>useWorkflowPolling
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$services$2f$workflowApi$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/services/workflowApi.ts [app-ssr] (ecmascript)");
'use client';
;
;
const initialState = {
    nodeStates: {},
    nodeOutputs: {},
    executionOrder: [],
    sessionStatus: null,
    isComplete: false,
    isError: false,
    error: null,
    isPolling: false
};
function useWorkflowPolling(sessionId, interval = 2000) {
    const [state, setState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(initialState);
    const intervalRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const isMountedRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(true);
    const poll = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(async ()=>{
        if (!sessionId) return;
        try {
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$services$2f$workflowApi$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getWorkflowStatus"])(sessionId);
            if (!isMountedRef.current) return;
            const isComplete = response.status === 'completed';
            const isError = response.status === 'error';
            setState({
                nodeStates: response.node_states,
                nodeOutputs: response.node_outputs,
                executionOrder: response.execution_order,
                sessionStatus: response.status,
                isComplete,
                isError,
                error: null,
                isPolling: !isComplete && !isError
            });
            // Stop polling if complete or error
            if (isComplete || isError) {
                if (intervalRef.current) {
                    clearInterval(intervalRef.current);
                    intervalRef.current = null;
                }
            }
        } catch (err) {
            if (!isMountedRef.current) return;
            setState((prev)=>({
                    ...prev,
                    isError: true,
                    error: err instanceof Error ? err.message : 'Unknown error',
                    isPolling: false
                }));
            // Stop polling on error
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        }
    }, [
        sessionId
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        isMountedRef.current = true;
        if (sessionId) {
            // Reset state when session changes
            setState({
                ...initialState,
                isPolling: true
            });
            // Initial poll
            poll();
            // Start interval polling
            intervalRef.current = setInterval(poll, interval);
        } else {
            // No session, reset state
            setState(initialState);
        }
        return ()=>{
            isMountedRef.current = false;
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [
        sessionId,
        interval,
        poll
    ]);
    return state;
}
const __TURBOPACK__default__export__ = useWorkflowPolling;
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "XPWorkflowSystem",
    ()=>XPWorkflowSystem
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPCard.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPButton.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/ui/XPInput.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$XPAgentResponseStream$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/XPAgentResponseStream.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/streaming/SimpleStreamingProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/WorkflowCanvas/WorkflowCanvas.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$services$2f$workflowApi$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/services/workflowApi.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$hooks$2f$useWorkflowPolling$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/hooks/useWorkflowPolling.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts [app-ssr] (ecmascript)");
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
const mapBackendStateToNodeStatus = (state)=>{
    switch(state){
        case 'processing':
            return 'processing';
        case 'completed':
            return 'complete';
        case 'error':
            return 'error';
        default:
            return 'idle';
    }
};
const mapBackendStateToConnectionStatus = (state)=>{
    switch(state){
        case 'processing':
            return 'active';
        case 'completed':
            return 'success';
        case 'error':
            return 'error';
        default:
            return 'idle';
    }
};
const XPWorkflowSystem = ()=>{
    const [problemStatement, setProblemStatement] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('');
    const [selectedAgents, setSelectedAgents] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [workflowStatus, setWorkflowStatus] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('idle');
    const [activeTab, setActiveTab] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('status');
    const [canvasNodes, setCanvasNodes] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [canvasConnections, setCanvasConnections] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [sessionId, setSessionId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isStarting, setIsStarting] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const { addResponse, setIsStreaming, clearResponses } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$SimpleStreamingProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useStreaming"])();
    const { nodeStates, nodeOutputs, isComplete, error: pollingError, sessionStatus } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$hooks$2f$useWorkflowPolling$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useWorkflowPolling"])(sessionId);
    const previousOutputsRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])({});
    const handleAgentToggle = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((agent)=>{
        setSelectedAgents((prev)=>prev.some((a)=>a.id === agent.id) ? prev.filter((a)=>a.id !== agent.id) : [
                ...prev,
                agent
            ]);
    }, []);
    const buildCanvasNodes = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        const timestamp = Date.now();
        return selectedAgents.map((agent, index)=>{
            const column = index % 3;
            const row = Math.floor(index / 3);
            return {
                id: `node-${agent.id}-${timestamp}-${index}`,
                type: agent.type,
                name: agent.name,
                description: agent.description,
                status: 'idle',
                position: {
                    x: 60 + column * 220,
                    y: 60 + row * 160
                },
                inputs: [
                    'input'
                ],
                outputs: [
                    'output'
                ],
                data: {
                    agentId: agent.id
                }
            };
        });
    }, [
        selectedAgents
    ]);
    const generateConnections = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((nodes)=>nodes.slice(0, -1).map((node, index)=>({
                id: `conn-${node.id}-${nodes[index + 1].id}`,
                fromNodeId: node.id,
                toNodeId: nodes[index + 1].id,
                fromPort: node.outputs[0] || 'output',
                toPort: nodes[index + 1].inputs[0] || 'input',
                status: 'idle'
            })), []);
    const handleNodePositionChange = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((nodeId, position)=>{
        setCanvasNodes((prev)=>prev.map((node)=>node.id === nodeId ? {
                    ...node,
                    position
                } : node));
    }, []);
    const handleConnectionCreate = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((fromNodeId, toNodeId, fromPort, toPort)=>{
        setCanvasConnections((prev)=>{
            if (prev.some((conn)=>conn.fromNodeId === fromNodeId && conn.toNodeId === toNodeId)) {
                return prev;
            }
            return [
                ...prev,
                {
                    id: `conn-${fromNodeId}-${toNodeId}`,
                    fromNodeId,
                    toNodeId,
                    fromPort,
                    toPort,
                    status: 'idle'
                }
            ];
        });
    }, []);
    const handleConnectionDelete = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((connectionId)=>{
        setCanvasConnections((prev)=>prev.filter((conn)=>conn.id !== connectionId));
    }, []);
    const startWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(async ()=>{
        if (!problemStatement.trim()) {
            alert('Please enter a problem statement.');
            return;
        }
        if (selectedAgents.length === 0) {
            alert('Please select at least one agent.');
            return;
        }
        setWorkflowStatus('running');
        setActiveTab('status');
        setIsStreaming(true);
        clearResponses();
        setIsStarting(true);
        previousOutputsRef.current = {};
        const nodes = buildCanvasNodes();
        const connections = generateConnections(nodes);
        setCanvasNodes(nodes);
        setCanvasConnections(connections);
        const nodePayloads = nodes.map((node)=>({
                id: node.id,
                type: node.type,
                title: problemStatement,
                agent: node.name,
                metadata: {
                    description: node.description,
                    agentId: node.data?.agentId
                }
            }));
        const connectionPayloads = connections.map((conn)=>({
                from: conn.fromNodeId,
                to: conn.toNodeId
            }));
        try {
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$services$2f$workflowApi$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["executeWorkflow"])(nodePayloads, connectionPayloads);
            setSessionId(response.session_id);
        } catch (error) {
            console.error('Failed to start workflow', error);
            setWorkflowStatus('error');
            setIsStreaming(false);
            setSessionId(null);
            const message = error instanceof Error ? error.message : 'Failed to start workflow';
            addResponse({
                agentId: 'System',
                content: message,
                timestamp: Date.now(),
                status: 'error'
            });
        } finally{
            setIsStarting(false);
        }
    }, [
        addResponse,
        buildCanvasNodes,
        clearResponses,
        generateConnections,
        problemStatement,
        selectedAgents.length,
        setIsStreaming
    ]);
    const stopWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setWorkflowStatus('idle');
        setIsStreaming(false);
        setSessionId(null);
        addResponse({
            agentId: 'System',
            content: 'Workflow stopped by user.',
            timestamp: Date.now(),
            status: 'complete'
        });
    }, [
        addResponse,
        setIsStreaming
    ]);
    const resetWorkflow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setProblemStatement('');
        setSelectedAgents([]);
        setWorkflowStatus('idle');
        setSessionId(null);
        setCanvasNodes([]);
        setCanvasConnections([]);
        previousOutputsRef.current = {};
        clearResponses();
        setIsStreaming(false);
        setActiveTab('status');
    }, [
        clearResponses,
        setIsStreaming
    ]);
    const getAgentNodeStatus = (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((agentId)=>{
        const node = canvasNodes.find((n)=>n.data?.agentId === agentId);
        return node?.status || 'idle';
    }, [
        canvasNodes
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!canvasNodes.length) return;
        setCanvasNodes((prev)=>prev.map((node)=>{
                const backendState = nodeStates[node.id];
                if (!backendState) return node;
                return {
                    ...node,
                    status: mapBackendStateToNodeStatus(backendState)
                };
            }));
    }, [
        nodeStates,
        canvasNodes.length
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!canvasConnections.length) return;
        setCanvasConnections((prev)=>prev.map((conn)=>({
                    ...conn,
                    status: mapBackendStateToConnectionStatus(nodeStates[conn.fromNodeId])
                })));
    }, [
        nodeStates,
        canvasConnections.length
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!sessionId) return;
        if (pollingError) {
            setWorkflowStatus('error');
            setIsStreaming(false);
            return;
        }
        const nodeStateValues = Object.values(nodeStates);
        const hasErrors = nodeStateValues.some((state)=>state === 'error') || sessionStatus === 'error';
        const allFinished = nodeStateValues.length > 0 && nodeStateValues.every((state)=>state === 'completed' || state === 'error');
        if (isComplete || allFinished) {
            setWorkflowStatus(hasErrors ? 'error' : 'completed');
            setIsStreaming(false);
        } else {
            setWorkflowStatus('running');
        }
    }, [
        isComplete,
        nodeStates,
        pollingError,
        sessionId,
        sessionStatus,
        setIsStreaming
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!sessionId) return;
        Object.entries(nodeOutputs).forEach(([nodeId, output])=>{
            if (!output || previousOutputsRef.current[nodeId] === output) {
                return;
            }
            previousOutputsRef.current[nodeId] = output;
            const node = canvasNodes.find((n)=>n.id === nodeId);
            addResponse({
                agentId: node?.name || nodeId,
                content: output,
                timestamp: Date.now(),
                status: 'complete'
            });
        });
    }, [
        addResponse,
        canvasNodes,
        nodeOutputs,
        sessionId
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex h-full gap-4 p-4 bg-[#ece9d8]",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
                className: "w-1/3 flex flex-col",
                variant: "outset",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center gap-2",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "text-lg",
                                    children: "⚙️"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 307,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    children: "Workflow Configuration"
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 308,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                            lineNumber: 306,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 305,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                        className: "flex-1 overflow-y-auto space-y-4",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPInput$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPTextArea"], {
                                    label: "Problem Statement",
                                    placeholder: "Describe the problem you want to solve...",
                                    value: problemStatement,
                                    onChange: (e)=>setProblemStatement(e.target.value),
                                    disabled: workflowStatus === 'running' || isStarting,
                                    rows: 4
                                }, void 0, false, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 313,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 312,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        className: "text-sm font-bold text-black mb-2",
                                        children: "Select Agents"
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 324,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "grid grid-cols-2 gap-2",
                                        children: MOCK_AGENTS.map((agent)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
                                                className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("p-2 cursor-pointer transition-all duration-100", selectedAgents.some((a)=>a.id === agent.id) ? "border-[#0054e3] bg-[#e6f2ff]" : "border-[#c0c0c0] hover:bg-[#f0f0f0]"),
                                                variant: "outset",
                                                onClick: ()=>handleAgentToggle(agent),
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-center gap-2 mb-1",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "text-sm",
                                                                children: agent.icon
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 339,
                                                                columnNumber: 21
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                className: "font-medium text-black text-xs",
                                                                children: agent.name
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 340,
                                                                columnNumber: 21
                                                            }, ("TURBOPACK compile-time value", void 0))
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 338,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-xs text-[#666666]",
                                                        children: agent.description
                                                    }, void 0, false, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 342,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0))
                                                ]
                                            }, agent.id, true, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 327,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0)))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 325,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 323,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 311,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Footer, {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "default",
                                onClick: resetWorkflow,
                                disabled: workflowStatus === 'running' || isStarting,
                                children: "Reset"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 349,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            workflowStatus === 'running' ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "danger",
                                onClick: stopWorkflow,
                                children: "Stop Workflow"
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 353,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                variant: "primary",
                                onClick: startWorkflow,
                                disabled: !problemStatement.trim() || selectedAgents.length === 0 || isStarting,
                                children: isStarting ? 'Starting...' : 'Start Workflow'
                            }, void 0, false, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 357,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 348,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                lineNumber: 304,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
                className: "w-2/3 flex flex-col",
                variant: "outset",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Header, {
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex justify-between items-center",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex items-center gap-2",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "text-lg",
                                            children: "🔄"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 373,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: "Workflow Execution"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 374,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 372,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "flex gap-1",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'status' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('status'),
                                            size: "sm",
                                            children: "Status"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 377,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'responses' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('responses'),
                                            size: "sm",
                                            children: "Responses"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 384,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPButton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPButton"], {
                                            variant: activeTab === 'results' ? 'primary' : 'default',
                                            onClick: ()=>setActiveTab('results'),
                                            size: "sm",
                                            children: "Results"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 391,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                    lineNumber: 376,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0))
                            ]
                        }, void 0, true, {
                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                            lineNumber: 371,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 370,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"].Content, {
                        className: "flex-1 overflow-hidden flex flex-col gap-3",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex-1 overflow-hidden",
                                children: [
                                    activeTab === 'status' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "h-full flex flex-col space-y-4 overflow-y-auto",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "flex items-center gap-2",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: "text-sm font-bold text-black",
                                                        children: "Current Status:"
                                                    }, void 0, false, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 406,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("text-sm font-bold capitalize", workflowStatus === 'running' && "text-[#0054e3]", workflowStatus === 'completed' && "text-[#6bbf44]", workflowStatus === 'error' && "text-[#ff4444]"),
                                                        children: workflowStatus
                                                    }, void 0, false, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 407,
                                                        columnNumber: 19
                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                    sessionId && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: "text-[11px] text-[#3a3a3a] ml-2",
                                                        children: [
                                                            "Session ",
                                                            sessionId.slice(0, 8)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 416,
                                                        columnNumber: 21
                                                    }, ("TURBOPACK compile-time value", void 0))
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 405,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "grid grid-cols-2 gap-3",
                                                children: selectedAgents.map((agent)=>{
                                                    const nodeStatus = getAgentNodeStatus(agent.id);
                                                    const statusText = nodeStatus === 'processing' ? 'Processing...' : nodeStatus === 'complete' ? 'Complete' : nodeStatus === 'error' ? 'Error' : 'Idle';
                                                    const dotClass = nodeStatus === 'processing' ? "bg-[#0054e3] animate-pulse" : nodeStatus === 'complete' ? "bg-[#6bbf44]" : nodeStatus === 'error' ? "bg-[#ff4444]" : "bg-[#808080]";
                                                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$ui$2f$XPCard$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPCard"], {
                                                        className: "p-2",
                                                        variant: "inset",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "flex items-center gap-2 mb-1",
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                        className: "text-sm",
                                                                        children: agent.icon
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                        lineNumber: 441,
                                                                        columnNumber: 27
                                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                        className: "font-medium text-black text-xs",
                                                                        children: agent.name
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                        lineNumber: 442,
                                                                        columnNumber: 27
                                                                    }, ("TURBOPACK compile-time value", void 0))
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 440,
                                                                columnNumber: 25
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                className: "text-xs text-[#666666] mb-2",
                                                                children: agent.description
                                                            }, void 0, false, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 444,
                                                                columnNumber: 25
                                                            }, ("TURBOPACK compile-time value", void 0)),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "flex items-center gap-2",
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$lib$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["cn"])("w-2 h-2 rounded-full", dotClass)
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                        lineNumber: 446,
                                                                        columnNumber: 27
                                                                    }, ("TURBOPACK compile-time value", void 0)),
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                        className: "text-xs text-[#666666]",
                                                                        children: statusText
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                        lineNumber: 447,
                                                                        columnNumber: 27
                                                                    }, ("TURBOPACK compile-time value", void 0))
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                                lineNumber: 445,
                                                                columnNumber: 25
                                                            }, ("TURBOPACK compile-time value", void 0))
                                                        ]
                                                    }, agent.id, true, {
                                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                        lineNumber: 439,
                                                        columnNumber: 23
                                                    }, ("TURBOPACK compile-time value", void 0));
                                                })
                                            }, void 0, false, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 419,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 404,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    activeTab === 'responses' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "h-full",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$streaming$2f$XPAgentResponseStream$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPAgentResponseStream"], {
                                            className: "h-full"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 459,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 458,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    activeTab === 'results' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "h-full flex items-center justify-center text-[#666666]",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "text-center",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    className: "text-4xl mb-2",
                                                    children: "📊"
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                    lineNumber: 465,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0)),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "text-sm",
                                                    children: "Workflow results will appear here after completion."
                                                }, void 0, false, {
                                                    fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                    lineNumber: 466,
                                                    columnNumber: 19
                                                }, ("TURBOPACK compile-time value", void 0))
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 464,
                                            columnNumber: 17
                                        }, ("TURBOPACK compile-time value", void 0))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 463,
                                        columnNumber: 15
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 402,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "h-[360px] border border-[#c0c0c0] bg-white shadow-inner rounded-sm overflow-hidden",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center justify-between px-3 py-2 border-b border-[#c0c0c0] bg-[#f3f3f3] text-xs text-black",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "font-bold",
                                                children: "Workflow Canvas"
                                            }, void 0, false, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 474,
                                                columnNumber: 15
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            sessionId && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "text-[#0054e3] font-semibold text-[11px]",
                                                children: [
                                                    "Live from session ",
                                                    sessionId.slice(0, 8)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                                lineNumber: 476,
                                                columnNumber: 17
                                            }, ("TURBOPACK compile-time value", void 0))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 473,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "h-[300px]",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$WorkflowCanvas$2f$WorkflowCanvas$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["WorkflowCanvas"], {
                                            nodes: canvasNodes,
                                            connections: canvasConnections,
                                            onNodePositionChange: handleNodePositionChange,
                                            onConnectionCreate: handleConnectionCreate,
                                            onConnectionDelete: handleConnectionDelete,
                                            className: "h-full"
                                        }, void 0, false, {
                                            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                            lineNumber: 482,
                                            columnNumber: 15
                                        }, ("TURBOPACK compile-time value", void 0))
                                    }, void 0, false, {
                                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                        lineNumber: 481,
                                        columnNumber: 13
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                                lineNumber: 472,
                                columnNumber: 11
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                        lineNumber: 401,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
                lineNumber: 369,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx",
        lineNumber: 302,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>WorkflowPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$layout$2f$MainLayout$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/layout/MainLayout.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$XPWorkflowSystem$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/components/workflow/XPWorkflowSystem.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
function WorkflowPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$layout$2f$MainLayout$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MainLayout"], {
        title: "Workflow Engine",
        icon: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm"
        }, void 0, false, {
            fileName: "[project]/NovaSystem-Streamlined/novasystem_modern_ui/src/app/workflow/page.tsx",
            lineNumber: 11,
            columnNumber: 13
        }, void 0),
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$NovaSystem$2d$Streamlined$2f$novasystem_modern_ui$2f$src$2f$components$2f$workflow$2f$XPWorkflowSystem$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["XPWorkflowSystem"], {}, void 0, false, {
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
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__cf25c7be._.js.map