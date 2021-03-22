
var urlbase = null

function escapeAll(str) {
    var r =  encodeURI(escapeHash(str))
    return r
}

function escapeHash(str) {
    var r = str.replace(/#/g,"_");
    return r
}

function reject_split(id) {
    $("#card"+id).addClass("d-none")
}

function parse_split(id) {
    split = $("#header"+id).text()
    url = urlbase + "sanskrit_parser/v1/parse-presegmented/" + split
    var btn = $(this);
    var btxt = btn.text();
    btn.removeClass("btn-primary").addClass("btn-secondary");
    btn.text("Loading ...");
    $("#issueButton").addClass("d-none");
    $.getJSON(url, function (result) {
	var s = JSON.stringify(result);
        $("#sgraph"+id).removeClass("d-none");
	$("#sgraph"+id).attr("data-graph", escapeAll(result.split_dot))
        $("#jsonbox").text(s);
        $("#jsonButton").removeClass("d-none");
        $("#issueButton").removeClass("d-none");
        btn.removeClass("btn-secondary").addClass("btn-primary");
        btn.text(btxt);
	var h = "<h5>Sabdabodha Interpretations</h5>"
	if (result.analysis.length == 0) {
	     h = "<p>No sabdabodha Interpretations</p>"
	}
	h += "<ol class=\"list-group\">";
	result.analysis.forEach(function(aitem, index) {
            h += "<li class=\"list-group-item\"><table class=\"table table-striped\">";
	    h += "<button type=\"button\" class=\"btn btn-light alignright\" data-toggle=\"modal\" data-target=\"#graphModal\"\ data-graph=\"" +escapeAll(result.parse_dots[index]) +  "\" data-title=\"Sabdabodha Parse Graph\">View As Graph</button><div style=\"clear: both;\"></div></div>";
            h += "<thead><th scope=\"col\">Word</th><th scope=\"col\">Tags</th><th scope=\"col\">Role</th><th scope=\"col\">Linked To</th></thead><tbody>";
	    aitem.graph.forEach(function(gitem) {
		console.log(gitem)
		if ('node' in gitem) {
		    h += "<tr><th scope=\"row\">" + gitem.node.pada + "</th><td>";
		    h += gitem.node.root + " - " + gitem.node.tags + "</td><td>";
		    h += gitem.sambandha + "</td><td>";
		    h += gitem.predecessor.pada + "</td></tr>";
		} else {
		    h += "<tr><th scope=\"row\">" + gitem.pada + "</th><td>";
		    h += gitem.root + " - " + gitem.tags + "</td><td>";
		    h += "" + "</td><td>";
		    h += "" + "</td></tr>";
		}
	    })
            h += "</tbody></table></li>";
	})
	h += "</ol>";
	$("#collapse"+id).html(h);
	$("#collapse"+id).addClass("show");
    })
 }

function createSplitPanel(heading, urlbase, id) {
    "use strict;"
    // var cardClass = id % 2 ? "bg-secondary" : "bg-primary";
    var cardClass =  "border-dark mb-3";
    var expanded = id === 0 ? "show" : "";
    var h = "<div  id=\"card" + id + "\" class=\"text-dark\" class=\"card " + cardClass + " \"><div class=\"card-header text-dark\">";
    h += "<a class=\"text-dark\" id=\"header" + id + "\" data-toggle=\"collapse\" href=\"#collapse" + id + "\" aria-expanded=\"false\" aria-controls=\"collapse" + id + "\">";
    h += heading + "</a>";
    h += "<button type=\"button\" id=\"reject" + id + "\" class=\"btn btn-primary alignright\" onclick=\"reject_split(" + id + ")\" >Reject</button>"
    h += "<button type=\"button\" id=\"analyze" + id + "\" class=\"btn btn-primary alignright\" onclick=\"parse_split(" + id + ")\" >Sabdabodha</button>"
    h += "<button type=\"button\" id=\"sgraph" + id + "\" class=\"d-none btn btn-primary alignright\" data-toggle=\"modal\" data-target=\"#graphModal\" data-title=\"Possible Sabdabodha Relationships\">Full Graph</button>";
    h += "<div style=\"clear: both;\"></div></div>";
    h += "<div id=\"collapse" + id + "\" class=\"collapse" +  "\"><div id=\"body" + id + "\"class=\"card-block\">";
    h += "Please click on Reject to remove, or Sabdabodha to see the interpretations of this vakya"
    h += "</div></div></div>";
    return h;
}

function createPanel(heading, row, dot, urlbase, id) {
    "use strict;"
    var cardClass = id % 2 ? "bg-secondary" : "bg-primary";
    var expanded = id === 0 ? "show" : "";
    var h = "<div class=\"card " + cardClass + " \"><div class=\"card-header " + cardClass + "\">";
    h += "<a class=\"text-white\" data-toggle=\"collapse\" href=\"#collapse" + id + "\" aria-expanded=\"false\" aria-controls=\"collapse" + id + "\">";
    h += heading + "</a>";
/*    h += heading + "</a><p class=\"alignright\"> <a target=\"_blank\" class=\"text-white\" href=\""; */
/*    h += urlbase + "static/" + imgbase + ".dot.png\">(View Graph)</a></p><div style=\"clear: both;\"></div></div>"; */
/*    h += urlbase + "sanskrit_parser/v1/graph/" + imgbase + "\">(View Graph)</a></p><div style=\"clear: both;\"></div></div>"; */
/*    h += encodeURI("https://image-charts.com/chart?cht=gv:dot&chl=" + dot["split"]) + "\">(View Graph)</a></p><div style=\"clear: both;\"></div></div>"; */
    h += "<button type=\"button\" class=\"btn btn-primary alignright\" data-toggle=\"modal\" data-target=\"#graphModal\" data-graph=\"" +  escapeAll(dot["split"]) + "\" data-title=\"Sandhi Graph\">View Graph</button><div style=\"clear: both;\"></div></div>";
    h += "<div id=\"collapse" + id + "\" class=\"collapse " + expanded + "\"><div class=\"card-block\">";
    h += "<ol class=\"list-group\">";
    row.forEach(function (sitem, index) {
        h += "<li class=\"list-group-item\"><table class=\"table table-striped\">";
//	h += "<p class=\"alignright\"> <a target=\"_blank\" href=\"";
//	h += urlbase + "static/" + imgbase + "_parse" + index + ".dot.png\">(View Parse Graph)</a></p><div style=\"clear: both;\"></div>"
//	h += encodeURI("https://image-charts.com/chart?cht=gv:dot&chl=" + dot[index]) + "\">(View Parse Graph)</a></p><div style=\"clear: both;\"></div>"
	h += "<button type=\"button\" class=\"btn btn-light alignright\" data-toggle=\"modal\" data-target=\"#graphModal\"\ data-graph=\"" +escapeAll(dot[index]) +  "\" data-title=\"Parse Graph\">View Parse Graph</button><div style=\"clear: both;\"></div></div>";
        h += "<thead><th scope=\"col\">Word</th><th scope=\"col\">Possible Interpretations</th><th scope=\"col\">Role</th><th scope=\"col\">Linked To</th></thead><tbody>";
        sitem.forEach(function (item) {
            h += "<tr><th scope=\"row\">" + item[0] + "</th><td>";
            h += item[1][0] + " - " + item[1][1] + "</td><td>";
            h += item[2] + "</td><td>";
            h += item[3] + "</td></tr>";
        });
        h += "</tbody></table></li>";
    });
    h += "</ol>";
    h += "</div></div></div>";
    return h;
}

// write small plugin for keypress enter detection
$.fn.enterKey = function (fnc) {
    "use strict;"
    return this.each(function () {
        $(this).keypress(function (e) {
            var keycode = (e.keyCode ? e.keyCode : e.which);
            if (keycode === 13) {
                fnc.call(this, e);
            }
        });
    });
};

$('#graphModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var graph = button.data('graph') // Extract info from data-* attributes
    var title = button.data('title')
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text(title)
    modal.find('img').attr("src", "https://image-charts.com/chart?cht=gv:dot&chl=" + graph)
    modal.modal('handleUpdate')
})

