"use strict";
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
return (self["webpackChunkdazzler_name_"] = self["webpackChunkdazzler_name_"] || []).push([["renderer"],{

/***/ "./src/renderer/js/aspects.ts":
/*!************************************!*\
  !*** ./src/renderer/js/aspects.ts ***!
  \************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.isSameAspect = exports.getAspectKey = exports.coerceAspect = exports.isAspect = void 0;
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var isAspect = function (obj) {
    return ramda_1.is(Object, obj) && ramda_1.has('identity', obj) && ramda_1.has('aspect', obj);
};
exports.isAspect = isAspect;
var coerceAspect = function (obj, getAspect) { return (exports.isAspect(obj) ? getAspect(obj.identity, obj.aspect) : obj); };
exports.coerceAspect = coerceAspect;
var getAspectKey = function (identity, aspect) {
    return aspect + "@" + identity;
};
exports.getAspectKey = getAspectKey;
var isSameAspect = function (a, b) {
    return a.identity === b.identity && a.aspect === b.aspect;
};
exports.isSameAspect = isSameAspect;


/***/ }),

/***/ "./src/renderer/js/components/Renderer.tsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.tsx ***!
  \*************************************************/
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
var Updater_1 = __importDefault(__webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.tsx"));
var Renderer = function (props) {
    var _a = react_1.useState(1), reloadKey = _a[0], setReloadKey = _a[1];
    // FIXME find where this is used and refactor/remove
    // @ts-ignore
    window.dazzler_base_url = props.baseUrl;
    return (react_1["default"].createElement("div", { className: "dazzler-renderer" },
        react_1["default"].createElement(Updater_1["default"], __assign({}, props, { key: "upd-" + reloadKey, hotReload: function () { return setReloadKey(reloadKey + 1); } }))));
};
exports.default = Renderer;


/***/ }),

/***/ "./src/renderer/js/components/Updater.tsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.tsx ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var requests_1 = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.ts");
var hydrator_1 = __webpack_require__(/*! ../hydrator */ "./src/renderer/js/hydrator.tsx");
var requirements_1 = __webpack_require__(/*! ../requirements */ "./src/renderer/js/requirements.ts");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var transforms_1 = __webpack_require__(/*! ../transforms */ "./src/renderer/js/transforms.ts");
var aspects_1 = __webpack_require__(/*! ../aspects */ "./src/renderer/js/aspects.ts");
var Updater = /** @class */ (function (_super) {
    __extends(Updater, _super);
    function Updater(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            layout: null,
            ready: false,
            page: null,
            bindings: {},
            packages: {},
            reload: false,
            rebindings: [],
            requirements: [],
            reloading: false,
            needRefresh: false,
            ties: [],
        };
        // The api url for the page is the same but a post.
        // Fetch bindings, packages & requirements
        _this.pageApi = requests_1.apiRequest(window.location.href);
        // All components get connected.
        _this.boundComponents = {};
        _this.ws = null;
        _this.updateAspects = _this.updateAspects.bind(_this);
        _this.connect = _this.connect.bind(_this);
        _this.disconnect = _this.disconnect.bind(_this);
        _this.onMessage = _this.onMessage.bind(_this);
        return _this;
    }
    Updater.prototype.updateAspects = function (identity, aspects, initial) {
        var _this = this;
        if (initial === void 0) { initial = false; }
        return new Promise(function (resolve) {
            var aspectKeys = ramda_1.keys(aspects);
            var bindings = aspectKeys
                .map(function (key) { return (__assign(__assign({}, _this.state.bindings[aspects_1.getAspectKey(identity, key)]), { value: aspects[key] })); })
                .filter(function (e) { return e.trigger && !(e.trigger.skip_initial && initial); });
            _this.state.rebindings.forEach(function (binding) {
                if (binding.trigger.identity.test(identity) &&
                    !(binding.trigger.skip_initial && initial)) {
                    // @ts-ignore
                    bindings = ramda_1.concat(bindings, aspectKeys
                        .filter(function (k) {
                        return binding.trigger.aspect.test(k);
                    })
                        .map(function (k) { return (__assign(__assign({}, binding), { value: aspects[k], trigger: __assign(__assign({}, binding.trigger), { identity: identity, aspect: k }) })); }));
                }
            });
            var removableTies = [];
            ramda_1.flatten(aspectKeys.map(function (aspect) {
                var ties = [];
                for (var i = 0; i < _this.state.ties.length; i++) {
                    var tie = _this.state.ties[i];
                    var trigger = tie.trigger;
                    if (!(trigger.skip_initial && initial) &&
                        ((trigger.regex &&
                            // @ts-ignore
                            trigger.identity.test(identity) &&
                            // @ts-ignore
                            trigger.aspect.test(aspect)) ||
                            aspects_1.isSameAspect(trigger, { identity: identity, aspect: aspect }))) {
                        ties.push(__assign(__assign({}, tie), { value: aspects[aspect] }));
                    }
                }
                return ties;
            })).forEach(function (tie) {
                var transforms = tie.transforms;
                var value = tie.value;
                if (tie.trigger.once) {
                    removableTies.push(tie);
                }
                if (transforms) {
                    value = transforms.reduce(function (acc, e) {
                        return transforms_1.executeTransform(e.transform, acc, e.args, e.next, _this.getAspect.bind(_this));
                    }, value);
                }
                tie.targets.forEach(function (t) {
                    var _a;
                    var component = _this.boundComponents[t.identity];
                    if (component) {
                        component.updateAspects((_a = {}, _a[t.aspect] = value, _a));
                    }
                });
                if (tie.regexTargets.length) {
                    // FIXME probably a more efficient way to do this
                    //  refactor later.
                    ramda_1.values(_this.boundComponents).forEach(function (c) {
                        tie.regexTargets.forEach(function (t) {
                            var _a;
                            if (t.identity.test(c.identity)) {
                                c.updateAspects((_a = {}, _a[t.aspect] = value, _a));
                            }
                        });
                    });
                }
            });
            if (removableTies.length) {
                _this.setState({
                    ties: _this.state.ties.filter(function (t) {
                        return !removableTies.reduce(function (acc, tie) {
                            return acc ||
                                (aspects_1.isSameAspect(t.trigger, tie.trigger) &&
                                    ramda_1.all(function (_a) {
                                        var t1 = _a[0], t2 = _a[1];
                                        return aspects_1.isSameAspect(t1, t2);
                                    })(ramda_1.zip(t.targets, tie.targets)));
                        }, false);
                    }),
                });
            }
            if (!bindings) {
                resolve(0);
            }
            else {
                var removableBindings_1 = [];
                bindings.forEach(function (binding) {
                    _this.sendBinding(binding, binding.value, binding.call);
                    if (binding.trigger.once) {
                        removableBindings_1.push(binding);
                    }
                });
                if (removableBindings_1.length) {
                    _this.setState({
                        bindings: removableBindings_1.reduce(function (acc, binding) {
                            return ramda_1.dissoc(aspects_1.getAspectKey(binding.trigger.identity, binding.trigger.aspect), acc);
                        }, _this.state.bindings),
                    });
                }
                // Promise is for wrapper ready
                // TODO investigate reasons/uses of length resolve?
                resolve(bindings.length);
            }
        });
    };
    Updater.prototype.getAspect = function (identity, aspect) {
        var c = this.boundComponents[identity];
        if (c) {
            return c.getAspect(aspect);
        }
        return undefined;
    };
    Updater.prototype.connect = function (identity, setAspects, getAspect, matchAspects, updateAspects) {
        this.boundComponents[identity] = {
            identity: identity,
            setAspects: setAspects,
            getAspect: getAspect,
            matchAspects: matchAspects,
            updateAspects: updateAspects,
        };
    };
    Updater.prototype.disconnect = function (identity) {
        delete this.boundComponents[identity];
    };
    Updater.prototype.onMessage = function (response) {
        var _this = this;
        var data = JSON.parse(response.data);
        var identity = data.identity, kind = data.kind, payload = data.payload, storage = data.storage, request_id = data.request_id;
        var store;
        if (storage === 'session') {
            store = window.sessionStorage;
        }
        else {
            store = window.localStorage;
        }
        switch (kind) {
            case 'set-aspect':
                var setAspects = function (component) {
                    return component
                        .setAspects(hydrator_1.hydrateProps(payload, _this.updateAspects, _this.connect, _this.disconnect))
                        .then(function () { return _this.updateAspects(identity, payload); });
                };
                if (data.regex) {
                    var pattern_1 = new RegExp(data.identity);
                    ramda_1.keys(this.boundComponents)
                        .filter(function (k) { return pattern_1.test(k); })
                        .map(function (k) { return _this.boundComponents[k]; })
                        .forEach(setAspects);
                }
                else {
                    setAspects(this.boundComponents[identity]);
                }
                break;
            case 'get-aspect':
                var aspect = data.aspect;
                var wanted = this.boundComponents[identity];
                if (!wanted) {
                    this.ws.send(JSON.stringify({
                        kind: kind,
                        identity: identity,
                        aspect: aspect,
                        request_id: request_id,
                        error: "Aspect not found " + identity + "." + aspect,
                    }));
                    return;
                }
                var value = wanted.getAspect(aspect);
                this.ws.send(JSON.stringify({
                    kind: kind,
                    identity: identity,
                    aspect: aspect,
                    value: hydrator_1.prepareProp(value),
                    request_id: request_id,
                }));
                break;
            case 'set-storage':
                store.setItem(identity, JSON.stringify(payload));
                break;
            case 'get-storage':
                this.ws.send(JSON.stringify({
                    kind: kind,
                    identity: identity,
                    request_id: request_id,
                    value: JSON.parse(store.getItem(identity)),
                }));
                break;
            case 'reload':
                var filenames = data.filenames, hot = data.hot, refresh = data.refresh, deleted = data.deleted;
                if (refresh) {
                    this.ws.close();
                    this.setState({ reloading: true, needRefresh: true });
                    return;
                }
                if (hot) {
                    // The ws connection will close, when it
                    // reconnect it will do a hard reload of the page api.
                    this.setState({ reloading: true });
                    return;
                }
                filenames.forEach(requirements_1.loadRequirement);
                deleted.forEach(function (r) { return commons_1.disableCss(r.url); });
                break;
            case 'ping':
                // Just do nothing.
                break;
        }
    };
    Updater.prototype.sendBinding = function (binding, value, call) {
        var _this = this;
        if (call === void 0) { call = false; }
        // Collect all values and send a binding payload
        var trigger = __assign(__assign({}, binding.trigger), { value: hydrator_1.prepareProp(value) });
        var states = binding.states.reduce(function (acc, state) {
            if (state.regex) {
                var identityPattern_1 = new RegExp(state.identity);
                var aspectPattern_1 = new RegExp(state.aspect);
                return ramda_1.concat(acc, ramda_1.flatten(ramda_1.keys(_this.boundComponents).map(function (k) {
                    var values = [];
                    if (identityPattern_1.test(k)) {
                        values = _this.boundComponents[k]
                            .matchAspects(aspectPattern_1)
                            .map(function (_a) {
                            var name = _a[0], val = _a[1];
                            return (__assign(__assign({}, state), { identity: k, aspect: name, value: hydrator_1.prepareProp(val) }));
                        });
                    }
                    return values;
                })));
            }
            acc.push(__assign(__assign({}, state), { value: _this.boundComponents[state.identity] &&
                    hydrator_1.prepareProp(_this.boundComponents[state.identity].getAspect(state.aspect)) }));
            return acc;
        }, []);
        var payload = {
            trigger: trigger,
            states: states,
            kind: 'binding',
            page: this.state.page,
            key: binding.key,
        };
        if (call) {
            this.callBinding(payload);
        }
        else {
            this.ws.send(JSON.stringify(payload));
        }
    };
    Updater.prototype.callBinding = function (payload) {
        var _this = this;
        this.pageApi('', {
            method: 'PATCH',
            payload: payload,
            json: true,
        }).then(function (response) {
            ramda_1.toPairs(response.output).forEach(function (_a) {
                var identity = _a[0], aspects = _a[1];
                var component = _this.boundComponents[identity];
                if (component) {
                    component.updateAspects(hydrator_1.hydrateProps(aspects, _this.updateAspects, _this.connect, _this.disconnect));
                }
            });
        });
    };
    Updater.prototype._connectWS = function () {
        var _this = this;
        // Setup websocket for updates
        var tries = 0;
        var hardClose = false;
        var connexion = function () {
            var url = "ws" + (window.location.href.startsWith('https') ? 's' : '') + "://" + ((_this.props.baseUrl && _this.props.baseUrl) ||
                window.location.host) + "/" + _this.state.page + "/ws";
            _this.ws = new WebSocket(url);
            _this.ws.addEventListener('message', _this.onMessage);
            _this.ws.onopen = function () {
                if (_this.state.reloading) {
                    hardClose = true;
                    _this.ws.close();
                    if (_this.state.needRefresh) {
                        window.location.reload();
                    }
                    else {
                        _this.props.hotReload();
                    }
                }
                else {
                    _this.setState({ ready: true });
                    tries = 0;
                }
            };
            _this.ws.onclose = function () {
                var reconnect = function () {
                    tries++;
                    connexion();
                };
                if (!hardClose && tries < _this.props.retries) {
                    setTimeout(reconnect, 1000);
                }
            };
        };
        connexion();
    };
    Updater.prototype.componentDidMount = function () {
        var _this = this;
        this.pageApi('', { method: 'POST' }).then(function (response) {
            var toRegex = function (x) { return new RegExp(x); };
            _this.setState({
                page: response.page,
                layout: response.layout,
                bindings: ramda_1.pickBy(function (b) { return !b.regex; }, response.bindings),
                // Regex bindings triggers
                rebindings: ramda_1.map(function (x) {
                    var binding = response.bindings[x];
                    binding.trigger = ramda_1.evolve({
                        identity: toRegex,
                        aspect: toRegex,
                    }, binding.trigger);
                    return binding;
                }, ramda_1.keys(ramda_1.pickBy(function (b) { return b.regex; }, response.bindings))),
                packages: response.packages,
                requirements: response.requirements,
                // @ts-ignore
                ties: ramda_1.map(function (tie) {
                    var newTie = ramda_1.pipe(ramda_1.assoc('targets', tie.targets.filter(ramda_1.propSatisfies(ramda_1.not, 'regex'))), ramda_1.assoc('regexTargets', 
                    // @ts-ignore
                    tie.targets.filter(ramda_1.propEq('regex', true)).map(ramda_1.evolve({
                        // Only match identity for targets.
                        identity: toRegex,
                    }))))(tie);
                    if (tie.trigger.regex) {
                        return ramda_1.evolve({
                            trigger: {
                                identity: toRegex,
                                aspect: toRegex,
                            },
                        }, newTie);
                    }
                    return newTie;
                }, response.ties),
            }, function () {
                return requirements_1.loadRequirements(response.requirements, response.packages).then(function () {
                    if (response.reload ||
                        ramda_1.values(response.bindings).filter(function (binding) { return !binding.call; }).length) {
                        _this._connectWS();
                    }
                    else {
                        _this.setState({ ready: true });
                    }
                });
            });
        });
    };
    Updater.prototype.render = function () {
        var _a = this.state, layout = _a.layout, ready = _a.ready, reloading = _a.reloading;
        if (!ready) {
            return (react_1["default"].createElement("div", { className: "dazzler-loading-container" },
                react_1["default"].createElement("div", { className: "dazzler-spin" }),
                react_1["default"].createElement("div", { className: "dazzler-loading" }, "Loading...")));
        }
        if (reloading) {
            return (react_1["default"].createElement("div", { className: "dazzler-loading-container" },
                react_1["default"].createElement("div", { className: "dazzler-spin reload" }),
                react_1["default"].createElement("div", { className: "dazzler-loading" }, "Reloading...")));
        }
        if (!hydrator_1.isComponent(layout)) {
            throw new Error("Layout is not a component: " + layout);
        }
        var contexts = [];
        var onContext = function (contextComponent) {
            contexts.push(contextComponent);
        };
        var hydrated = hydrator_1.hydrateComponent(layout.name, layout.package, layout.identity, hydrator_1.hydrateProps(layout.aspects, this.updateAspects, this.connect, this.disconnect, onContext), this.updateAspects, this.connect, this.disconnect, onContext);
        return (react_1["default"].createElement("div", { className: "dazzler-rendered" }, contexts.length
            ? contexts.reduce(function (acc, Context) {
                if (!acc) {
                    return react_1["default"].createElement(Context, null, hydrated);
                }
                return react_1["default"].createElement(Context, null, acc);
            }, null)
            : hydrated));
    };
    return Updater;
}(react_1["default"].Component));
exports.default = Updater;


