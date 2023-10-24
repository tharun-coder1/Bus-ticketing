from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
			path("index.html", views.index, name="index"),
			path("Chat", views.Chat, name="Chat"),
			path("Faq", views.Faq, name="Faq"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    	
			path("UserLogin.html", views.UserLogin, name="UserLogin"),
			path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
			path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
			path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
			path("AddRoutes", views.AddRoutes, name="AddRoutes"),
			path("SearchBuses", views.SearchBuses, name="SearchBuses"),
			path("AddRoutesAction", views.AddRoutesAction, name="AddRoutesAction"),
			path("BookSeat", views.BookSeat, name="BookSeat"),
			path("SearchBusesAction", views.SearchBusesAction, name="SearchBusesAction"),
			path("BookSeatAction", views.BookSeatAction, name="BookSeatAction"),
			path("ViewBookings", views.ViewBookings, name="ViewBookings"),
			path("ViewPastBookings", views.ViewPastBookings, name="ViewPastBookings"),
			path("CancelBooking", views.CancelBooking, name="CancelBooking"),
]