(self["webpackChunkmetanno"] = self["webpackChunkmetanno"] || []).push([["lib_jupyter_plugin_js"],{

/***/ "./lib/jupyter/dontDisplayHiddenOutput.js":
/*!************************************************!*\
  !*** ./lib/jupyter/dontDisplayHiddenOutput.ts ***!
  \************************************************/
/***/ (function(__unused_webpack_module, __unused_webpack_exports, __webpack_require__) {

"use strict";


var _outputarea = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");

var _cells = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");

/***/ }),

/***/ "./lib/jupyter/manager.js":
/*!********************************!*\
  !*** ./lib/jupyter/manager.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _redux = __webpack_require__(/*! redux */ "webpack/sharing/consume/default/redux/redux?375d");

var _parse = __webpack_require__(/*! ../parse */ "./lib/parse.js");

var _immer = __webpack_require__(/*! immer */ "webpack/sharing/consume/default/immer/immer");

var _jupyterlab_toastify = __webpack_require__(/*! jupyterlab_toastify */ "webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify");

var _sourcemapCodec = __webpack_require__(/*! sourcemap-codec */ "webpack/sharing/consume/default/sourcemap-codec/sourcemap-codec");

__webpack_require__(/*! ./metanno.css */ "./lib/jupyter/metanno.css");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

(0, _immer.enablePatches)();

var metannoManager = //modelsSync: Map<any>;
function metannoManager(context, settings) {
  var _this = this,
      _context$sessionConte;

  _classCallCheck(this, metannoManager);

  _defineProperty(this, "actions", void 0);

  _defineProperty(this, "app", void 0);

  _defineProperty(this, "store", void 0);

  _defineProperty(this, "views", void 0);

  _defineProperty(this, "context", void 0);

  _defineProperty(this, "isDisposed", void 0);

  _defineProperty(this, "comm_target_name", void 0);

  _defineProperty(this, "settings", void 0);

  _defineProperty(this, "comm", void 0);

  _defineProperty(this, "source_code_py", void 0);

  _defineProperty(this, "sourcemap", void 0);

  _defineProperty(this, "_handleCommOpen", function (comm, msg) {
    // const data = (msg.content.data);
    // hydrate state ?
    _this.comm = comm;
    _this.comm.onMsg = _this.onMsg;

    _this.comm.send({
      "method": "sync_request",
      "data": {}
    });
  });

  _defineProperty(this, "_create_comm", /*#__PURE__*/function () {
    var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(target_name, model_id, data, metadata, buffers) {
      var _this$context$session;

      var kernel, comm;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              kernel = (_this$context$session = _this.context.sessionContext.session) === null || _this$context$session === void 0 ? void 0 : _this$context$session.kernel;

              if (kernel) {
                _context.next = 3;
                break;
              }

              throw new Error('No current kernel');

            case 3:
              comm = kernel.createComm(target_name, model_id);

              if (data || metadata) {
                comm.open(data, metadata, buffers);
              }

              return _context.abrupt("return", comm);

            case 6:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }));

    return function (_x, _x2, _x3, _x4, _x5) {
      return _ref.apply(this, arguments);
    };
  }());

  _defineProperty(this, "_get_comm_info", /*#__PURE__*/_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
    var _this$context$session2;

    var kernel, reply;
    return regeneratorRuntime.wrap(function _callee2$(_context2) {
      while (1) {
        switch (_context2.prev = _context2.next) {
          case 0:
            kernel = (_this$context$session2 = _this.context.sessionContext.session) === null || _this$context$session2 === void 0 ? void 0 : _this$context$session2.kernel;

            if (kernel) {
              _context2.next = 3;
              break;
            }

            throw new Error('No current kernel');

          case 3:
            _context2.next = 5;
            return kernel.requestCommInfo({
              target_name: _this.comm_target_name
            });

          case 5:
            reply = _context2.sent;

            if (!(reply.content.status === 'ok')) {
              _context2.next = 10;
              break;
            }

            return _context2.abrupt("return", reply.content.comms);

          case 10:
            return _context2.abrupt("return", {});

          case 11:
          case "end":
            return _context2.stop();
        }
      }
    }, _callee2);
  })));

  _defineProperty(this, "connectToAnyKernel", /*#__PURE__*/_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
    var all_comm_ids, relevant_comm_ids, comm;
    return regeneratorRuntime.wrap(function _callee3$(_context3) {
      while (1) {
        switch (_context3.prev = _context3.next) {
          case 0:
            if (_this.context.sessionContext) {
              _context3.next = 2;
              break;
            }

            return _context3.abrupt("return");

          case 2:
            _context3.next = 4;
            return _this.context.sessionContext.ready;

          case 4:
            if (!(_this.context.sessionContext.session.kernel.handleComms === false)) {
              _context3.next = 6;
              break;
            }

            return _context3.abrupt("return");

          case 6:
            _context3.next = 8;
            return _this._get_comm_info();

          case 8:
            all_comm_ids = _context3.sent;
            relevant_comm_ids = Object.keys(all_comm_ids).filter(function (key) {
              return all_comm_ids[key]['target_name'] === _this.comm_target_name;
            });
            console.log("Jupyter annotator comm ids", relevant_comm_ids, "(there should be at most one)");

            if (!(relevant_comm_ids.length > 0)) {
              _context3.next = 16;
              break;
            }

            _context3.next = 14;
            return _this._create_comm(_this.comm_target_name, relevant_comm_ids[0]);

          case 14:
            comm = _context3.sent;

            _this._handleCommOpen(comm);

          case 16:
          case "end":
            return _context3.stop();
        }
      }
    }, _callee3);
  })));

  _defineProperty(this, "onMsg", function (msg) {
    try {
      var _ref4 = msg.content.data,
          method = _ref4.method,
          data = _ref4.data;

      if (method === "action") {
        _this.store.dispatch(data);
      } else if (method === "run_method") {
        var _this$app;

        (_this$app = _this.app)[data.method_name].apply(_this$app, _toConsumableArray(data.args));
      } else if (method === "patch") {
        try {
          var newState = (0, _immer.applyPatches)(_this.store.getState(), data.patches);

          _this.store.dispatch({
            'type': 'SET_STATE',
            'payload': newState
          });
        } catch (error) {
          console.error("ERROR DURING PATCHING");
          console.error(error);
        }
      } else if (method === "set_app_code") {
        _this.app = (0, _parse.eval_code)(data.code)();
        _this.sourcemap = (0, _sourcemapCodec.decode)(data.sourcemap);
        _this.source_code_py = data.py_code;
        _this.app.manager = _this;

        _this.views.forEach(function (view) {
          return view.showContent();
        });
      } else if (method === "sync") {
        _this.store.dispatch({
          'type': 'SET_STATE',
          'payload': data.state
        });
      }
    } catch (e) {
      console.error("Error during comm message reception", e);
    }
  });

  _defineProperty(this, "try_catch_exec", function (fn) {
    return function () {
      try {
        if (fn) return fn.apply(void 0, arguments);
      } catch (e) {
        console.log("Got an error !");
        console.log(e);

        var py_lines = _toConsumableArray(e.stack.matchAll(/<anonymous>:(\d+):(\d+)/gm));

        if (py_lines.length > 0 && _this.sourcemap !== null) {
          var _py_lines$ = _slicedToArray(py_lines[0], 3),
              _ = _py_lines$[0],
              lineStr = _py_lines$[1],
              columnStr = _py_lines$[2];

          var source_line_str = _this.source_code_py.split("\n")[_this.sourcemap[parseInt(lineStr) - 1][0][2]].trim();

          _this.toastError("Error: ".concat(e.message, " at \n").concat(source_line_str));
        } else if (e.__args__) {
          _this.toastError("Error: ".concat(e.__args__[0]));
        } else {
          _this.toastError("Error: ".concat(e.message));
        }
      }
    };
  });

  _defineProperty(this, "toastError", function (message) {
    var autoClose = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 10000;

    //INotification.error(`Message: ${e.message} at ${parseInt(lineStr)-1}:${parseInt(columnStr)-1}`);
    _jupyterlab_toastify.INotification.error( /*#__PURE__*/_react.default.createElement("div", null, message.split("\n").map(function (line) {
      return /*#__PURE__*/_react.default.createElement("p", null, line);
    })), {
      autoClose: autoClose
    });
  });

  _defineProperty(this, "toastInfo", function (message) {
    var autoClose = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 10000;

    //INotification.error(`Message: ${e.message} at ${parseInt(lineStr)-1}:${parseInt(columnStr)-1}`);
    _jupyterlab_toastify.INotification.info( /*#__PURE__*/_react.default.createElement("div", null, message.split("\n").map(function (line) {
      return /*#__PURE__*/_react.default.createElement("p", null, line);
    })), {
      autoClose: autoClose
    });
  });

  _defineProperty(this, "_handleKernelChanged", function (_ref5) {
    var name = _ref5.name,
        oldValue = _ref5.oldValue,
        newValue = _ref5.newValue;

    if (oldValue) {
      console.log("Removing comm", oldValue);
      _this.comm = null;
      oldValue.removeCommTarget(_this.comm_target_name, _this._handleCommOpen);
    }

    if (newValue) {
      console.log("Registering comm", newValue);
      newValue.registerCommTarget(_this.comm_target_name, _this._handleCommOpen);
    }
  });

  _defineProperty(this, "_handleKernelStatusChange", function (status) {
    switch (status) {
      case 'autorestarting':
      case 'restarting':
      case 'dead':
        //this.disconnect();
        break;

      default:
    }
  });

  _defineProperty(this, "dispose", function () {
    if (_this.isDisposed) {
      return;
    }

    _this.isDisposed = true; // TODO do something with the comm ?
  });

  _defineProperty(this, "reduce", function () {
    var _this$app2;

    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.type === 'SET_STATE') {
      return action.payload;
    }

    if ((_this$app2 = _this.app) !== null && _this$app2 !== void 0 && _this$app2.reduce) {
      return _this.app.reduce(state, action);
    }

    return state;
  });

  _defineProperty(this, "getState", function () {
    return _this.store.getState();
  });

  _defineProperty(this, "dispatch", function (action) {
    return _this.store.dispatch(action);
  });

  _defineProperty(this, "createStore", function () {
    var composeEnhancers = (typeof window === "undefined" ? "undefined" : _typeof(window)) === 'object' && // @ts-ignore
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ? // @ts-ignore
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({// Specify extension’s options like name, actionsBlacklist, actionsCreators, serialize...
    }) : _redux.compose;
    return (0, _redux.createStore)(_this.reduce, composeEnhancers((0, _redux.applyMiddleware)()));
  });

  this.store = this.createStore();
  this.actions = {};
  this.app = null;
  this.comm_target_name = 'metanno';
  this.context = context;
  this.comm = null;
  this.views = new Set();
  this.source_code_py = '';
  this.sourcemap = null; // this.modelsSync = new Map();
  // this.onUnhandledIOPubMessage = new Signal(this);
  // https://github.com/jupyter-widgets/ipywidgets/commit/5b922f23e54f3906ed9578747474176396203238

  context.sessionContext.kernelChanged.connect(function (sender, args) {
    _this._handleKernelChanged(args);
  });
  context.sessionContext.statusChanged.connect(function (sender, status) {
    _this._handleKernelStatusChange(status);
  });

  if ((_context$sessionConte = context.sessionContext.session) !== null && _context$sessionConte !== void 0 && _context$sessionConte.kernel) {
    var _context$sessionConte2;

    this._handleKernelChanged({
      name: 'kernel',
      oldValue: null,
      newValue: (_context$sessionConte2 = context.sessionContext.session) === null || _context$sessionConte2 === void 0 ? void 0 : _context$sessionConte2.kernel
    });
  }

  this.connectToAnyKernel().then(); //() => {});

  this.settings = settings;
  /*context.saveState.connect((sender, saveState) => {
      if (saveState === 'started' && settings.saveState) {
          this.saveState();
      }
  });*/
};

