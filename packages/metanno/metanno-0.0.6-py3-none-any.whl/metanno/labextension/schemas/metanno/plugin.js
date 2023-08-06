"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.contextTometannoManagerRegistry = void 0;
exports.registermetannoManager = registermetannoManager;

require("regenerator-runtime/runtime");

var _manager = _interopRequireDefault(require("./manager"));

var _renderer = _interopRequireDefault(require("./renderer"));

var _services = require("@jupyterlab/services");

var _disposable = require("@lumino/disposable");

var _mainmenu = require("@jupyterlab/mainmenu");

var _logconsole = require("@jupyterlab/logconsole");

var _rendermime = require("@jupyterlab/rendermime");

var _notebook = require("@jupyterlab/notebook");

var _settingregistry = require("@jupyterlab/settingregistry");

var _algorithm = require("@lumino/algorithm");

var _properties = require("@lumino/properties");

require("./dontDisplayHiddenOutput");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var _marked = /*#__PURE__*/regeneratorRuntime.mark(getEditorsFromNotebook),
    _marked2 = /*#__PURE__*/regeneratorRuntime.mark(chain),
    _marked3 = /*#__PURE__*/regeneratorRuntime.mark(getLinkedEditorsFromApp);

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var MIMETYPE = 'application/vnd.jupyter.annotator+json';
var contextTometannoManagerRegistry = new _properties.AttachedProperty({
  name: 'widgetManager',
  create: function create() {
    return undefined;
  }
});
exports.contextTometannoManagerRegistry = contextTometannoManagerRegistry;
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
/*
Here we add the singleton metannoManager to the given editor (context)
 */


function registermetannoManager(context, rendermime, renderers) {
  var wManager = contextTometannoManagerRegistry.get(context);

  if (!wManager) {
    wManager = new _manager.default(context, SETTINGS);
    contextTometannoManagerRegistry.set(context, wManager);
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


function activatemetannoExtension(app, rendermime, tracker, settingRegistry, menu, loggerRegistry //palette: ICommandPalette,
) {
  var commands = app.commands,
      shell = app.shell,
      contextMenu = app.contextMenu;

  var bindUnhandledIOPubMessageSignal = function bindUnhandledIOPubMessageSignal(nb) {
    if (!loggerRegistry) {
      return;
    }

    var wManager = contextTometannoManagerRegistry[nb.context]; // Don't know what it is

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
  }, 0); // Adds the singleton metannoManager to all existing editors in the labapp/notebook

  if (tracker !== null) {
    tracker.forEach(function (panel) {
      registermetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
      getEditorsFromNotebook(panel.content), getLinkedEditorsFromApp(app, panel.sessionContext.path)));
      bindUnhandledIOPubMessageSignal(panel);
    });
    tracker.widgetAdded.connect(function (sender, panel) {
      registermetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
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
    return tracker.currentWidget !== null && tracker.currentWidget === shell.currentWidget;
  }
  /**
   * Whether there is an notebook active, with a single selected cell.
   */


  function isEnabledAndSingleSelected() {
    // :boolean
    if (!isEnabled()) {
      return false;
    }

    var content = tracker.currentWidget.content;
    var index = content.activeCellIndex; // If there are selections that are not the active cell,
    // this command is confusing, so disable it.

    for (var i = 0; i < content.widgets.length; ++i) {
      if (content.isSelected(content.widgets[i]) && i !== index) {
        return false;
      }
    }

    return true;
  }

  commands.addCommand('metanno:detachOutput', {
    label: 'Detach Output',
    execute: function () {
      var _execute = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(args) {
        return regeneratorRuntime.wrap(function _callee$(_context4) {
          while (1) {
            switch (_context4.prev = _context4.next) {
              case 0:
                _context4.next = 2;
                return Promise.all([commands.execute("notebook:create-output-view", args), commands.execute("notebook:hide-cell-outputs", args)]);

              case 2:
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
  }); // CodeCell context menu groups

  contextMenu.addItem({
    command: 'metanno:detachOutput',
    selector: '.jp-Notebook .jp-CodeCell',
    rank: 10.5
  });
}

function updateSettings(settings) {
  SETTINGS.saveState = !!settings.get('saveState').composite;
}

var plugin = {
  id: 'metanno:plugin',
  requires: [_rendermime.IRenderMimeRegistry],
  optional: [_notebook.INotebookTracker, _settingregistry.ISettingRegistry, _mainmenu.IMainMenu, _logconsole.ILoggerRegistry //ICommandPalette
  ],
  activate: activatemetannoExtension,
  autoStart: true
};
var _default = plugin;
exports.default = _default;