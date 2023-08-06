"use strict";
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_icons"] = factory(require("react"));
	else
		root["dazzler_icons"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return (self["webpackChunkdazzler_name_"] = self["webpackChunkdazzler_name_"] || []).push([["icons"],{

/***/ "./src/icons/ts/IconContext.ts":
/*!*************************************!*\
  !*** ./src/icons/ts/IconContext.ts ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
exports.default = react_1["default"].createContext({
    packs: {},
    addPack: function () { return null; },
    isLoaded: function () { return false; },
});


/***/ }),

/***/ "./src/icons/ts/components/FlagIconPack.tsx":
/*!**************************************************!*\
  !*** ./src/icons/ts/components/FlagIconPack.tsx ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var IconPack_1 = __importDefault(__webpack_require__(/*! ./IconPack */ "./src/icons/ts/components/IconPack.tsx"));
/**
 * Free icon pack from https://github.com/lipis/flag-icons
 *
 * :Pack:
 *     ``flag-icon``
 *
 * :Example:
 *      .. code-block:: python
 *
 *          icons.FlagIconPack()
 *          icons.Icon('flag-icon flag-icon-ca')
 */
var FlagIconPack = function (_) {
    return (react_1["default"].createElement(IconPack_1["default"], { name: "flag-icon", url: "https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/4.1.5/css/flag-icons.min.css" }));
};
FlagIconPack.defaultProps = {};
exports.default = FlagIconPack;


/***/ }),

/***/ "./src/icons/ts/components/FoundIconPack.tsx":
/*!***************************************************!*\
  !*** ./src/icons/ts/components/FoundIconPack.tsx ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var IconPack_1 = __importDefault(__webpack_require__(/*! ./IconPack */ "./src/icons/ts/components/IconPack.tsx"));
/**
 * Free icon pack from https://zurb.com/playground/foundation-icon-fonts-3
 *
 * :Pack: ``fi``
 *
 * :Example:
 *     .. code-block::python
 *
 *         icons.FoundIconPack()
 *         icons.Icon('fi-home')
 */
var FoundIconPack = function (_) {
    return (react_1["default"].createElement(IconPack_1["default"], { name: "fi", url: "https://cdnjs.cloudflare.com/ajax/libs/foundicons/3.0.0/foundation-icons.min.css" }));
};
FoundIconPack.defaultProps = {};
exports.default = FoundIconPack;


/***/ }),

/***/ "./src/icons/ts/components/Icon.tsx":
/*!******************************************!*\
  !*** ./src/icons/ts/components/Icon.tsx ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var IconContext_1 = __importDefault(__webpack_require__(/*! ../IconContext */ "./src/icons/ts/IconContext.ts"));
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
/**
 * Icon from a pack, prefix the name with the pack name.
 *
 * .. code-block:: python
 *
 *     icon = Icon('fi-home')
 */
var Icon = function (props) {
    var name = props.name, class_name = props.class_name, style = props.style, identity = props.identity, icon_pack = props.icon_pack, rest = __rest(props, ["name", "class_name", "style", "identity", "icon_pack"]);
    var context = react_1.useContext(IconContext_1["default"]);
    var pack = react_1.useMemo(function () {
        if (icon_pack) {
            return icon_pack;
        }
        var split1 = name.split(' ');
        if (split1.length > 1) {
            return split1[0];
        }
        var split2 = name.split('-');
        if (split2.length > 1) {
            return split2[0];
        }
        return name;
    }, [icon_pack, name]);
    var css = react_1.useMemo(function () { return commons_1.getPresetsClassNames(rest, class_name, name, pack); }, [rest, class_name, name, pack]);
    var styling = react_1.useMemo(function () { return commons_1.getCommonStyles(rest, style); }, [rest, style]);
    if (!context.isLoaded(pack)) {
        return null;
    }
    return react_1["default"].createElement("i", { className: css, style: styling, id: identity });
};
Icon.defaultProps = {};
exports.default = Icon;


/***/ }),

/***/ "./src/icons/ts/components/IconLoader.tsx":
/*!************************************************!*\
  !*** ./src/icons/ts/components/IconLoader.tsx ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var IconContext_1 = __importDefault(__webpack_require__(/*! ../IconContext */ "./src/icons/ts/IconContext.ts"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var reducer = function (state, pack) {
    return ramda_1.assoc(pack.name, pack, state);
};
/**
 * Manager for loading icon packs
 *
 * Insert once in the layout, can load the packs from the props.
 * Manage the loaded packs so icons knows when to render.
 * ``IconPack``'s in the layout need this component.
 */