exports["default"] = metannoManager;

/***/ }),

/***/ "./lib/jupyter/plugin.js":
/*!*******************************!*\
  !*** ./lib/jupyter/plugin.js ***!
  \*******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = exports.contextToMetannoManagerRegistry = exports.MetannoArea = void 0;
exports.registerMetannoManager = registerMetannoManager;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _manager = _interopRequireDefault(__webpack_require__(/*! ./manager */ "./lib/jupyter/manager.js"));

var _renderer = _interopRequireDefault(__webpack_require__(/*! ./renderer */ "./lib/jupyter/renderer.js"));

var _services = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");

var _disposable = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");

var _docmanager = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");

var _mainmenu = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");

var _logconsole = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");

var _rendermime = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");

var _apputils = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");

var _notebook = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");

var _settingregistry = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");

var _uiComponents = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");

var _algorithm = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");

var _properties = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties");

__webpack_require__(/*! ./dontDisplayHiddenOutput */ "./lib/jupyter/dontDisplayHiddenOutput.js");

var _widgets = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");

var _coreutils = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } else if (call !== void 0) { throw new TypeError("Derived constructors may only return object or undefined"); } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var _marked = /*#__PURE__*/regeneratorRuntime.mark(getEditorsFromNotebook),
    _marked2 = /*#__PURE__*/regeneratorRuntime.mark(chain),
    _marked3 = /*#__PURE__*/regeneratorRuntime.mark(getLinkedEditorsFromApp);

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var OUTPUT_AREA_OUTPUT_CLASS = 'jp-OutputArea-output';
var MIMETYPE = 'application/vnd.jupyter.annotator+json';
var contextToMetannoManagerRegistry = new _properties.AttachedProperty({
  name: 'widgetManager',
  create: function create() {
    return undefined;
  }
});
exports.contextToMetannoManagerRegistry = contextToMetannoManagerRegistry;
var SETTINGS = {
  saveState: false
};
/**
 * Iterate through all widget renderers in a notebook.
 */

