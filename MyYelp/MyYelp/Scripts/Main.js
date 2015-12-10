$(document).ready(function () {
    var myhtml = "<dl class='dl-horizontal'><dt> Name</dt> <dd> {name} </dd><dt>Number Of Reviews</dt> <dd> {numberOfReviews} </dd> <dt>Stars</dt><dd> {stars} </dd></dl><hr/>"
    var ajaxCall = function (tempUrl) {
        $.ajax({
            type: "GET",
            url: tempUrl,
            contentType: 'application/json',
            beforeSend: function () {
            
            },
            dataType: 'json',
            success: function (a,b,response) {
                debugger;
                var toAppend = "";
                for (var i = 0 ; i < a.length; i++) {
                    var h1 = myhtml;
                    h1 = h1.replace('{name}', a[i].name).replace('{numberOfReviews}', a[i].review_count).replace('{stars}', a[i].stars)
                    toAppend += h1;
                }
                //var objects = jQuery.parseJSON(response.responseText)
                //objects = jQuery.parseJSON(objects)
                //for (var i = 0; i < objects.length; i++) {
                //    var h1 = html.replace('{user_id}', objects[i].user_id[0])
                //}
                //$("#solrResults").append(h1);
                $("#recs").html("")
                $("#recs").append(toAppend);
            },
            
            error: function (a, b, c) {
                //console.log(a)
                //console.log(b)
                //console.log(c)
            }
        })
    }


    $("#FetchResults").on("click", function () {
        var searchTerms = $("#searchTerms").val();
        //searchTerms = searchTerms.replace(" ", "+");
        tempUrl = '/business/SolrResults?param=' + searchTerms;
        ajaxCall(tempUrl)
        //$.getJSON(tempUrl)
    });

    $("#FetchResultsOnUserId").on("click", function() {
        var userId = $("#userId").val();
        tempUrl = '/business/FetchResultsOnUserId?param=' + userId;
        ajaxCall(tempUrl)
    });
});