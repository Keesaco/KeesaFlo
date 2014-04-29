/**
 * \file app/static/js/landing.js
 * \brief JavaScript library specifically for the app's landing page. Provides functionality specifically for pre-authentication interaction.
 * \author jmccrea@keesaco.com of Keesaco
 */

/** \package app.static.js.landing
 * \brief Provides methods for user interaction before logging in.
 */

$(document).ready(function()
{
	var hashVals = window.location.href.split('#!/')
	if (hashVals.length > 1)
	{
		switch(hashVals[1])
		{
			case 'signup':
				landingSignup();
				break;
		}
				  
	}
});

				  
/**
 * Shows a signup interface
 * \return None
 * \author jmccrea@keesaco.com of Keesaco
 */
function landingSignup()
{
	bootbox.confirm("Sign up to use KeesaFlo?",
		function(result)
		{
			if (result)
			{
				var signup = {
						action		: 'signup'
				}
						
				ksfReq.postJSON("/app/data/edit/signup/", signup,
					function(response)
					{
						if (response.success)
						{
							bootbox.confirm("You've been signed up successfully. Please click 'Ok' to log in to KeesaFlo.",
								function (goToApp)
								{
									if (goToApp)
									{
										window.location.href = "/app/";
									}
								});
							}
						else if (response.error)
						{
							bootbox.alert("Error: " + response.error);
						}
					},
					function()
					{
						bootbox.alert("Something went wrong. Please refresh and try again.");
					});
			}
		}
	);
}