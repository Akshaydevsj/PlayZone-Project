from django.views import View

from django.shortcuts import render,redirect,get_object_or_404

from django.db.models import Q

from .models import Product

from .forms import ProductForm

from django.contrib import messages


class ProductListView(View) :

    template = 'shop/product-list.html'

    def get(self,request,*args,**kwargs) :

        query = request.GET.get('query')

        products = Product.objects.filter(active_status=True)

        if query :

            products = products.filter(

                Q(name__icontains=query) |

                Q(description__icontains=query) |

                Q(category__name__icontains=query)

            ).distinct()

        data = {

            'page' : 'Shop',

            'products' : products,

            'query' : query

        }

        return render(request,self.template,context=data)




class ProductCreateView(View) :

    template = 'shop/product-create.html'

    form_class = ProductForm

    def get(self,request,*args,**kwargs) :

        form = self.form_class()

        return render(request,self.template,{'form':form})


    def post(self,request,*args,**kwargs) :

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid() :

            form.save()

            return redirect('product-list')

        return render(request,self.template,{'form':form})
    



class ProductDetailView(View) :

    template = 'shop/product-detail.html'

    def get(self,request,uuid,*args,**kwargs) :

        product = get_object_or_404(Product,uuid=uuid,active_status=True)

        data = {

            'page' : product.name,

            'product' : product

        }

        return render(request,self.template,context=data)
    


class ProductEditView(View) :

    template = 'shop/product-edit.html'

    form_class = ProductForm

    def get(self,request,uuid,*args,**kwargs) :

        product = Product.objects.get(uuid=uuid)

        form = self.form_class(instance=product)

        return render(request,self.template,{'form':form})


    def post(self,request,uuid,*args,**kwargs) :

        product = Product.objects.get(uuid=uuid)

        form = self.form_class(request.POST,request.FILES,instance=product)

        if form.is_valid() :

            form.save()

            return redirect('product-list')

        return render(request,self.template,{'form':form})
    


class ProductDeleteView(View) :

    def get(self,request,uuid,*args,**kwargs) :

        Product.objects.filter(uuid=uuid).update(active_status=False)

        return redirect('product-list')




class AddToCartView(View):

    def get(self, request, uuid):

        product = get_object_or_404(Product, uuid=uuid)

        cart = request.session.get('cart', {})

        item = cart.get(str(product.uuid))

        if item:

            if item['quantity'] < product.quantity:

                item['quantity'] += 1

            else:

                messages.error(request,f"Only {product.quantity} items available in stock.")

        else:

            cart[str(product.uuid)] = {

                                        'name': product.name,

                                        'price': float(product.price),

                                        'quantity': 1,

                                        'stock': product.quantity,

                                        'photo': product.photo.url if product.photo else ''

                                    }

        request.session['cart'] = cart

        request.session.modified = True

        return redirect('cart')




class UpdateCartView(View):

    def get(self, request, uuid, action):

        cart = request.session.get('cart', {})

        if uuid in cart:

            if action == 'plus':

                if cart[uuid]['quantity'] < cart[uuid]['stock']:

                    cart[uuid]['quantity'] += 1

                else:

                    messages.error(request,f"Only {cart[uuid]['stock']} items available."
                    )

            elif action == 'minus':

                cart[uuid]['quantity'] -= 1

                if cart[uuid]['quantity'] <= 0:

                    del cart[uuid]

        request.session['cart'] = cart

        request.session.modified = True

        return redirect('cart')
    

class RemoveFromCartView(View):

    def get(self, request, uuid):

        cart = request.session.get('cart', {})

        if uuid in cart:

            del cart[uuid]

        request.session['cart'] = cart

        request.session.modified = True

        return redirect('cart')




class CartView(View):

    template = 'shop/cart.html'

    def get(self, request):

        cart = request.session.get('cart', {})

        total = sum(item['price'] * item['quantity']for item in cart.values())

        return render(request, self.template, {

                                                    'cart': cart,

                                                    'total': total
                                                }
        
        )
    
