(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_electron"] = factory(require("react"));
	else
		root["dazzler_electron"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return /******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/electron/common/ipcEvents.ts":
/*!******************************************!*\
  !*** ./src/electron/common/ipcEvents.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports) => {


exports.__esModule = true;
exports.WINDOW_STATE_INIT = exports.WINDOW_FULLSCREEN = exports.WINDOW_MOVE = exports.WINDOW_RESIZE = void 0;
exports.WINDOW_RESIZE = 'WINDOW_RESIZE';
exports.WINDOW_MOVE = 'WINDOW_MOVE';
exports.WINDOW_FULLSCREEN = 'WINDOW_FULLSCREEN';
exports.WINDOW_STATE_INIT = 'WINDOW_STATE_INIT';
// export type WindowEvent =
//     | typeof WINDOW_RESIZE
//     | typeof WINDOW_MOVE
//     | typeof WINDOW_FULLSCREEN;


/***/ }),

/***/ "./src/electron/renderer/components/WindowState.tsx":
/*!**********************************************************!*\
  !*** ./src/electron/renderer/components/WindowState.tsx ***!
  \**********************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
exports.__esModule = true;
var react_1 = __webpack_require__(/*! react */ "react");
var electron_1 = __webpack_require__(/*! electron */ "electron");
var ipcEvents_1 = __webpack_require__(/*! ../../common/ipcEvents */ "./src/electron/common/ipcEvents.ts");
var WindowState = function (props) {
    var updateAspects = props.updateAspects;
    react_1.useEffect(function () {
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_MOVE, function (event, data) {
            updateAspects(__assign({}, data));
        });
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_FULLSCREEN, function (event, data) {
            updateAspects(__assign({}, data));
        });
        electron_1.ipcRenderer
            .invoke(ipcEvents_1.WINDOW_STATE_INIT)
            .then(function (initial) { return updateAspects(__assign({}, initial)); });
    }, []);
    return null;
};
exports.default = WindowState;


/***/ }),

/***/ "./src/electron/renderer/index.ts":
/*!****************************************!*\
  !*** ./src/electron/renderer/index.ts ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.WindowState = void 0;
var WindowState_1 = __importDefault(__webpack_require__(/*! ./components/WindowState */ "./src/electron/renderer/components/WindowState.tsx"));
exports.WindowState = WindowState_1["default"];


/***/ }),

/***/ "electron":
/*!***************************!*\
  !*** external "electron" ***!
  \***************************/