$(document).ready( function () {
    "use strict;"
    urlbase = $.query.get("api_url_base") !== ""? $.query.get("api_url_base") : "https://sanskrit-parser.appspot.com/";
    var vurl = urlbase + "sanskrit_parser/v1/version/"
    // Get library version and change message to connected
    var heartbeat = null
    $.getJSON(vurl, function (result) {
		 $("#statusmsg").html("Library version: " + result.version + "&nbsp;")
		 $("#status").text("Connected")
		 $("#status").attr("class", "text-success")
    })
    $(window).focus(function() {
	 heartbeat = setInterval(function () {
	     $("#status").text("Disconnected")
	     $("#status").attr("class", "text-danger")
 	     $.getJSON(vurl, function (result) {
		 $("#statusmsg").html("Library version: " + result.version + "&nbsp;")
		 $("#status").text("Connected")
		 $("#status").attr("class", "text-success")
    })}, 300000);
    }).blur(function() {
	clearInterval(heartbeat);
    });

    $(window).focus();
    $("[name='vakyaRadio']").on("change", function () {
	var radioValue = $("input[name='vakyaRadio']:checked").val();
	if (radioValue == "vakya") {
	    $("#SplitCheck").attr("disabled", null)
	} else {
	    $("#SplitCheck").attr("disabled", true)
	}
    })
    $("#goButton").on("click", function () {
        var txt = $("#inputText").val();
        //var urlbase = $.query.get("api_url_base") !== ""? $.query.get("api_url_base") : "https://sanskrit-parser.appspot.com/";
        var option = {};
        var tsel = null // $("#analysisType").val();
        if (!txt) {
            alert("Please enter input text");
            return;
        }
        option.Tags = "sanskrit_parser/v1/tags/";
        option.Split = "sanskrit_parser/v1/splits/";
        option.Analyze = "sanskrit_parser/v1/analyses/";
        var btn = $(this);
        var btxt = btn.text();
        btn.removeClass("btn-primary").addClass("btn-secondary");
        btn.text("Loading ...");
        $("#issueButton").addClass("d-none");
	var radioValue = $("input[name='vakyaRadio']:checked").val();
	var needSplit = $("#SplitCheck").is(':checked');
        var url = urlbase +  "sanskrit_parser/v1/" // urlbase + option[tsel] + txt;
	if (radioValue == "vakya") {
	    if (needSplit) {
		url = url + "splits/" + txt
	    } else {
		url = url + "presegmented/" + txt
	    }
	    tsel = "Sandhi"
	    $.getJSON(url, function (result) {
		var panelID;
		var keys;
		var s = JSON.stringify(result);
		$("#devinp").text(result.devanagari);
		$("#jsonbox").text(s);
		$("#restable").html("");
		var restable = "";
		panelID = 0;
                if (needSplit) {
		    $("#reshead").text("Possible Sandhi Splits");
		} else {
		    $("#reshead").text("");
		}
		splits = result.splits
		// Sort by size
		splits.sort(function (a, b) {
		    return a.length > b.length;
                });
		splits.forEach(function (res) {
		    var item = res.join(" ");
		    restable += createSplitPanel(item, urlbase, panelID);
		    panelID += 1;
                });
		$("#restable").append(restable);
		$("#jsonButton").removeClass("d-none");
		$("#devtab").removeClass("d-none");
		$("#restab").removeClass("d-none");
		$("#issueButton").removeClass("d-none");
		btn.removeClass("btn-secondary").addClass("btn-primary");
		btn.text(btxt);
            });
	} else {
	    url = url + "tags/" + txt
	    tsel = "Tags"
	    $.getJSON(url, function (result) {
		var panelID;
		var keys;
		var s = JSON.stringify(result);
		$("#devinp").text(result.devanagari);
		$("#jsonbox").text(s);
		$("#restable").html("");
		var restable = "";
                if (result.tags.length > 0) {
                    $("#reshead").text("Tags");
                } else {
                    $("#reshead").text("No Tags Found");
                }
                restable += "<table class=\"table table-striped\">";
                result.tags.forEach(function (res) {
                    var item = res[0];
                    var itags = res[1];
                    restable += "<tr><th scope=\"row\">" + item + "</th><td>" + itags + "</td></tr>";
                });
                restable += "</table>";
		$("#restable").append(restable);
		$("#jsonButton").removeClass("d-none");
		$("#devtab").removeClass("d-none");
		$("#restab").removeClass("d-none");
		$("#issueButton").removeClass("d-none");
		btn.removeClass("btn-secondary").addClass("btn-primary");
		btn.text(btxt);
            });
	}
    });

    $("#issueButtonButton").on("click", function () {
        var txt = $("#inputText").val();
        var tsel = $("#analysisType").val();
        var str = "mailto:kmadathil@gmail.com?subject=Sanskrit Parser Issue&body=" + txt + "_" + tsel;
        str = str + "%0D%0A--- Please enter your issue below ---%0D%0A + ";
        window.open(str);
        $("#gmailLink").removeClass("d-none");
    });

    $("#gmailLink").on("click", function () {
        window.open("https://blog.hubspot.com/marketing/set-gmail-as-browser-default-email-client-ht");
        $(this).addClass("d-none");
    });

    // use custom plugin
    $("#inputText").enterKey(function () {
        $("#goButton").click();
    });


});

