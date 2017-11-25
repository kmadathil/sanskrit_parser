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
            $("#resbox").html("")
	    switch (tsel) {
            case "Tags":
                $("#rescard").removeClass('hidden')
                if (result.tags.length > 0) {
		    $("#reshead").text("Tags")
		} else {
		    $("#reshead").text("No Tags Found")
		}
                for(var i =0;i < result.tags.length;i++)
		{
                    var item = result.tags[i][0];
		    var itags = result.tags[i][1];
                    $("#resbox").append("<li class=\"list-group-item\"><b>"+item+"</b><div>"+itags+"</div></li>");
                }
		break;
	    case "Split":
                $("#rescard").removeClass('hidden')
                $("#reshead").text("Sandhi Splits")
                for(var i =0;i < result.splits.length;i++)
		{
                    var item = result.splits[i].join(" ");
                    $("#resbox").append("<li class=\"list-group-item\">"+item+"</li>");
                }
		break;
	    case "Analyze":
                $("#rescard").removeClass('hidden')
                $("#reshead").text("Morphological Analysis")
                for(var key in result.analysis)
		{
                    var item = key.split("_").join(" ");
                    $("#resbox").append("<li class=\"list-group-item\">"+item+"<ul>");
		     for (var i=0; i<result.analysis[key].length;i++) {
		     	var sitem = result.analysis[key][i];
		     	$("#resbox").append("<li class=\"list-group-item\">"+sitem+"</li>");
		     }
		    $("#resbox").append("</ul></li>");
                }
		break;
		
            } 
	});
    });
});

