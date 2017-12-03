function createPanel(heading, row, id) {
    var cardClass = id % 2 ? "bg-secondary" : "bg-primary";
    var expanded = id == 0 ? "show" : "";
    var h = '<div class="card ' + cardClass + ' "><div class="card-header ' + cardClass + '">'
    h += '<a class="text-white" data-toggle="collapse" href="#collapse' + id +'" aria-expanded="false" aria-controls="collapse' + id +'">'
    h += heading + '</a></div>'
    h += '<div id="collapse' + id +'" class="collapse '+expanded+'"><div class="card-block">'
    h += '<ol class="list-group">'
    for (var i=0; i<row.length;i++) {
        var sitem = row[i];
        h += '<li class="list-group-item"><table class="table table-striped">'
        h += '<thead><th scope="col">Word</th><th scope="col">Tags</th></thead><tbody>'
        for(var item in sitem){
            h += '<tr><th scope="row">' + sitem[item][0] +'</th><td>'
            h += sitem[item][1][0] + ' - ' + sitem[item][1][1] + '</td></tr>'
        }
        h += "</tbody></table></li>";
    }
    h+= '</ol>'
    h += '</div></div></div>'
    return h
}

$(document).ready(function(){
    $("#goButton").click(function(){
        var txt = $("#inputText").val();
        var urlbase = "http://localhost:5000/api/";
        var option = {};
        var tsel = $("#analysisType").val()
        if (!txt) {
            alert("Please enter input text");
            return;
        }
        option["Tags"]="tags/"
        option["Split"]="split/"
        option["Analyze"]="analyze/"
	
        var url = urlbase+option[tsel]+txt
        $.getJSON(url, function(result){
            var s = JSON.stringify(result)
            $("#devinp").text(result.devanagari)
            $("#jsonbox").text(s);
            $("#restable").html("")
            var restable = ""
            switch (tsel) {
                case "Tags":
                    if (result.tags.length > 0) {
                        $("#reshead").text("Tags")
                    } else {
                        $("#reshead").text("No Tags Found")
                    }
                    restable += "<table class='table table-striped'>"
                    for(var i =0;i < result.tags.length;i++)
                    {
                        var item = result.tags[i][0];
                        var itags = result.tags[i][1];
                        restable += "<tr><th scope='row'>"+item+"</th><td>"+itags+"</td></tr>";
                    }
                    restable += "</table>"
                    break;
                case "Split":
                    $("#reshead").text("Sandhi Splits")
                    restable += "<table class='table table-striped'>"
                    for(var i =0;i < result.splits.length;i++)
                    {
                        var item = result.splits[i].join(" ");
                        restable += "<tr><td>"+item+"</td></tr>";
                    }
                    restable += "</table>"
                    break;
                case "Analyze":
                    $("#reshead").text("Morphological Analysis")
                    var panelID = 0
                    for(var key in result.analysis)
                    {
                        var item = key.split("_").join(" ");
                        restable += createPanel(item, result.analysis[key], panelID);
                        panelID += 1;
                    }
                    break;
            }
            $("#restable").append(restable);
            $("#jsonButton").removeClass("d-none")
            $("#devtab").removeClass("d-none")
            $("#restab").removeClass("d-none")
        });
    });
});

