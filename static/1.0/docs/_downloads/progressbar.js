// progressbar.js
// requires: mochikit >= 1.3.1
//
// Iterates through all file inputs in all forms in the window
// and adds a progress bar on submit, using tweekgeek's CherryPy
// UploadFilter and a helper TurboGears controller as the  backend.
//
// created by Ian Charnas <icc@case.edu>
// thanks to James Kassemi <james@tweekgeek.com> for UploadFilter
//
// December 5, 2006 - Original


// borrowed from MochiKit 1.4
/** @id MochiKit.DOM.isParent */
var isParent = function(child, element) {
  if (!child.parentNode || child == element) {
    return false;
  }

  if (child.parentNode == element) {
    return true;
  }
  
  return isParent(child.parentNode, element);
}


// borrowed from MochiKit 1.4
/** @id MochiKit.DOM.insertSiblingNodesBefore */
function insertSiblingNodesBefore(node/*, nodes...*/) {
    var elem = node;
    var self = MochiKit.DOM;
    if (typeof(node) == 'string') {
        elem = self.getElement(node);
    }
    var nodeStack = [
        self.coerceToDOM(
            MochiKit.Base.extend(null, arguments, 1),
            elem
        )
    ];
    var parentnode = elem.parentNode;
    var concat = MochiKit.Base.concat;
    while (nodeStack.length) {
        var n = nodeStack.shift();
        if (typeof(n) == 'undefined' || n === null) {
            // pass
        } else if (typeof(n.nodeType) == 'number') {
            parentnode.insertBefore(n, elem);
        } else {
            nodeStack = concat(n, nodeStack);
        }
    }
    return parentnode;
}

// borrowed from MochiKit 1.4
/** @id MochiKit.DOM.insertSiblingNodesAfter */
function insertSiblingNodesAfter(node/*, nodes...*/) {
    var elem = node;
    var self = MochiKit.DOM;

    if (typeof(node) == 'string') {
        elem = self.getElement(node);
    }
    var nodeStack = [
        self.coerceToDOM(
            MochiKit.Base.extend(null, arguments, 1),
            elem
        )
    ];

    if (elem.nextSibling) {
        return insertSiblingNodesBefore(elem.nextSibling, nodeStack);
    }
    else {
        return self.appendChildNodes(elem.parentNode, nodeStack);
    }
}

myObjectRepr = function (elem) {
    // gives a nice, stable string representation for objects,
    // ignoring any methods
    var keyValuePairs = [];
    for (var k in elem) {
        var v = elem[k];
        if (typeof(v) != 'function') {
            keyValuePairs.push([k, v]);
        }
    };
    keyValuePairs.sort(compare);
    return "{" + map(
        function (pair) {
            return map(repr, pair).join(":");
        },
        keyValuePairs
    ).join(", ") + "}";
};

// Styles and updates the progress bar and restarts get_stats()
var show_progress = function(progressbar, results) {
  log(myObjectRepr(results));
  if (results.progressbar_xhtml) {
    progressbar.innerHTML = results.progressbar_xhtml;
  }
  callLater(1, get_stats, progressbar);
};

// Call the 'get_upload_stats' JSON controller method on the server,
// and give the results to show_progress().
var get_stats = function(progressbar) {
  // we need to include this random value in the query string so IE won't cache results.
  var random_number= Math.random()
  var d = loadJSONDoc('/get_upload_stats', {filename: progressbar.filename, junk: random_number});
  d.addCallback(show_progress, progressbar);
};

// Inserts a new <div> right after the file input field, to hold the stats that
// are sent by the 'get_upload_stats' JSON controller method.  Note that
// part of the JSON results are going to contain the XHTML to stick inside this <div>.
function create_progressbar_dom(fileinputfield) {
  var progressbar_dom = DIV({'style':'display:none;'});
  fileinputfield.progressbar = progressbar_dom;
  insertSiblingNodesAfter(fileinputfield, progressbar_dom);
}

// Set css 'display' to 'block' (initially it's 'none');
function show_progressbar(progressbar) {
  setNodeAttribute(progressbar, 'style', 'display: block;');
}

// This is the 'onsubmit' handler for forms with file input fields.
var start_progressbars = function(form, fileinputfields) {
  return function(evt) {
    // for each file input field, show the progressbar DIV and start a poller to update the progress bar.
    for (var i in fileinputfields) {
        progressbar = fileinputfields[i].progressbar;
        progressbar.filename = fileinputfields[i].value;
        show_progressbar(progressbar);
        // for some reason XMLHttpRequests are failing if we try them immediately as the
        // form is submitting, so we add this slight delay of 0.25 seconds:
        callLater(0.25, get_stats, progressbar);
    }
  }
}


// Returns true if field is a file input field.
function is_fileinput(field) {
  inputtype = getNodeAttribute(field, 'type');
  if ( (inputtype == null) || (inputtype != 'file') )
    return false;
  else
    return true;
}

// Initialize form with progress bars
function init_form(form) {
  // Find file input fields in this form
  var allinputfields = getElementsByTagAndClassName("input", null);
  var allfileinputfields = filter(is_fileinput, allinputfields);
  var formfileinputfields = new Array();
  for (var i in allfileinputfields) {
    if (isParent(allfileinputfields[i], form)) {
      formfileinputfields.push(allfileinputfields[i]);
    }
  }

  // If the form has file input fields, add our progress bar code
  // to the 'onsubmit' signal stack for the form, and add the
  // progressbar DOM just below each file input.
  if (formfileinputfields.length > 0) {
    map(create_progressbar_dom, formfileinputfields);
    connect(form, 'onsubmit', start_progressbars(form, formfileinputfields));
  }
}

// Iterate through all forms in the document and initialize progress bars
function init_progressbars() {
  forms = getElementsByTagAndClassName("form", null);
  map(init_form, forms);
}

addLoadEvent(init_progressbars);