/***/ }),

/***/ "./src/renderer/js/components/Wrapper.tsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.tsx ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
/**
 * Wraps components for aspects updating.
 */
var Wrapper = /** @class */ (function (_super) {
    __extends(Wrapper, _super);
    function Wrapper(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            aspects: props.aspects || {},
            ready: false,
            initial: false,
            error: null,
        };
        _this.setAspects = _this.setAspects.bind(_this);
        _this.getAspect = _this.getAspect.bind(_this);
        _this.updateAspects = _this.updateAspects.bind(_this);
        _this.matchAspects = _this.matchAspects.bind(_this);
        return _this;
    }
    Wrapper.getDerivedStateFromError = function (error) {
        return { error: error };
    };
    Wrapper.prototype.updateAspects = function (aspects) {
        var _this = this;
        return this.setAspects(aspects).then(function () {
            return _this.props.updateAspects(_this.props.identity, aspects);
        });
    };
    Wrapper.prototype.setAspects = function (aspects) {
        var _this = this;
        return new Promise(function (resolve) {
            _this.setState({ aspects: __assign(__assign({}, _this.state.aspects), aspects) }, resolve);
        });
    };
    Wrapper.prototype.getAspect = function (aspect) {
        return this.state.aspects[aspect];
    };
    Wrapper.prototype.matchAspects = function (pattern) {
        var _this = this;
        return ramda_1.keys(this.state.aspects)
            .filter(function (k) { return pattern.test(k); })
            .map(function (k) { return [k, _this.state.aspects[k]]; });
    };
    Wrapper.prototype.componentDidMount = function () {
        var _this = this;
        // Only update the component when mounted.
        // Otherwise gets a race condition with willUnmount
        this.props.connect(this.props.identity, this.setAspects, this.getAspect, this.matchAspects, this.updateAspects);
        if (!this.state.initial) {
            // Need to set aspects first, not sure why but it
            // sets them for the initial states and ties.
            this.setAspects(this.state.aspects).then(function () {
                return _this.props
                    .updateAspects(_this.props.identity, _this.state.aspects, true)
                    .then(function () {
                    _this.setState({ ready: true, initial: true });
                });
            });
        }
    };
    Wrapper.prototype.componentWillUnmount = function () {
        this.props.disconnect(this.props.identity);
    };
    Wrapper.prototype.render = function () {
        var _a = this.props, component = _a.component, component_name = _a.component_name, package_name = _a.package_name, identity = _a.identity;
        var _b = this.state, aspects = _b.aspects, ready = _b.ready, error = _b.error;
        if (!ready) {
            return null;
        }
        if (error) {
            return (react_1["default"].createElement("div", { style: { color: 'red' } },
                "\u26A0 Error with ",
                package_name,
                ".",
                component_name,
                " #",
                identity));
        }
        return react_1["default"].cloneElement(component, __assign(__assign({}, aspects), { updateAspects: this.updateAspects, identity: identity, class_name: ramda_1.join(' ', ramda_1.concat([
                package_name
                    .replace('_', '-')
                    .toLowerCase() + "-" + commons_1.camelToSpinal(component_name),
            ], aspects.class_name ? aspects.class_name.split(' ') : [])) }));
    };
    return Wrapper;
}(react_1["default"].Component));
exports.default = Wrapper;


/***/ }),

/***/ "./src/renderer/js/hydrator.tsx":
/*!**************************************!*\
  !*** ./src/renderer/js/hydrator.tsx ***!
  \**************************************/
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.prepareProp = exports.hydrateComponent = exports.hydrateProps = exports.isComponent = void 0;
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var Wrapper_1 = __importDefault(__webpack_require__(/*! ./components/Wrapper */ "./src/renderer/js/components/Wrapper.tsx"));
function isComponent(c) {
    return (ramda_1.type(c) === 'Object' &&
        c.hasOwnProperty('package') &&
        c.hasOwnProperty('aspects') &&
        c.hasOwnProperty('name') &&
        c.hasOwnProperty('identity'));
}
exports.isComponent = isComponent;
function hydrateProp(value, updateAspects, connect, disconnect, onContext) {
    if (ramda_1.type(value) === 'Array') {
        return value.map(function (e) {
            if (isComponent(e)) {
                if (!e.aspects.key) {
                    e.aspects.key = e.identity;
                }
            }
            return hydrateProp(e, updateAspects, connect, disconnect, onContext);
        });
    }
    else if (isComponent(value)) {
        var newProps = hydrateProps(value.aspects, updateAspects, connect, disconnect, onContext);
        return hydrateComponent(value.name, value.package, value.identity, newProps, updateAspects, connect, disconnect, onContext);
    }
    else if (ramda_1.type(value) === 'Object') {
        return hydrateProps(value, updateAspects, connect, disconnect, onContext);
    }
    return value;
}
function hydrateProps(props, updateAspects, connect, disconnect, onContext) {
    return ramda_1.toPairs(props).reduce(function (acc, _a) {
        var aspect = _a[0], value = _a[1];
        acc[aspect] = hydrateProp(value, updateAspects, connect, disconnect, onContext);
        return acc;
    }, {});
}
exports.hydrateProps = hydrateProps;
function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect, onContext) {
    var pack = window[package_name];
    if (!pack) {
        throw new Error("Invalid package name: " + package_name);
    }
    var component = pack[name];
    if (!component) {
        throw new Error("Invalid component name: " + package_name + "." + name);
    }
    // @ts-ignore
    var element = react_1["default"].createElement(component, props);
    /* eslint-disable react/prop-types */
    var wrapper = function (_a) {
        var children = _a.children;
        return (react_1["default"].createElement(Wrapper_1["default"], { identity: identity, updateAspects: updateAspects, component: element, connect: connect, package_name: package_name, component_name: name, aspects: __assign({ children: children }, props), disconnect: disconnect, key: "wrapper-" + identity }));
    };
    if (component.isContext) {
        onContext(wrapper);
        return null;
    }
    return wrapper({});
}
exports.hydrateComponent = hydrateComponent;
function prepareProp(prop) {
    if (react_1["default"].isValidElement(prop)) {
        // @ts-ignore
        var props = prop.props;
        return {
            identity: props.identity,
            // @ts-ignore
            aspects: ramda_1.map(prepareProp, ramda_1.omit([
                'identity',
                'updateAspects',
                '_name',
                '_package',
                'aspects',
                'key',
            ], props.aspects)),
            name: props.component_name,
            package: props.package_name,
        };
    }
    if (ramda_1.type(prop) === 'Array') {
        return prop.map(prepareProp);
    }
    if (ramda_1.type(prop) === 'Object') {
        return ramda_1.map(prepareProp, prop);
    }
    return prop;
}
exports.prepareProp = prepareProp;


/***/ }),

/***/ "./src/renderer/js/index.tsx":
/*!***********************************!*\
  !*** ./src/renderer/js/index.tsx ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.render = exports.Renderer = void 0;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "react-dom"));
var Renderer_1 = __importDefault(__webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.tsx"));
exports.Renderer = Renderer_1["default"];
function render(_a, element) {
    var baseUrl = _a.baseUrl, ping = _a.ping, ping_interval = _a.ping_interval, retries = _a.retries;
    react_dom_1["default"].render(react_1["default"].createElement(Renderer_1["default"], { baseUrl: baseUrl, ping: ping, ping_interval: ping_interval, retries: retries }), element);
}
exports.render = render;


/***/ }),

/***/ "./src/renderer/js/requests.ts":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.ts ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports) {


/* eslint-disable no-magic-numbers */
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
exports.apiRequest = exports.xhrRequest = exports.JSONHEADERS = void 0;
var jsonPattern = /json/i;
var defaultXhrOptions = {
    method: 'GET',
    headers: {},
    payload: '',
    json: true,
};
exports.JSONHEADERS = {
    'Content-Type': 'application/json',
};
function xhrRequest(url, options) {
    if (options === void 0) { options = defaultXhrOptions; }
    return new Promise(function (resolve, reject) {
        var _a = __assign(__assign({}, defaultXhrOptions), options), method = _a.method, headers = _a.headers, payload = _a.payload, json = _a.json;
        var xhr = new XMLHttpRequest();
        xhr.open(method, url);
        var head = json ? __assign(__assign({}, exports.JSONHEADERS), headers) : headers;
        Object.keys(head).forEach(function (k) { return xhr.setRequestHeader(k, head[k]); });
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var responseValue = xhr.response;
                    if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
                        responseValue = JSON.parse(xhr.responseText);
                    }
                    resolve(responseValue);
                }
                else {
                    reject({
                        error: 'RequestError',
                        message: "XHR " + url + " FAILED - STATUS: " + xhr.status + " MESSAGE: " + xhr.statusText,
                        status: xhr.status,
                        xhr: xhr,
                    });
                }
            }
        };
        xhr.onerror = function (err) { return reject(err); };
        // @ts-ignore
        xhr.send(json ? JSON.stringify(payload) : payload);
    });
}
exports.xhrRequest = xhrRequest;
function apiRequest(baseUrl) {
    return function (uri, options) {
        if (options === void 0) { options = undefined; }
        var url = baseUrl + uri;
        options.headers = __assign({}, options.headers);
        return xhrRequest(url, options);
    };
}
exports.apiRequest = apiRequest;


/***/ }),

/***/ "./src/renderer/js/requirements.ts":
/*!*****************************************!*\
  !*** ./src/renderer/js/requirements.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.loadRequirements = exports.loadRequirement = void 0;
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function loadRequirement(requirement) {
    return new Promise(function (resolve, reject) {
        var url = requirement.url, kind = requirement.kind;
        var method;
        if (kind === 'js') {
            method = commons_1.loadScript;
        }
        else if (kind === 'css') {
            method = commons_1.loadCss;
        }
        else if (kind === 'map') {
            return resolve();
        }
        else {
            return reject("Invalid requirement kind: " + kind);
        }
        return method(url).then(resolve)["catch"](reject);
    });
}
exports.loadRequirement = loadRequirement;
function loadOneByOne(requirements) {
    return new Promise(function (resolve) {
        var handle = function (reqs) {
            if (reqs.length) {
                var requirement = reqs[0];
                loadRequirement(requirement).then(function () { return handle(ramda_1.drop(1, reqs)); });
            }
            else {
                resolve(null);
            }
        };
        handle(requirements);
    });
}
function loadRequirements(requirements, packages) {
    return new Promise(function (resolve, reject) {
        var loadings = [];
        Object.keys(packages).forEach(function (pack_name) {
            var pack = packages[pack_name];
            loadings = loadings.concat(loadOneByOne(pack.requirements.filter(function (r) { return r.kind === 'js'; })));
            loadings = loadings.concat(pack.requirements
                .filter(function (r) { return r.kind === 'css'; })
                .map(loadRequirement));
        });
        // Then load requirements so they can use packages
        // and override css.
        Promise.all(loadings)
            .then(function () {
            var i = 0;
            // Load in order.
            var handler = function () {
                if (i < requirements.length) {
                    loadRequirement(requirements[i]).then(function () {
                        i++;
                        handler();
                    });
                }
                else {
                    resolve();
                }
            };
            handler();
        })["catch"](reject);
    });
}
exports.loadRequirements = loadRequirements;


/***/ }),