function getEditorsFromNotebook(notebook) {
  var _iterator, _step, cell, _iterator2, _step2, codecell, _iterator3, _step3, output;

  return regeneratorRuntime.wrap(function getEditorsFromNotebook$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          // @ts-ignore
          _iterator = _createForOfIteratorHelper(notebook.widgets);
          _context.prev = 1;

          _iterator.s();

        case 3:
          if ((_step = _iterator.n()).done) {
            _context.next = 41;
            break;
          }

          cell = _step.value;

          if (!(cell.model.type === 'code')) {
            _context.next = 39;
            break;
          }

          _iterator2 = _createForOfIteratorHelper(cell.outputArea.widgets);
          _context.prev = 7;

          _iterator2.s();

        case 9:
          if ((_step2 = _iterator2.n()).done) {
            _context.next = 31;
            break;
          }

          codecell = _step2.value;
          _iterator3 = _createForOfIteratorHelper((0, _algorithm.toArray)(codecell.children()));
          _context.prev = 12;

          _iterator3.s();

        case 14:
          if ((_step3 = _iterator3.n()).done) {
            _context.next = 21;
            break;
          }

          output = _step3.value;

          if (!(output instanceof _renderer.default)) {
            _context.next = 19;
            break;
          }

          _context.next = 19;
          return output;

        case 19:
          _context.next = 14;
          break;

        case 21:
          _context.next = 26;
          break;

        case 23:
          _context.prev = 23;
          _context.t0 = _context["catch"](12);

          _iterator3.e(_context.t0);

        case 26:
          _context.prev = 26;

          _iterator3.f();

          return _context.finish(26);

        case 29:
          _context.next = 9;
          break;

        case 31:
          _context.next = 36;
          break;

        case 33:
          _context.prev = 33;
          _context.t1 = _context["catch"](7);

          _iterator2.e(_context.t1);

        case 36:
          _context.prev = 36;

          _iterator2.f();

          return _context.finish(36);

        case 39:
          _context.next = 3;
          break;

        case 41:
          _context.next = 46;
          break;

        case 43:
          _context.prev = 43;
          _context.t2 = _context["catch"](1);

          _iterator.e(_context.t2);

        case 46:
          _context.prev = 46;

          _iterator.f();

          return _context.finish(46);

        case 49:
        case "end":
          return _context.stop();
      }
    }
  }, _marked, null, [[1, 43, 46, 49], [7, 33, 36, 39], [12, 23, 26, 29]]);
}

function chain() {
  var _len,
      args,
      _key,
      _i,
      _args2,
      it,
      _args3 = arguments;

  return regeneratorRuntime.wrap(function chain$(_context2) {
    while (1) {
      switch (_context2.prev = _context2.next) {
        case 0:
          for (_len = _args3.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = _args3[_key];
          }

          _i = 0, _args2 = args;

        case 2:
          if (!(_i < _args2.length)) {
            _context2.next = 8;
            break;
          }

          it = _args2[_i];
          return _context2.delegateYield(it, "t0", 5);

        case 5:
          _i++;
          _context2.next = 2;
          break;

        case 8:
        case "end":
          return _context2.stop();
      }
    }
  }, _marked2);
}
/**
 * Iterate through all matching linked output views
 */


function getLinkedEditorsFromApp(jupyterApp, path) {
  var linkedViews, _iterator4, _step4, view, _iterator5, _step5, outputs, _iterator6, _step6, output;

  return regeneratorRuntime.wrap(function getLinkedEditorsFromApp$(_context3) {
    while (1) {
      switch (_context3.prev = _context3.next) {
        case 0:
          linkedViews = (0, _algorithm.filter)(jupyterApp.shell.widgets("main"), // @ts-ignore
          function (w) {
            return w.id.startsWith('LinkedOutputView-') && w.path === path;
          });
          _iterator4 = _createForOfIteratorHelper((0, _algorithm.toArray)(linkedViews));
          _context3.prev = 2;

          _iterator4.s();

        case 4:
          if ((_step4 = _iterator4.n()).done) {
            _context3.next = 41;
            break;
          }

          view = _step4.value;
          _iterator5 = _createForOfIteratorHelper((0, _algorithm.toArray)(view.children()));
          _context3.prev = 7;

          _iterator5.s();

        case 9:
          if ((_step5 = _iterator5.n()).done) {
            _context3.next = 31;
            break;
          }

          outputs = _step5.value;
          _iterator6 = _createForOfIteratorHelper((0, _algorithm.toArray)(outputs.children()));
          _context3.prev = 12;

          _iterator6.s();

        case 14:
          if ((_step6 = _iterator6.n()).done) {
            _context3.next = 21;
            break;
          }

          output = _step6.value;

          if (!(output instanceof _renderer.default)) {
            _context3.next = 19;
            break;
          }

          _context3.next = 19;
          return output;

        case 19:
          _context3.next = 14;
          break;

        case 21:
          _context3.next = 26;
          break;

        case 23:
          _context3.prev = 23;
          _context3.t0 = _context3["catch"](12);

          _iterator6.e(_context3.t0);

        case 26:
          _context3.prev = 26;

          _iterator6.f();

          return _context3.finish(26);

        case 29:
          _context3.next = 9;
          break;

        case 31:
          _context3.next = 36;
          break;

        case 33:
          _context3.prev = 33;
          _context3.t1 = _context3["catch"](7);

          _iterator5.e(_context3.t1);

        case 36:
          _context3.prev = 36;

          _iterator5.f();

          return _context3.finish(36);

        case 39:
          _context3.next = 4;
          break;

        case 41:
          _context3.next = 46;
          break;

        case 43:
          _context3.prev = 43;
          _context3.t2 = _context3["catch"](2);

          _iterator4.e(_context3.t2);

        case 46:
          _context3.prev = 46;

          _iterator4.f();

          return _context3.finish(46);

        case 49:
        case "end":
          return _context3.stop();
      }
    }
  }, _marked3, null, [[2, 43, 46, 49], [7, 33, 36, 39], [12, 23, 26, 29]]);
}
/**
 * A widget hosting a metanno area.
 */


