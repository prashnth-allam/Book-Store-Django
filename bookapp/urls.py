from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.Login_view, name="login"),
    path('register/', views.Register, name="register"),
    path('Registration/', views.Registration, name="registration"),
    path('logout',views.signout,name="logout"),
    path("create_book",views.Create_Book,name="create_book"),
    path("add", views.add,name="add"),
    path("show_book",views.Book_List,name="show_book"),
    path("delete/<int:pk>",views.Delete_data,name="delete_data"),
    path("updated_data/<int:pk>",views.Updated,name="updated_data"),
    path("update_book/<int:pk>",views.update_book,name="update_book"),
    path("index",views.index,name="index"),

    # E-commerce routing
    path('shop/', views.Shop_View, name='shop'),
    path('cart/', views.Cart_View, name='cart'),
    path('cart/add/<int:book_id>/', views.Add_To_Cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.Remove_From_Cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.Update_Cart_Quantity, name='update_cart_quantity'),
    path('checkout/', views.Checkout_View, name='checkout'),
    path('orders/', views.Orders_View, name='orders'),

]