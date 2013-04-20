$(function() {  
  $(".button").click(function() {  
    // validate and process form here  
      var artist = $("input#artist").val();  
 
      return false;  
    }  

    var dataString = artist;  
    //alert (dataString);return false;  
    $.ajax({  
      type: "POST",  
      url: "bin/process.php",  
      data: dataString,  
      success: function() {  
        $('#simArtist1').html(artist);    
      }  
    });  
    return false;   
  });  
});  