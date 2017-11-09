$(document).ready(function(){
    $("#goButton").click(function(){
        var txt = $("#inputText").val();
        var urlbase = "http://localhost:5000/api/";
        var option = {};
        var tsel = $("#analysisType").val()
        option["Tags"]="tags/"
        option["Split"]="split/"
        option["Analyze"]="analyze/"
	
        var url = urlbase+option[tsel]+txt
        $.getJSON(url, function(result){
            var s = JSON.stringify(result)
            $("#devinp").text(result.devanagari)
            $("#resbox").text(s);
            $("#resoutp").html("")
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
                    $("#resoutp").append("<li class=\"list-group-item\"><b>"+item+"</b><div>"+itags+"</div></li>");
                }
		break;
	    case "Split":
                $("#rescard").removeClass('hidden')
                $("#reshead").text("Sandhi Splits")
                for(var i =0;i < result.splits.length;i++)
		{
                    var item = result.splits[i];
                    $("#resoutp").append("<li class=\"list-group-item\">"+item+"</li>");
                }
		break;
	    case "Analyze":
                $("#rescard").removeClass('hidden')
                $("#reshead").text("Morphological Analysis")
                for(var key in result.analysis)
		{
                    var item = key;
                    $("#resoutp").append("<li class=\"list-group-item\">"+item+"<ul class=\"list-group\">");
		    for (var i=0; i<result.analysis[key].length;i++) {
			var sitem = result.analysis[key][i];
			$("#resoutp").append("<li class=\"list-group-item\">"+sitem+"<ul>");
		    }
		    $("#resoutp").append("</ul></li>");
                }
		break;
		
            } 
	});
    });
});

