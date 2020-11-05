function createPanel(heading, row, imgbase, urlbase, id) {
    "use strict;"
    var cardClass = id % 2 ? "bg-secondary" : "bg-primary";
    var expanded = id === 0 ? "show" : "";
    var h = "<div class=\"card " + cardClass + " \"><div class=\"card-header " + cardClass + "\">";
    h += "<a class=\"text-white\" data-toggle=\"collapse\" href=\"#collapse" + id + "\" aria-expanded=\"false\" aria-controls=\"collapse" + id + "\">";
    h += heading + "</a><p class=\"alignright\"> <a target=\"_blank\" class=\"text-white\" href=\"";
/*    h += urlbase + "static/" + imgbase + ".dot.png\">(View Graph)</a></p><div style=\"clear: both;\"></div></div>"; */
    h += urlbase + "sanskrit_parser/v1/graph/" + imgbase + "\">(View Graph)</a></p><div style=\"clear: both;\"></div></div>";
    h += "<div id=\"collapse" + id + "\" class=\"collapse " + expanded + "\"><div class=\"card-block\">";
    h += "<ol class=\"list-group\">";
    row.forEach(function (sitem, index) {
        h += "<li class=\"list-group-item\"><table class=\"table table-striped\">";
	h += "<p class=\"alignright\"> <a target=\"_blank\" href=\"";
//	h += urlbase + "static/" + imgbase + "_parse" + index + ".dot.png\">(View Parse Graph)</a></p><div style=\"clear: both;\"></div>"
	h += urlbase + "sanskrit_parser/v1/graph/" + imgbase + "_parse" + index + "\">(View Parse Graph)</a></p><div style=\"clear: both;\"></div>"
        h += "<thead><th scope=\"col\">Word</th><th scope=\"col\">Tags</th><th scope=\"col\">Role</th><th scope=\"col\">Linked To</th></thead><tbody>";
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

$(document).ready( function () {
    "use strict;"
    $("#goButton").on("click", function () {
        var txt = $("#inputText").val();
        var urlbase = $.query.get("api_url_base") !== ""? $.query.get("api_url_base") : "https://sktparserapi.madathil.org/";
        var option = {};
        var tsel = $("#analysisType").val();
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
        var url = urlbase + option[tsel] + txt;
        $.getJSON(url, function (result) {
            var panelID;
            var keys;
            var s = JSON.stringify(result);
            $("#devinp").text(result.devanagari);
            $("#jsonbox").text(s);
            $("#restable").html("");
            var restable = "";
            switch (tsel) {
            case "Tags":
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
                break;
            case "Split":
                $("#reshead").text("Sandhi Splits");
                restable += "<table class=\"table table-striped\">";
                result.splits.forEach(function (res) {
                    var item = res.join(" ");
                    restable += "<tr><td>" + item + "</td></tr>";
                });
                restable += "</table>";
                break;
            case "Analyze":
                $("#reshead").text("Sentence Analysis");
                panelID = 0;
                keys = Object.keys(result.analysis);
                restable += "<strong>Found " + keys.length + " valid morphologies</strong>";
                restable += "<br>Please click on a result below to expand/collapse";
                // Shorter splits should come first
                keys.sort(function (a, b) {
                    return a.split("_").length > b.split("_").length;
                });
                keys.forEach(function (key) {
                    var item = key.split("_").join(" ");
                    console.log(key);
                    restable += createPanel(item, result.analysis[key], result.plotbase[key], urlbase, panelID);
                    panelID += 1;
                });
                break;
            }
            $("#restable").append(restable);
            $("#jsonButton").removeClass("d-none");
            $("#devtab").removeClass("d-none");
            $("#restab").removeClass("d-none");
            $("#issueButton").removeClass("d-none");
            btn.removeClass("btn-secondary").addClass("btn-primary");
            btn.text(btxt);
        });
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