var MetannoArea = /*#__PURE__*/function (_Panel) {
  _inherits(MetannoArea, _Panel);

  var _super = _createSuper(MetannoArea);

  function MetannoArea(options) {
    var _this;

    _classCallCheck(this, MetannoArea);

    _this = _super.call(this);

    _defineProperty(_assertThisInitialized(_this), "_notebook", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_id", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_type", void 0);

    _defineProperty(_assertThisInitialized(_this), "_path", void 0);

    _defineProperty(_assertThisInitialized(_this), "_cell", null);

    _this._notebook = options.notebook;
    _this._editor_id = options.editor_id;
    _this._editor_type = options.editor_type;
    _this._cell = options.cell || null;

    if (!_this._editor_id || !_this._editor_type) {
      var widget = _this._cell.outputArea.widgets[0].widgets[1];
      _this._editor_id = widget.editor_id;
      _this._editor_type = widget.editor_type;
    }

    _this.id = "MetannoArea-".concat(_coreutils.UUID.uuid4());
    _this.title.label = options.editor_id;
    _this.title.icon = _uiComponents.notebookIcon;
    _this.title.caption = _this._notebook.title.label ? "For Notebook: ".concat(_this._notebook.title.label || '') : '';

    _this.addClass('jp-LinkedOutputView'); // Wait for the notebook to be loaded before
    // cloning the output area.


    void _this._notebook.context.ready.then(function () {
      if (!(_this._editor_id && _this._editor_type)) {
        _this.dispose();

        return;
      }

      _this.addWidget(new _renderer.default({
        editor_id: _this._editor_id,
        editor_type: _this._editor_type
      }, contextToMetannoManagerRegistry.get(_this._notebook.context)));
    });
    return _this;
  }

  _createClass(MetannoArea, [{
    key: "editor_id",
    get: function get() {
      return this._editor_id;
    }
  }, {
    key: "editor_type",
    get: function get() {
      return this._editor_type;
    }
  }, {
    key: "path",
    get: function get() {
      var _this$_notebook, _this$_notebook$conte;

      return this === null || this === void 0 ? void 0 : (_this$_notebook = this._notebook) === null || _this$_notebook === void 0 ? void 0 : (_this$_notebook$conte = _this$_notebook.context) === null || _this$_notebook$conte === void 0 ? void 0 : _this$_notebook$conte._path;
    }
  }]);

  return MetannoArea;
}(_widgets.Panel);
/*
Here we add the singleton MetannoManager to the given editor (context)
 */


exports.MetannoArea = MetannoArea;

function registerMetannoManager(context, rendermime, renderers) {
  var wManager = contextToMetannoManagerRegistry.get(context);

  if (!wManager) {
    wManager = new _manager.default(context, SETTINGS);
    contextToMetannoManagerRegistry.set(context, wManager);
  }

  var _iterator7 = _createForOfIteratorHelper(renderers),
      _step7;

  try {
    for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
      var r = _step7.value;
      r.manager = wManager;
    } // Replace the placeholder widget renderer with one bound to this widget
    // manager.

  } catch (err) {
    _iterator7.e(err);
  } finally {
    _iterator7.f();
  }

  rendermime.removeMimeType(MIMETYPE);
  rendermime.addFactory({
    safe: true,
    mimeTypes: [MIMETYPE],
    createRenderer: function createRenderer(options) {
      return new _renderer.default(options, wManager);
    }
  }, 0);
  return new _disposable.DisposableDelegate(function () {
    if (rendermime) {
      rendermime.removeMimeType(MIMETYPE);
    }

    wManager.dispose();
  });
}
/*
Activate the extension:
-
 */


