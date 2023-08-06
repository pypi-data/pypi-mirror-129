"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("regenerator-runtime/runtime");

var _react = _interopRequireDefault(require("react"));

var _redux = require("redux");

var _parse = require("../parse");

var _immer = require("immer");

var _jupyterlab_toastify = require("jupyterlab_toastify");

var _sourcemapCodec = require("sourcemap-codec");

require("./metanno.css");

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

exports.default = metannoManager;