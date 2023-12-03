// This function is called when the form is submitted
function submitForm() {
  // Collect form data
  var formData = {
    postal_code: $("#postal_code").val(),
    boundary_coordinates: $("#boundary_coordinates").val(),
    target_gpr: $("#target_gpr").val(),
  };

  // Show the loading screen
  $("#loadingScreen").show();

  // Make an AJAX POST request to the server
  $.ajax({
    type: "POST",
    url: "/submit",
    data: formData,
    success: function (response) {
      // Update the page content with the response
      $("#results").html(response);
      // Remove the 'hidden' class to display the sections
      $(
        ".information, .development-restrictions, .possible-site-plans"
      ).removeClass("hidden");
      $("#loadingScreen").hide();
      updateSitePlanImages(response.imageUrls);
    },
    error: function (error) {
      // Handle any errors
      console.log(error);
      $("#loadingScreen").hide(); // Hide the loading screen
    },
  });
}

function updateSitePlanImages(imageUrls) {
  let imageContainer = $("#sitePlanImages");
  imageContainer.empty(); // Clear any existing content

  // Loop through the image URLs and create image elements
  imageUrls.forEach((url) => {
    let imgTag = $("<img>").attr("src", url).attr("alt", "Site Plan Image");
    imageContainer.append(imgTag);
  });
}