function activateMetannoExtension(app, rendermime, docManager, notebookTracker, settingRegistry, menu, loggerRegistry, restorer //palette: ICommandPalette,
) {
  var commands = app.commands,
      shell = app.shell,
      contextMenu = app.contextMenu;
  var metannoAreas = new _apputils.WidgetTracker({
    namespace: 'metanno-areas'
  });

  if (restorer) {
    restorer.restore(metannoAreas, {
      command: 'metanno:create-view',
      args: function args(widget) {
        return {
          editor_id: widget.content.editor_id,
          editor_type: widget.content.editor_type,
          path: widget.content.path
        };
      },
      name: function name(widget) {
        return "".concat(widget.content.path, ":").concat(widget.content.editor_type, ":").concat(widget.content.editor_id);
      },
      when: notebookTracker.restored // After the notebook widgets (but not contents).

    });
  }

  var bindUnhandledIOPubMessageSignal = function bindUnhandledIOPubMessageSignal(nb) {
    if (!loggerRegistry) {
      return;
    }

    var wManager = contextToMetannoManagerRegistry[nb.context]; // Don't know what it is

    if (wManager) {
      wManager.onUnhandledIOPubMessage.connect(function (sender, msg) {
        var logger = loggerRegistry.getLogger(nb.context.path);
        var level = 'warning';

        if (_services.KernelMessage.isErrorMsg(msg) || _services.KernelMessage.isStreamMsg(msg) && msg.content.name === 'stderr') {
          level = 'error';
        }

        var data = _objectSpread(_objectSpread({}, msg.content), {}, {
          output_type: msg.header.msg_type
        });

        logger.rendermime = nb.content.rendermime;
        logger.log({
          type: 'output',
          data: data,
          level: level
        });
      });
    }
  }; // Some settings stuff, haven't used it yet


  if (settingRegistry !== null) {
    settingRegistry.load(plugin.id).then(function (settings) {
      settings.changed.connect(updateSettings);
      updateSettings(settings);
    }).catch(function (reason) {
      console.error(reason.message);
    });
  } // Sets the renderer everytime we see our special SpanComponent/TableEditor mimetype


  rendermime.addFactory({
    safe: false,
    mimeTypes: [MIMETYPE],
    // @ts-ignore
    createRenderer: function createRenderer(options) {
      new _renderer.default(options, null);
    }
  }, 0); // Adds the singleton MetannoManager to all existing editors in the labapp/notebook

  if (notebookTracker !== null) {
    notebookTracker.forEach(function (panel) {
      registerMetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
      getEditorsFromNotebook(panel.content), getLinkedEditorsFromApp(app, panel.sessionContext.path)));
      bindUnhandledIOPubMessageSignal(panel);
    });
    notebookTracker.widgetAdded.connect(function (sender, panel) {
      registerMetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
      getEditorsFromNotebook(panel.content), getLinkedEditorsFromApp(app, panel.sessionContext.path)));
      bindUnhandledIOPubMessageSignal(panel);
    });
  } // -----------------
  // Add some commands
  // -----------------


  if (settingRegistry !== null) {
    // Add a command for automatically saving metanno state.
    commands.addCommand('metanno:saveAnnotatorState', {
      label: 'Save Annotator State Automatically',
      execute: function execute() {
        return settingRegistry.set(plugin.id, 'saveState', !SETTINGS.saveState).catch(function (reason) {
          console.error("Failed to set ".concat(plugin.id, ": ").concat(reason.message));
        });
      },
      isToggled: function isToggled() {
        return SETTINGS.saveState;
      }
    });
  }

  if (menu) {
    menu.settingsMenu.addGroup([{
      command: 'metanno:saveAnnotatorState'
    }]);
  }
  /**
   * Whether there is an active notebook.
   */


  function isEnabled() {
    // : boolean
    return notebookTracker.currentWidget !== null && notebookTracker.currentWidget === shell.currentWidget;
  }
  /**
   * Whether there is an notebook active, with a single selected cell.
   */


  function isEnabledAndSingleSelected() {
    // :boolean
    if (!isEnabled()) {
      return false;
    }

    var content = notebookTracker.currentWidget.content;
    var index = content.activeCellIndex; // If there are selections that are not the active cell,
    // this command is confusing, so disable it.

    for (var i = 0; i < content.widgets.length; ++i) {
      if (content.isSelected(content.widgets[i]) && i !== index) {
        return false;
      }
    }

    return true;
  } // CodeCell context menu groups


  contextMenu.addItem({
    command: 'metanno:create-view',
    selector: '.jp-Notebook .jp-CodeCell',
    rank: 10.5
  });
  commands.addCommand('metanno:create-view', {
    label: 'Detach',
    execute: function () {
      var _execute = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(args) {
        var cell, current, editor_id, editor_type, path, content, widget;
        return regeneratorRuntime.wrap(function _callee$(_context4) {
          while (1) {
            switch (_context4.prev = _context4.next) {
              case 0:
                // If we are given a notebook path and cell index, then
                // use that, otherwise use the current active cell.
                editor_id = args.editor_id;
                editor_type = args.editor_type;
                path = args.path;

                if (!(editor_id && editor_type && path)) {
                  _context4.next = 9;
                  break;
                }

                current = docManager.findWidget(path, 'Notebook');

                if (current) {
                  _context4.next = 7;
                  break;
                }

                return _context4.abrupt("return");

              case 7:
                _context4.next = 13;
                break;

              case 9:
                current = notebookTracker.currentWidget;

                if (current) {
                  _context4.next = 12;
                  break;
                }

                return _context4.abrupt("return");

              case 12:
                cell = current.content.activeCell;

              case 13:
                // Create a MainAreaWidget
                content = new MetannoArea({
                  notebook: current,
                  cell: cell,
                  editor_id: editor_id,
                  editor_type: editor_type
                });
                widget = new _apputils.MainAreaWidget({
                  content: content
                });
                current.context.addSibling(widget, {
                  ref: current.id,
                  mode: 'split-bottom'
                }); // Add the cloned output to the output widget tracker.

                void metannoAreas.add(widget);
                void metannoAreas.save(widget); // Remove the output view if the parent notebook is closed.

                current.content.disposed.connect(function () {
                  widget.dispose();
                });

              case 19:
              case "end":
                return _context4.stop();
            }
          }
        }, _callee);
      }));

      function execute(_x) {
        return _execute.apply(this, arguments);
      }

      return execute;
    }(),
    isEnabled: isEnabledAndSingleSelected
  });
}

function updateSettings(settings) {
  SETTINGS.saveState = !!settings.get('saveState').composite;
}

var plugin = {
  id: 'metanno:plugin',
  requires: [_rendermime.IRenderMimeRegistry, _docmanager.IDocumentManager],
  optional: [_notebook.INotebookTracker, _settingregistry.ISettingRegistry, _mainmenu.IMainMenu, _logconsole.ILoggerRegistry //ICommandPalette
  ],
  activate: activateMetannoExtension,
  autoStart: true
};
var _default = plugin;
exports["default"] = _default;

/***/ }),

/***/ "./lib/jupyter/renderer.js":
/*!*********************************!*\
  !*** ./lib/jupyter/renderer.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _widgets = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");

var _reactDom = _interopRequireDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));

var _reactRedux = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _SpanEditor = _interopRequireDefault(__webpack_require__(/*! ../containers/SpanEditor */ "./lib/containers/SpanEditor/index.js"));