/***/ "./src/renderer/js/transforms.ts":
/*!***************************************!*\
  !*** ./src/renderer/js/transforms.ts ***!
  \***************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.executeTransform = void 0;
/* eslint-disable no-use-before-define */
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var aspects_1 = __webpack_require__(/*! ./aspects */ "./src/renderer/js/aspects.ts");
var transforms = {
    /* String transforms */
    ToUpper: function (value) {
        return value.toUpperCase();
    },
    ToLower: function (value) {
        return value.toLowerCase();
    },
    Format: function (value, args) {
        var template = args.template;
        if (ramda_1.is(String, value) || ramda_1.is(Number, value) || ramda_1.is(Boolean, value)) {
            return ramda_1.replace('${value}', value, template);
        }
        else if (ramda_1.is(Object, value)) {
            return ramda_1.reduce(function (acc, _a) {
                var k = _a[0], v = _a[1];
                return ramda_1.replace("${" + k + "}", v, acc);
            }, template, ramda_1.toPairs(value));
        }
        return value;
    },
    Split: function (value, args) {
        var separator = args.separator;
        return ramda_1.split(separator, value);
    },
    Trim: function (value) {
        return ramda_1.trim(value);
    },
    /* Number Transform */
    Add: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value + args.value;
        }
        return value + aspects_1.coerceAspect(args.value, getAspect);
    },
    Sub: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value - args.value;
        }
        return value - aspects_1.coerceAspect(args.value, getAspect);
    },
    Divide: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value / args.value;
        }
        return value / aspects_1.coerceAspect(args.value, getAspect);
    },
    Multiply: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value * args.value;
        }
        return value * aspects_1.coerceAspect(args.value, getAspect);
    },
    Modulus: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value % args.value;
        }
        return value % aspects_1.coerceAspect(args.value, getAspect);
    },
    ToPrecision: function (value, args) {
        return value.toPrecision(args.precision);
    },
    /* Array transforms  */
    Concat: function (value, args, getAspect) {
        var other = args.other;
        return ramda_1.concat(value, aspects_1.coerceAspect(other, getAspect));
    },
    Slice: function (value, args) {
        return ramda_1.slice(args.start, args.stop, value);
    },
    Map: function (value, args, getAspect) {
        var transform = args.transform;
        return value.map(function (e) {
            return exports.executeTransform(transform.transform, e, transform.args, transform.next, getAspect);
        });
    },
    Filter: function (value, args, getAspect) {
        var comparison = args.comparison;
        return value.filter(function (e) {
            return exports.executeTransform(comparison.transform, e, comparison.args, comparison.next, getAspect);
        });
    },
    Reduce: function (value, args, getAspect) {
        var transform = args.transform, accumulator = args.accumulator;
        var acc = aspects_1.coerceAspect(accumulator, getAspect);
        return value.reduce(function (previous, next) {
            return exports.executeTransform(transform.transform, [previous, next], transform.args, transform.next, getAspect);
        }, acc);
    },
    Pluck: function (value, args) {
        var field = args.field;
        return ramda_1.pluck(field, value);
    },
    Append: function (value, args, getAspect) {
        return ramda_1.concat(value, [aspects_1.coerceAspect(args.value, getAspect)]);
    },
    Prepend: function (value, args, getAspect) {
        return ramda_1.concat([aspects_1.coerceAspect(args.value, getAspect)], value);
    },
    Insert: function (value, args, getAspect) {
        var target = args.target, front = args.front;
        var t = aspects_1.coerceAspect(target, getAspect);
        return front ? ramda_1.concat([value], t) : ramda_1.concat(t, [value]);
    },
    Take: function (value, args, getAspect) {
        var n = args.n;
        return ramda_1.take(aspects_1.coerceAspect(n, getAspect), value);
    },
    Length: function (value) {
        return value.length;
    },
    Range: function (value, args, getAspect) {
        var start = args.start, end = args.end, step = args.step;
        var s = aspects_1.coerceAspect(start, getAspect);
        var e = aspects_1.coerceAspect(end, getAspect);
        var i = s;
        var arr = [];
        while (i < e) {
            arr.push(i);
            i += step;
        }
        return arr;
    },
    Includes: function (value, args, getAspect) {
        return ramda_1.includes(aspects_1.coerceAspect(args.value, getAspect), value);
    },
    Find: function (value, args, getAspect) {
        var comparison = args.comparison;
        return ramda_1.find(function (a) {
            return exports.executeTransform(comparison.transform, a, comparison.args, comparison.next, getAspect);
        })(value);
    },
    Join: function (value, args, getAspect) {
        return ramda_1.join(aspects_1.coerceAspect(args.separator, getAspect), value);
    },
    Sort: function (value, args, getAspect) {
        var transform = args.transform;
        return ramda_1.sort(function (a, b) {
            return exports.executeTransform(transform.transform, [a, b], transform.args, transform.next, getAspect);
        }, value);
    },
    Reverse: function (value) {
        return ramda_1.reverse(value);
    },
    Unique: function (value) {
        return ramda_1.uniq(value);
    },
    Zip: function (value, args, getAspect) {
        return ramda_1.zip(value, aspects_1.coerceAspect(args.value, getAspect));
    },
    /* Object transforms */
    Pick: function (value, args) {
        return ramda_1.pick(args.fields, value);
    },
    Get: function (value, args) {
        return value[args.field];
    },
    Set: function (v, args, getAspect) {
        var key = args.key, value = args.value;
        v[key] = aspects_1.coerceAspect(value, getAspect);
        return v;
    },
    Put: function (value, args, getAspect) {
        var key = args.key, target = args.target;
        var obj = aspects_1.coerceAspect(target, getAspect);
        obj[key] = value;
        return obj;
    },
    Merge: function (value, args, getAspect) {
        var deep = args.deep, direction = args.direction, other = args.other;
        var otherValue = other;
        if (aspects_1.isAspect(other)) {
            otherValue = getAspect(other.identity, other.aspect);
        }
        if (direction === 'right') {
            if (deep) {
                return ramda_1.mergeDeepRight(value, otherValue);
            }
            return ramda_1.mergeRight(value, otherValue);
        }
        if (deep) {
            return ramda_1.mergeDeepLeft(value, otherValue);
        }
        return ramda_1.mergeLeft(value, otherValue);
    },
    ToJson: function (value) {
        return JSON.stringify(value);
    },
    FromJson: function (value) {
        return JSON.parse(value);
    },
    ToPairs: function (value) {
        return ramda_1.toPairs(value);
    },
    FromPairs: function (value) {
        return ramda_1.fromPairs(value);
    },
    /* Conditionals */
    If: function (value, args, getAspect) {
        var comparison = args.comparison, then = args.then, otherwise = args.otherwise;
        var c = transforms[comparison.transform];
        if (c(value, comparison.args, getAspect)) {
            return exports.executeTransform(then.transform, value, then.args, then.next, getAspect);
        }
        if (otherwise) {
            return exports.executeTransform(otherwise.transform, value, otherwise.args, otherwise.next, getAspect);
        }
        return value;
    },
    Equals: function (value, args, getAspect) {
        return ramda_1.equals(value, aspects_1.coerceAspect(args.other, getAspect));
    },
    NotEquals: function (value, args, getAspect) {
        return !ramda_1.equals(value, aspects_1.coerceAspect(args.other, getAspect));
    },
    Match: function (value, args, getAspect) {
        var r = new RegExp(aspects_1.coerceAspect(args.other, getAspect));
        return r.test(value);
    },
    Greater: function (value, args, getAspect) {
        return value > aspects_1.coerceAspect(args.other, getAspect);
    },
    GreaterOrEquals: function (value, args, getAspect) {
        return value >= aspects_1.coerceAspect(args.other, getAspect);
    },
    Lesser: function (value, args, getAspect) {
        return value < aspects_1.coerceAspect(args.other, getAspect);
    },
    LesserOrEquals: function (value, args, getAspect) {
        return value <= aspects_1.coerceAspect(args.other, getAspect);
    },
    And: function (value, args, getAspect) {
        return value && aspects_1.coerceAspect(args.other, getAspect);
    },
    Or: function (value, args, getAspect) {
        return value || aspects_1.coerceAspect(args.other, getAspect);
    },
    Not: function (value) {
        return !value;
    },
    RawValue: function (value, args) {
        return args.value;
    },
    AspectValue: function (value, args, getAspect) {
        var _a = args.target, identity = _a.identity, aspect = _a.aspect;
        return getAspect(identity, aspect);
    },
};
var executeTransform = function (transform, value, args, next, getAspect) {
    var t = transforms[transform];
    var newValue = t(value, args, getAspect);
    if (next.length) {
        var n = next[0];
        return exports.executeTransform(n.transform, newValue, n.args, 
        // Execute the next first, then back to chain.
        ramda_1.concat(n.next, ramda_1.drop(1, next)), getAspect);
    }
    return newValue;
};
exports.executeTransform = executeTransform;
exports.default = transforms;


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ var __webpack_exports__ = (__webpack_exec__("./src/renderer/js/index.tsx"));
/******/ return __webpack_exports__;
/******/ }
]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9yZW5kZXJlcl85ZGRjODMzNDYyNjhjZDk1ODc0Yi5qcyIsIm1hcHBpbmdzIjoiO0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUNELE87Ozs7Ozs7Ozs7O0FDVkEsbUZBQThCO0FBR3ZCLElBQU0sUUFBUSxHQUFHLFVBQUMsR0FBUTtJQUM3QixpQkFBRSxDQUFDLE1BQU0sRUFBRSxHQUFHLENBQUMsSUFBSSxXQUFHLENBQUMsVUFBVSxFQUFFLEdBQUcsQ0FBQyxJQUFJLFdBQUcsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDO0FBQTdELENBQTZELENBQUM7QUFEckQsZ0JBQVEsWUFDNkM7QUFFM0QsSUFBTSxZQUFZLEdBQUcsVUFDeEIsR0FBUSxFQUNSLFNBQWlDLElBQzNCLFFBQUMsZ0JBQVEsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDLE1BQU0sQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFHLENBQUMsRUFBM0QsQ0FBMkQsQ0FBQztBQUh6RCxvQkFBWSxnQkFHNkM7QUFFL0QsSUFBTSxZQUFZLEdBQUcsVUFBQyxRQUFnQixFQUFFLE1BQWM7SUFDekQsT0FBRyxNQUFNLFNBQUksUUFBVTtBQUF2QixDQUF1QixDQUFDO0FBRGYsb0JBQVksZ0JBQ0c7QUFFckIsSUFBTSxZQUFZLEdBQUcsVUFBQyxDQUFTLEVBQUUsQ0FBUztJQUM3QyxRQUFDLENBQUMsUUFBUSxLQUFLLENBQUMsQ0FBQyxRQUFRLElBQUksQ0FBQyxDQUFDLE1BQU0sS0FBSyxDQUFDLENBQUMsTUFBTTtBQUFsRCxDQUFrRCxDQUFDO0FBRDFDLG9CQUFZLGdCQUM4Qjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ2Z2RCxzRUFBc0M7QUFDdEMsa0hBQWdDO0FBSWhDLElBQU0sUUFBUSxHQUFHLFVBQUMsS0FBb0I7SUFD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QUFDO0lBQ3ZELENBQUM7SUFDRCxRQUFRLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSSxFQUFFLFNBQVM7UUFDN0IsSUFBSSxVQUFFLENBQUMsTUFBTSxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUN4QixPQUFPLEtBQUssR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDO1NBQzdCO1FBQ0QsT0FBTyxLQUFLLEdBQUcsc0JBQVksQ0FBQyxJQUFJLENBQUMsS0FBSyxFQUFFLFNBQVMsQ0FBQyxDQUFDO0lBQ3ZELENBQUM7SUFDRCxPQUFPLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSSxFQUFFLFNBQVM7UUFDNUIsSUFBSSxVQUFFLENBQUMsTUFBTSxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMsRUFBRTtZQUN4QixPQUFPLEtBQUssR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDO1NBQzdCO1FBQ0QsT0FBTyxLQUFLLEdBQUcsc0JBQVksQ0FBQyxJQUFJLENBQUMsS0FBSyxFQUFFLFNBQVMsQ0FBQyxDQUFDO0lBQ3ZELENBQUM7SUFDRCxXQUFXLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtRQUNyQixPQUFPLEtBQUssQ0FBQyxXQUFXLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxDQUFDO0lBQzdDLENBQUM7SUFDRCx1QkFBdUI7SUFDdkIsTUFBTSxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUksRUFBRSxTQUFTO1FBQ3BCLFNBQUssR0FBSSxJQUFJLE1BQVIsQ0FBUztRQUNyQixPQUFPLGNBQU0sQ0FBQyxLQUFLLEVBQUUsc0JBQVksQ0FBQyxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUMsQ0FBQztJQUN6RCxDQUFDO0lBQ0QsS0FBSyxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7UUFDZixPQUFPLGFBQUssQ0FBQyxJQUFJLENBQUMsS0FBSyxFQUFFLElBQUksQ0FBQyxJQUFJLEVBQUUsS0FBSyxDQUFDLENBQUM7SUFDL0MsQ0FBQztJQUNELEdBQUcsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJLEVBQUUs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QUMsQ0FBQyxJQUFJLEVBQUUsWUFBSSxDQUFDLENBQUMsRUFBRSxJQUFJLENBQUMsQ0FBQyxFQUM3QixTQUFTLENBQ1osQ0FBQztLQUNMO0lBQ0QsT0FBTyxRQUFRLENBQUM7QUFDcEIsQ0FBQyxDQUFDO0FBckJXLHdCQUFnQixvQkFxQjNCO0FBRUYsa0JBQWUsVUFBVSxDQUFDOzs7Ozs7Ozs7OztBQzlWMUI7Ozs7Ozs7Ozs7QUNBQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL3JlbmRlcmVyL2pzL2FzcGVjdHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9SZW5kZXJlci50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvY29tcG9uZW50cy9VcGRhdGVyLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1dyYXBwZXIudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL3JlbmRlcmVyL2pzL2h5ZHJhdG9yLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9pbmRleC50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvcmVxdWVzdHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvcmVxdWlyZW1lbnRzLnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL3JlbmRlcmVyL2pzL3RyYW5zZm9ybXMudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3QtZG9tXCIsXCJjb21tb25qczJcIjpcInJlYWN0LWRvbVwiLFwiYW1kXCI6XCJyZWFjdC1kb21cIixcInVtZFwiOlwicmVhY3QtZG9tXCIsXCJyb290XCI6XCJSZWFjdERPTVwifT8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIiksIHJlcXVpcmUoXCJyZWFjdC1kb21cIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIiwgXCJyZWFjdC1kb21cIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9yZW5kZXJlclwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpLCByZXF1aXJlKFwicmVhY3QtZG9tXCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX3JlbmRlcmVyXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0sIHJvb3RbXCJSZWFjdERPTVwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18sIF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfZG9tX18pIHtcbnJldHVybiAiLCJpbXBvcnQge2hhcywgaXN9IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7QXNwZWN0LCBUcmFuc2Zvcm1HZXRBc3BlY3RGdW5jfSBmcm9tICcuL3R5cGVzJztcblxuZXhwb3J0IGNvbnN0IGlzQXNwZWN0ID0gKG9iajogYW55KTogYm9vbGVhbiA9PlxuICAgIGlzKE9iamVjdCwgb2JqKSAmJiBoYXMoJ2lkZW50aXR5Jywgb2JqKSAmJiBoYXMoJ2FzcGVjdCcsIG9iaik7XG5cbmV4cG9ydCBjb25zdCBjb2VyY2VBc3BlY3QgPSAoXG4gICAgb2JqOiBhbnksXG4gICAgZ2V0QXNwZWN0OiBUcmFuc2Zvcm1HZXRBc3BlY3RGdW5jXG4pOiBhbnkgPT4gKGlzQXNwZWN0KG9iaikgPyBnZXRBc3BlY3Qob2JqLmlkZW50aXR5LCBvYmouYXNwZWN0KSA6IG9iaik7XG5cbmV4cG9ydCBjb25zdCBnZXRBc3BlY3RLZXkgPSAoaWRlbnRpdHk6IHN0cmluZywgYXNwZWN0OiBzdHJpbmcpOiBzdHJpbmcgPT5cbiAgICBgJHthc3BlY3R9QCR7aWRlbnRpdHl9YDtcblxuZXhwb3J0IGNvbnN0IGlzU2FtZUFzcGVjdCA9IChhOiBBc3BlY3QsIGI6IEFzcGVjdCkgPT5cbiAgICBhLmlkZW50aXR5ID09PSBiLmlkZW50aXR5ICYmIGEuYXNwZWN0ID09PSBiLmFzcGVjdDtcbiIsImltcG9ydCBSZWFjdCwge3VzZVN0YXRlfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgVXBkYXRlciBmcm9tICcuL1VwZGF0ZXInO1xuXG5pbXBvcnQge1JlbmRlck9wdGlvbnN9IGZyb20gJy4uL3R5cGVzJztcblxuY29uc3QgUmVuZGVyZXIgPSAocHJvcHM6IFJlbmRlck9wdGlvbnMpID0+IHtcbiAgICBjb25zdCBbcmVsb2FkS2V5LCBzZXRSZWxvYWRLZXldID0gdXNlU3RhdGUoMSk7XG5cbiAgICAvLyBGSVhNRSBmaW5kIHdoZXJlIHRoaXMgaXMgdXNlZCBhbmQgcmVmYWN0b3IvcmVtb3ZlXG4gICAgLy8gQHRzLWlnbm9yZVxuICAgIHdpbmRvdy5kYXp6bGVyX2Jhc2VfdXJsID0gcHJvcHMuYmFzZVVybDtcbiAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZXJcIj5cbiAgICAgICAgICAgIDxVcGRhdGVyXG4gICAgICAgICAgICAgICAgey4uLnByb3BzfVxuICAgICAgICAgICAgICAgIGtleT17YHVwZC0ke3JlbG9hZEtleX1gfVxuICAgICAgICAgICAgICAgIGhvdFJlbG9hZD17KCkgPT4gc2V0UmVsb2FkS2V5KHJlbG9hZEtleSArIDEpfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgPC9kaXY+XG4gICAgKTtcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFJlbmRlcmVyO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7YXBpUmVxdWVzdH0gZnJvbSAnLi4vcmVxdWVzdHMnO1xuaW1wb3J0IHtcbiAgICBoeWRyYXRlQ29tcG9uZW50LFxuICAgIGh5ZHJhdGVQcm9wcyxcbiAgICBpc0NvbXBvbmVudCxcbiAgICBwcmVwYXJlUHJvcCxcbn0gZnJvbSAnLi4vaHlkcmF0b3InO1xuaW1wb3J0IHtsb2FkUmVxdWlyZW1lbnQsIGxvYWRSZXF1aXJlbWVudHN9IGZyb20gJy4uL3JlcXVpcmVtZW50cyc7XG5pbXBvcnQge2Rpc2FibGVDc3N9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtcbiAgICBwaWNrQnksXG4gICAga2V5cyxcbiAgICBtYXAsXG4gICAgZXZvbHZlLFxuICAgIGNvbmNhdCxcbiAgICBmbGF0dGVuLFxuICAgIGRpc3NvYyxcbiAgICB6aXAsXG4gICAgYWxsLFxuICAgIHRvUGFpcnMsXG4gICAgdmFsdWVzIGFzIHJWYWx1ZXMsXG4gICAgcHJvcFNhdGlzZmllcyxcbiAgICBub3QsXG4gICAgYXNzb2MsXG4gICAgcGlwZSxcbiAgICBwcm9wRXEsXG59IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7ZXhlY3V0ZVRyYW5zZm9ybX0gZnJvbSAnLi4vdHJhbnNmb3Jtcyc7XG5pbXBvcnQge1xuICAgIEJpbmRpbmcsXG4gICAgQm91bmRDb21wb25lbnRzLFxuICAgIENhbGxPdXRwdXQsXG4gICAgRXZvbHZlZEJpbmRpbmcsXG4gICAgQXBpRnVuYyxcbiAgICBUaWUsXG4gICAgVXBkYXRlclByb3BzLFxuICAgIFVwZGF0ZXJTdGF0ZSxcbiAgICBQYWdlQXBpUmVzcG9uc2UsXG4gICAgQXNwZWN0LFxufSBmcm9tICcuLi90eXBlcyc7XG5pbXBvcnQge2dldEFzcGVjdEtleSwgaXNTYW1lQXNwZWN0fSBmcm9tICcuLi9hc3BlY3RzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVXBkYXRlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxcbiAgICBVcGRhdGVyUHJvcHMsXG4gICAgVXBkYXRlclN0YXRlXG4+IHtcbiAgICBwcml2YXRlIHBhZ2VBcGk6IEFwaUZ1bmM7XG4gICAgcHJpdmF0ZSByZWFkb25seSBib3VuZENvbXBvbmVudHM6IEJvdW5kQ29tcG9uZW50cztcbiAgICBwcml2YXRlIHdzOiBXZWJTb2NrZXQ7XG5cbiAgICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgICAgICBzdXBlcihwcm9wcyk7XG4gICAgICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAgICAgICBsYXlvdXQ6IG51bGwsXG4gICAgICAgICAgICByZWFkeTogZmFsc2UsXG4gICAgICAgICAgICBwYWdlOiBudWxsLFxuICAgICAgICAgICAgYmluZGluZ3M6IHt9LFxuICAgICAgICAgICAgcGFja2FnZXM6IHt9LFxuICAgICAgICAgICAgcmVsb2FkOiBmYWxzZSxcbiAgICAgICAgICAgIHJlYmluZGluZ3M6IFtdLFxuICAgICAgICAgICAgcmVxdWlyZW1lbnRzOiBbXSxcbiAgICAgICAgICAgIHJlbG9hZGluZzogZmFsc2UsXG4gICAgICAgICAgICBuZWVkUmVmcmVzaDogZmFsc2UsXG4gICAgICAgICAgICB0aWVzOiBbXSxcbiAgICAgICAgfTtcbiAgICAgICAgLy8gVGhlIGFwaSB1cmwgZm9yIHRoZSBwYWdlIGlzIHRoZSBzYW1lIGJ1dCBhIHBvc3QuXG4gICAgICAgIC8vIEZldGNoIGJpbmRpbmdzLCBwYWNrYWdlcyAmIHJlcXVpcmVtZW50c1xuICAgICAgICB0aGlzLnBhZ2VBcGkgPSBhcGlSZXF1ZXN0KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgICAgLy8gQWxsIGNvbXBvbmVudHMgZ2V0IGNvbm5lY3RlZC5cbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHMgPSB7fTtcbiAgICAgICAgdGhpcy53cyA9IG51bGw7XG5cbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuY29ubmVjdCA9IHRoaXMuY29ubmVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmRpc2Nvbm5lY3QgPSB0aGlzLmRpc2Nvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5vbk1lc3NhZ2UgPSB0aGlzLm9uTWVzc2FnZS5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoaWRlbnRpdHk6IHN0cmluZywgYXNwZWN0cywgaW5pdGlhbCA9IGZhbHNlKSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZTxudW1iZXI+KChyZXNvbHZlKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBhc3BlY3RLZXlzOiBzdHJpbmdbXSA9IGtleXM8c3RyaW5nPihhc3BlY3RzKTtcbiAgICAgICAgICAgIGxldCBiaW5kaW5nczogQmluZGluZ1tdIHwgRXZvbHZlZEJpbmRpbmdbXSA9IGFzcGVjdEtleXNcbiAgICAgICAgICAgICAgICAubWFwKChrZXk6IHN0cmluZykgPT4gKHtcbiAgICAgICAgICAgICAgICAgICAgLi4udGhpcy5zdGF0ZS5iaW5kaW5nc1tnZXRBc3BlY3RLZXkoaWRlbnRpdHksIGtleSldLFxuICAgICAgICAgICAgICAgICAgICB2YWx1ZTogYXNwZWN0c1trZXldLFxuICAgICAgICAgICAgICAgIH0pKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoXG4gICAgICAgICAgICAgICAgICAgIChlKSA9PiBlLnRyaWdnZXIgJiYgIShlLnRyaWdnZXIuc2tpcF9pbml0aWFsICYmIGluaXRpYWwpXG4gICAgICAgICAgICAgICAgKTtcblxuICAgICAgICAgICAgdGhpcy5zdGF0ZS5yZWJpbmRpbmdzLmZvckVhY2goKGJpbmRpbmcpID0+IHtcbiAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmcudHJpZ2dlci5pZGVudGl0eS50ZXN0KGlkZW50aXR5KSAmJlxuICAgICAgICAgICAgICAgICAgICAhKGJpbmRpbmcudHJpZ2dlci5za2lwX2luaXRpYWwgJiYgaW5pdGlhbClcbiAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgICAgICAgICBiaW5kaW5ncyA9IGNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzLFxuICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0S2V5c1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5maWx0ZXIoKGs6IHN0cmluZykgPT5cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZy50cmlnZ2VyLmFzcGVjdC50ZXN0KGspXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXAoKGspID0+ICh7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLmJpbmRpbmcsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBhc3BlY3RzW2tdLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cmlnZ2VyOiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAuLi5iaW5kaW5nLnRyaWdnZXIsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdDogayxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KSlcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgY29uc3QgcmVtb3ZhYmxlVGllcyA9IFtdO1xuXG4gICAgICAgICAgICBmbGF0dGVuKFxuICAgICAgICAgICAgICAgIGFzcGVjdEtleXMubWFwKChhc3BlY3QpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgY29uc3QgdGllcyA9IFtdO1xuICAgICAgICAgICAgICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRoaXMuc3RhdGUudGllcy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc3QgdGllID0gdGhpcy5zdGF0ZS50aWVzW2ldO1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc3Qge3RyaWdnZXJ9ID0gdGllO1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICEodHJpZ2dlci5za2lwX2luaXRpYWwgJiYgaW5pdGlhbCkgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAoKHRyaWdnZXIucmVnZXggJiZcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cmlnZ2VyLmlkZW50aXR5LnRlc3QoaWRlbnRpdHkpICYmXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJpZ2dlci5hc3BlY3QudGVzdChhc3BlY3QpKSB8fFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpc1NhbWVBc3BlY3QodHJpZ2dlciwge2lkZW50aXR5LCBhc3BlY3R9KSlcbiAgICAgICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRpZXMucHVzaCh7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLnRpZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU6IGFzcGVjdHNbYXNwZWN0XSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICByZXR1cm4gdGllcztcbiAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgKS5mb3JFYWNoKCh0aWU6IFRpZSkgPT4ge1xuICAgICAgICAgICAgICAgIGNvbnN0IHt0cmFuc2Zvcm1zfSA9IHRpZTtcbiAgICAgICAgICAgICAgICBsZXQgdmFsdWUgPSB0aWUudmFsdWU7XG5cbiAgICAgICAgICAgICAgICBpZiAodGllLnRyaWdnZXIub25jZSkge1xuICAgICAgICAgICAgICAgICAgICByZW1vdmFibGVUaWVzLnB1c2godGllKTtcbiAgICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgICBpZiAodHJhbnNmb3Jtcykge1xuICAgICAgICAgICAgICAgICAgICB2YWx1ZSA9IHRyYW5zZm9ybXMucmVkdWNlKChhY2MsIGUpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGUudHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFjYyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlLmFyZ3MsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgZS5uZXh0LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuZ2V0QXNwZWN0LmJpbmQodGhpcylcbiAgICAgICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgICAgIH0sIHZhbHVlKTtcbiAgICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgICB0aWUudGFyZ2V0cy5mb3JFYWNoKCh0OiBBc3BlY3QpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgY29uc3QgY29tcG9uZW50ID0gdGhpcy5ib3VuZENvbXBvbmVudHNbdC5pZGVudGl0eV07XG4gICAgICAgICAgICAgICAgICAgIGlmIChjb21wb25lbnQpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbXBvbmVudC51cGRhdGVBc3BlY3RzKHtbdC5hc3BlY3RdOiB2YWx1ZX0pO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgICAgICBpZiAodGllLnJlZ2V4VGFyZ2V0cy5sZW5ndGgpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gRklYTUUgcHJvYmFibHkgYSBtb3JlIGVmZmljaWVudCB3YXkgdG8gZG8gdGhpc1xuICAgICAgICAgICAgICAgICAgICAvLyAgcmVmYWN0b3IgbGF0ZXIuXG4gICAgICAgICAgICAgICAgICAgIHJWYWx1ZXModGhpcy5ib3VuZENvbXBvbmVudHMpLmZvckVhY2goKGMpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRpZS5yZWdleFRhcmdldHMuZm9yRWFjaCgodCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmICgodC5pZGVudGl0eSBhcyBSZWdFeHApLnRlc3QoYy5pZGVudGl0eSkpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYy51cGRhdGVBc3BlY3RzKHtbdC5hc3BlY3QgYXMgc3RyaW5nXTogdmFsdWV9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgIGlmIChyZW1vdmFibGVUaWVzLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe1xuICAgICAgICAgICAgICAgICAgICB0aWVzOiB0aGlzLnN0YXRlLnRpZXMuZmlsdGVyKFxuICAgICAgICAgICAgICAgICAgICAgICAgKHQpID0+XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgIXJlbW92YWJsZVRpZXMucmVkdWNlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAoYWNjLCB0aWUpID0+XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhY2MgfHxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIChpc1NhbWVBc3BlY3QodC50cmlnZ2VyLCB0aWUudHJpZ2dlcikgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhbGwoKFt0MSwgdDJdKSA9PiBpc1NhbWVBc3BlY3QodDEsIHQyKSkoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHppcCh0LnRhcmdldHMsIHRpZS50YXJnZXRzKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICkpLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmYWxzZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgaWYgKCFiaW5kaW5ncykge1xuICAgICAgICAgICAgICAgIHJlc29sdmUoMCk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgIGNvbnN0IHJlbW92YWJsZUJpbmRpbmdzID0gW107XG4gICAgICAgICAgICAgICAgYmluZGluZ3MuZm9yRWFjaCgoYmluZGluZykgPT4ge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnNlbmRCaW5kaW5nKGJpbmRpbmcsIGJpbmRpbmcudmFsdWUsIGJpbmRpbmcuY2FsbCk7XG4gICAgICAgICAgICAgICAgICAgIGlmIChiaW5kaW5nLnRyaWdnZXIub25jZSkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVtb3ZhYmxlQmluZGluZ3MucHVzaChiaW5kaW5nKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIGlmIChyZW1vdmFibGVCaW5kaW5ncy5sZW5ndGgpIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7XG4gICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nczogcmVtb3ZhYmxlQmluZGluZ3MucmVkdWNlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIChhY2MsIGJpbmRpbmcpID0+XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRpc3NvYyhcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdldEFzcGVjdEtleShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLnRyaWdnZXIuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZy50cmlnZ2VyLmFzcGVjdFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFjY1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc3RhdGUuYmluZGluZ3NcbiAgICAgICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAvLyBQcm9taXNlIGlzIGZvciB3cmFwcGVyIHJlYWR5XG4gICAgICAgICAgICAgICAgLy8gVE9ETyBpbnZlc3RpZ2F0ZSByZWFzb25zL3VzZXMgb2YgbGVuZ3RoIHJlc29sdmU/XG4gICAgICAgICAgICAgICAgcmVzb2x2ZShiaW5kaW5ncy5sZW5ndGgpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBnZXRBc3BlY3Q8VD4oaWRlbnRpdHk6IHN0cmluZywgYXNwZWN0OiBzdHJpbmcpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICAgICAgY29uc3QgYyA9IHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XTtcbiAgICAgICAgaWYgKGMpIHtcbiAgICAgICAgICAgIHJldHVybiBjLmdldEFzcGVjdChhc3BlY3QpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB1bmRlZmluZWQ7XG4gICAgfVxuXG4gICAgY29ubmVjdChpZGVudGl0eSwgc2V0QXNwZWN0cywgZ2V0QXNwZWN0LCBtYXRjaEFzcGVjdHMsIHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldID0ge1xuICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICBzZXRBc3BlY3RzLFxuICAgICAgICAgICAgZ2V0QXNwZWN0LFxuICAgICAgICAgICAgbWF0Y2hBc3BlY3RzLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgfTtcbiAgICB9XG5cbiAgICBkaXNjb25uZWN0KGlkZW50aXR5KSB7XG4gICAgICAgIGRlbGV0ZSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgfVxuXG4gICAgb25NZXNzYWdlKHJlc3BvbnNlKSB7XG4gICAgICAgIGNvbnN0IGRhdGEgPSBKU09OLnBhcnNlKHJlc3BvbnNlLmRhdGEpO1xuICAgICAgICBjb25zdCB7aWRlbnRpdHksIGtpbmQsIHBheWxvYWQsIHN0b3JhZ2UsIHJlcXVlc3RfaWR9ID0gZGF0YTtcbiAgICAgICAgbGV0IHN0b3JlO1xuICAgICAgICBpZiAoc3RvcmFnZSA9PT0gJ3Nlc3Npb24nKSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5zZXNzaW9uU3RvcmFnZTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHN0b3JlID0gd2luZG93LmxvY2FsU3RvcmFnZTtcbiAgICAgICAgfVxuICAgICAgICBzd2l0Y2ggKGtpbmQpIHtcbiAgICAgICAgICAgIGNhc2UgJ3NldC1hc3BlY3QnOlxuICAgICAgICAgICAgICAgIGNvbnN0IHNldEFzcGVjdHMgPSAoY29tcG9uZW50KSA9PlxuICAgICAgICAgICAgICAgICAgICBjb21wb25lbnRcbiAgICAgICAgICAgICAgICAgICAgICAgIC5zZXRBc3BlY3RzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcGF5bG9hZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuZGlzY29ubmVjdFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgIC50aGVuKCgpID0+IHRoaXMudXBkYXRlQXNwZWN0cyhpZGVudGl0eSwgcGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlZ2V4KSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHBhdHRlcm4gPSBuZXcgUmVnRXhwKGRhdGEuaWRlbnRpdHkpO1xuICAgICAgICAgICAgICAgICAgICBrZXlzKHRoaXMuYm91bmRDb21wb25lbnRzKVxuICAgICAgICAgICAgICAgICAgICAgICAgLmZpbHRlcigoazogc3RyaW5nKSA9PiBwYXR0ZXJuLnRlc3QoaykpXG4gICAgICAgICAgICAgICAgICAgICAgICAubWFwKChrKSA9PiB0aGlzLmJvdW5kQ29tcG9uZW50c1trXSlcbiAgICAgICAgICAgICAgICAgICAgICAgIC5mb3JFYWNoKHNldEFzcGVjdHMpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHNldEFzcGVjdHModGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdnZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCB7YXNwZWN0fSA9IGRhdGE7XG4gICAgICAgICAgICAgICAgY29uc3Qgd2FudGVkID0gdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgICAgICAgICAgICAgIGlmICghd2FudGVkKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVycm9yOiBgQXNwZWN0IG5vdCBmb3VuZCAke2lkZW50aXR5fS4ke2FzcGVjdH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IHdhbnRlZC5nZXRBc3BlY3QoYXNwZWN0KTtcbiAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWx1ZSksXG4gICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdzZXQtc3RvcmFnZSc6XG4gICAgICAgICAgICAgICAgc3RvcmUuc2V0SXRlbShpZGVudGl0eSwgSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnZ2V0LXN0b3JhZ2UnOlxuICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBKU09OLnBhcnNlKHN0b3JlLmdldEl0ZW0oaWRlbnRpdHkpKSxcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAncmVsb2FkJzpcbiAgICAgICAgICAgICAgICBjb25zdCB7ZmlsZW5hbWVzLCBob3QsIHJlZnJlc2gsIGRlbGV0ZWR9ID0gZGF0YTtcbiAgICAgICAgICAgICAgICBpZiAocmVmcmVzaCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLmNsb3NlKCk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZSwgbmVlZFJlZnJlc2g6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAoaG90KSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIFRoZSB3cyBjb25uZWN0aW9uIHdpbGwgY2xvc2UsIHdoZW4gaXRcbiAgICAgICAgICAgICAgICAgICAgLy8gcmVjb25uZWN0IGl0IHdpbGwgZG8gYSBoYXJkIHJlbG9hZCBvZiB0aGUgcGFnZSBhcGkuXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGZpbGVuYW1lcy5mb3JFYWNoKGxvYWRSZXF1aXJlbWVudCk7XG4gICAgICAgICAgICAgICAgZGVsZXRlZC5mb3JFYWNoKChyKSA9PiBkaXNhYmxlQ3NzKHIudXJsKSk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdwaW5nJzpcbiAgICAgICAgICAgICAgICAvLyBKdXN0IGRvIG5vdGhpbmcuXG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBzZW5kQmluZGluZyhiaW5kaW5nLCB2YWx1ZSwgY2FsbCA9IGZhbHNlKSB7XG4gICAgICAgIC8vIENvbGxlY3QgYWxsIHZhbHVlcyBhbmQgc2VuZCBhIGJpbmRpbmcgcGF5bG9hZFxuICAgICAgICBjb25zdCB0cmlnZ2VyID0ge1xuICAgICAgICAgICAgLi4uYmluZGluZy50cmlnZ2VyLFxuICAgICAgICAgICAgdmFsdWU6IHByZXBhcmVQcm9wKHZhbHVlKSxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3Qgc3RhdGVzID0gYmluZGluZy5zdGF0ZXMucmVkdWNlKChhY2MsIHN0YXRlKSA9PiB7XG4gICAgICAgICAgICBpZiAoc3RhdGUucmVnZXgpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBpZGVudGl0eVBhdHRlcm4gPSBuZXcgUmVnRXhwKHN0YXRlLmlkZW50aXR5KTtcbiAgICAgICAgICAgICAgICBjb25zdCBhc3BlY3RQYXR0ZXJuID0gbmV3IFJlZ0V4cChzdGF0ZS5hc3BlY3QpO1xuICAgICAgICAgICAgICAgIHJldHVybiBjb25jYXQoXG4gICAgICAgICAgICAgICAgICAgIGFjYyxcbiAgICAgICAgICAgICAgICAgICAgZmxhdHRlbihcbiAgICAgICAgICAgICAgICAgICAgICAgIGtleXModGhpcy5ib3VuZENvbXBvbmVudHMpLm1hcCgoazogc3RyaW5nKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgbGV0IHZhbHVlcyA9IFtdO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIChpZGVudGl0eVBhdHRlcm4udGVzdChrKSkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZXMgPSB0aGlzLmJvdW5kQ29tcG9uZW50c1trXVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLm1hdGNoQXNwZWN0cyhhc3BlY3RQYXR0ZXJuKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLm1hcCgoW25hbWUsIHZhbF0pID0+ICh7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4uc3RhdGUsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IGssXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0OiBuYW1lLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWwpLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSkpO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gdmFsdWVzO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIGFjYy5wdXNoKHtcbiAgICAgICAgICAgICAgICAuLi5zdGF0ZSxcbiAgICAgICAgICAgICAgICB2YWx1ZTpcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbc3RhdGUuaWRlbnRpdHldICYmXG4gICAgICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wKFxuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHNbc3RhdGUuaWRlbnRpdHldLmdldEFzcGVjdChcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGF0ZS5hc3BlY3RcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgcmV0dXJuIGFjYztcbiAgICAgICAgfSwgW10pO1xuXG4gICAgICAgIGNvbnN0IHBheWxvYWQgPSB7XG4gICAgICAgICAgICB0cmlnZ2VyLFxuICAgICAgICAgICAgc3RhdGVzLFxuICAgICAgICAgICAga2luZDogJ2JpbmRpbmcnLFxuICAgICAgICAgICAgcGFnZTogdGhpcy5zdGF0ZS5wYWdlLFxuICAgICAgICAgICAga2V5OiBiaW5kaW5nLmtleSxcbiAgICAgICAgfTtcbiAgICAgICAgaWYgKGNhbGwpIHtcbiAgICAgICAgICAgIHRoaXMuY2FsbEJpbmRpbmcocGF5bG9hZCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLndzLnNlbmQoSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY2FsbEJpbmRpbmcocGF5bG9hZCkge1xuICAgICAgICB0aGlzLnBhZ2VBcGk8Q2FsbE91dHB1dD4oJycsIHtcbiAgICAgICAgICAgIG1ldGhvZDogJ1BBVENIJyxcbiAgICAgICAgICAgIHBheWxvYWQsXG4gICAgICAgICAgICBqc29uOiB0cnVlLFxuICAgICAgICB9KS50aGVuKChyZXNwb25zZSkgPT4ge1xuICAgICAgICAgICAgdG9QYWlycyhyZXNwb25zZS5vdXRwdXQpLmZvckVhY2goKFtpZGVudGl0eSwgYXNwZWN0c10pID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCBjb21wb25lbnQgPSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgICAgICAgICAgICAgaWYgKGNvbXBvbmVudCkge1xuICAgICAgICAgICAgICAgICAgICBjb21wb25lbnQudXBkYXRlQXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBhc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIF9jb25uZWN0V1MoKSB7XG4gICAgICAgIC8vIFNldHVwIHdlYnNvY2tldCBmb3IgdXBkYXRlc1xuICAgICAgICBsZXQgdHJpZXMgPSAwO1xuICAgICAgICBsZXQgaGFyZENsb3NlID0gZmFsc2U7XG4gICAgICAgIGNvbnN0IGNvbm5leGlvbiA9ICgpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHVybCA9IGB3cyR7XG4gICAgICAgICAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYuc3RhcnRzV2l0aCgnaHR0cHMnKSA/ICdzJyA6ICcnXG4gICAgICAgICAgICB9Oi8vJHtcbiAgICAgICAgICAgICAgICAodGhpcy5wcm9wcy5iYXNlVXJsICYmIHRoaXMucHJvcHMuYmFzZVVybCkgfHxcbiAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24uaG9zdFxuICAgICAgICAgICAgfS8ke3RoaXMuc3RhdGUucGFnZX0vd3NgO1xuICAgICAgICAgICAgdGhpcy53cyA9IG5ldyBXZWJTb2NrZXQodXJsKTtcbiAgICAgICAgICAgIHRoaXMud3MuYWRkRXZlbnRMaXN0ZW5lcignbWVzc2FnZScsIHRoaXMub25NZXNzYWdlKTtcbiAgICAgICAgICAgIHRoaXMud3Mub25vcGVuID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgIGlmICh0aGlzLnN0YXRlLnJlbG9hZGluZykge1xuICAgICAgICAgICAgICAgICAgICBoYXJkQ2xvc2UgPSB0cnVlO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLmNsb3NlKCk7XG4gICAgICAgICAgICAgICAgICAgIGlmICh0aGlzLnN0YXRlLm5lZWRSZWZyZXNoKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24ucmVsb2FkKCk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnByb3BzLmhvdFJlbG9hZCgpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgdHJpZXMgPSAwO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgICAgICB0aGlzLndzLm9uY2xvc2UgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgcmVjb25uZWN0ID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICB0cmllcysrO1xuICAgICAgICAgICAgICAgICAgICBjb25uZXhpb24oKTtcbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIGlmICghaGFyZENsb3NlICYmIHRyaWVzIDwgdGhpcy5wcm9wcy5yZXRyaWVzKSB7XG4gICAgICAgICAgICAgICAgICAgIHNldFRpbWVvdXQocmVjb25uZWN0LCAxMDAwKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9O1xuICAgICAgICB9O1xuICAgICAgICBjb25uZXhpb24oKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgdGhpcy5wYWdlQXBpPFBhZ2VBcGlSZXNwb25zZT4oJycsIHttZXRob2Q6ICdQT1NUJ30pLnRoZW4oKHJlc3BvbnNlKSA9PiB7XG4gICAgICAgICAgICBjb25zdCB0b1JlZ2V4ID0gKHgpID0+IG5ldyBSZWdFeHAoeCk7XG4gICAgICAgICAgICB0aGlzLnNldFN0YXRlKFxuICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgcGFnZTogcmVzcG9uc2UucGFnZSxcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0OiByZXNwb25zZS5sYXlvdXQsXG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzOiBwaWNrQnkoKGIpID0+ICFiLnJlZ2V4LCByZXNwb25zZS5iaW5kaW5ncyksXG4gICAgICAgICAgICAgICAgICAgIC8vIFJlZ2V4IGJpbmRpbmdzIHRyaWdnZXJzXG4gICAgICAgICAgICAgICAgICAgIHJlYmluZGluZ3M6IG1hcCgoeCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc3QgYmluZGluZyA9IHJlc3BvbnNlLmJpbmRpbmdzW3hdO1xuICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZy50cmlnZ2VyID0gZXZvbHZlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IHRvUmVnZXgsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdDogdG9SZWdleCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmcudHJpZ2dlclxuICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBiaW5kaW5nO1xuICAgICAgICAgICAgICAgICAgICB9LCBrZXlzKHBpY2tCeSgoYikgPT4gYi5yZWdleCwgcmVzcG9uc2UuYmluZGluZ3MpKSksXG4gICAgICAgICAgICAgICAgICAgIHBhY2thZ2VzOiByZXNwb25zZS5wYWNrYWdlcyxcbiAgICAgICAgICAgICAgICAgICAgcmVxdWlyZW1lbnRzOiByZXNwb25zZS5yZXF1aXJlbWVudHMsXG4gICAgICAgICAgICAgICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgICAgICAgICAgICAgdGllczogbWFwKCh0aWUpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnN0IG5ld1RpZSA9IHBpcGUoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNzb2MoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICd0YXJnZXRzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGllLnRhcmdldHMuZmlsdGVyKHByb3BTYXRpc2ZpZXMobm90LCAncmVnZXgnKSlcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzc29jKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAncmVnZXhUYXJnZXRzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aWUudGFyZ2V0cy5maWx0ZXIocHJvcEVxKCdyZWdleCcsIHRydWUpKS5tYXAoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBldm9sdmUoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIE9ubHkgbWF0Y2ggaWRlbnRpdHkgZm9yIHRhcmdldHMuXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IHRvUmVnZXgsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAgICAgKSh0aWUpO1xuXG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAodGllLnRyaWdnZXIucmVnZXgpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gZXZvbHZlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cmlnZ2VyOiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IHRvUmVnZXgsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0OiB0b1JlZ2V4LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbmV3VGllXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBuZXdUaWU7XG4gICAgICAgICAgICAgICAgICAgIH0sIHJlc3BvbnNlLnRpZXMpLFxuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgKCkgPT5cbiAgICAgICAgICAgICAgICAgICAgbG9hZFJlcXVpcmVtZW50cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlLnJlcXVpcmVtZW50cyxcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlLnBhY2thZ2VzXG4gICAgICAgICAgICAgICAgICAgICkudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2UucmVsb2FkIHx8XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgclZhbHVlcyhyZXNwb25zZS5iaW5kaW5ncykuZmlsdGVyKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAoYmluZGluZzogQmluZGluZykgPT4gIWJpbmRpbmcuY2FsbFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICkubGVuZ3RoXG4gICAgICAgICAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLl9jb25uZWN0V1MoKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2xheW91dCwgcmVhZHksIHJlbG9hZGluZ30gPSB0aGlzLnN0YXRlO1xuICAgICAgICBpZiAoIXJlYWR5KSB7XG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nLWNvbnRhaW5lclwiPlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItc3BpblwiIC8+XG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nXCI+TG9hZGluZy4uLjwvZGl2PlxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAocmVsb2FkaW5nKSB7XG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nLWNvbnRhaW5lclwiPlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItc3BpbiByZWxvYWRcIiAvPlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItbG9hZGluZ1wiPlJlbG9hZGluZy4uLjwvZGl2PlxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoIWlzQ29tcG9uZW50KGxheW91dCkpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcihgTGF5b3V0IGlzIG5vdCBhIGNvbXBvbmVudDogJHtsYXlvdXR9YCk7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBjb250ZXh0cyA9IFtdO1xuXG4gICAgICAgIGNvbnN0IG9uQ29udGV4dCA9IChjb250ZXh0Q29tcG9uZW50KSA9PiB7XG4gICAgICAgICAgICBjb250ZXh0cy5wdXNoKGNvbnRleHRDb21wb25lbnQpO1xuICAgICAgICB9O1xuXG4gICAgICAgIGNvbnN0IGh5ZHJhdGVkID0gaHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgIGxheW91dC5uYW1lLFxuICAgICAgICAgICAgbGF5b3V0LnBhY2thZ2UsXG4gICAgICAgICAgICBsYXlvdXQuaWRlbnRpdHksXG4gICAgICAgICAgICBoeWRyYXRlUHJvcHMoXG4gICAgICAgICAgICAgICAgbGF5b3V0LmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3QsXG4gICAgICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0LFxuICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICk7XG5cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1yZW5kZXJlZFwiPlxuICAgICAgICAgICAgICAgIHtjb250ZXh0cy5sZW5ndGhcbiAgICAgICAgICAgICAgICAgICAgPyBjb250ZXh0cy5yZWR1Y2UoKGFjYywgQ29udGV4dCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoIWFjYykge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIDxDb250ZXh0PntoeWRyYXRlZH08L0NvbnRleHQ+O1xuICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiA8Q29udGV4dD57YWNjfTwvQ29udGV4dD47XG4gICAgICAgICAgICAgICAgICAgICAgfSwgbnVsbClcbiAgICAgICAgICAgICAgICAgICAgOiBoeWRyYXRlZH1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQge2NvbmNhdCwgam9pbiwga2V5c30gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtjYW1lbFRvU3BpbmFsfSBmcm9tICdjb21tb25zJztcbmltcG9ydCB7V3JhcHBlclByb3BzLCBXcmFwcGVyU3RhdGV9IGZyb20gJy4uL3R5cGVzJztcblxuLyoqXG4gKiBXcmFwcyBjb21wb25lbnRzIGZvciBhc3BlY3RzIHVwZGF0aW5nLlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBXcmFwcGVyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50PFxuICAgIFdyYXBwZXJQcm9wcyxcbiAgICBXcmFwcGVyU3RhdGVcbj4ge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGFzcGVjdHM6IHByb3BzLmFzcGVjdHMgfHwge30sXG4gICAgICAgICAgICByZWFkeTogZmFsc2UsXG4gICAgICAgICAgICBpbml0aWFsOiBmYWxzZSxcbiAgICAgICAgICAgIGVycm9yOiBudWxsLFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLnNldEFzcGVjdHMgPSB0aGlzLnNldEFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5nZXRBc3BlY3QgPSB0aGlzLmdldEFzcGVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMgPSB0aGlzLnVwZGF0ZUFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5tYXRjaEFzcGVjdHMgPSB0aGlzLm1hdGNoQXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHN0YXRpYyBnZXREZXJpdmVkU3RhdGVGcm9tRXJyb3IoZXJyb3IpIHtcbiAgICAgICAgcmV0dXJuIHtlcnJvcn07XG4gICAgfVxuXG4gICAgdXBkYXRlQXNwZWN0cyhhc3BlY3RzKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnNldEFzcGVjdHMoYXNwZWN0cykudGhlbigoKSA9PlxuICAgICAgICAgICAgdGhpcy5wcm9wcy51cGRhdGVBc3BlY3RzKHRoaXMucHJvcHMuaWRlbnRpdHksIGFzcGVjdHMpXG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgc2V0QXNwZWN0cyhhc3BlY3RzKSB7XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZTx2b2lkPigocmVzb2x2ZSkgPT4ge1xuICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgICAgICAgICB7YXNwZWN0czogey4uLnRoaXMuc3RhdGUuYXNwZWN0cywgLi4uYXNwZWN0c319LFxuICAgICAgICAgICAgICAgIHJlc29sdmVcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGdldEFzcGVjdChhc3BlY3QpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuc3RhdGUuYXNwZWN0c1thc3BlY3RdO1xuICAgIH1cblxuICAgIG1hdGNoQXNwZWN0cyhwYXR0ZXJuKSB7XG4gICAgICAgIHJldHVybiBrZXlzKHRoaXMuc3RhdGUuYXNwZWN0cylcbiAgICAgICAgICAgIC5maWx0ZXIoKGspID0+IHBhdHRlcm4udGVzdChrKSlcbiAgICAgICAgICAgIC5tYXAoKGspID0+IFtrLCB0aGlzLnN0YXRlLmFzcGVjdHNba11dKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgLy8gT25seSB1cGRhdGUgdGhlIGNvbXBvbmVudCB3aGVuIG1vdW50ZWQuXG4gICAgICAgIC8vIE90aGVyd2lzZSBnZXRzIGEgcmFjZSBjb25kaXRpb24gd2l0aCB3aWxsVW5tb3VudFxuICAgICAgICB0aGlzLnByb3BzLmNvbm5lY3QoXG4gICAgICAgICAgICB0aGlzLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgdGhpcy5zZXRBc3BlY3RzLFxuICAgICAgICAgICAgdGhpcy5nZXRBc3BlY3QsXG4gICAgICAgICAgICB0aGlzLm1hdGNoQXNwZWN0cyxcbiAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0c1xuICAgICAgICApO1xuICAgICAgICBpZiAoIXRoaXMuc3RhdGUuaW5pdGlhbCkge1xuICAgICAgICAgICAgLy8gTmVlZCB0byBzZXQgYXNwZWN0cyBmaXJzdCwgbm90IHN1cmUgd2h5IGJ1dCBpdFxuICAgICAgICAgICAgLy8gc2V0cyB0aGVtIGZvciB0aGUgaW5pdGlhbCBzdGF0ZXMgYW5kIHRpZXMuXG4gICAgICAgICAgICB0aGlzLnNldEFzcGVjdHModGhpcy5zdGF0ZS5hc3BlY3RzKS50aGVuKCgpID0+XG4gICAgICAgICAgICAgICAgdGhpcy5wcm9wc1xuICAgICAgICAgICAgICAgICAgICAudXBkYXRlQXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMucHJvcHMuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnN0YXRlLmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgICAgICB0cnVlXG4gICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWUsIGluaXRpYWw6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBjb21wb25lbnRXaWxsVW5tb3VudCgpIHtcbiAgICAgICAgdGhpcy5wcm9wcy5kaXNjb25uZWN0KHRoaXMucHJvcHMuaWRlbnRpdHkpO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2NvbXBvbmVudCwgY29tcG9uZW50X25hbWUsIHBhY2thZ2VfbmFtZSwgaWRlbnRpdHl9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgY29uc3Qge2FzcGVjdHMsIHJlYWR5LCBlcnJvcn0gPSB0aGlzLnN0YXRlO1xuICAgICAgICBpZiAoIXJlYWR5KSB7XG4gICAgICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZXJyb3IpIHtcbiAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgPGRpdiBzdHlsZT17e2NvbG9yOiAncmVkJ319PlxuICAgICAgICAgICAgICAgICAgICDimqAgRXJyb3Igd2l0aCB7cGFja2FnZV9uYW1lfS57Y29tcG9uZW50X25hbWV9ICN7aWRlbnRpdHl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICApO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIFJlYWN0LmNsb25lRWxlbWVudChjb21wb25lbnQsIHtcbiAgICAgICAgICAgIC4uLmFzcGVjdHMsXG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzOiB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgIGNsYXNzX25hbWU6IGpvaW4oXG4gICAgICAgICAgICAgICAgJyAnLFxuICAgICAgICAgICAgICAgIGNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgW1xuICAgICAgICAgICAgICAgICAgICAgICAgYCR7cGFja2FnZV9uYW1lXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnJlcGxhY2UoJ18nLCAnLScpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnRvTG93ZXJDYXNlKCl9LSR7Y2FtZWxUb1NwaW5hbChjb21wb25lbnRfbmFtZSl9YCxcbiAgICAgICAgICAgICAgICAgICAgXSxcbiAgICAgICAgICAgICAgICAgICAgYXNwZWN0cy5jbGFzc19uYW1lID8gYXNwZWN0cy5jbGFzc19uYW1lLnNwbGl0KCcgJykgOiBbXVxuICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICksXG4gICAgICAgIH0pO1xuICAgIH1cbn1cbiIsImltcG9ydCB7bWFwLCBvbWl0LCB0b1BhaXJzLCB0eXBlfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFdyYXBwZXIgZnJvbSAnLi9jb21wb25lbnRzL1dyYXBwZXInO1xuaW1wb3J0IHtBbnlEaWN0fSBmcm9tICdjb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7XG4gICAgQ29ubmVjdEZ1bmMsXG4gICAgRGlzY29ubmVjdEZ1bmMsXG4gICAgV3JhcHBlclByb3BzLFxuICAgIFdyYXBwZXJVcGRhdGVBc3BlY3RGdW5jLFxufSBmcm9tICcuL3R5cGVzJztcblxuZXhwb3J0IGZ1bmN0aW9uIGlzQ29tcG9uZW50KGM6IGFueSk6IGJvb2xlYW4ge1xuICAgIHJldHVybiAoXG4gICAgICAgIHR5cGUoYykgPT09ICdPYmplY3QnICYmXG4gICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ3BhY2thZ2UnKSAmJlxuICAgICAgICBjLmhhc093blByb3BlcnR5KCdhc3BlY3RzJykgJiZcbiAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnbmFtZScpICYmXG4gICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ2lkZW50aXR5JylcbiAgICApO1xufVxuXG5mdW5jdGlvbiBoeWRyYXRlUHJvcChcbiAgICB2YWx1ZTogYW55LFxuICAgIHVwZGF0ZUFzcGVjdHM6IFdyYXBwZXJVcGRhdGVBc3BlY3RGdW5jLFxuICAgIGNvbm5lY3Q6IENvbm5lY3RGdW5jLFxuICAgIGRpc2Nvbm5lY3Q6IERpc2Nvbm5lY3RGdW5jLFxuICAgIG9uQ29udGV4dD86IEZ1bmN0aW9uXG4pIHtcbiAgICBpZiAodHlwZSh2YWx1ZSkgPT09ICdBcnJheScpIHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLm1hcCgoZSkgPT4ge1xuICAgICAgICAgICAgaWYgKGlzQ29tcG9uZW50KGUpKSB7XG4gICAgICAgICAgICAgICAgaWYgKCFlLmFzcGVjdHMua2V5KSB7XG4gICAgICAgICAgICAgICAgICAgIGUuYXNwZWN0cy5rZXkgPSBlLmlkZW50aXR5O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBoeWRyYXRlUHJvcChcbiAgICAgICAgICAgICAgICBlLFxuICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgY29ubmVjdCxcbiAgICAgICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgICAgIG9uQ29udGV4dFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG4gICAgfSBlbHNlIGlmIChpc0NvbXBvbmVudCh2YWx1ZSkpIHtcbiAgICAgICAgY29uc3QgbmV3UHJvcHMgPSBoeWRyYXRlUHJvcHMoXG4gICAgICAgICAgICB2YWx1ZS5hc3BlY3RzLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICk7XG4gICAgICAgIHJldHVybiBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgdmFsdWUubmFtZSxcbiAgICAgICAgICAgIHZhbHVlLnBhY2thZ2UsXG4gICAgICAgICAgICB2YWx1ZS5pZGVudGl0eSxcbiAgICAgICAgICAgIG5ld1Byb3BzLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICk7XG4gICAgfSBlbHNlIGlmICh0eXBlKHZhbHVlKSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgcmV0dXJuIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgIHZhbHVlLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICk7XG4gICAgfVxuICAgIHJldHVybiB2YWx1ZTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGh5ZHJhdGVQcm9wcyhcbiAgICBwcm9wczogQW55RGljdCxcbiAgICB1cGRhdGVBc3BlY3RzOiBXcmFwcGVyVXBkYXRlQXNwZWN0RnVuYyxcbiAgICBjb25uZWN0OiBDb25uZWN0RnVuYyxcbiAgICBkaXNjb25uZWN0OiBEaXNjb25uZWN0RnVuYyxcbiAgICBvbkNvbnRleHQ/OiBGdW5jdGlvblxuKSB7XG4gICAgcmV0dXJuIHRvUGFpcnMocHJvcHMpLnJlZHVjZSgoYWNjLCBbYXNwZWN0LCB2YWx1ZV0pID0+IHtcbiAgICAgICAgYWNjW2FzcGVjdF0gPSBoeWRyYXRlUHJvcChcbiAgICAgICAgICAgIHZhbHVlLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICk7XG4gICAgICAgIHJldHVybiBhY2M7XG4gICAgfSwge30pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gaHlkcmF0ZUNvbXBvbmVudChcbiAgICBuYW1lOiBzdHJpbmcsXG4gICAgcGFja2FnZV9uYW1lOiBzdHJpbmcsXG4gICAgaWRlbnRpdHk6IHN0cmluZyxcbiAgICBwcm9wczogQW55RGljdCxcbiAgICB1cGRhdGVBc3BlY3RzOiBXcmFwcGVyVXBkYXRlQXNwZWN0RnVuYyxcbiAgICBjb25uZWN0OiBDb25uZWN0RnVuYyxcbiAgICBkaXNjb25uZWN0OiBEaXNjb25uZWN0RnVuYyxcbiAgICBvbkNvbnRleHQ6IEZ1bmN0aW9uXG4pIHtcbiAgICBjb25zdCBwYWNrID0gd2luZG93W3BhY2thZ2VfbmFtZV07XG4gICAgaWYgKCFwYWNrKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihgSW52YWxpZCBwYWNrYWdlIG5hbWU6ICR7cGFja2FnZV9uYW1lfWApO1xuICAgIH1cbiAgICBjb25zdCBjb21wb25lbnQgPSBwYWNrW25hbWVdO1xuICAgIGlmICghY29tcG9uZW50KSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihgSW52YWxpZCBjb21wb25lbnQgbmFtZTogJHtwYWNrYWdlX25hbWV9LiR7bmFtZX1gKTtcbiAgICB9XG4gICAgLy8gQHRzLWlnbm9yZVxuICAgIGNvbnN0IGVsZW1lbnQgPSBSZWFjdC5jcmVhdGVFbGVtZW50KGNvbXBvbmVudCwgcHJvcHMpO1xuXG4gICAgLyogZXNsaW50LWRpc2FibGUgcmVhY3QvcHJvcC10eXBlcyAqL1xuICAgIGNvbnN0IHdyYXBwZXIgPSAoe2NoaWxkcmVufToge2NoaWxkcmVuPzogYW55fSkgPT4gKFxuICAgICAgICA8V3JhcHBlclxuICAgICAgICAgICAgaWRlbnRpdHk9e2lkZW50aXR5fVxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cz17dXBkYXRlQXNwZWN0c31cbiAgICAgICAgICAgIGNvbXBvbmVudD17ZWxlbWVudH1cbiAgICAgICAgICAgIGNvbm5lY3Q9e2Nvbm5lY3R9XG4gICAgICAgICAgICBwYWNrYWdlX25hbWU9e3BhY2thZ2VfbmFtZX1cbiAgICAgICAgICAgIGNvbXBvbmVudF9uYW1lPXtuYW1lfVxuICAgICAgICAgICAgYXNwZWN0cz17e2NoaWxkcmVuLCAuLi5wcm9wc319XG4gICAgICAgICAgICBkaXNjb25uZWN0PXtkaXNjb25uZWN0fVxuICAgICAgICAgICAga2V5PXtgd3JhcHBlci0ke2lkZW50aXR5fWB9XG4gICAgICAgIC8+XG4gICAgKTtcblxuICAgIGlmIChjb21wb25lbnQuaXNDb250ZXh0KSB7XG4gICAgICAgIG9uQ29udGV4dCh3cmFwcGVyKTtcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIHJldHVybiB3cmFwcGVyKHt9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHByZXBhcmVQcm9wKHByb3A6IGFueSkge1xuICAgIGlmIChSZWFjdC5pc1ZhbGlkRWxlbWVudChwcm9wKSkge1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGNvbnN0IHByb3BzOiBXcmFwcGVyUHJvcHMgPSBwcm9wLnByb3BzO1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgaWRlbnRpdHk6IHByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgYXNwZWN0czogbWFwKFxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wLFxuICAgICAgICAgICAgICAgIG9taXQoXG4gICAgICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgICAgICAgICdpZGVudGl0eScsXG4gICAgICAgICAgICAgICAgICAgICAgICAndXBkYXRlQXNwZWN0cycsXG4gICAgICAgICAgICAgICAgICAgICAgICAnX25hbWUnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ19wYWNrYWdlJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdhc3BlY3RzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdrZXknLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBwcm9wcy5hc3BlY3RzXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgKSxcbiAgICAgICAgICAgIG5hbWU6IHByb3BzLmNvbXBvbmVudF9uYW1lLFxuICAgICAgICAgICAgcGFja2FnZTogcHJvcHMucGFja2FnZV9uYW1lLFxuICAgICAgICB9O1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ0FycmF5Jykge1xuICAgICAgICByZXR1cm4gcHJvcC5tYXAocHJlcGFyZVByb3ApO1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgcmV0dXJuIG1hcChwcmVwYXJlUHJvcCwgcHJvcCk7XG4gICAgfVxuICAgIHJldHVybiBwcm9wO1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IFJlbmRlcmVyIGZyb20gJy4vY29tcG9uZW50cy9SZW5kZXJlcic7XG5pbXBvcnQge1JlbmRlck9wdGlvbnN9IGZyb20gJy4vdHlwZXMnO1xuXG5mdW5jdGlvbiByZW5kZXIoXG4gICAge2Jhc2VVcmwsIHBpbmcsIHBpbmdfaW50ZXJ2YWwsIHJldHJpZXN9OiBSZW5kZXJPcHRpb25zLFxuICAgIGVsZW1lbnQ6IHN0cmluZ1xuKSB7XG4gICAgUmVhY3RET00ucmVuZGVyKFxuICAgICAgICA8UmVuZGVyZXJcbiAgICAgICAgICAgIGJhc2VVcmw9e2Jhc2VVcmx9XG4gICAgICAgICAgICBwaW5nPXtwaW5nfVxuICAgICAgICAgICAgcGluZ19pbnRlcnZhbD17cGluZ19pbnRlcnZhbH1cbiAgICAgICAgICAgIHJldHJpZXM9e3JldHJpZXN9XG4gICAgICAgIC8+LFxuICAgICAgICBlbGVtZW50XG4gICAgKTtcbn1cblxuLy8gQHRzLWlnbm9yZVxuZXhwb3J0IHtSZW5kZXJlciwgcmVuZGVyfTtcbiIsIi8qIGVzbGludC1kaXNhYmxlIG5vLW1hZ2ljLW51bWJlcnMgKi9cblxuaW1wb3J0IHtYaHJSZXF1ZXN0T3B0aW9uc30gZnJvbSAnLi90eXBlcyc7XG5cbmNvbnN0IGpzb25QYXR0ZXJuID0gL2pzb24vaTtcblxuY29uc3QgZGVmYXVsdFhock9wdGlvbnM6IFhoclJlcXVlc3RPcHRpb25zID0ge1xuICAgIG1ldGhvZDogJ0dFVCcsXG4gICAgaGVhZGVyczoge30sXG4gICAgcGF5bG9hZDogJycsXG4gICAganNvbjogdHJ1ZSxcbn07XG5cbmV4cG9ydCBjb25zdCBKU09OSEVBREVSUyA9IHtcbiAgICAnQ29udGVudC1UeXBlJzogJ2FwcGxpY2F0aW9uL2pzb24nLFxufTtcblxuZXhwb3J0IGZ1bmN0aW9uIHhoclJlcXVlc3Q8VD4oXG4gICAgdXJsOiBzdHJpbmcsXG4gICAgb3B0aW9uczogWGhyUmVxdWVzdE9wdGlvbnMgPSBkZWZhdWx0WGhyT3B0aW9uc1xuKSB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlPFQ+KChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgY29uc3Qge21ldGhvZCwgaGVhZGVycywgcGF5bG9hZCwganNvbn0gPSB7XG4gICAgICAgICAgICAuLi5kZWZhdWx0WGhyT3B0aW9ucyxcbiAgICAgICAgICAgIC4uLm9wdGlvbnMsXG4gICAgICAgIH07XG4gICAgICAgIGNvbnN0IHhociA9IG5ldyBYTUxIdHRwUmVxdWVzdCgpO1xuICAgICAgICB4aHIub3BlbihtZXRob2QsIHVybCk7XG4gICAgICAgIGNvbnN0IGhlYWQgPSBqc29uID8gey4uLkpTT05IRUFERVJTLCAuLi5oZWFkZXJzfSA6IGhlYWRlcnM7XG4gICAgICAgIE9iamVjdC5rZXlzKGhlYWQpLmZvckVhY2goKGspID0+IHhoci5zZXRSZXF1ZXN0SGVhZGVyKGssIGhlYWRba10pKTtcbiAgICAgICAgeGhyLm9ucmVhZHlzdGF0ZWNoYW5nZSA9ICgpID0+IHtcbiAgICAgICAgICAgIGlmICh4aHIucmVhZHlTdGF0ZSA9PT0gWE1MSHR0cFJlcXVlc3QuRE9ORSkge1xuICAgICAgICAgICAgICAgIGlmICh4aHIuc3RhdHVzID09PSAyMDApIHtcbiAgICAgICAgICAgICAgICAgICAgbGV0IHJlc3BvbnNlVmFsdWUgPSB4aHIucmVzcG9uc2U7XG4gICAgICAgICAgICAgICAgICAgIGlmIChcbiAgICAgICAgICAgICAgICAgICAgICAgIGpzb25QYXR0ZXJuLnRlc3QoeGhyLmdldFJlc3BvbnNlSGVhZGVyKCdDb250ZW50LVR5cGUnKSlcbiAgICAgICAgICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXNwb25zZVZhbHVlID0gSlNPTi5wYXJzZSh4aHIucmVzcG9uc2VUZXh0KTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICByZXNvbHZlKHJlc3BvbnNlVmFsdWUpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHJlamVjdCh7XG4gICAgICAgICAgICAgICAgICAgICAgICBlcnJvcjogJ1JlcXVlc3RFcnJvcicsXG4gICAgICAgICAgICAgICAgICAgICAgICBtZXNzYWdlOiBgWEhSICR7dXJsfSBGQUlMRUQgLSBTVEFUVVM6ICR7eGhyLnN0YXR1c30gTUVTU0FHRTogJHt4aHIuc3RhdHVzVGV4dH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgc3RhdHVzOiB4aHIuc3RhdHVzLFxuICAgICAgICAgICAgICAgICAgICAgICAgeGhyLFxuICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIHhoci5vbmVycm9yID0gKGVycikgPT4gcmVqZWN0KGVycik7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgeGhyLnNlbmQoanNvbiA/IEpTT04uc3RyaW5naWZ5KHBheWxvYWQpIDogcGF5bG9hZCk7XG4gICAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBhcGlSZXF1ZXN0KGJhc2VVcmw6IHN0cmluZykge1xuICAgIHJldHVybiBmdW5jdGlvbiA8VD4odXJpOiBzdHJpbmcsIG9wdGlvbnM6IFhoclJlcXVlc3RPcHRpb25zID0gdW5kZWZpbmVkKSB7XG4gICAgICAgIGNvbnN0IHVybCA9IGJhc2VVcmwgKyB1cmk7XG4gICAgICAgIG9wdGlvbnMuaGVhZGVycyA9IHsuLi5vcHRpb25zLmhlYWRlcnN9O1xuICAgICAgICByZXR1cm4geGhyUmVxdWVzdDxUPih1cmwsIG9wdGlvbnMpO1xuICAgIH07XG59XG4iLCJpbXBvcnQge2xvYWRDc3MsIGxvYWRTY3JpcHR9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtQYWNrYWdlLCBSZXF1aXJlbWVudH0gZnJvbSAnLi90eXBlcyc7XG5pbXBvcnQge2Ryb3B9IGZyb20gJ3JhbWRhJztcblxuZXhwb3J0IGZ1bmN0aW9uIGxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudDogUmVxdWlyZW1lbnQpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2U8dm9pZD4oKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7dXJsLCBraW5kfSA9IHJlcXVpcmVtZW50O1xuICAgICAgICBsZXQgbWV0aG9kO1xuICAgICAgICBpZiAoa2luZCA9PT0gJ2pzJykge1xuICAgICAgICAgICAgbWV0aG9kID0gbG9hZFNjcmlwdDtcbiAgICAgICAgfSBlbHNlIGlmIChraW5kID09PSAnY3NzJykge1xuICAgICAgICAgICAgbWV0aG9kID0gbG9hZENzcztcbiAgICAgICAgfSBlbHNlIGlmIChraW5kID09PSAnbWFwJykge1xuICAgICAgICAgICAgcmV0dXJuIHJlc29sdmUoKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiByZWplY3QoYEludmFsaWQgcmVxdWlyZW1lbnQga2luZDogJHtraW5kfWApO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBtZXRob2QodXJsKS50aGVuKHJlc29sdmUpLmNhdGNoKHJlamVjdCk7XG4gICAgfSk7XG59XG5cbmZ1bmN0aW9uIGxvYWRPbmVCeU9uZShyZXF1aXJlbWVudHM6IFJlcXVpcmVtZW50W10pIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHtcbiAgICAgICAgY29uc3QgaGFuZGxlID0gKHJlcXMpID0+IHtcbiAgICAgICAgICAgIGlmIChyZXFzLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgIGNvbnN0IHJlcXVpcmVtZW50ID0gcmVxc1swXTtcbiAgICAgICAgICAgICAgICBsb2FkUmVxdWlyZW1lbnQocmVxdWlyZW1lbnQpLnRoZW4oKCkgPT4gaGFuZGxlKGRyb3AoMSwgcmVxcykpKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcmVzb2x2ZShudWxsKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgaGFuZGxlKHJlcXVpcmVtZW50cyk7XG4gICAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2FkUmVxdWlyZW1lbnRzKFxuICAgIHJlcXVpcmVtZW50czogUmVxdWlyZW1lbnRbXSxcbiAgICBwYWNrYWdlczoge1trOiBzdHJpbmddOiBQYWNrYWdlfVxuKSB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlPHZvaWQ+KChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgbGV0IGxvYWRpbmdzID0gW107XG4gICAgICAgIE9iamVjdC5rZXlzKHBhY2thZ2VzKS5mb3JFYWNoKChwYWNrX25hbWUpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHBhY2sgPSBwYWNrYWdlc1twYWNrX25hbWVdO1xuICAgICAgICAgICAgbG9hZGluZ3MgPSBsb2FkaW5ncy5jb25jYXQoXG4gICAgICAgICAgICAgICAgbG9hZE9uZUJ5T25lKHBhY2sucmVxdWlyZW1lbnRzLmZpbHRlcigocikgPT4gci5raW5kID09PSAnanMnKSlcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICBsb2FkaW5ncyA9IGxvYWRpbmdzLmNvbmNhdChcbiAgICAgICAgICAgICAgICBwYWNrLnJlcXVpcmVtZW50c1xuICAgICAgICAgICAgICAgICAgICAuZmlsdGVyKChyKSA9PiByLmtpbmQgPT09ICdjc3MnKVxuICAgICAgICAgICAgICAgICAgICAubWFwKGxvYWRSZXF1aXJlbWVudClcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBUaGVuIGxvYWQgcmVxdWlyZW1lbnRzIHNvIHRoZXkgY2FuIHVzZSBwYWNrYWdlc1xuICAgICAgICAvLyBhbmQgb3ZlcnJpZGUgY3NzLlxuICAgICAgICBQcm9taXNlLmFsbChsb2FkaW5ncylcbiAgICAgICAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICBsZXQgaSA9IDA7XG4gICAgICAgICAgICAgICAgLy8gTG9hZCBpbiBvcmRlci5cbiAgICAgICAgICAgICAgICBjb25zdCBoYW5kbGVyID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICBpZiAoaSA8IHJlcXVpcmVtZW50cy5sZW5ndGgpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudHNbaV0pLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGkrKztcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBoYW5kbGVyKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlc29sdmUoKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgICAgaGFuZGxlcigpO1xuICAgICAgICAgICAgfSlcbiAgICAgICAgICAgIC5jYXRjaChyZWplY3QpO1xuICAgIH0pO1xufVxuIiwiLyogZXNsaW50LWRpc2FibGUgbm8tdXNlLWJlZm9yZS1kZWZpbmUgKi9cbmltcG9ydCB7XG4gICAgY29uY2F0LFxuICAgIGRyb3AsXG4gICAgZXF1YWxzLFxuICAgIGZpbmQsXG4gICAgZnJvbVBhaXJzLFxuICAgIGluY2x1ZGVzLFxuICAgIGlzLFxuICAgIGpvaW4sXG4gICAgbWVyZ2VEZWVwTGVmdCxcbiAgICBtZXJnZURlZXBSaWdodCxcbiAgICBtZXJnZUxlZnQsXG4gICAgbWVyZ2VSaWdodCxcbiAgICBwaWNrLFxuICAgIHBsdWNrLFxuICAgIHJlZHVjZSxcbiAgICByZXBsYWNlLFxuICAgIHJldmVyc2UsXG4gICAgc2xpY2UsXG4gICAgc29ydCxcbiAgICBzcGxpdCxcbiAgICB0YWtlLFxuICAgIHRvUGFpcnMsXG4gICAgdHJpbSxcbiAgICB1bmlxLFxuICAgIHppcCxcbn0gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtUcmFuc2Zvcm0sIFRyYW5zZm9ybUZ1bmMsIFRyYW5zZm9ybUdldEFzcGVjdEZ1bmN9IGZyb20gJy4vdHlwZXMnO1xuaW1wb3J0IHtjb2VyY2VBc3BlY3QsIGlzQXNwZWN0fSBmcm9tICcuL2FzcGVjdHMnO1xuXG5jb25zdCB0cmFuc2Zvcm1zOiB7W2tleTogc3RyaW5nXTogVHJhbnNmb3JtRnVuY30gPSB7XG4gICAgLyogU3RyaW5nIHRyYW5zZm9ybXMgKi9cbiAgICBUb1VwcGVyOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLnRvVXBwZXJDYXNlKCk7XG4gICAgfSxcbiAgICBUb0xvd2VyOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLnRvTG93ZXJDYXNlKCk7XG4gICAgfSxcbiAgICBGb3JtYXQ6ICh2YWx1ZSwgYXJncykgPT4ge1xuICAgICAgICBjb25zdCB7dGVtcGxhdGV9ID0gYXJncztcbiAgICAgICAgaWYgKGlzKFN0cmluZywgdmFsdWUpIHx8IGlzKE51bWJlciwgdmFsdWUpIHx8IGlzKEJvb2xlYW4sIHZhbHVlKSkge1xuICAgICAgICAgICAgcmV0dXJuIHJlcGxhY2UoJyR7dmFsdWV9JywgdmFsdWUsIHRlbXBsYXRlKTtcbiAgICAgICAgfSBlbHNlIGlmIChpcyhPYmplY3QsIHZhbHVlKSkge1xuICAgICAgICAgICAgcmV0dXJuIHJlZHVjZShcbiAgICAgICAgICAgICAgICAoYWNjLCBbaywgdl0pID0+IHJlcGxhY2UoYCRcXHske2t9fWAsIHYsIGFjYyksXG4gICAgICAgICAgICAgICAgdGVtcGxhdGUsXG4gICAgICAgICAgICAgICAgdG9QYWlycyh2YWx1ZSlcbiAgICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlO1xuICAgIH0sXG4gICAgU3BsaXQ6ICh2YWx1ZSwgYXJncykgPT4ge1xuICAgICAgICBjb25zdCB7c2VwYXJhdG9yfSA9IGFyZ3M7XG4gICAgICAgIHJldHVybiBzcGxpdChzZXBhcmF0b3IsIHZhbHVlKTtcbiAgICB9LFxuICAgIFRyaW06ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdHJpbSh2YWx1ZSk7XG4gICAgfSxcbiAgICAvKiBOdW1iZXIgVHJhbnNmb3JtICovXG4gICAgQWRkOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBpZiAoaXMoTnVtYmVyLCBhcmdzLnZhbHVlKSkge1xuICAgICAgICAgICAgcmV0dXJuIHZhbHVlICsgYXJncy52YWx1ZTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdmFsdWUgKyBjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIFN1YjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgaWYgKGlzKE51bWJlciwgYXJncy52YWx1ZSkpIHtcbiAgICAgICAgICAgIHJldHVybiB2YWx1ZSAtIGFyZ3MudmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlIC0gY29lcmNlQXNwZWN0KGFyZ3MudmFsdWUsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBEaXZpZGU6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGlmIChpcyhOdW1iZXIsIGFyZ3MudmFsdWUpKSB7XG4gICAgICAgICAgICByZXR1cm4gdmFsdWUgLyBhcmdzLnZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB2YWx1ZSAvIGNvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgTXVsdGlwbHk6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGlmIChpcyhOdW1iZXIsIGFyZ3MudmFsdWUpKSB7XG4gICAgICAgICAgICByZXR1cm4gdmFsdWUgKiBhcmdzLnZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB2YWx1ZSAqIGNvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgTW9kdWx1czogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgaWYgKGlzKE51bWJlciwgYXJncy52YWx1ZSkpIHtcbiAgICAgICAgICAgIHJldHVybiB2YWx1ZSAlIGFyZ3MudmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlICUgY29lcmNlQXNwZWN0KGFyZ3MudmFsdWUsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBUb1ByZWNpc2lvbjogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZS50b1ByZWNpc2lvbihhcmdzLnByZWNpc2lvbik7XG4gICAgfSxcbiAgICAvKiBBcnJheSB0cmFuc2Zvcm1zICAqL1xuICAgIENvbmNhdDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge290aGVyfSA9IGFyZ3M7XG4gICAgICAgIHJldHVybiBjb25jYXQodmFsdWUsIGNvZXJjZUFzcGVjdChvdGhlciwgZ2V0QXNwZWN0KSk7XG4gICAgfSxcbiAgICBTbGljZTogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIHJldHVybiBzbGljZShhcmdzLnN0YXJ0LCBhcmdzLnN0b3AsIHZhbHVlKTtcbiAgICB9LFxuICAgIE1hcDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge3RyYW5zZm9ybX0gPSBhcmdzO1xuICAgICAgICByZXR1cm4gdmFsdWUubWFwKChlKSA9PlxuICAgICAgICAgICAgZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgICAgICB0cmFuc2Zvcm0udHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgIGUsXG4gICAgICAgICAgICAgICAgdHJhbnNmb3JtLmFyZ3MsXG4gICAgICAgICAgICAgICAgdHJhbnNmb3JtLm5leHQsXG4gICAgICAgICAgICAgICAgZ2V0QXNwZWN0XG4gICAgICAgICAgICApXG4gICAgICAgICk7XG4gICAgfSxcbiAgICBGaWx0ZXI6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtjb21wYXJpc29ufSA9IGFyZ3M7XG4gICAgICAgIHJldHVybiB2YWx1ZS5maWx0ZXIoKGUpID0+XG4gICAgICAgICAgICBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgICAgIGNvbXBhcmlzb24udHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgIGUsXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi5hcmdzLFxuICAgICAgICAgICAgICAgIGNvbXBhcmlzb24ubmV4dCxcbiAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgIClcbiAgICAgICAgKTtcbiAgICB9LFxuICAgIFJlZHVjZTogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge3RyYW5zZm9ybSwgYWNjdW11bGF0b3J9ID0gYXJncztcbiAgICAgICAgY29uc3QgYWNjID0gY29lcmNlQXNwZWN0KGFjY3VtdWxhdG9yLCBnZXRBc3BlY3QpO1xuICAgICAgICByZXR1cm4gdmFsdWUucmVkdWNlKFxuICAgICAgICAgICAgKHByZXZpb3VzLCBuZXh0KSA9PlxuICAgICAgICAgICAgICAgIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgICAgIFtwcmV2aW91cywgbmV4dF0sXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS5hcmdzLFxuICAgICAgICAgICAgICAgICAgICB0cmFuc2Zvcm0ubmV4dCxcbiAgICAgICAgICAgICAgICAgICAgZ2V0QXNwZWN0XG4gICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgIGFjY1xuICAgICAgICApO1xuICAgIH0sXG4gICAgUGx1Y2s6ICh2YWx1ZSwgYXJncykgPT4ge1xuICAgICAgICBjb25zdCB7ZmllbGR9ID0gYXJncztcbiAgICAgICAgcmV0dXJuIHBsdWNrKGZpZWxkLCB2YWx1ZSk7XG4gICAgfSxcbiAgICBBcHBlbmQ6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiBjb25jYXQodmFsdWUsIFtjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KV0pO1xuICAgIH0sXG4gICAgUHJlcGVuZDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIGNvbmNhdChbY29lcmNlQXNwZWN0KGFyZ3MudmFsdWUsIGdldEFzcGVjdCldLCB2YWx1ZSk7XG4gICAgfSxcbiAgICBJbnNlcnQ6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHt0YXJnZXQsIGZyb250fSA9IGFyZ3M7XG4gICAgICAgIGNvbnN0IHQgPSBjb2VyY2VBc3BlY3QodGFyZ2V0LCBnZXRBc3BlY3QpO1xuICAgICAgICByZXR1cm4gZnJvbnQgPyBjb25jYXQoW3ZhbHVlXSwgdCkgOiBjb25jYXQodCwgW3ZhbHVlXSk7XG4gICAgfSxcbiAgICBUYWtlOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7bn0gPSBhcmdzO1xuICAgICAgICByZXR1cm4gdGFrZShjb2VyY2VBc3BlY3QobiwgZ2V0QXNwZWN0KSwgdmFsdWUpO1xuICAgIH0sXG4gICAgTGVuZ3RoOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLmxlbmd0aDtcbiAgICB9LFxuICAgIFJhbmdlOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7c3RhcnQsIGVuZCwgc3RlcH0gPSBhcmdzO1xuICAgICAgICBjb25zdCBzID0gY29lcmNlQXNwZWN0KHN0YXJ0LCBnZXRBc3BlY3QpO1xuICAgICAgICBjb25zdCBlID0gY29lcmNlQXNwZWN0KGVuZCwgZ2V0QXNwZWN0KTtcbiAgICAgICAgbGV0IGkgPSBzO1xuICAgICAgICBjb25zdCBhcnIgPSBbXTtcbiAgICAgICAgd2hpbGUgKGkgPCBlKSB7XG4gICAgICAgICAgICBhcnIucHVzaChpKTtcbiAgICAgICAgICAgIGkgKz0gc3RlcDtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gYXJyO1xuICAgIH0sXG4gICAgSW5jbHVkZXM6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiBpbmNsdWRlcyhjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KSwgdmFsdWUpO1xuICAgIH0sXG4gICAgRmluZDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2NvbXBhcmlzb259ID0gYXJncztcbiAgICAgICAgcmV0dXJuIGZpbmQoKGEpID0+XG4gICAgICAgICAgICBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgICAgIGNvbXBhcmlzb24udHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgIGEsXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi5hcmdzLFxuICAgICAgICAgICAgICAgIGNvbXBhcmlzb24ubmV4dCxcbiAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgIClcbiAgICAgICAgKSh2YWx1ZSk7XG4gICAgfSxcbiAgICBKb2luOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gam9pbihjb2VyY2VBc3BlY3QoYXJncy5zZXBhcmF0b3IsIGdldEFzcGVjdCksIHZhbHVlKTtcbiAgICB9LFxuICAgIFNvcnQ6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHt0cmFuc2Zvcm19ID0gYXJncztcbiAgICAgICAgcmV0dXJuIHNvcnQoXG4gICAgICAgICAgICAoYSwgYikgPT5cbiAgICAgICAgICAgICAgICBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgICAgICAgICB0cmFuc2Zvcm0udHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgICAgICBbYSwgYl0sXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS5hcmdzLFxuICAgICAgICAgICAgICAgICAgICB0cmFuc2Zvcm0ubmV4dCxcbiAgICAgICAgICAgICAgICAgICAgZ2V0QXNwZWN0XG4gICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgIHZhbHVlXG4gICAgICAgICk7XG4gICAgfSxcbiAgICBSZXZlcnNlOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHJldmVyc2UodmFsdWUpO1xuICAgIH0sXG4gICAgVW5pcXVlOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHVuaXEodmFsdWUpO1xuICAgIH0sXG4gICAgWmlwOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gemlwKHZhbHVlLCBjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KSk7XG4gICAgfSxcbiAgICAvKiBPYmplY3QgdHJhbnNmb3JtcyAqL1xuICAgIFBpY2s6ICh2YWx1ZSwgYXJncykgPT4ge1xuICAgICAgICByZXR1cm4gcGljayhhcmdzLmZpZWxkcywgdmFsdWUpO1xuICAgIH0sXG4gICAgR2V0OiAodmFsdWUsIGFyZ3MpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlW2FyZ3MuZmllbGRdO1xuICAgIH0sXG4gICAgU2V0OiAodiwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtrZXksIHZhbHVlfSA9IGFyZ3M7XG4gICAgICAgIHZba2V5XSA9IGNvZXJjZUFzcGVjdCh2YWx1ZSwgZ2V0QXNwZWN0KTtcbiAgICAgICAgcmV0dXJuIHY7XG4gICAgfSxcbiAgICBQdXQ6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtrZXksIHRhcmdldH0gPSBhcmdzO1xuICAgICAgICBjb25zdCBvYmogPSBjb2VyY2VBc3BlY3QodGFyZ2V0LCBnZXRBc3BlY3QpO1xuICAgICAgICBvYmpba2V5XSA9IHZhbHVlO1xuICAgICAgICByZXR1cm4gb2JqO1xuICAgIH0sXG4gICAgTWVyZ2U6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtkZWVwLCBkaXJlY3Rpb24sIG90aGVyfSA9IGFyZ3M7XG4gICAgICAgIGxldCBvdGhlclZhbHVlID0gb3RoZXI7XG4gICAgICAgIGlmIChpc0FzcGVjdChvdGhlcikpIHtcbiAgICAgICAgICAgIG90aGVyVmFsdWUgPSBnZXRBc3BlY3Qob3RoZXIuaWRlbnRpdHksIG90aGVyLmFzcGVjdCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRpcmVjdGlvbiA9PT0gJ3JpZ2h0Jykge1xuICAgICAgICAgICAgaWYgKGRlZXApIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gbWVyZ2VEZWVwUmlnaHQodmFsdWUsIG90aGVyVmFsdWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcmV0dXJuIG1lcmdlUmlnaHQodmFsdWUsIG90aGVyVmFsdWUpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChkZWVwKSB7XG4gICAgICAgICAgICByZXR1cm4gbWVyZ2VEZWVwTGVmdCh2YWx1ZSwgb3RoZXJWYWx1ZSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG1lcmdlTGVmdCh2YWx1ZSwgb3RoZXJWYWx1ZSk7XG4gICAgfSxcbiAgICBUb0pzb246ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gSlNPTi5zdHJpbmdpZnkodmFsdWUpO1xuICAgIH0sXG4gICAgRnJvbUpzb246ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gSlNPTi5wYXJzZSh2YWx1ZSk7XG4gICAgfSxcbiAgICBUb1BhaXJzOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIHRvUGFpcnModmFsdWUpO1xuICAgIH0sXG4gICAgRnJvbVBhaXJzOiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuIGZyb21QYWlycyh2YWx1ZSk7XG4gICAgfSxcbiAgICAvKiBDb25kaXRpb25hbHMgKi9cbiAgICBJZjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2NvbXBhcmlzb24sIHRoZW4sIG90aGVyd2lzZX0gPSBhcmdzO1xuICAgICAgICBjb25zdCBjID0gdHJhbnNmb3Jtc1tjb21wYXJpc29uLnRyYW5zZm9ybV07XG5cbiAgICAgICAgaWYgKGModmFsdWUsIGNvbXBhcmlzb24uYXJncywgZ2V0QXNwZWN0KSkge1xuICAgICAgICAgICAgcmV0dXJuIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgdGhlbi50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgdmFsdWUsXG4gICAgICAgICAgICAgICAgdGhlbi5hcmdzLFxuICAgICAgICAgICAgICAgIHRoZW4ubmV4dCxcbiAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKG90aGVyd2lzZSkge1xuICAgICAgICAgICAgcmV0dXJuIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgb3RoZXJ3aXNlLnRyYW5zZm9ybSxcbiAgICAgICAgICAgICAgICB2YWx1ZSxcbiAgICAgICAgICAgICAgICBvdGhlcndpc2UuYXJncyxcbiAgICAgICAgICAgICAgICBvdGhlcndpc2UubmV4dCxcbiAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlO1xuICAgIH0sXG4gICAgRXF1YWxzOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gZXF1YWxzKHZhbHVlLCBjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KSk7XG4gICAgfSxcbiAgICBOb3RFcXVhbHM6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiAhZXF1YWxzKHZhbHVlLCBjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KSk7XG4gICAgfSxcbiAgICBNYXRjaDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3QgciA9IG5ldyBSZWdFeHAoY29lcmNlQXNwZWN0KGFyZ3Mub3RoZXIsIGdldEFzcGVjdCkpO1xuICAgICAgICByZXR1cm4gci50ZXN0KHZhbHVlKTtcbiAgICB9LFxuICAgIEdyZWF0ZXI6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZSA+IGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgR3JlYXRlck9yRXF1YWxzOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUgPj0gY29lcmNlQXNwZWN0KGFyZ3Mub3RoZXIsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBMZXNzZXI6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZSA8IGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgTGVzc2VyT3JFcXVhbHM6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZSA8PSBjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIEFuZDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlICYmIGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgT3I6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZSB8fCBjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIE5vdDogKHZhbHVlKSA9PiB7XG4gICAgICAgIHJldHVybiAhdmFsdWU7XG4gICAgfSxcbiAgICBSYXdWYWx1ZTogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIHJldHVybiBhcmdzLnZhbHVlO1xuICAgIH0sXG4gICAgQXNwZWN0VmFsdWU6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtpZGVudGl0eSwgYXNwZWN0fSA9IGFyZ3MudGFyZ2V0O1xuICAgICAgICByZXR1cm4gZ2V0QXNwZWN0KGlkZW50aXR5LCBhc3BlY3QpO1xuICAgIH0sXG59O1xuXG5leHBvcnQgY29uc3QgZXhlY3V0ZVRyYW5zZm9ybSA9IChcbiAgICB0cmFuc2Zvcm06IHN0cmluZyxcbiAgICB2YWx1ZTogYW55LFxuICAgIGFyZ3M6IGFueSxcbiAgICBuZXh0OiBBcnJheTxUcmFuc2Zvcm0+LFxuICAgIGdldEFzcGVjdDogVHJhbnNmb3JtR2V0QXNwZWN0RnVuY1xuKSA9PiB7XG4gICAgY29uc3QgdCA9IHRyYW5zZm9ybXNbdHJhbnNmb3JtXTtcbiAgICBjb25zdCBuZXdWYWx1ZSA9IHQodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCk7XG4gICAgaWYgKG5leHQubGVuZ3RoKSB7XG4gICAgICAgIGNvbnN0IG4gPSBuZXh0WzBdO1xuICAgICAgICByZXR1cm4gZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgIG4udHJhbnNmb3JtLFxuICAgICAgICAgICAgbmV3VmFsdWUsXG4gICAgICAgICAgICBuLmFyZ3MsXG4gICAgICAgICAgICAvLyBFeGVjdXRlIHRoZSBuZXh0IGZpcnN0LCB0aGVuIGJhY2sgdG8gY2hhaW4uXG4gICAgICAgICAgICBjb25jYXQobi5uZXh0LCBkcm9wKDEsIG5leHQpKSxcbiAgICAgICAgICAgIGdldEFzcGVjdFxuICAgICAgICApO1xuICAgIH1cbiAgICByZXR1cm4gbmV3VmFsdWU7XG59O1xuXG5leHBvcnQgZGVmYXVsdCB0cmFuc2Zvcm1zO1xuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X2RvbV9fOyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==