var IconLoader = function (props) {
    var packs = props.packs, children = props.children;
    var _a = react_1.useReducer(reducer, {}), loadedPacks = _a[0], dispatch = _a[1];
    var addPack = function (pack) {
        dispatch(pack);
    };
    var isLoaded = function (packName) { return !!loadedPacks[packName]; };
    react_1.useEffect(function () {
        packs.forEach(function (pack) { return commons_1.loadCss(pack.url).then(function () { return addPack(pack); }); });
    }, [packs]);
    return (react_1["default"].createElement(IconContext_1["default"].Provider, { value: { packs: loadedPacks, addPack: addPack, isLoaded: isLoaded } }, children));
};
IconLoader.defaultProps = {
    packs: [],
};
IconLoader.isContext = true;
exports.default = IconLoader;


/***/ }),

/***/ "./src/icons/ts/components/IconPack.tsx":
/*!**********************************************!*\
  !*** ./src/icons/ts/components/IconPack.tsx ***!
  \**********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var IconContext_1 = __importDefault(__webpack_require__(/*! ../IconContext */ "./src/icons/ts/IconContext.ts"));
/**
 * A pack of font icons to load.
 */
var IconPack = function (props) {
    var name = props.name, url = props.url;
    var context = react_1.useContext(IconContext_1["default"]);
    react_1.useEffect(function () {
        commons_1.loadCss(url).then(function () {
            context.addPack({ name: name, url: url });
        });
    }, []);
    return react_1["default"].createElement(react_1["default"].Fragment, null);
};
exports.default = IconPack;


/***/ }),

/***/ "./src/icons/ts/components/LinearIconPack.tsx":
/*!****************************************************!*\
  !*** ./src/icons/ts/components/LinearIconPack.tsx ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var IconPack_1 = __importDefault(__webpack_require__(/*! ./IconPack */ "./src/icons/ts/components/IconPack.tsx"));
/**
 * Free Icon pack from "https://linearicons.com/free"
 *
 * :Pack: ``lnr``
 *
 * :Example:
 *     .. code-block:: python
 *
 *         icons.LinearIconPack()
 *         icons.Icon('lnr-home')
 */
var LinearIconPack = function (_) {
    return (react_1["default"].createElement(IconPack_1["default"], { name: "lnr", url: "https://cdn.linearicons.com/free/1.0.0/icon-font.min.css" }));
};
LinearIconPack.defaultProps = {};
exports.default = LinearIconPack;


/***/ }),

/***/ "./src/icons/ts/components/OpenIconicPack.tsx":
/*!****************************************************!*\
  !*** ./src/icons/ts/components/OpenIconicPack.tsx ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var IconPack_1 = __importDefault(__webpack_require__(/*! ./IconPack */ "./src/icons/ts/components/IconPack.tsx"));
/**
 * Icon pack from https://useiconic.com/
 *
 * :Pack: ``oi``
 *
 * :Example:
 *     .. code-block:: python
 *
 *         icons.OpenIconicPack()
 *         icons.Icon('oi-bug')
 */
var OpenIconicPack = function (_) {
    return (react_1["default"].createElement(IconPack_1["default"], { name: "oi", url: "https://cdnjs.cloudflare.com/ajax/libs/open-iconic/1.1.1/font/css/open-iconic-bootstrap.min.css" }));
};
OpenIconicPack.defaultProps = {};
exports.default = OpenIconicPack;


/***/ }),

/***/ "./src/icons/ts/components/TypiconsPack.tsx":
/*!**************************************************!*\
  !*** ./src/icons/ts/components/TypiconsPack.tsx ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var IconPack_1 = __importDefault(__webpack_require__(/*! ./IconPack */ "./src/icons/ts/components/IconPack.tsx"));
/**
 * Free Icon pack from: https://www.s-ings.com/typicons/
 *
 * :Pack: ``typcn``
 *
 * :Example:
 *     .. code-block:: python
 *
 *         icons.TypiconsPack()
 *         icons.Icon('typcn-globe')
 */
var TypiconsPack = function (_) {
    return (react_1["default"].createElement(IconPack_1["default"], { name: "typcn", url: "https://cdnjs.cloudflare.com/ajax/libs/typicons/2.1.2/typicons.min.css" }));
};
TypiconsPack.defaultProps = {};
exports.default = TypiconsPack;


/***/ }),

