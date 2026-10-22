from django.contrib import admin
from .models import Autor, Livro, Membro, Emprestimo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nome", "nacionalidade", "data_nascimento")
    search_fields = ("nome",)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "copias_totais", "copias_disponiveis")
    list_filter = ("autor",)
    search_fields = ("titulo", "isbn")


class EmprestimoInline(admin.TabularInline):
    model = Emprestimo
    extra = 0
    fields = ("livro", "data_prevista_devolucao", "data_devolucao", "status")


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "data_cadastro")
    inlines = [EmprestimoInline]


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ("livro", "membro", "data_emprestimo", "data_prevista_devolucao", "status")
    list_filter = ("status",)
    search_fields = ("livro__titulo", "membro__nome", "membro__email")
