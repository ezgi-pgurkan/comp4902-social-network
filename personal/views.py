from django.shortcuts import render

def home_screen_view(request, *args, **kwargs):
	context ={}
	if not request.user.is_authenticated:
				return redirect('login')
	return render(request, "personal/home.html", context)