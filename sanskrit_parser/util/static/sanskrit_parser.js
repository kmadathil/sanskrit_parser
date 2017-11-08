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
                for(var i =0;i < result.tags.length-1;i++)
		{
                    $("#reshead").text("Tags")
                    var item = result.tags[i][0];
		    var itags = result.tags[i][1];
                    $("#resoutp").append("<li class=\"list-group-item\"><b>"+item+"</b><div>"+itags+"</div></li>");
                }
		break;
		
            } 
        });
    });
});
  
