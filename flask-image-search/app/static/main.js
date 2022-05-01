// ----- custom js ----- //
//global
var url = '';
var data = [];
$(function() {
    // sanity check
    console.log( "ready!" );
    // image click
    $(".img").click(function() {
      // add active class to clicked picture
      $(this).addClass("active")
      // grab image url
      var image = $(this).attr("src")
      console.log(image)
      // ajax request
      $.ajax({
        type: "POST",
        url: "/search",
        data : { img : image },
        // handle success
        success: function(result) {
            console.log(result.results);
            var data = result.results
// loop through results, append to dom
for (i = 0; i < data.length; i++) {
    $("#results").append('<tr><th><a href="'+url+data[i]["image"]+'"><img src="'+url+data[i]["image"]+
      '" class="result-img"></a></th><th>'+data[i]['score']+'</th></tr>')
  };
        },
        // handle error
        error: function(error) {
            console.log(error);
            // show error
            $("#error").show();
        }
      });
    });
  })