var _TableEditor = _interopRequireDefault(__webpack_require__(/*! ../containers/TableEditor */ "./lib/containers/TableEditor/index.js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _get(target, property, receiver) { if (typeof Reflect !== "undefined" && Reflect.get) { _get = Reflect.get; } else { _get = function _get(target, property, receiver) { var base = _superPropBase(target, property); if (!base) return; var desc = Object.getOwnPropertyDescriptor(base, property); if (desc.get) { return desc.get.call(receiver); } return desc.value; }; } return _get(target, property, receiver || target); }

function _superPropBase(object, property) { while (!Object.prototype.hasOwnProperty.call(object, property)) { object = _getPrototypeOf(object); if (object === null) break; } return object; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } else if (call !== void 0) { throw new TypeError("Derived constructors may only return object or undefined"); } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/**
 * A renderer for widgets.
 */
var MetannoRenderer = /*#__PURE__*/function (_Widget) {
  _inherits(MetannoRenderer, _Widget);

  var _super = _createSuper(MetannoRenderer);

  function MetannoRenderer(options, manager) {
    var _this;

    _classCallCheck(this, MetannoRenderer);

    _this = _super.call(this);

    _defineProperty(_assertThisInitialized(_this), "_mimeType", void 0);

    _defineProperty(_assertThisInitialized(_this), "_manager", void 0);

    _defineProperty(_assertThisInitialized(_this), "setManager", void 0);

    _defineProperty(_assertThisInitialized(_this), "_rerenderMimeModel", void 0);

    _defineProperty(_assertThisInitialized(_this), "model", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_id", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_type", void 0);

    _this._mimeType = options.mimeType;
    _this._editor_id = options.editor_id;
    _this._editor_type = options.editor_type;

    if (manager) {
      _this._manager = Promise.resolve(manager);
    } else {
      _this._manager = new Promise(function (resolve, reject) {
        _this.setManager = resolve;
      });
    }

    _this._rerenderMimeModel = null;
    _this.model = null; // Widget will either show up "immediately", ie as soon as the manager is ready,
    // or this method will return prematurely (no editor_id/editor_type/model) and will
    // wait for the mimetype manager to assign a model to this widget and call renderModel
    // on its own (which will call showContent)

    _this.showContent();

    return _this;
  }

  _createClass(MetannoRenderer, [{
    key: "editor_id",
    get: function get() {
      if (!this._editor_id) {
        var source = this.model.data[this._mimeType];
        this._editor_id = source['editor-id'];
      }

      return this._editor_id;
    }
  }, {
    key: "editor_type",
    get: function get() {
      if (!this._editor_type) {
        var source = this.model.data[this._mimeType];
        this._editor_type = source['editor-type'];
      }

      return this._editor_type;
    }
    /**
     * The widget manager.
     */

  }, {
    key: "manager",
    set: function set(value) {
      value.restored.connect(this._rerender, this);
      this.setManager(value);
    }
  }, {
    key: "setFlag",
    value: function setFlag(flag) {
      var wasVisible = this.isVisible;

      _get(_getPrototypeOf(MetannoRenderer.prototype), "setFlag", this).call(this, flag);

      if (this.isVisible && !wasVisible) {
        this.showContent();
      } else if (!this.isVisible && wasVisible) {
        this.hideContent();
      }
    }
  }, {
    key: "clearFlag",
    value: function clearFlag(flag) {
      var wasVisible = this.isVisible;

      _get(_getPrototypeOf(MetannoRenderer.prototype), "clearFlag", this).call(this, flag);

      if (this.isVisible && !wasVisible) {
        this.showContent();
      } else if (!this.isVisible && wasVisible) {
        this.hideContent();
      }
    }
  }, {
    key: "renderModel",
    value: function () {
      var _renderModel = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(model) {
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                this.model = model;
                _context.next = 3;
                return this.showContent();

              case 3:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, this);
      }));

      function renderModel(_x) {
        return _renderModel.apply(this, arguments);
      }

      return renderModel;
    }()
  }, {
    key: "hideContent",
    value: function () {
      var _hideContent = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
        var _this2 = this;

        return regeneratorRuntime.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                if (!this.isVisible) {
                  _reactDom.default.unmountComponentAtNode(this.node);

                  this._manager.then(function (manager) {
                    return manager.views.delete(_this2);
                  });
                }

              case 1:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2, this);
      }));

      function hideContent() {
        return _hideContent.apply(this, arguments);
      }

      return hideContent;
    }()
  }, {
    key: "showContent",
    value: function () {
      var _showContent = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
        var editor_id, editor_type, source, manager;
        return regeneratorRuntime.wrap(function _callee3$(_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                if (this.isVisible) {
                  _context3.next = 2;
                  break;
                }

                return _context3.abrupt("return");

              case 2:
                editor_id = this._editor_id;
                editor_type = this._editor_type;

                if (!(!editor_id || !editor_type)) {
                  _context3.next = 12;
                  break;
                }

                if (!this.model) {
                  _context3.next = 11;
                  break;
                }

                source = this.model.data[this._mimeType];
                editor_id = source['editor-id'];
                editor_type = source['editor-type'];
                _context3.next = 12;
                break;

              case 11:
                return _context3.abrupt("return");

              case 12:
                // Let's be optimistic, and hope the widget state will come later.
                this.node.textContent = 'Loading widget...' + editor_id;
                _context3.next = 15;
                return this._manager;

              case 15:
                manager = _context3.sent;
                manager.views.add(this);

                try {
                  _reactDom.default.unmountComponentAtNode(this.node);
                } catch (e) {}

                if (editor_type === "span-editor") {
                  _reactDom.default.render( /*#__PURE__*/_react.default.createElement(_reactRedux.Provider, {
                    store: manager.store
                  }, /*#__PURE__*/_react.default.createElement(_SpanEditor.default, {
                    id: editor_id,
                    onClickSpan: function onClickSpan() {
                      var _manager$app;

                      for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
                        args[_key] = arguments[_key];
                      }

                      return manager.try_catch_exec((_manager$app = manager.app) === null || _manager$app === void 0 ? void 0 : _manager$app.handle_click_span).apply(void 0, [editor_id].concat(args));
                    },
                    onEnterSpan: function onEnterSpan() {
                      var _manager$app2;

                      for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
                        args[_key2] = arguments[_key2];
                      }

                      return manager.try_catch_exec((_manager$app2 = manager.app) === null || _manager$app2 === void 0 ? void 0 : _manager$app2.handle_enter_span).apply(void 0, [editor_id].concat(args));
                    },
                    onLeaveSpan: function onLeaveSpan() {
                      var _manager$app3;

                      for (var _len3 = arguments.length, args = new Array(_len3), _key3 = 0; _key3 < _len3; _key3++) {
                        args[_key3] = arguments[_key3];
                      }

                      return manager.try_catch_exec((_manager$app3 = manager.app) === null || _manager$app3 === void 0 ? void 0 : _manager$app3.handle_leave_span).apply(void 0, [editor_id].concat(args));
                    },
                    onKeyPress: function onKeyPress() {
                      var _manager$app4;

                      for (var _len4 = arguments.length, args = new Array(_len4), _key4 = 0; _key4 < _len4; _key4++) {
                        args[_key4] = arguments[_key4];
                      }

                      return manager.try_catch_exec((_manager$app4 = manager.app) === null || _manager$app4 === void 0 ? void 0 : _manager$app4.handle_key_press).apply(void 0, [editor_id].concat(args));
                    } //onKeyDown={(...args) => manager.try_catch_exec(manager.app?.handle_key_down)(editor_id, ...args)}
                    ,
                    onMouseSelect: function onMouseSelect() {
                      var _manager$app5;

                      for (var _len5 = arguments.length, args = new Array(_len5), _key5 = 0; _key5 < _len5; _key5++) {
                        args[_key5] = arguments[_key5];
                      }

                      return manager.try_catch_exec((_manager$app5 = manager.app) === null || _manager$app5 === void 0 ? void 0 : _manager$app5.handle_mouse_select).apply(void 0, [editor_id].concat(args));
                    },
                    onButtonPress: function onButtonPress() {
                      var _manager$app6;

                      for (var _len6 = arguments.length, args = new Array(_len6), _key6 = 0; _key6 < _len6; _key6++) {
                        args[_key6] = arguments[_key6];
                      }

                      return manager.try_catch_exec((_manager$app6 = manager.app) === null || _manager$app6 === void 0 ? void 0 : _manager$app6.handle_button_press).apply(void 0, [editor_id].concat(args));
                    },
                    registerActions: function registerActions(methods) {
                      manager.actions[editor_id] = methods;
                    },
                    selectEditorState: function selectEditorState() {
                      var _manager$app7;

                      return manager.try_catch_exec((_manager$app7 = manager.app) === null || _manager$app7 === void 0 ? void 0 : _manager$app7.select_editor_state).apply(void 0, arguments);
                    }
                  })), this.node);
                } else if (editor_type === "table-editor") {
                  _reactDom.default.render( /*#__PURE__*/_react.default.createElement(_reactRedux.Provider, {
                    store: manager.store
                  }, /*#__PURE__*/_react.default.createElement(_TableEditor.default, {
                    id: editor_id,
                    onKeyPress: function onKeyPress() {
                      var _manager$app8;

                      for (var _len7 = arguments.length, args = new Array(_len7), _key7 = 0; _key7 < _len7; _key7++) {
                        args[_key7] = arguments[_key7];
                      }

                      return manager.try_catch_exec((_manager$app8 = manager.app) === null || _manager$app8 === void 0 ? void 0 : _manager$app8.handle_key_press).apply(void 0, [editor_id].concat(args));
                    },
                    onClickCellContent: function onClickCellContent() {
                      var _manager$app9;

                      for (var _len8 = arguments.length, args = new Array(_len8), _key8 = 0; _key8 < _len8; _key8++) {
                        args[_key8] = arguments[_key8];
                      }

                      return manager.try_catch_exec((_manager$app9 = manager.app) === null || _manager$app9 === void 0 ? void 0 : _manager$app9.handle_click_cell_content).apply(void 0, [editor_id].concat(args));
                    },
                    onSelectedCellChange: function onSelectedCellChange() {
                      var _manager$app10;

                      for (var _len9 = arguments.length, args = new Array(_len9), _key9 = 0; _key9 < _len9; _key9++) {
                        args[_key9] = arguments[_key9];
                      }

                      return manager.try_catch_exec((_manager$app10 = manager.app) === null || _manager$app10 === void 0 ? void 0 : _manager$app10.handle_select_cell).apply(void 0, [editor_id].concat(args));
                    },
                    onSelectedRowsChange: function onSelectedRowsChange() {
                      var _manager$app11;

                      for (var _len10 = arguments.length, args = new Array(_len10), _key10 = 0; _key10 < _len10; _key10++) {
                        args[_key10] = arguments[_key10];
                      }

                      return manager.try_catch_exec((_manager$app11 = manager.app) === null || _manager$app11 === void 0 ? void 0 : _manager$app11.handle_select_rows).apply(void 0, [editor_id].concat(args));
                    },
                    onCellChange: function onCellChange() {
                      var _manager$app12;

                      for (var _len11 = arguments.length, args = new Array(_len11), _key11 = 0; _key11 < _len11; _key11++) {
                        args[_key11] = arguments[_key11];
                      }

                      return manager.try_catch_exec((_manager$app12 = manager.app) === null || _manager$app12 === void 0 ? void 0 : _manager$app12.handle_cell_change).apply(void 0, [editor_id].concat(args));
                    },
                    registerActions: function registerActions(methods) {
                      manager.actions[editor_id] = methods;
                    },
                    selectEditorState: function selectEditorState() {
                      var _manager$app13;

                      return manager.try_catch_exec((_manager$app13 = manager.app) === null || _manager$app13 === void 0 ? void 0 : _manager$app13.select_editor_state).apply(void 0, arguments);
                    },
                    onButtonPress: function onButtonPress() {
                      var _manager$app14;

                      for (var _len12 = arguments.length, args = new Array(_len12), _key12 = 0; _key12 < _len12; _key12++) {
                        args[_key12] = arguments[_key12];
                      }

                      return manager.try_catch_exec((_manager$app14 = manager.app) === null || _manager$app14 === void 0 ? void 0 : _manager$app14.handle_button_press).apply(void 0, [editor_id].concat(args));
                    }
                  })), this.node);
                }
                /*let wModel;
                try {
                    // Presume we have a DOMWidgetModel. Should we check for sure?
                    wModel = (await manager.get_model(source.model_id));
                } catch (err) {
                    if (manager.restoredStatus) {
                        // The manager has been restored, so this error won't be going away.
                        this.node.textContent = 'Error displaying widget: model not found';
                        this.addClass('jupyter-widgets');
                        console.error(err);
                        return;
                    }
                     // Store the model for a possible rerender
                    this._rerenderMimeModel = model;
                    return;
                }
                 // Successful getting the model, so we don't need to try to rerender.
                this._rerenderMimeModel = null;
                 let widget;
                try {
                    widget = (await manager.create_view(wModel)).pWidget;
                } catch (err) {
                    this.node.textContent = 'Error displaying widget';
                    this.addClass('jupyter-widgets');
                    console.error(err);
                    return;
                }
                 // When the widget is disposed, hide this container and make sure we
                // change the output model to reflect the view was closed.
                widget.disposed.connect(() => {
                    this.hide();
                    source.model_id = '';
                });*/


              case 19:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3, this);
      }));

      function showContent() {
        return _showContent.apply(this, arguments);
      }

      return showContent;
    }()
    /**
     * Get whether the manager is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    // @ts-ignore

  }, {
    key: "isDisposed",
    get: function get() {
      return this._manager === null;
    }
    /**
     * Dispose the resources held by the manager.
     */

  }, {
    key: "dispose",
    value: function dispose() {
      if (this.isDisposed) {
        return;
      }

      _get(_getPrototypeOf(MetannoRenderer.prototype), "dispose", this).call(this);

      this._manager = null;
    }
  }, {
    key: "_rerender",
    value: function _rerender() {
      if (this._rerenderMimeModel) {
        // Clear the error message
        this.node.textContent = '';
        this.removeClass('jupyter-widgets'); // Attempt to rerender.

        this.renderModel(this._rerenderMimeModel).then();
      }
    }
    /**
     * The mimetype being rendered.
     */

  }]);

  return MetannoRenderer;
}(_widgets.Widget);