/***/ ((module) => {

module.exports = require("electron");

/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./src/electron/renderer/index.ts");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl8yYzgyZTQyYWVhMmRmNWIwMjZlZC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUmxDLHdEQUFnQztBQUVoQyxpRUFBcUM7QUFDckMsMEdBS2dDO0FBS2hDLElBQU0sV0FBVyxHQUFHLFVBQUMsS0FBdUI7SUFDakMsaUJBQWEsR0FBSSxLQUFLLGNBQVQsQ0FBVTtJQUU5QixpQkFBUyxDQUFDO1FBQ04sc0JBQVcsQ0FBQyxFQUFFLENBQUMseUJBQWEsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJO1lBQ3RDLElBQU0sSUFBSSxHQUFlLElBQUksQ0FBQztZQUM5QixhQUFhLGNBQUssSUFBSSxFQUFFLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxzQkFBVyxDQUFDLEVBQUUsQ0FBQyx1QkFBVyxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDcEMsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsc0JBQVcsQ0FBQyxFQUFFLENBQUMsNkJBQWlCLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUMxQyxhQUFhLGNBQUssSUFBSSxFQUFFLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxzQkFBVzthQUNOLE1BQU0sQ0FBQyw2QkFBaUIsQ0FBQzthQUN6QixJQUFJLENBQUMsVUFBQyxPQUFPLElBQUssb0JBQWEsY0FBSyxPQUFPLEVBQUUsRUFBM0IsQ0FBMkIsQ0FBQyxDQUFDO0lBQ3hELENBQUMsRUFBRSxFQUFFLENBQUMsQ0FBQztJQUVQLE9BQU8sSUFBSSxDQUFDO0FBQ2hCLENBQUMsQ0FBQztBQUVGLGtCQUFlLFdBQVcsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNuQzNCLCtJQUFtRDtBQUcvQyxzQkFIRyx3QkFBVyxDQUdIOzs7Ozs7Ozs7OztBQ0hmOzs7Ozs7Ozs7O0FDQUE7Ozs7OztVQ0FBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7O1VBRUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7Ozs7VUV0QkE7VUFDQTtVQUNBO1VBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vL3dlYnBhY2svdW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbj8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9jb21tb24vaXBjRXZlbnRzLnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2NvbXBvbmVudHMvV2luZG93U3RhdGUudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIFwiZWxlY3Ryb25cIj8iLCJ3ZWJwYWNrOi8vLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9PyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYm9vdHN0cmFwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYmVmb3JlLXN0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYWZ0ZXItc3RhcnR1cD8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9lbGVjdHJvblwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkoc2VsZiwgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fKSB7XG5yZXR1cm4gIiwiZXhwb3J0IGNvbnN0IFdJTkRPV19SRVNJWkUgPSAnV0lORE9XX1JFU0laRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX01PVkUgPSAnV0lORE9XX01PVkUnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19GVUxMU0NSRUVOID0gJ1dJTkRPV19GVUxMU0NSRUVOJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU1RBVEVfSU5JVCA9ICdXSU5ET1dfU1RBVEVfSU5JVCc7XG5cbi8vIGV4cG9ydCB0eXBlIFdpbmRvd0V2ZW50ID1cbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfUkVTSVpFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX01PVkVcbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfRlVMTFNDUkVFTjtcbiIsImltcG9ydCB7dXNlRWZmZWN0fSBmcm9tICdyZWFjdCc7XG5pbXBvcnQge0RhenpsZXJQcm9wc30gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5pbXBvcnQge2lwY1JlbmRlcmVyfSBmcm9tICdlbGVjdHJvbic7XG5pbXBvcnQge1xuICAgIFdJTkRPV19SRVNJWkUsXG4gICAgV0lORE9XX01PVkUsXG4gICAgV0lORE9XX0ZVTExTQ1JFRU4sXG4gICAgV0lORE9XX1NUQVRFX0lOSVQsXG59IGZyb20gJy4uLy4uL2NvbW1vbi9pcGNFdmVudHMnO1xuaW1wb3J0IHtXaW5kb3dTaXplLCBXaW5kb3dTdGF0dXN9IGZyb20gJy4uLy4uL2NvbW1vbi90eXBlcyc7XG5cbnR5cGUgV2luZG93U3RhdGVQcm9wcyA9IFdpbmRvd1N0YXR1cyAmIHt9ICYgRGF6emxlclByb3BzO1xuXG5jb25zdCBXaW5kb3dTdGF0ZSA9IChwcm9wczogV2luZG93U3RhdGVQcm9wcykgPT4ge1xuICAgIGNvbnN0IHt1cGRhdGVBc3BlY3RzfSA9IHByb3BzO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgaXBjUmVuZGVyZXIub24oV0lORE9XX1JFU0laRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBzaXplOiBXaW5kb3dTaXplID0gZGF0YTtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLnNpemV9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIGlwY1JlbmRlcmVyLm9uKFdJTkRPV19NT1ZFLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIGlwY1JlbmRlcmVyLm9uKFdJTkRPV19GVUxMU0NSRUVOLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIGlwY1JlbmRlcmVyXG4gICAgICAgICAgICAuaW52b2tlKFdJTkRPV19TVEFURV9JTklUKVxuICAgICAgICAgICAgLnRoZW4oKGluaXRpYWwpID0+IHVwZGF0ZUFzcGVjdHMoey4uLmluaXRpYWx9KSk7XG4gICAgfSwgW10pO1xuXG4gICAgcmV0dXJuIG51bGw7XG59O1xuXG5leHBvcnQgZGVmYXVsdCBXaW5kb3dTdGF0ZTtcbiIsImltcG9ydCBXaW5kb3dTdGF0ZSBmcm9tICcuL2NvbXBvbmVudHMvV2luZG93U3RhdGUnO1xuXG5leHBvcnQge1xuICAgIFdpbmRvd1N0YXRlLFxufVxuIiwibW9kdWxlLmV4cG9ydHMgPSByZXF1aXJlKFwiZWxlY3Ryb25cIik7IiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIiIsIi8vIHN0YXJ0dXBcbi8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLy8gVGhpcyBlbnRyeSBtb2R1bGUgaXMgcmVmZXJlbmNlZCBieSBvdGhlciBtb2R1bGVzIHNvIGl0IGNhbid0IGJlIGlubGluZWRcbnZhciBfX3dlYnBhY2tfZXhwb3J0c19fID0gX193ZWJwYWNrX3JlcXVpcmVfXyhcIi4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzXCIpO1xuIiwiIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9