"use strict";

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

require("regenerator-runtime/runtime");

var _widgets = require("@lumino/widgets");

var _reactDom = _interopRequireDefault(require("react-dom"));

var _reactRedux = require("react-redux");

var _react = _interopRequireDefault(require("react"));

var _SpanEditor = _interopRequireDefault(require("../containers/SpanEditor"));

var _TableEditor = _interopRequireDefault(require("../containers/TableEditor"));

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

exports.default = MetannoRenderer;
;