exports["default"] = MetannoRenderer;
;

/***/ }),

/***/ "./lib/parse.js":
/*!**********************!*\
  !*** ./lib/parse.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.eval_code = eval_code;

var _immer = __webpack_require__(/*! immer */ "webpack/sharing/consume/default/immer/immer");

var _widgets = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");

var _require = __webpack_require__(/*! ./org.transcrypt.__runtime__.js */ "./lib/org.transcrypt.__runtime__.js"),
    AssertionError = _require.AssertionError,
    AttributeError = _require.AttributeError,
    BaseException = _require.BaseException,
    DeprecationWarning = _require.DeprecationWarning,
    Exception = _require.Exception,
    IndexError = _require.IndexError,
    IterableError = _require.IterableError,
    KeyError = _require.KeyError,
    NotImplementedError = _require.NotImplementedError,
    RuntimeWarning = _require.RuntimeWarning,
    StopIteration = _require.StopIteration,
    UserWarning = _require.UserWarning,
    ValueError = _require.ValueError,
    Warning = _require.Warning,
    __JsIterator__ = _require.__JsIterator__,
    __PyIterator__ = _require.__PyIterator__,
    __Terminal__ = _require.__Terminal__,
    __add__ = _require.__add__,
    __and__ = _require.__and__,
    __call__ = _require.__call__,
    __class__ = _require.__class__,
    __envir__ = _require.__envir__,
    __eq__ = _require.__eq__,
    __floordiv__ = _require.__floordiv__,
    __ge__ = _require.__ge__,
    __get__ = _require.__get__,
    __getcm__ = _require.__getcm__,
    __getitem__ = _require.__getitem__,
    __getslice__ = _require.__getslice__,
    __getsm__ = _require.__getsm__,
    __gt__ = _require.__gt__,
    __i__ = _require.__i__,
    __iadd__ = _require.__iadd__,
    __iand__ = _require.__iand__,
    __idiv__ = _require.__idiv__,
    __ijsmod__ = _require.__ijsmod__,
    __ilshift__ = _require.__ilshift__,
    __imatmul__ = _require.__imatmul__,
    __imod__ = _require.__imod__,
    __imul__ = _require.__imul__,
    __in__ = _require.__in__,
    __init__ = _require.__init__,
    __ior__ = _require.__ior__,
    __ipow__ = _require.__ipow__,
    __irshift__ = _require.__irshift__,
    __isub__ = _require.__isub__,
    __ixor__ = _require.__ixor__,
    __jsUsePyNext__ = _require.__jsUsePyNext__,
    __jsmod__ = _require.__jsmod__,
    __k__ = _require.__k__,
    __kwargtrans__ = _require.__kwargtrans__,
    __le__ = _require.__le__,
    __lshift__ = _require.__lshift__,
    __lt__ = _require.__lt__,
    __matmul__ = _require.__matmul__,
    __mergefields__ = _require.__mergefields__,
    __mergekwargtrans__ = _require.__mergekwargtrans__,
    __mod__ = _require.__mod__,
    __mul__ = _require.__mul__,
    __ne__ = _require.__ne__,
    __neg__ = _require.__neg__,
    __nest__ = _require.__nest__,
    __or__ = _require.__or__,
    __pow__ = _require.__pow__,
    __pragma__ = _require.__pragma__,
    __proxy__ = _require.__proxy__,
    __pyUseJsNext__ = _require.__pyUseJsNext__,
    __rshift__ = _require.__rshift__,
    __setitem__ = _require.__setitem__,
    __setproperty__ = _require.__setproperty__,
    __setslice__ = _require.__setslice__,
    __sort__ = _require.__sort__,
    __specialattrib__ = _require.__specialattrib__,
    __sub__ = _require.__sub__,
    __super__ = _require.__super__,
    __t__ = _require.__t__,
    __terminal__ = _require.__terminal__,
    __truediv__ = _require.__truediv__,
    __withblock__ = _require.__withblock__,
    __xor__ = _require.__xor__,
    abs = _require.abs,
    all = _require.all,
    any = _require.any,
    assert = _require.assert,
    bool = _require.bool,
    bytearray = _require.bytearray,
    bytes = _require.bytes,
    callable = _require.callable,
    chr = _require.chr,
    copy = _require.copy,
    deepcopy = _require.deepcopy,
    delattr = _require.delattr,
    dict = _require.dict,
    dir = _require.dir,
    divmod = _require.divmod,
    enumerate = _require.enumerate,
    filter = _require.filter,
    float = _require.float,
    getattr = _require.getattr,
    hasattr = _require.hasattr,
    input = _require.input,
    int = _require.int,
    isinstance = _require.isinstance,
    issubclass = _require.issubclass,
    len = _require.len,
    list = _require.list,
    map = _require.map,
    max = _require.max,
    min = _require.min,
    object = _require.object,
    ord = _require.ord,
    pow = _require.pow,
    print = _require.print,
    property = _require.property,
    py_TypeError = _require.py_TypeError,
    py_iter = _require.py_iter,
    py_metatype = _require.py_metatype,
    py_next = _require.py_next,
    py_reversed = _require.py_reversed,
    py_typeof = _require.py_typeof,
    range = _require.range,
    repr = _require.repr,
    round = _require.round,
    set = _require.set,
    setattr = _require.setattr,
    sorted = _require.sorted,
    str = _require.str,
    sum = _require.sum,
    tuple = _require.tuple,
    zip = _require.zip;

