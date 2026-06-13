from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . models import Book, Cart, CartItem, Order, OrderItem

# Create your views here.

@login_required(login_url='login')
def add(request):
    return render(request, "add.html")

def index(re):
    return redirect("show_book")

def home(req):
    return render(req,"home.html")  

def Login_view(req):
    if req.user.is_authenticated:
        return redirect("show_book")
    else:
        if req.method == "POST":
            username = req.POST["username"]
            password = req.POST["password"]

            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)
                return redirect("show_book")
        return render(req, "login.html")


@login_required(login_url='login')
def Create_Book(req):
    if req.method=="POST":
        title=req.POST.get("title")
        author=req.POST.get("author")
        isbn=req.POST.get("isbn")
        genre=req.POST.get("genre")
        price=req.POST.get("price")

        book=Book.objects.create(title=title,author=author,isbn=isbn,genre=genre,price=price,user=req.user)

        return redirect('show_book')
    else:
        return render(req,"add.html")

@login_required(login_url='login')
def Delete_data(req,pk):
    data=get_object_or_404(Book,pk=pk)
    data.delete()
    return redirect("show_book") 

@login_required(login_url='login')
def Updated(req,pk):
    updated_data=get_object_or_404(Book,pk=pk) 
    return render(req,"update.html",{"updated_data":updated_data})

@login_required(login_url='login')
def update_book(req,pk):
    updated_data=get_object_or_404(Book,pk=pk)
    updated_data.title=req.POST.get("title")
    updated_data.author=req.POST.get("author")
    updated_data.isbn=req.POST.get("isbn")
    updated_data.genre=req.POST.get("genre")
    updated_data.price=req.POST.get("price")
    updated_data.save()
    return redirect("show_book")

@login_required(login_url='login')
def Book_List(req):
    query=Book.objects.filter(user=req.user)
    name=req.GET.get('search')

    if name:
        query=query.filter(Q(title__icontains=name) | Q(author__icontains=name))
    return render(req,"index.html",{"query":query,"name":name})


def Register(req):
    return render(req,"register.html")

def Registration(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST.get('confirm_password')

        if password == cpassword:
            new_data_created = User.objects.create( username=username, password=password,first_name = name, email = email )
            new_data_created.set_password(password)
            new_data_created.save()
            return redirect("login")
        else:
            return render(request, "register.html")
    return HttpResponse("error")

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")

# E-commerce Shop and Checkout Views

def Shop_View(req):
    books = Book.objects.all()
    genres = Book.objects.values_list('genre', flat=True).distinct()
    
    search_query = req.GET.get('search')
    selected_genre = req.GET.get('genre')
    
    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query) | Q(isbn__icontains=search_query))
    if selected_genre:
        books = books.filter(genre=selected_genre)
        
    return render(req, "shop.html", {
        "books": books,
        "genres": genres,
        "selected_genre": selected_genre,
        "search_query": search_query
    })

@login_required(login_url='login')
def Cart_View(req):
    cart, created = Cart.objects.get_or_create(user=req.user)
    cart_items = cart.items.all()
    return render(req, "cart.html", {
        "cart": cart,
        "cart_items": cart_items
    })

@login_required(login_url='login')
def Add_To_Cart(req, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.user == req.user:
        # Prevent seller from buying their own listing
        return redirect('shop')
        
    cart, created = Cart.objects.get_or_create(user=req.user)
    cart_item, created_item = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created_item:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')

@login_required(login_url='login')
def Remove_From_Cart(req, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=req.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def Update_Cart_Quantity(req, item_id):
    if req.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=req.user)
        action = req.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def Checkout_View(req):
    cart, created = Cart.objects.get_or_create(user=req.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        return redirect('shop')
        
    if req.method == 'POST':
        name = req.POST.get('name')
        phone = req.POST.get('phone')
        shipping_address = req.POST.get('shipping_address')
        total_price = cart.total_price
        
        order = Order.objects.create(
            user=req.user,
            total_price=total_price,
            name=name,
            phone=phone,
            shipping_address=shipping_address
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                title=item.book.title,
                price=item.book.price,
                quantity=item.quantity
            )
            
        # Clear cart
        cart_items.delete()
        return redirect('orders')
        
    return render(req, "checkout.html", {
        "cart": cart,
        "cart_items": cart_items
    })

@login_required(login_url='login')
def Orders_View(req):
    orders = Order.objects.filter(user=req.user).order_by('-created_at')
    return render(req, "orders.html", {
        "orders": orders
    })