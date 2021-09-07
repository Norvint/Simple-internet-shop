import csv
import io
from datetime import datetime
from decimal import Decimal

from django.views.generic import TemplateView

from app_files.forms import UploadFileForm, DocumentForm
from app_files.models import Product


class FileSizeView(TemplateView):
    template_name = 'app_files/files_size.html'

    def get_context_data(self, **kwargs):
        context = super(FileSizeView, self).get_context_data()
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        uploaded_form = UploadFileForm(request.POST, request.FILES)
        if uploaded_form.is_valid:
            file = request.FILES['file']
            context['answer'] = f'Имя файла - {file.name}, его размер - {file.size} байт'
        return self.render_to_response(context=context)


class ForbiddenFileView(TemplateView):
    template_name = 'app_files/forbidden_file.html'

    def get_context_data(self, **kwargs):
        context = super(ForbiddenFileView, self).get_context_data()
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        uploaded_form = UploadFileForm(request.POST, request.FILES)
        if uploaded_form.is_valid:
            file = request.FILES['file'].read()
            decoded_file = file.decode('utf-8').split('\n')
            forbidden_words = ['Это', 'слово', 'нельзя', 'использовать']
            for row in decoded_file:
                for word in forbidden_words:
                    if word in row:
                        context['answer'] = 'Файл не прошел проверку!'
                        return self.render_to_response(context=context)
        context['answer'] = 'Все хорошо!'
        return self.render_to_response(context=context)


class UpdatePricesView(TemplateView):
    template_name = 'app_files/update_prices.html'

    def get_context_data(self, **kwargs):
        context = super(UpdatePricesView, self).get_context_data()
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        uploaded_form = DocumentForm(request.POST, request.FILES)
        if uploaded_form.is_valid:
            file = request.FILES['file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(file), fieldnames=['code', 'price'])
            updated_products = 0
            invalid_codes = []
            for row in reader:
                product = Product.objects.all().filter(code=row['code'])
                if product:
                    product.update(price=Decimal(row['price']))
                    updated_products += 1
                else:
                    invalid_codes.append(row['code'])
            static_products = len(Product.objects.all()) - updated_products
            context['answer'] = f'Продуктов обновлено - {updated_products},' \
                                f' количестов необновленных продуктов - {static_products}, ' \
                                f'артикулы, которых нет в базе данных - {invalid_codes}'
            uploaded_form.save()
        return self.render_to_response(context=context)
