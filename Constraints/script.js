// This function is called when the form is submitted
function submitForm() {
  var formData = {
    postal_code: $("#postal_code").val(),
    boundary_coordinates: $("#boundary_coordinates").val(),
    target_gpr: $("#target_gpr").val(),
  };

  $("#loadingScreen").show();

  $.ajax({
    type: "POST",
    url: "/submit",
    data: formData,
    success: function (response) {
      console.log(response);
      // Check if the development_restrictions data is available
      if (response.development_restrictions) {
        var restrictions = response.development_restrictions;

        // Update the HTML content
        $(".information")
          .html(
            "<p>Address: " +
              restrictions.address +
              "</p>" +
              "<p>Target GPR: " +
              restrictions.gpr +
              "</p>" +
              "<p>Area: " +
              restrictions.area +
              "</p>"
          )
          .removeClass("hidden");

        // Hide the loading screen
        $("#loadingScreen").hide();
      } else {
        console.error(
          "No development_restrictions found in response:",
          response
        );
        $("#loadingScreen").hide();
      }
    },
    error: function (error) {
      console.log("Error:", error);
      $("#loadingScreen").hide();
    },
  });
}

function updateSitePlanImages(imageUrls) {
  let imageContainer = $("#sitePlanImages");
  imageContainer.empty(); // Clear any existing content

  // Loop through the image URLs and create image elements
  imageUrls.forEach((url) => {
    let img = $("<img>").attr("src", url).attr("alt", "Site Plan Image");
    imageContainer.append(img);
  });
}