var chain_map = function chain_map() {
  for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
    args[_key] = arguments[_key];
  }

  return Object.assign.apply(Object, [{}].concat(args));
};

var chain_list = function chain_list() {
  for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
    args[_key2] = arguments[_key2];
  }

  return [].concat.apply([], args);
};

var kernel_only = function kernel_only(fn) {
  var func_name = fn();
  return function (self) {
    for (var _len3 = arguments.length, args = new Array(_len3 > 1 ? _len3 - 1 : 0), _key3 = 1; _key3 < _len3; _key3++) {
      args[_key3 - 1] = arguments[_key3];
    }

    self.manager.comm.send({
      'method': 'run_method',
      'data': {
        'method_name': func_name,
        'args': args
      }
    });
  };
};

var frontend_only = function frontend_only(fn) {
  fn.frontend_only = true;
  return fn;
};

var produce = function produce(fn) {
  var new_fn = function new_fn(self) {
    for (var _len4 = arguments.length, args = new Array(_len4 > 1 ? _len4 - 1 : 0), _key4 = 1; _key4 < _len4; _key4++) {
      args[_key4 - 1] = arguments[_key4];
    }

    var recordedPatches = [];
    var newState = (0, _immer.produce)(self.manager.store.getState(), function (draft) {
      self.state = draft;
      fn.apply(void 0, [self].concat(args));
    }, function (patches, inversePatches) {
      return recordedPatches = patches;
    });
    self.manager.store.dispatch({
      type: 'SET_STATE',
      payload: newState
    });
    if (new_fn.frontend_only || fn.frontend_only) return;
    self.manager.comm.send({
      'method': 'patch',
      'data': {
        'patches': recordedPatches
      }
    });
    delete self.state;
  };

  return new_fn;
};

var make_uid = function make_uid() {
  for (var _len5 = arguments.length, args = new Array(_len5), _key5 = 0; _key5 < _len5; _key5++) {
    args[_key5] = arguments[_key5];
  }

  return args.map(String).join("-");
};

function eval_code(code) {
  return eval(code);
}

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css":
/*!***********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css ***!
  \***********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".jp-toastContainer .Toastify__toast-body {\n    display: flex;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/jupyter/metanno.css":
/*!*********************************!*\
  !*** ./lib/jupyter/metanno.css ***!
  \*********************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../node_modules/css-loader/dist/cjs.js!./metanno.css */ "./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ })

}]);
//# sourceMappingURL=lib_jupyter_plugin_js.a452f887cc827ec74cf3.js.map