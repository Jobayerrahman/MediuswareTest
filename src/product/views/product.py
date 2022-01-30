from django.views import generic
from django.core.paginator import Paginator
from product.models import Variant,ProductVariantPrice,Product,ProductVariant,ProductImage
from datetime import datetime
from django.shortcuts import render,redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    #Create Product
    def index(self, request, *args, **kwargs):
        #Database accessing
        product     = Product()
        productImg  = ProductImage()
        variant     = ProductVariant()
        information = ProductVariantPrice()
        
        if request.method == 'POST' and request.FILES['product_image']:
            product.title                       = self.request.POST.get('title')
            product.sku                         = self.request.POST.get('sku')
            product.description                 = self.request.POST.get('description')
            product.file_path                   = self.request.FILES['product_image']
            variant.variant_title               = self.request.POST.get('product_variant')
            information.price                   = self.request.POST.get('product_variant_prices')

            #Updated Data Save
            product.save()
            information.save()
            variant.save()
            productImg.save()
            
            return redirect("product:list.product")
    
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


#Data List & Data Filter
class ViewProductList(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        List = ProductVariantPrice.objects.all() 
        variant = Variant.objects.all()
        
        #Pagination
        paginator = Paginator(List, 2)
        page_number = self.request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        total_product = paginator.count
        start_index = page_obj.start_index()
        end_index = page_obj.end_index()

        #Data GET
        product_name = self.request.GET.get('title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        product_variant = self.request.GET.get('variant')
        product_Date = self.request.GET.get('date')

        #Filtering
        if product_name !='' and product_name is not None:
            context['product'] = ProductVariantPrice.objects.filter(product__title=product_name)
        elif price_from !='' and price_from is not None:
            context['product'] = ProductVariantPrice.objects.filter(price__gte=price_from)
        elif price_to !='' and price_to is not None:
            context['product'] = ProductVariantPrice.objects.filter(min_price__lt=price_to)
        elif product_variant !='' and product_variant is not None:
            if product_variant =="red" or product_variant =="green" or product_variant =="blue":
                context['product'] = ProductVariantPrice.objects.filter(product_variant_one__variant_title=product_variant)
            elif product_variant =="sm" or product_variant =="xl" or product_variant =="xxl":
                context['product'] = ProductVariantPrice.objects.filter(product_variant_two__variant_title=product_variant)
            else:
                context['product'] = ProductVariantPrice.objects.filter(product_variant_three__variant_title=product_variant)
        elif product_Date !='' and product_Date is not None:
            context['product'] = ProductVariantPrice.objects.filter(insertion_time=product_Date)
        elif product_name !='' and product_name is not None and price_from !='' and price_from is not None:
            context['product'] = ProductVariantPrice.objects.filter(product__title=product_name,price=price_from)
        else:
            context['product'] = page_obj.object_list
        

        #Context sending
        context['paginator'] = paginator
        context['total'] = total_product
        context['start'] = start_index
        context['end'] = end_index
        context['variant'] = variant
        
        return context




#Edit Product
class ProductUpdate(generic.TemplateView):
    template_name = 'products/update.html'
    
    #Data update
    def post(self, request, *args, **kwargs):
        #Database accessing
        information = get_object_or_404(ProductVariantPrice,id=kwargs['pk'])
        product = get_object_or_404(Product,id=information.product.id)
        variant_one = get_object_or_404(ProductVariant,id=information.product_variant_one.id)
        variant_two = get_object_or_404(ProductVariant,id=information.product_variant_two.id)
        
        if request.method == 'POST':
            #Data Receive Form Field
            product.title                       = self.request.POST.get('product_title')
            product.sku                         = self.request.POST.get('product_sku')
            product.description                 = self.request.POST.get('product_desc')
            variant_one.variant_title           = self.request.POST.get('varitant_one')
            variant_two.variant_title           = self.request.POST.get('varitant_two')
            information.price                   = self.request.POST.get('price_from')
            information.min_price               = self.request.POST.get('price_to')
            information.stock                   = self.request.POST.get('stock_from')
            information.min_stock               = self.request.POST.get('stock_to')

            #Updated Data Save
            product.save()
            information.save()
            variant_one.save()
            variant_two.save()
            
            return redirect("product:list.product")
        else:
            context = super().get_context_data(**kwargs)
            context['information'] = ProductVariantPrice.objects.get(id=kwargs['pk'])
            return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['information'] = ProductVariantPrice.objects.get(id=kwargs['pk'])
        return context