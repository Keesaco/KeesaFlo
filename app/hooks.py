###########################################################################
## \file app/hooks.py
## \brief Runs app services when webhooks are accessed.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
from django.http import HttpResponse
import API.APIInstance as instances
import API.APIBackground as background

###########################################################################
## \brief Balances the number of instances after a delay of 30 seconds.
## \param request - Django variable defining the hook request.
## \return redirect
###########################################################################
def balance(request):
	background.run(instances.balance, 30)
	return HttpResponse('')