/***/ "./src/icons/ts/index.ts":
/*!*******************************!*\
  !*** ./src/icons/ts/index.ts ***!
  \*******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.FlagIconPack = exports.TypiconsPack = exports.OpenIconicPack = exports.FoundIconPack = exports.LinearIconPack = exports.IconPack = exports.IconLoader = exports.Icon = void 0;
var Icon_1 = __importDefault(__webpack_require__(/*! ./components/Icon */ "./src/icons/ts/components/Icon.tsx"));
exports.Icon = Icon_1["default"];
var IconLoader_1 = __importDefault(__webpack_require__(/*! ./components/IconLoader */ "./src/icons/ts/components/IconLoader.tsx"));
exports.IconLoader = IconLoader_1["default"];
var IconPack_1 = __importDefault(__webpack_require__(/*! ./components/IconPack */ "./src/icons/ts/components/IconPack.tsx"));
exports.IconPack = IconPack_1["default"];
var LinearIconPack_1 = __importDefault(__webpack_require__(/*! ./components/LinearIconPack */ "./src/icons/ts/components/LinearIconPack.tsx"));
exports.LinearIconPack = LinearIconPack_1["default"];
var FoundIconPack_1 = __importDefault(__webpack_require__(/*! ./components/FoundIconPack */ "./src/icons/ts/components/FoundIconPack.tsx"));
exports.FoundIconPack = FoundIconPack_1["default"];
var OpenIconicPack_1 = __importDefault(__webpack_require__(/*! ./components/OpenIconicPack */ "./src/icons/ts/components/OpenIconicPack.tsx"));
exports.OpenIconicPack = OpenIconicPack_1["default"];
var TypiconsPack_1 = __importDefault(__webpack_require__(/*! ./components/TypiconsPack */ "./src/icons/ts/components/TypiconsPack.tsx"));
exports.TypiconsPack = TypiconsPack_1["default"];
var FlagIconPack_1 = __importDefault(__webpack_require__(/*! ./components/FlagIconPack */ "./src/icons/ts/components/FlagIconPack.tsx"));
exports.FlagIconPack = FlagIconPack_1["default"];


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ var __webpack_exports__ = (__webpack_exec__("./src/icons/ts/index.ts"));
/******/ return __webpack_exports__;
/******/ }
]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9pY29uc18wNmYyMDljMWM5Y2NjODQwMDdiZC5qcyIsIm1hcHBpbmdzIjoiO0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUNELE87Ozs7Ozs7Ozs7Ozs7QUNWQSx5RUFBMEI7QUFDMUIsa0JBQWUsa0JBQUssQ0FBQyxhQUFhLENBQWtCO0lBQ2hELEtBQUssRUFBRSxFQUFFO0lBQ1QsT0FBTyxFQUFFLGNBQU0sV0FBSSxFQUFKLENBQUk7SUFDbkIsUUFBUSxFQUFFLGNBQU0sWUFBSyxFQUFMLENBQUs7Q0FDeEIsQ0FBQyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7O0FDTEgseUVBQTBCO0FBQzFCLGtIQUFrQztBQUdsQzs7Ozs7Ozs7Ozs7R0FXRztBQUNILElBQU0sWUFBWSxHQUFHLFVBQUMsQ0FBZTtJQUNqQyxPQUFPLENBQ0gsaUNBQUMscUJBQVEsSUFDTCxJQUFJLEVBQUMsV0FBVyxFQUNoQixHQUFHLEVBQUMsbUZBQW1GLEdBQ3pGLENBQ0wsQ0FBQztBQUNOLENBQUMsQ0FBQztBQUVGLFlBQVksQ0FBQyxZQUFZLEdBQUcsRUFBRSxDQUFDO0FBRS9CLGtCQUFlLFlBQVksQ0FBQzs7Ozs7Ozs7Ozs7Ozs7OztBQzNCNUIseUVBQTBCO0FBQzFCLGtIQUFrQztBQUdsQzs7Ozs7Ozs7OztHQVVHO0FBQ0gsSUFBTSxhQUFhLEdBQUcsVUFBQyxDQUFlO0lBQ2xDLE9BQU8sQ0FDSCxpQ0FBQyxxQkFBUSxJQUNMLElBQUksRUFBQyxJQUFJLEVBQ1QsR0FBRyxFQUFDLGtGQUFrRixHQUN4RixDQUNMLENBQUM7QUFDTixDQUFDLENBQUM7QUFFRixhQUFhLENBQUMsWUFBWSxHQUFHLEVBQUUsQ0FBQztBQUVoQyxrQkFBZSxhQUFhLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUMxQjdCLHNFQUFpRDtBQUNqRCxnSEFBeUM7QUFNekMsZ0ZBQThEO0FBb0I5RDs7Ozs7O0dB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VXJELHlCQVZHLDJCQUFjLENBVUg7QUFUbEIseUlBQXFEO0FBVWpELHVCQVZHLHlCQUFZLENBVUg7QUFUaEIseUlBQXFEO0FBVWpELHVCQVZHLHlCQUFZLENBVUg7Ozs7Ozs7Ozs7O0FDakJoQiIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2ljb25zL3RzL0ljb25Db250ZXh0LnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2ljb25zL3RzL2NvbXBvbmVudHMvRmxhZ0ljb25QYWNrLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pY29ucy90cy9jb21wb25lbnRzL0ZvdW5kSWNvblBhY2sudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2ljb25zL3RzL2NvbXBvbmVudHMvSWNvbi50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvaWNvbnMvdHMvY29tcG9uZW50cy9JY29uTG9hZGVyLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pY29ucy90cy9jb21wb25lbnRzL0ljb25QYWNrLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pY29ucy90cy9jb21wb25lbnRzL0xpbmVhckljb25QYWNrLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pY29ucy90cy9jb21wb25lbnRzL09wZW5JY29uaWNQYWNrLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pY29ucy90cy9jb21wb25lbnRzL1R5cGljb25zUGFjay50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvaWNvbnMvdHMvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9pY29uc1wiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX2ljb25zXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkoc2VsZiwgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fKSB7XG5yZXR1cm4gIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmV4cG9ydCBkZWZhdWx0IFJlYWN0LmNyZWF0ZUNvbnRleHQ8SWNvbkNvbnRleHRUeXBlPih7XG4gICAgcGFja3M6IHt9LFxuICAgIGFkZFBhY2s6ICgpID0+IG51bGwsXG4gICAgaXNMb2FkZWQ6ICgpID0+IGZhbHNlLFxufSk7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEljb25QYWNrIGZyb20gJy4vSWNvblBhY2snO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuXG4vKipcbiAqIEZyZWUgaWNvbiBwYWNrIGZyb20gaHR0cHM6Ly9naXRodWIuY29tL2xpcGlzL2ZsYWctaWNvbnNcbiAqXG4gKiA6UGFjazpcbiAqICAgICBgYGZsYWctaWNvbmBgXG4gKlxuICogOkV4YW1wbGU6XG4gKiAgICAgIC4uIGNvZGUtYmxvY2s6OiBweXRob25cbiAqXG4gKiAgICAgICAgICBpY29ucy5GbGFnSWNvblBhY2soKVxuICogICAgICAgICAgaWNvbnMuSWNvbignZmxhZy1pY29uIGZsYWctaWNvbi1jYScpXG4gKi9cbmNvbnN0IEZsYWdJY29uUGFjayA9IChfOiBEYXp6bGVyUHJvcHMpID0+IHtcbiAgICByZXR1cm4gKFxuICAgICAgICA8SWNvblBhY2tcbiAgICAgICAgICAgIG5hbWU9XCJmbGFnLWljb25cIlxuICAgICAgICAgICAgdXJsPVwiaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvZmxhZy1pY29uLWNzcy80LjEuNS9jc3MvZmxhZy1pY29ucy5taW4uY3NzXCJcbiAgICAgICAgLz5cbiAgICApO1xufTtcblxuRmxhZ0ljb25QYWNrLmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5leHBvcnQgZGVmYXVsdCBGbGFnSWNvblBhY2s7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEljb25QYWNrIGZyb20gJy4vSWNvblBhY2snO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuXG4vKipcbiAqIEZyZWUgaWNvbiBwYWNrIGZyb20gaHR0cHM6Ly96dXJiLmNvbS9wbGF5Z3JvdW5kL2ZvdW5kYXRpb24taWNvbi1mb250cy0zXG4gKlxuICogOlBhY2s6IGBgZmlgYFxuICpcbiAqIDpFeGFtcGxlOlxuICogICAgIC4uIGNvZGUtYmxvY2s6OnB5dGhvblxuICpcbiAqICAgICAgICAgaWNvbnMuRm91bmRJY29uUGFjaygpXG4gKiAgICAgICAgIGljb25zLkljb24oJ2ZpLWhvbWUnKVxuICovXG5jb25zdCBGb3VuZEljb25QYWNrID0gKF86IERhenpsZXJQcm9wcykgPT4ge1xuICAgIHJldHVybiAoXG4gICAgICAgIDxJY29uUGFja1xuICAgICAgICAgICAgbmFtZT1cImZpXCJcbiAgICAgICAgICAgIHVybD1cImh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL2ZvdW5kaWNvbnMvMy4wLjAvZm91bmRhdGlvbi1pY29ucy5taW4uY3NzXCJcbiAgICAgICAgLz5cbiAgICApO1xufTtcblxuRm91bmRJY29uUGFjay5kZWZhdWx0UHJvcHMgPSB7fTtcblxuZXhwb3J0IGRlZmF1bHQgRm91bmRJY29uUGFjaztcbiIsImltcG9ydCBSZWFjdCwge3VzZUNvbnRleHQsIHVzZU1lbW99IGZyb20gJ3JlYWN0JztcbmltcG9ydCBJY29uQ29udGV4dCBmcm9tICcuLi9JY29uQ29udGV4dCc7XG5pbXBvcnQge1xuICAgIENvbW1vblByZXNldHNQcm9wcyxcbiAgICBDb21tb25TdHlsZVByb3BzLFxuICAgIERhenpsZXJQcm9wcyxcbn0gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5pbXBvcnQge2dldENvbW1vblN0eWxlcywgZ2V0UHJlc2V0c0NsYXNzTmFtZXN9IGZyb20gJ2NvbW1vbnMnO1xuXG50eXBlIFByb3BzID0ge1xuICAgIC8qKlxuICAgICAqIE5hbWUgb2YgdGhlIGljb24gdG8gcmVuZGVyLCBpdCB3aWxsIHRyeSB0byBzZXQgdGhlIGljb25fcGFjayBwcm9wIGZyb21cbiAgICAgKiB0aGUgbmFtZSBpZiBpdCdzIG5vdCBwcm92aWRlZC4gU3BsaXQgd2l0aCBgYC1gYCBvciBlbXB0eSBzcGFjZSwgdGhlXG4gICAgICogZmlyc3QgZm91bmQgd2lsbCBiZSB0aGUgaWNvbl9wYWNrLiBJRTogRm9yIEZvdW5kSWNvbiBgYGZpLVtpY29uLW5hbWVdYGAuXG4gICAgICovXG4gICAgbmFtZTogc3RyaW5nO1xuICAgIC8qKlxuICAgICAqIENvcnJlc3BvbmQgdG8gdGhlIGBgbmFtZWBgIHByb3BlciBvZiB0aGUgaWNvbl9wYWNrLCBtb3N0IGZvbnQgaWNvbnNcbiAgICAgKiBwYWNrYWdlcyByZXF1aXJlcyB0aGVpciBwYWNrIG5hbWUgdG8gYmUgaW5jbHVkZWQgaW4gdGhlIGNsYXNzX25hbWUsIGFzXG4gICAgICogc3VjaCwgdGhpcyBjb21wb25lbnQgd2lsbCBhZGQgaXQgYXV0b21hdGljYWxseSBmcm9tIGZvdW5kIG9yIHByb3ZpZGVkXG4gICAgICogaWNvbiBwYWNrIG5hbWUuXG4gICAgICovXG4gICAgaWNvbl9wYWNrPzogc3RyaW5nO1xufSAmIERhenpsZXJQcm9wcyAmXG4gICAgQ29tbW9uUHJlc2V0c1Byb3BzICZcbiAgICBDb21tb25TdHlsZVByb3BzO1xuXG4vKipcbiAqIEljb24gZnJvbSBhIHBhY2ssIHByZWZpeCB0aGUgbmFtZSB3aXRoIHRoZSBwYWNrIG5hbWUuXG4gKlxuICogLi4gY29kZS1ibG9jazo6IHB5dGhvblxuICpcbiAqICAgICBpY29uID0gSWNvbignZmktaG9tZScpXG4gKi9cbmNvbnN0IEljb24gPSAocHJvcHM6IFByb3BzKSA9PiB7XG4gICAgY29uc3Qge25hbWUsIGNsYXNzX25hbWUsIHN0eWxlLCBpZGVudGl0eSwgaWNvbl9wYWNrLCAuLi5yZXN0fSA9IHByb3BzO1xuICAgIGNvbnN0IGNvbnRleHQgPSB1c2VDb250ZXh0KEljb25Db250ZXh0KTtcblxuICAgIGNvbnN0IHBhY2sgPSB1c2VNZW1vKCgpID0+IHtcbiAgICAgICAgaWYgKGljb25fcGFjaykge1xuICAgICAgICAgICAgcmV0dXJuIGljb25fcGFjaztcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBzcGxpdDEgPSBuYW1lLnNwbGl0KCcgJyk7XG4gICAgICAgIGlmIChzcGxpdDEubGVuZ3RoID4gMSkge1xuICAgICAgICAgICAgcmV0dXJuIHNwbGl0MVswXTtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBzcGxpdDIgPSBuYW1lLnNwbGl0KCctJyk7XG4gICAgICAgIGlmIChzcGxpdDIubGVuZ3RoID4gMSkge1xuICAgICAgICAgICAgcmV0dXJuIHNwbGl0MlswXTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gbmFtZTtcbiAgICB9LCBbaWNvbl9wYWNrLCBuYW1lXSk7XG5cbiAgICBjb25zdCBjc3MgPSB1c2VNZW1vKFxuICAgICAgICAoKSA9PiBnZXRQcmVzZXRzQ2xhc3NOYW1lcyhyZXN0LCBjbGFzc19uYW1lLCBuYW1lLCBwYWNrKSxcbiAgICAgICAgW3Jlc3QsIGNsYXNzX25hbWUsIG5hbWUsIHBhY2tdXG4gICAgKTtcbiAgICBjb25zdCBzdHlsaW5nID0gdXNlTWVtbygoKSA9PiBnZXRDb21tb25TdHlsZXMocmVzdCwgc3R5bGUpLCBbcmVzdCwgc3R5bGVdKTtcblxuICAgIGlmICghY29udGV4dC5pc0xvYWRlZChwYWNrKSkge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICByZXR1cm4gPGkgY2xhc3NOYW1lPXtjc3N9IHN0eWxlPXtzdHlsaW5nfSBpZD17aWRlbnRpdHl9IC8+O1xufTtcblxuSWNvbi5kZWZhdWx0UHJvcHMgPSB7fTtcblxuZXhwb3J0IGRlZmF1bHQgSWNvbjtcbiIsImltcG9ydCBSZWFjdCwge3VzZUVmZmVjdCwgdXNlUmVkdWNlcn0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IEljb25Db250ZXh0IGZyb20gJy4uL0ljb25Db250ZXh0JztcbmltcG9ydCB7YXNzb2N9IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7bG9hZENzc30gZnJvbSAnY29tbW9ucyc7XG5pbXBvcnQge0RhenpsZXJQcm9wc30gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5cbmNvbnN0IHJlZHVjZXIgPSAoc3RhdGU6IEljb25QYWNrRGljdCwgcGFjazogSWNvblBhY2tUeXBlKSA9PlxuICAgIGFzc29jKHBhY2submFtZSwgcGFjaywgc3RhdGUpO1xuXG50eXBlIFByb3BzID0ge1xuICAgIC8qKlxuICAgICAqIFBhY2tzIHRvIGF1dG9tYXRpY2FsbHkgbG9hZCB3aGVuIHRoaXMgY29tcG9uZW50IG1vdW50cy5cbiAgICAgKi9cbiAgICBwYWNrcz86IHtcbiAgICAgICAgdXJsOiBzdHJpbmc7XG4gICAgICAgIG5hbWU6IHN0cmluZztcbiAgICB9W107XG4gICAgY2hpbGRyZW4/OiBKU1guRWxlbWVudDtcbn0gJiBEYXp6bGVyUHJvcHM7XG5cbi8qKlxuICogTWFuYWdlciBmb3IgbG9hZGluZyBpY29uIHBhY2tzXG4gKlxuICogSW5zZXJ0IG9uY2UgaW4gdGhlIGxheW91dCwgY2FuIGxvYWQgdGhlIHBhY2tzIGZyb20gdGhlIHByb3BzLlxuICogTWFuYWdlIHRoZSBsb2FkZWQgcGFja3Mgc28gaWNvbnMga25vd3Mgd2hlbiB0byByZW5kZXIuXG4gKiBgYEljb25QYWNrYGAncyBpbiB0aGUgbGF5b3V0IG5lZWQgdGhpcyBjb21wb25lbnQuXG4gKi9cbmNvbnN0IEljb25Mb2FkZXIgPSAocHJvcHM6IFByb3BzKSA9PiB7XG4gICAgY29uc3Qge3BhY2tzLCBjaGlsZHJlbn0gPSBwcm9wcztcbiAgICBjb25zdCBbbG9hZGVkUGFja3MsIGRpc3BhdGNoXSA9IHVzZVJlZHVjZXIocmVkdWNlciwge30pO1xuXG4gICAgY29uc3QgYWRkUGFjayA9IChwYWNrKSA9PiB7XG4gICAgICAgIGRpc3BhdGNoKHBhY2spO1xuICAgIH07XG5cbiAgICBjb25zdCBpc0xvYWRlZCA9IChwYWNrTmFtZTogc3RyaW5nKSA9PiAhIWxvYWRlZFBhY2tzW3BhY2tOYW1lXTtcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgIHBhY2tzLmZvckVhY2goKHBhY2spID0+IGxvYWRDc3MocGFjay51cmwpLnRoZW4oKCkgPT4gYWRkUGFjayhwYWNrKSkpO1xuICAgIH0sIFtwYWNrc10pO1xuXG4gICAgcmV0dXJuIChcbiAgICAgICAgPEljb25Db250ZXh0LlByb3ZpZGVyIHZhbHVlPXt7cGFja3M6IGxvYWRlZFBhY2tzLCBhZGRQYWNrLCBpc0xvYWRlZH19PlxuICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICA8L0ljb25Db250ZXh0LlByb3ZpZGVyPlxuICAgICk7XG59O1xuXG5JY29uTG9hZGVyLmRlZmF1bHRQcm9wcyA9IHtcbiAgICBwYWNrczogW10sXG59O1xuXG5JY29uTG9hZGVyLmlzQ29udGV4dCA9IHRydWU7XG5cbmV4cG9ydCBkZWZhdWx0IEljb25Mb2FkZXI7XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3QsIHVzZUNvbnRleHR9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7bG9hZENzc30gZnJvbSAnY29tbW9ucyc7XG5pbXBvcnQgSWNvbkNvbnRleHQgZnJvbSAnLi4vSWNvbkNvbnRleHQnO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuXG50eXBlIFByb3BzID0ge25hbWU6IHN0cmluZzsgdXJsOiBzdHJpbmd9ICYgRGF6emxlclByb3BzO1xuXG4vKipcbiAqIEEgcGFjayBvZiBmb250IGljb25zIHRvIGxvYWQuXG4gKi9cbmNvbnN0IEljb25QYWNrID0gKHByb3BzOiBQcm9wcykgPT4ge1xuICAgIGNvbnN0IHtuYW1lLCB1cmx9ID0gcHJvcHM7XG4gICAgY29uc3QgY29udGV4dCA9IHVzZUNvbnRleHQoSWNvbkNvbnRleHQpO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgbG9hZENzcyh1cmwpLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgY29udGV4dC5hZGRQYWNrKHtuYW1lLCB1cmx9KTtcbiAgICAgICAgfSk7XG4gICAgfSwgW10pO1xuXG4gICAgcmV0dXJuIDw+PC8+O1xufTtcblxuZXhwb3J0IGRlZmF1bHQgSWNvblBhY2s7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEljb25QYWNrIGZyb20gJy4vSWNvblBhY2snO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuXG4vKipcbiAqIEZyZWUgSWNvbiBwYWNrIGZyb20gXCJodHRwczovL2xpbmVhcmljb25zLmNvbS9mcmVlXCJcbiAqXG4gKiA6UGFjazogYGBsbnJgYFxuICpcbiAqIDpFeGFtcGxlOlxuICogICAgIC4uIGNvZGUtYmxvY2s6OiBweXRob25cbiAqXG4gKiAgICAgICAgIGljb25zLkxpbmVhckljb25QYWNrKClcbiAqICAgICAgICAgaWNvbnMuSWNvbignbG5yLWhvbWUnKVxuICovXG5jb25zdCBMaW5lYXJJY29uUGFjayA9IChfOiBEYXp6bGVyUHJvcHMpID0+IHtcbiAgICByZXR1cm4gKFxuICAgICAgICA8SWNvblBhY2tcbiAgICAgICAgICAgIG5hbWU9XCJsbnJcIlxuICAgICAgICAgICAgdXJsPVwiaHR0cHM6Ly9jZG4ubGluZWFyaWNvbnMuY29tL2ZyZWUvMS4wLjAvaWNvbi1mb250Lm1pbi5jc3NcIlxuICAgICAgICAvPlxuICAgICk7XG59O1xuXG5MaW5lYXJJY29uUGFjay5kZWZhdWx0UHJvcHMgPSB7fTtcblxuZXhwb3J0IGRlZmF1bHQgTGluZWFySWNvblBhY2s7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IEljb25QYWNrIGZyb20gJy4vSWNvblBhY2snO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuXG4vKipcbiAqIEljb24gcGFjayBmcm9tIGh0dHBzOi8vdXNlaWNvbmljLmNvbS9cbiAqXG4gKiA6UGFjazogYGBvaWBgXG4gKlxuICogOkV4YW1wbGU6XG4gKiAgICAgLi4gY29kZS1ibG9jazo6IHB5dGhvblxuICpcbiAqICAgICAgICAgaWNvbnMuT3Blbkljb25pY1BhY2soKVxuICogICAgICAgICBpY29ucy5JY29uKCdvaS1idWcnKVxuICovXG5jb25zdCBPcGVuSWNvbmljUGFjayA9IChfOiBEYXp6bGVyUHJvcHMpID0+IHtcbiAgICByZXR1cm4gKFxuICAgICAgICA8SWNvblBhY2tcbiAgICAgICAgICAgIG5hbWU9XCJvaVwiXG4gICAgICAgICAgICB1cmw9XCJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9vcGVuLWljb25pYy8xLjEuMS9mb250L2Nzcy9vcGVuLWljb25pYy1ib290c3RyYXAubWluLmNzc1wiXG4gICAgICAgIC8+XG4gICAgKTtcbn07XG5cbk9wZW5JY29uaWNQYWNrLmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5leHBvcnQgZGVmYXVsdCBPcGVuSWNvbmljUGFjaztcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgSWNvblBhY2sgZnJvbSAnLi9JY29uUGFjayc7XG5pbXBvcnQge0RhenpsZXJQcm9wc30gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5cbi8qKlxuICogRnJlZSBJY29uIHBhY2sgZnJvbTogaHR0cHM6Ly93d3cucy1pbmdzLmNvbS90eXBpY29ucy9cbiAqXG4gKiA6UGFjazogYGB0eXBjbmBgXG4gKlxuICogOkV4YW1wbGU6XG4gKiAgICAgLi4gY29kZS1ibG9jazo6IHB5dGhvblxuICpcbiAqICAgICAgICAgaWNvbnMuVHlwaWNvbnNQYWNrKClcbiAqICAgICAgICAgaWNvbnMuSWNvbigndHlwY24tZ2xvYmUnKVxuICovXG5jb25zdCBUeXBpY29uc1BhY2sgPSAoXzogRGF6emxlclByb3BzKSA9PiB7XG4gICAgcmV0dXJuIChcbiAgICAgICAgPEljb25QYWNrXG4gICAgICAgICAgICBuYW1lPVwidHlwY25cIlxuICAgICAgICAgICAgdXJsPVwiaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvdHlwaWNvbnMvMi4xLjIvdHlwaWNvbnMubWluLmNzc1wiXG4gICAgICAgIC8+XG4gICAgKTtcbn07XG5cblR5cGljb25zUGFjay5kZWZhdWx0UHJvcHMgPSB7fTtcblxuZXhwb3J0IGRlZmF1bHQgVHlwaWNvbnNQYWNrO1xuIiwiaW1wb3J0IEljb24gZnJvbSAnLi9jb21wb25lbnRzL0ljb24nO1xuaW1wb3J0IEljb25Mb2FkZXIgZnJvbSAnLi9jb21wb25lbnRzL0ljb25Mb2FkZXInO1xuaW1wb3J0IEljb25QYWNrIGZyb20gJy4vY29tcG9uZW50cy9JY29uUGFjayc7XG5pbXBvcnQgTGluZWFySWNvblBhY2sgZnJvbSAnLi9jb21wb25lbnRzL0xpbmVhckljb25QYWNrJztcbmltcG9ydCBGb3VuZEljb25QYWNrIGZyb20gJy4vY29tcG9uZW50cy9Gb3VuZEljb25QYWNrJztcbmltcG9ydCBPcGVuSWNvbmljUGFjayBmcm9tICcuL2NvbXBvbmVudHMvT3Blbkljb25pY1BhY2snO1xuaW1wb3J0IFR5cGljb25zUGFjayBmcm9tICcuL2NvbXBvbmVudHMvVHlwaWNvbnNQYWNrJztcbmltcG9ydCBGbGFnSWNvblBhY2sgZnJvbSAnLi9jb21wb25lbnRzL0ZsYWdJY29uUGFjayc7XG5cbmV4cG9ydCB7XG4gICAgSWNvbixcbiAgICBJY29uTG9hZGVyLFxuICAgIEljb25QYWNrLFxuICAgIExpbmVhckljb25QYWNrLFxuICAgIEZvdW5kSWNvblBhY2ssXG4gICAgT3Blbkljb25pY1BhY2ssXG4gICAgVHlwaWNvbnNQYWNrLFxuICAgIEZsYWdJY29uUGFjayxcbn07XG4iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=